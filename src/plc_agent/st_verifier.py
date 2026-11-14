"""Self-developed IEC 61131-3 Structured Text formal verification engine.

Compiles IEC 61131-3 Structured Text FUNCTION_BLOCK candidates into SMV models
(coupled to benchmark observer LTL/INVAR specifications or standalone property
monitors), invokes NuSMV / nuXmv, and translates counterexample traces into
actionable diagnostics and WebUI-compatible waveforms.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .common import ROOT, digest, now, write_json
from .compiler import normalize_candidate
from .model_checker import (
    LTL_RESULTS_MARKER,
    SBMC_START_MARKER,
    check_model,
    find_nusmv,
    find_nuxmv,
)


class UnsupportedSTConstructError(ValueError):
    """Raised when an ST construct is outside the symbolic verifier fragment."""


# ---------------------------------------------------------------------------
# Types, Declarations, AST Nodes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class STType:
    """Normalized IEC 61131-3 type representation."""

    kind: str  # BOOL, INT_SUBRANGE, INT_UNBOUNDED, REAL, WORD, TIME, ARRAY, STRUCT, ENUM, FB
    base_name: str
    low: int | None = None
    high: int | None = None
    signed: bool = True
    bitwidth: int | None = None
    elem_type: "STType | None" = None
    arr_low: int = 0
    arr_high: int = -1
    fields: tuple[tuple[str, "STType"], ...] = ()
    enum_values: tuple[str, ...] = ()
    fb_type: str | None = None

    @property
    def is_boolean(self) -> bool:
        return self.kind == "BOOL"

    @property
    def is_numeric(self) -> bool:
        return self.kind in ("INT_SUBRANGE", "INT_UNBOUNDED", "REAL", "TIME", "ENUM")

    @property
    def is_integer_like(self) -> bool:
        return self.kind in ("INT_SUBRANGE", "INT_UNBOUNDED", "TIME", "ENUM")


BOOL_TYPE = STType(kind="BOOL", base_name="BOOL", signed=False)
INT_UNBOUNDED_TYPE = STType(kind="INT_UNBOUNDED", base_name="INT", signed=True)
REAL_TYPE = STType(kind="REAL", base_name="REAL", signed=True)
TIME_TYPE = STType(kind="TIME", base_name="TIME", signed=True)


def make_subrange_type(base_name: str, low: int, high: int, signed: bool = True) -> STType:
    return STType(kind="INT_SUBRANGE", base_name=base_name, low=low, high=high, signed=signed)


def make_word_type(base_name: str, bitwidth: int) -> STType:
    return STType(kind="WORD", base_name=base_name, signed=False, bitwidth=bitwidth)


BUILTIN_SCALAR_TYPES: dict[str, STType] = {
    "BOOL": BOOL_TYPE,
    "SINT": make_subrange_type("SINT", -128, 127, signed=True),
    "USINT": make_subrange_type("USINT", 0, 255, signed=False),
    "BYTE": make_subrange_type("BYTE", 0, 255, signed=False),
    "INT": INT_UNBOUNDED_TYPE,
    "UINT": make_subrange_type("UINT", 0, 65535, signed=False),
    "DINT": INT_UNBOUNDED_TYPE,
    "UDINT": INT_UNBOUNDED_TYPE,
    "LINT": INT_UNBOUNDED_TYPE,
    "ULINT": INT_UNBOUNDED_TYPE,
    "WORD": make_word_type("WORD", 16),
    "DWORD": make_word_type("DWORD", 32),
    "LWORD": make_word_type("LWORD", 64),
    "REAL": REAL_TYPE,
    "LREAL": REAL_TYPE,
    "TIME": TIME_TYPE,
    "LTIME": TIME_TYPE,
}

STANDARD_FB_TYPES = {"TON", "TOF", "TP", "R_TRIG", "F_TRIG", "SR", "RS", "CTU", "CTD"}

UNSUPPORTED_TYPES = {
    "STRING",
    "WSTRING",
    "VARIANT",
    "ANY",
    "ANY_BIT",
    "ANY_NUM",
    "ANY_INT",
    "POINTER",
    "REFERENCE",
}


@dataclass
class STVarDecl:
    name: str
    section: str  # INPUT, OUTPUT, IN_OUT, VAR, VAR_TEMP, CONSTANT
    st_type: STType
    init_expr: Any = None


@dataclass
class STProgram:
    fb_name: str
    decls: list[STVarDecl]
    decls_by_lower: dict[str, STVarDecl]
    structs: dict[str, STType]
    enums: dict[str, int]
    statements: list[Any]
    raw_declaration: str
    raw_implementation: str


# AST Expressions
@dataclass(frozen=True)
class BoolLit:
    value: bool


@dataclass(frozen=True)
class IntLit:
    value: int
    bitwidth: int | None = None  # non-None when parsed from word bit literal if forced


@dataclass(frozen=True)
class RealLit:
    value: str


@dataclass(frozen=True)
class TimeLit:
    ms: int


@dataclass(frozen=True)
class VarRef:
    name: str


@dataclass(frozen=True)
class IndexRef:
    base: Any
    index: Any


@dataclass(frozen=True)
class FieldRef:
    base: Any
    field_name: str


@dataclass(frozen=True)
class UnaryOp:
    op: str
    operand: Any


@dataclass(frozen=True)
class BinOp:
    op: str
    left: Any
    right: Any


@dataclass(frozen=True)
class CallExpr:
    func: str
    args: list[tuple[str | None, Any]]


# AST Statements
@dataclass(frozen=True)
class AssignStmt:
    target: Any
    expr: Any


@dataclass(frozen=True)
class IfStmt:
    branches: list[tuple[Any, list[Any]]]  # [(cond, stmts), ...]
    else_stmts: list[Any]


@dataclass(frozen=True)
class CaseStmt:
    expr: Any
    arms: list[tuple[list[tuple[int, int | None]], list[Any]]]  # [([(v, None) | (lo, hi)], stmts)]
    else_stmts: list[Any]


@dataclass(frozen=True)
class ForStmt:
    var_name: str
    start_expr: Any
    end_expr: Any
    step_expr: Any | None
    body: list[Any]


@dataclass(frozen=True)
class FBCallStmt:
    inst_name: str
    args: list[tuple[str | None, Any, bool]]  # (param_name, expr_or_target, is_output_arrow)


@dataclass(frozen=True)
class ExitStmt:
    pass


# ---------------------------------------------------------------------------
# Lexer
# ---------------------------------------------------------------------------


ST_KEYWORDS = {
    "FUNCTION_BLOCK",
    "END_FUNCTION_BLOCK",
    "TYPE",
    "END_TYPE",
    "STRUCT",
    "END_STRUCT",
    "VAR_INPUT",
    "VAR_OUTPUT",
    "VAR_IN_OUT",
    "VAR_TEMP",
    "VAR",
    "CONSTANT",
    "RETAIN",
    "PERSISTENT",
    "END_VAR",
    "ARRAY",
    "OF",
    "IF",
    "THEN",
    "ELSIF",
    "ELSE",
    "END_IF",
    "CASE",
    "END_CASE",
    "FOR",
    "TO",
    "BY",
    "DO",
    "END_FOR",
    "WHILE",
    "END_WHILE",
    "REPEAT",
    "UNTIL",
    "END_REPEAT",
    "EXIT",
    "RETURN",
    "AND",
    "OR",
    "XOR",
    "NOT",
    "MOD",
    "TRUE",
    "FALSE",
}


@dataclass(frozen=True)
class Token:
    kind: str  # KW, ID, INT, REAL, TIME, OP, PUNCT, EOF
    value: Any
    raw: str
    pos: int


def strip_st_comments_and_pragmas(text: str) -> str:
    """Strip ST comments ((* *), /* */, //) and {attribute ...} pragmas preserving newlines."""
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if ch == "(" and nxt == "*":
            depth = 1
            i += 2
            while i < n and depth > 0:
                if i + 1 < n and text[i] == "(" and text[i + 1] == "*":
                    depth += 1
                    i += 2
                elif i + 1 < n and text[i] == "*" and text[i + 1] == ")":
                    depth -= 1
                    i += 2
                else:
                    if text[i] == "\n":
                        out.append("\n")
                    i += 1
            out.append(" ")
        elif ch == "/" and nxt == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                if text[i] == "\n":
                    out.append("\n")
                i += 1
            i = min(n, i + 2)
            out.append(" ")
        elif ch == "/" and nxt == "/":
            while i < n and text[i] != "\n":
                i += 1
        elif ch == "{":
            # CODESYS attribute pragma e.g. {attribute 'analysis' := '-27'}
            j = i + 1
            in_sq = False
            while j < n:
                if text[j] == "'":
                    in_sq = not in_sq
                elif text[j] == "}" and not in_sq:
                    break
                if text[j] == "\n":
                    out.append("\n")
                j += 1
            i = j + 1
            out.append(" ")
        elif ch in ("'", '"'):
            quote = ch
            j = i + 1
            while j < n:
                if text[j] == "$" and j + 1 < n:
                    j += 2
                    continue
                if text[j] == quote:
                    j += 1
                    break
                j += 1
            raise UnsupportedSTConstructError("String literals are outside the symbolic verification fragment")
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _parse_time_literal_ms(body: str) -> int:
    """Convert an IEC time literal body (after T# or TIME#) into integer milliseconds."""
    s = body.strip().upper().replace("_", "")
    sign = 1
    if s.startswith("-"):
        sign = -1
        s = s[1:]
    if not s:
        raise UnsupportedSTConstructError(f"Invalid TIME literal: {body}")
    total_ms = 0.0
    pos = 0
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(MS|US|NS|D|H|M|S)", s):
        if m.start() != pos:
            raise UnsupportedSTConstructError(f"Unsupported TIME literal format: {body}")
        pos = m.end()
        num = float(m.group(1))
        unit = m.group(2)
        scale = {
            "D": 86_400_000.0,
            "H": 3_600_000.0,
            "M": 60_000.0,
            "S": 1_000.0,
            "MS": 1.0,
            "US": 0.001,
            "NS": 1e-6,
        }[unit]
        total_ms += num * scale
    if pos != len(s):
        raise UnsupportedSTConstructError(f"Unsupported TIME literal format: {body}")
    return sign * int(round(total_ms))


def _parse_base_int(base_str: str, digits_str: str) -> int:
    base = int(base_str)
    clean = digits_str.replace("_", "")
    if base not in (2, 8, 10, 16):
        raise UnsupportedSTConstructError(f"Unsupported integer literal base {base}#{digits_str}")
    return int(clean, base)


def tokenize_st(text: str) -> list[Token]:
    """Tokenize pre-stripped IEC 61131-3 Structured Text."""
    clean = strip_st_comments_and_pragmas(text)
    tokens: list[Token] = []
    i = 0
    n = len(clean)
    while i < n:
        ch = clean[i]
        if ch.isspace():
            i += 1
            continue

        # Multi-character operators / punctuation
        two = clean[i : i + 2]
        if two in (":=", "=>", "<>", "<=", ">=", "..", "**"):
            kind = "PUNCT" if two == ".." else "OP"
            tokens.append(Token(kind, two, two, i))
            i += 2
            continue

        if ch in "+-*/=<>&":
            tokens.append(Token("OP", ch, ch, i))
            i += 1
            continue

        if ch in "(),;:[].":
            tokens.append(Token("PUNCT", ch, ch, i))
            i += 1
            continue

        # Time literal T#... or TIME#... or LT#... or LTIME#...
        m_time = re.match(
            r"(?:L?TIME|L?T)#(-?(?:\d+(?:\.\d+)?(?:MS|US|NS|D|H|M|S)_*)+)",
            clean[i:],
            re.IGNORECASE,
        )
        if m_time and (
            m_time.end() == len(clean[i:]) or not (clean[i + m_time.end()].isalnum() or clean[i + m_time.end()] == "_")
        ):
            raw = m_time.group(0)
            ms = _parse_time_literal_ms(m_time.group(1))
            tokens.append(Token("TIME", ms, raw, i))
            i += m_time.end()
            continue

        # Typed literal prefix TYPE#... (e.g., USINT#5, WORD#16#FF, BOOL#TRUE, REAL#1.0)
        m_typed = re.match(r"([A-Za-z_][A-Za-z0-9_]*)#", clean[i:])
        if m_typed:
            type_prefix = m_typed.group(1).upper()
            rest = clean[i + m_typed.end() :]
            m_sub_base = re.match(r"(2|8|10|16)#([0-9A-Fa-f_]+)", rest)
            if m_sub_base:
                val = _parse_base_int(m_sub_base.group(1), m_sub_base.group(2))
                raw = clean[i : i + m_typed.end() + m_sub_base.end()]
                tokens.append(Token("INT", val, raw, i))
                i += len(raw)
                continue
            m_sub_bool = re.match(r"(TRUE|FALSE)\b", rest, re.IGNORECASE)
            if m_sub_bool and type_prefix == "BOOL":
                raw = clean[i : i + m_typed.end() + m_sub_bool.end()]
                tokens.append(Token("KW", m_sub_bool.group(1).upper(), raw, i))
                i += len(raw)
                continue
            m_sub_real = re.match(r"(-?\d[\d_]*\.\d[\d_]*(?:[eE][+-]?\d+)?)", rest)
            if m_sub_real:
                raw = clean[i : i + m_typed.end() + m_sub_real.end()]
                tokens.append(Token("REAL", m_sub_real.group(1).replace("_", ""), raw, i))
                i += len(raw)
                continue
            m_sub_int = re.match(r"(-?\d[\d_]*)", rest)
            if m_sub_int:
                val = int(m_sub_int.group(1).replace("_", ""))
                raw = clean[i : i + m_typed.end() + m_sub_int.end()]
                tokens.append(Token("INT", val, raw, i))
                i += len(raw)
                continue

        # Based integer literal e.g. 16#00FF, 2#1010
        m_base = re.match(r"(2|8|10|16)#([0-9A-Fa-f_]+)", clean[i:])
        if m_base:
            val = _parse_base_int(m_base.group(1), m_base.group(2))
            raw = m_base.group(0)
            tokens.append(Token("INT", val, raw, i))
            i += len(raw)
            continue

        # Real or decimal integer literal (note: avoid swallowing "1..5" as float!)
        m_num = re.match(r"\d[\d_]*(?:\.\d[\d_]*(?:[eE][+-]?\d+)?)?", clean[i:])
        if m_num:
            raw = m_num.group(0)
            if "." in raw:
                tokens.append(Token("REAL", raw.replace("_", ""), raw, i))
            else:
                tokens.append(Token("INT", int(raw.replace("_", "")), raw, i))
            i += len(raw)
            continue

        # Identifier or keyword
        m_id = re.match(r"[A-Za-z_][A-Za-z0-9_]*", clean[i:])
        if m_id:
            raw = m_id.group(0)
            up = raw.upper()
            if up in ST_KEYWORDS:
                tokens.append(Token("KW", up, raw, i))
            else:
                tokens.append(Token("ID", raw, raw, i))
            i += len(raw)
            continue

        raise UnsupportedSTConstructError(f"Unexpected character in ST near position {i}: {clean[i : i + 20]!r}")

    tokens.append(Token("EOF", None, "", n))
    return tokens


# ---------------------------------------------------------------------------
# Recursive-Descent Parser
# ---------------------------------------------------------------------------


class _STParser:
    """Recursive-descent parser for IEC 61131-3 declarations and statements."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0
        self.structs: dict[str, STType] = {}
        self.enums: dict[str, int] = {}

    def peek(self, offset: int = 0) -> Token:
        idx = min(self.pos + offset, len(self.tokens) - 1)
        return self.tokens[idx]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        if tok.kind != "EOF":
            self.pos += 1
        return tok

    def match_kw(self, *kws: str) -> bool:
        t = self.peek()
        return t.kind == "KW" and t.value in kws

    def match_op(self, *ops: str) -> bool:
        t = self.peek()
        return t.kind == "OP" and t.value in ops

    def match_punct(self, *puncts: str) -> bool:
        t = self.peek()
        return t.kind == "PUNCT" and t.value in puncts

    def expect_kw(self, kw: str) -> Token:
        t = self.peek()
        if t.kind != "KW" or t.value != kw:
            raise UnsupportedSTConstructError(f"Expected keyword {kw}, got {t.raw!r} at pos {t.pos}")
        return self.advance()

    def expect_punct(self, punct: str) -> Token:
        t = self.peek()
        if t.kind != "PUNCT" or t.value != punct:
            raise UnsupportedSTConstructError(f"Expected {punct!r}, got {t.raw!r} at pos {t.pos}")
        return self.advance()

    def expect_op(self, op: str) -> Token:
        t = self.peek()
        if t.kind != "OP" or t.value != op:
            raise UnsupportedSTConstructError(f"Expected operator {op!r}, got {t.raw!r} at pos {t.pos}")
        return self.advance()

    def expect_id(self) -> Token:
        t = self.peek()
        if t.kind != "ID":
            raise UnsupportedSTConstructError(f"Expected identifier, got {t.raw!r} at pos {t.pos}")
        return self.advance()

    def parse_supporting_types(self) -> None:
        while self.match_kw("TYPE"):
            self._parse_type_block()

    def _parse_type_block(self) -> None:
        self.expect_kw("TYPE")
        while not self.match_kw("END_TYPE"):
            if self.peek().kind == "EOF":
                raise UnsupportedSTConstructError("Unterminated TYPE block")
            name_tok = self.expect_id()
            type_key = name_tok.value.upper()
            self.expect_punct(":")
            if self.match_kw("STRUCT"):
                self.advance()
                fields: list[tuple[str, STType]] = []
                while not self.match_kw("END_STRUCT"):
                    f_names = [self.expect_id().value]
                    while self.match_punct(","):
                        self.advance()
                        f_names.append(self.expect_id().value)
                    self.expect_punct(":")
                    f_type = self.parse_type_ref()
                    if self.match_op(":="):
                        self.advance()
                        self.parse_expr()
                    self.expect_punct(";")
                    for fn in f_names:
                        fields.append((fn, f_type))
                self.expect_kw("END_STRUCT")
                if self.match_punct(";"):
                    self.advance()
                self.structs[type_key] = STType(
                    kind="STRUCT",
                    base_name=name_tok.value,
                    fields=tuple(fields),
                )
            elif self.match_punct("("):
                # Enum type: TYPE MyEnum : (A := 0, B := 1); END_TYPE
                self.advance()
                enum_names: list[str] = []
                next_val = 0
                while not self.match_punct(")"):
                    ev = self.expect_id().value
                    if self.match_op(":="):
                        self.advance()
                        neg = False
                        if self.match_op("-"):
                            self.advance()
                            neg = True
                        if self.peek().kind != "INT":
                            raise UnsupportedSTConstructError("Expected integer enum initializer")
                        next_val = -self.advance().value if neg else self.advance().value
                    self.enums[ev.upper()] = next_val
                    enum_names.append(ev)
                    next_val += 1
                    if self.match_punct(","):
                        self.advance()
                    else:
                        break
                self.expect_punct(")")
                if self.match_kw("INT", "USINT", "SINT", "DINT", "UINT") or self.peek().kind == "ID":
                    # Optional underlying integer base type after enum list
                    self.advance()
                if self.match_op(":="):
                    self.advance()
                    self.parse_expr()
                if self.match_punct(";"):
                    self.advance()
                self.structs[type_key] = STType(
                    kind="ENUM",
                    base_name=name_tok.value,
                    enum_values=tuple(enum_names),
                )
            else:
                alias_t = self.parse_type_ref()
                if self.match_op(":="):
                    self.advance()
                    self.parse_expr()
                if self.match_punct(";"):
                    self.advance()
                self.structs[type_key] = alias_t
        self.expect_kw("END_TYPE")

    def _parse_const_int(self) -> int:
        neg = False
        if self.match_op("-"):
            self.advance()
            neg = True
        elif self.match_op("+"):
            self.advance()
        t = self.peek()
        if t.kind != "INT":
            raise UnsupportedSTConstructError(f"Expected integer bound, got {t.raw!r}")
        self.advance()
        return -t.value if neg else t.value

    def parse_type_ref(self) -> STType:
        if self.match_kw("ARRAY"):
            self.advance()
            self.expect_punct("[")
            dims: list[tuple[int, int]] = []
            while True:
                lo = self._parse_const_int()
                self.expect_punct("..")
                hi = self._parse_const_int()
                dims.append((lo, hi))
                if self.match_punct(","):
                    self.advance()
                else:
                    break
            self.expect_punct("]")
            self.expect_kw("OF")
            elem_t = self.parse_type_ref()
            for lo, hi in reversed(dims):
                if hi < lo or (hi - lo + 1) > 128:
                    raise UnsupportedSTConstructError(f"Unsupported ARRAY range [{lo}..{hi}]")
                elem_t = STType(
                    kind="ARRAY",
                    base_name=f"ARRAY[{lo}..{hi}] OF {elem_t.base_name}",
                    elem_type=elem_t,
                    arr_low=lo,
                    arr_high=hi,
                )
            return elem_t

        t = self.peek()
        if t.kind != "ID":
            raise UnsupportedSTConstructError(f"Unsupported type token {t.raw!r}")
        name = self.advance().value
        up = name.upper()
        if up in UNSUPPORTED_TYPES:
            raise UnsupportedSTConstructError(f"Type {up} is outside the symbolic verifier fragment")
        # Optional length spec like STRING[80] or subrange INT(0..5)
        if self.match_punct("("):
            self.advance()
            lo = self._parse_const_int()
            self.expect_punct("..")
            hi = self._parse_const_int()
            self.expect_punct(")")
            return make_subrange_type(up, lo, hi, signed=(lo < 0))
        if self.match_punct("["):
            raise UnsupportedSTConstructError(f"Unsupported bracketed type {up}[...]")
        if up in BUILTIN_SCALAR_TYPES:
            return BUILTIN_SCALAR_TYPES[up]
        if up in STANDARD_FB_TYPES:
            return STType(kind="FB", base_name=up, fb_type=up)
        if up in self.structs:
            return self.structs[up]
        raise UnsupportedSTConstructError(f"Unsupported type {name!r}")

    def parse_program(self, raw_decl: str, raw_impl: str) -> STProgram:
        while self.match_kw("TYPE"):
            self._parse_type_block()

        fb_name = "FB_Task"
        decls: list[STVarDecl] = []
        if self.match_kw("FUNCTION_BLOCK"):
            self.advance()
            fb_name = self.expect_id().value
            while self.match_kw("VAR_INPUT", "VAR_OUTPUT", "VAR_IN_OUT", "VAR_TEMP", "VAR"):
                sec_kw = self.advance().value
                section = sec_kw.replace("VAR_", "") if sec_kw != "VAR" else "VAR"
                if self.match_kw("CONSTANT"):
                    self.advance()
                    section = "CONSTANT"
                elif self.match_kw("RETAIN", "PERSISTENT"):
                    self.advance()
                while not self.match_kw("END_VAR"):
                    if self.peek().kind == "EOF":
                        raise UnsupportedSTConstructError("Unterminated VAR block")
                    var_names = [self.expect_id().value]
                    while self.match_punct(","):
                        self.advance()
                        var_names.append(self.expect_id().value)
                    self.expect_punct(":")
                    st_type = self.parse_type_ref()
                    init_expr = None
                    if self.match_op(":="):
                        self.advance()
                        if self.match_punct("["):
                            init_expr = self._parse_array_init()
                        else:
                            init_expr = self.parse_expr()
                    self.expect_punct(";")
                    for vn in var_names:
                        decls.append(STVarDecl(name=vn, section=section, st_type=st_type, init_expr=init_expr))
                self.expect_kw("END_VAR")

        stmts = self.parse_stmt_list(stop_kws=("END_FUNCTION_BLOCK",))
        if self.match_kw("END_FUNCTION_BLOCK"):
            self.advance()
        if self.peek().kind != "EOF":
            raise UnsupportedSTConstructError(f"Unexpected trailing token {self.peek().raw!r}")

        decls_by_lower = {d.name.lower(): d for d in decls}
        return STProgram(
            fb_name=fb_name,
            decls=decls,
            decls_by_lower=decls_by_lower,
            structs=self.structs,
            enums=self.enums,
            statements=stmts,
            raw_declaration=raw_decl,
            raw_implementation=raw_impl,
        )

    def _parse_array_init(self) -> list[Any]:
        self.expect_punct("[")
        items: list[Any] = []
        while not self.match_punct("]"):
            if self.peek().kind == "INT" and self.peek(1).kind == "PUNCT" and self.peek(1).value == "(":
                cnt = self.advance().value
                self.expect_punct("(")
                elem = self.parse_expr()
                self.expect_punct(")")
                items.extend([elem] * cnt)
            else:
                items.append(self.parse_expr())
            if self.match_punct(","):
                self.advance()
            else:
                break
        self.expect_punct("]")
        return items

    def parse_stmt_list(self, stop_kws: tuple[str, ...]) -> list[Any]:
        stmts: list[Any] = []
        while self.peek().kind != "EOF" and not self.match_kw(*stop_kws):
            if self.match_punct(";"):
                self.advance()
                continue
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self) -> Any:
        if self.match_kw("IF"):
            return self._parse_if()
        if self.match_kw("CASE"):
            return self._parse_case()
        if self.match_kw("FOR"):
            return self._parse_for()
        if self.match_kw("WHILE", "REPEAT"):
            raise UnsupportedSTConstructError(f"{self.peek().value} loops are outside the bounded symbolic fragment")
        if self.match_kw("EXIT"):
            self.advance()
            if self.match_punct(";"):
                self.advance()
            return ExitStmt()
        if self.match_kw("RETURN"):
            self.advance()
            if self.match_punct(";"):
                self.advance()
            raise UnsupportedSTConstructError("Early RETURN statements are outside the symbolic verifier fragment")

        # Assignment OR Function-Block invocation
        if self.peek().kind == "ID" and self.peek(1).kind == "PUNCT" and self.peek(1).value == "(":
            return self._parse_fb_call()

        target = self._parse_lvalue()
        if not self.match_op(":="):
            raise UnsupportedSTConstructError(f"Expected ':=' in statement, got {self.peek().raw!r}")
        self.advance()
        expr = self.parse_expr()
        self.expect_punct(";")
        return AssignStmt(target=target, expr=expr)

    def _parse_fb_call(self) -> FBCallStmt:
        inst_name = self.expect_id().value
        self.expect_punct("(")
        args: list[tuple[str | None, Any, bool]] = []
        while not self.match_punct(")"):
            if self.peek().kind == "ID" and self.peek(1).kind == "OP" and self.peek(1).value in (":=", "=>"):
                p_name = self.advance().value
                op = self.advance().value
                if op == "=>":
                    tgt = self._parse_lvalue()
                    args.append((p_name, tgt, True))
                else:
                    val = self.parse_expr()
                    args.append((p_name, val, False))
            else:
                args.append((None, self.parse_expr(), False))
            if self.match_punct(","):
                self.advance()
            else:
                break
        self.expect_punct(")")
        self.expect_punct(";")
        return FBCallStmt(inst_name=inst_name, args=args)

    def _parse_if(self) -> IfStmt:
        self.expect_kw("IF")
        branches: list[tuple[Any, list[Any]]] = []
        cond = self.parse_expr()
        self.expect_kw("THEN")
        body = self.parse_stmt_list(stop_kws=("ELSIF", "ELSE", "END_IF"))
        branches.append((cond, body))
        while self.match_kw("ELSIF"):
            self.advance()
            e_cond = self.parse_expr()
            self.expect_kw("THEN")
            e_body = self.parse_stmt_list(stop_kws=("ELSIF", "ELSE", "END_IF"))
            branches.append((e_cond, e_body))
        else_stmts: list[Any] = []
        if self.match_kw("ELSE"):
            self.advance()
            else_stmts = self.parse_stmt_list(stop_kws=("END_IF",))
        self.expect_kw("END_IF")
        if self.match_punct(";"):
            self.advance()
        return IfStmt(branches=branches, else_stmts=else_stmts)

    def _parse_case(self) -> CaseStmt:
        self.expect_kw("CASE")
        expr = self.parse_expr()
        self.expect_kw("OF")
        arms: list[tuple[list[tuple[int, int | None]], list[Any]]] = []
        else_stmts: list[Any] = []
        while not self.match_kw("ELSE", "END_CASE"):
            if self.peek().kind == "EOF":
                raise UnsupportedSTConstructError("Unterminated CASE statement")
            labels: list[tuple[int, int | None]] = []
            while True:
                lo = self._parse_case_label_atom()
                if self.match_punct(".."):
                    self.advance()
                    hi = self._parse_case_label_atom()
                    labels.append((lo, hi))
                else:
                    labels.append((lo, None))
                if self.match_punct(","):
                    self.advance()
                else:
                    break
            self.expect_punct(":")
            arm_stmts = self._parse_case_arm_stmts()
            arms.append((labels, arm_stmts))
        if self.match_kw("ELSE"):
            self.advance()
            else_stmts = self.parse_stmt_list(stop_kws=("END_CASE",))
        self.expect_kw("END_CASE")
        if self.match_punct(";"):
            self.advance()
        return CaseStmt(expr=expr, arms=arms, else_stmts=else_stmts)

    def _parse_case_label_atom(self) -> int:
        if self.peek().kind == "ID" and self.peek().value.upper() in self.enums:
            return self.enums[self.advance().value.upper()]
        return self._parse_const_int()

    def _looks_like_case_label(self) -> bool:
        """Look ahead to see whether the current tokens begin a new CASE branch label."""
        saved = self.pos
        try:
            while True:
                if self.match_op("-", "+"):
                    self.advance()
                t = self.peek()
                if t.kind == "INT":
                    self.advance()
                elif t.kind == "ID" and t.value.upper() in self.enums:
                    self.advance()
                else:
                    return False
                if self.match_punct(".."):
                    self.advance()
                    if self.match_op("-", "+"):
                        self.advance()
                    t2 = self.peek()
                    if t2.kind == "INT":
                        self.advance()
                    elif t2.kind == "ID" and t2.value.upper() in self.enums:
                        self.advance()
                    else:
                        return False
                if self.match_punct(","):
                    self.advance()
                    continue
                return self.match_punct(":")
        finally:
            self.pos = saved

    def _parse_case_arm_stmts(self) -> list[Any]:
        stmts: list[Any] = []
        while self.peek().kind != "EOF" and not self.match_kw("ELSE", "END_CASE"):
            if self._looks_like_case_label():
                break
            if self.match_punct(";"):
                self.advance()
                continue
            stmts.append(self.parse_stmt())
        return stmts

    def _parse_for(self) -> ForStmt:
        self.expect_kw("FOR")
        var_name = self.expect_id().value
        self.expect_op(":=")
        start_expr = self.parse_expr()
        self.expect_kw("TO")
        end_expr = self.parse_expr()
        step_expr = None
        if self.match_kw("BY"):
            self.advance()
            step_expr = self.parse_expr()
        self.expect_kw("DO")
        body = self.parse_stmt_list(stop_kws=("END_FOR",))
        self.expect_kw("END_FOR")
        if self.match_punct(";"):
            self.advance()
        return ForStmt(
            var_name=var_name,
            start_expr=start_expr,
            end_expr=end_expr,
            step_expr=step_expr,
            body=body,
        )

    def _parse_lvalue(self) -> Any:
        node: Any = VarRef(self.expect_id().value)
        while True:
            if self.match_punct("["):
                self.advance()
                idx = self.parse_expr()
                node = IndexRef(base=node, index=idx)
                while self.match_punct(","):
                    self.advance()
                    idx2 = self.parse_expr()
                    node = IndexRef(base=node, index=idx2)
                self.expect_punct("]")
            elif self.match_punct("."):
                self.advance()
                fld = self.expect_id().value
                node = FieldRef(base=node, field_name=fld)
            else:
                break
        return node

    def parse_expr(self) -> Any:
        return self._parse_or()

    def _parse_or(self) -> Any:
        left = self._parse_xor()
        while self.match_kw("OR"):
            self.advance()
            right = self._parse_xor()
            left = BinOp("OR", left, right)
        return left

    def _parse_xor(self) -> Any:
        left = self._parse_and()
        while self.match_kw("XOR"):
            self.advance()
            right = self._parse_and()
            left = BinOp("XOR", left, right)
        return left

    def _parse_and(self) -> Any:
        left = self._parse_cmp()
        while self.match_kw("AND") or self.match_op("&"):
            self.advance()
            right = self._parse_cmp()
            left = BinOp("AND", left, right)
        return left

    def _parse_cmp(self) -> Any:
        left = self._parse_add()
        while self.match_op("=", "<>", "<", "<=", ">", ">="):
            op = self.advance().value
            right = self._parse_add()
            left = BinOp(op, left, right)
        return left

    def _parse_add(self) -> Any:
        left = self._parse_mul()
        while self.match_op("+", "-"):
            op = self.advance().value
            right = self._parse_mul()
            left = BinOp(op, left, right)
        return left

    def _parse_mul(self) -> Any:
        left = self._parse_unary()
        while self.match_op("*", "/") or self.match_kw("MOD"):
            tok = self.advance()
            op = "MOD" if tok.kind == "KW" else tok.value
            right = self._parse_unary()
            left = BinOp(op, left, right)
        return left

    def _parse_unary(self) -> Any:
        if self.match_kw("NOT"):
            self.advance()
            return UnaryOp("NOT", self._parse_unary())
        if self.match_op("-", "+"):
            op = self.advance().value
            return UnaryOp(op, self._parse_unary())
        return self._parse_primary()

    def _parse_primary(self) -> Any:
        t = self.peek()
        if t.kind == "KW" and t.value == "TRUE":
            self.advance()
            return BoolLit(True)
        if t.kind == "KW" and t.value == "FALSE":
            self.advance()
            return BoolLit(False)
        if t.kind == "INT":
            self.advance()
            return IntLit(t.value)
        if t.kind == "REAL":
            self.advance()
            return RealLit(t.value)
        if t.kind == "TIME":
            self.advance()
            return TimeLit(t.value)
        if self.match_punct("("):
            self.advance()
            expr = self.parse_expr()
            self.expect_punct(")")
            return expr
        if t.kind == "ID":
            if self.peek(1).kind == "PUNCT" and self.peek(1).value == "(":
                fn = self.advance().value
                self.expect_punct("(")
                args: list[tuple[str | None, Any]] = []
                while not self.match_punct(")"):
                    if self.peek().kind == "ID" and self.peek(1).kind == "OP" and self.peek(1).value == ":=":
                        pname = self.advance().value
                        self.advance()
                        args.append((pname, self.parse_expr()))
                    else:
                        args.append((None, self.parse_expr()))
                    if self.match_punct(","):
                        self.advance()
                    else:
                        break
                self.expect_punct(")")
                return CallExpr(func=fn, args=args)
            node = self._parse_lvalue()
            if isinstance(node, VarRef) and node.name.upper() in self.enums:
                return IntLit(self.enums[node.name.upper()])
            return node
        raise UnsupportedSTConstructError(f"Unexpected token in expression: {t.raw!r} at pos {t.pos}")


def parse_st_function_block(candidate: dict[str, Any] | str) -> STProgram:
    """Parse candidate ST code and supporting_objects into an AST STProgram."""
    norm = normalize_candidate(candidate)
    raw_decl = norm.get("declaration", "") or ""
    raw_impl = norm.get("implementation", "") or ""
    supporting = norm.get("supporting_objects") or []

    # Strip any duplicate END_FUNCTION_BLOCK / preamble cleanly when stitching
    supp_src_parts: list[str] = []
    for obj in supporting:
        if isinstance(obj, dict):
            s_decl = (obj.get("declaration") or "").strip()
            if s_decl:
                supp_src_parts.append(s_decl)
            kind = (obj.get("kind") or "").upper()
            if kind in ("FUNCTION", "METHOD", "POU") and "FUNCTION " in s_decl.upper():
                raise UnsupportedSTConstructError(
                    f"User-defined supporting {kind} {obj.get('name')} is outside symbolic fragment"
                )

    combined = "\n".join(supp_src_parts + [raw_decl, raw_impl])
    tokens = tokenize_st(combined)
    parser = _STParser(tokens)
    return parser.parse_program(raw_decl=raw_decl, raw_impl=raw_impl)


# ---------------------------------------------------------------------------
# Pre-Scan Initial Instance Verification
# ---------------------------------------------------------------------------


def _eval_const_expr(expr: Any, enums: dict[str, int]) -> Any:
    if expr is None:
        return None
    if isinstance(expr, BoolLit):
        return expr.value
    if isinstance(expr, IntLit):
        return expr.value
    if isinstance(expr, RealLit):
        return float(expr.value)
    if isinstance(expr, TimeLit):
        return expr.ms
    if isinstance(expr, UnaryOp):
        v = _eval_const_expr(expr.operand, enums)
        if expr.op == "NOT":
            return not bool(v)
        if expr.op == "-":
            return -v
        if expr.op == "+":
            return +v
    if isinstance(expr, BinOp):
        l = _eval_const_expr(expr.left, enums)
        r = _eval_const_expr(expr.right, enums)
        if expr.op == "+":
            return l + r
        if expr.op == "-":
            return l - r
        if expr.op == "*":
            return l * r
    if isinstance(expr, VarRef) and expr.name.upper() in enums:
        return enums[expr.name.upper()]
    raise UnsupportedSTConstructError("Non-constant initializer expression")


def default_python_value(st_type: STType, enums: dict[str, int], init_expr: Any = None) -> Any:
    """Compute the IEC 61131-3 default pre-invocation value for a variable."""
    if init_expr is not None:
        if isinstance(init_expr, list):
            return [_eval_const_expr(x, enums) for x in init_expr]
        val = _eval_const_expr(init_expr, enums)
        if st_type.is_boolean and isinstance(val, int):
            return bool(val)
        return val
    if st_type.kind == "BOOL":
        return False
    if st_type.kind in ("INT_SUBRANGE", "INT_UNBOUNDED", "TIME", "ENUM", "WORD"):
        return 0
    if st_type.kind == "REAL":
        return 0.0
    if st_type.kind == "ARRAY":
        count = st_type.arr_high - st_type.arr_low + 1
        return [default_python_value(st_type.elem_type, enums) for _ in range(count)]
    if st_type.kind == "STRUCT":
        return {fn: default_python_value(ft, enums) for fn, ft in st_type.fields}
    return None


def check_st_initial_instance(program: STProgram, task: dict[str, Any]) -> list[str]:
    """Check pre-invocation INITIAL_INSTANCE constraints on OUTPUT initializers."""
    failures: list[str] = []
    init_cond = task.get("initial_conditions")
    if not isinstance(init_cond, dict):
        return failures

    output_names = {
        x.get("name")
        for x in task.get("interface", [])
        if isinstance(x, dict) and x.get("direction") in ("OUTPUT", "IN_OUT")
    }
    for key, expected_val in init_cond.items():
        if output_names and key not in output_names:
            # Skip reference-only observer variables such as internal `phase`
            continue
        decl = program.decls_by_lower.get(key.lower())
        if decl is None:
            failures.append(f"Missing declared OUTPUT variable {key} for INITIAL_INSTANCE check")
            continue
        if decl.st_type.kind in ("ARRAY", "STRUCT"):
            continue
        actual_val = default_python_value(decl.st_type, program.enums, decl.init_expr)
        if isinstance(expected_val, bool):
            ok = bool(actual_val) is expected_val
        else:
            ok = actual_val == expected_val
        if not ok:
            failures.append(
                f"INITIAL_INSTANCE mismatch on {key}: declared initial={actual_val!r}, expected={expected_val!r}"
            )
    return failures


# ---------------------------------------------------------------------------
# ST -> SMV Symbolic Compiler (SSA per Scan)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SMVExpr:
    """Symbolic expression paired with its SMV sort ('bool', 'int', 'real', 'word[N]')."""

    sort: str
    code: str


class _STToSMVCompiler:
    """Compiles a parsed STProgram into SMV VAR/INIT/INVAR/ASSIGN/DEFINE blocks."""

    def __init__(
        self,
        program: STProgram,
        force_smt_integers: bool = False,
        observer_clk_symbols: tuple[str, str, str] | None = None,
        mapped_inputs: dict[str, tuple[str, str]] | None = None,
    ) -> None:
        self.program = program
        self.force_smt_integers = force_smt_integers
        # Optional (dt_ms_sym, first_scan_sym, clk_now_sym) reused from observer SMV
        self.observer_clk_symbols = observer_clk_symbols
        # External ST paths mapped to observer SMV vars: lower_path -> (sort, smv_symbol)
        self.mapped_inputs = mapped_inputs or {}

        self.var_decls: list[str] = []
        self.init_clauses: list[str] = []
        self.invar_clauses: list[str] = []
        self.assign_clauses: list[str] = []
        self.define_clauses: list[str] = []

        self._ssa_counter = 0
        self._loop_exit_depth = 0
        self._loop_depth = 0
        self._fb_pending_inputs: dict[str, dict[str, SMVExpr]] = {}
        self._fb_state_vars: dict[str, dict[str, str]] = {}
        self._timer_used = False
        self._local_clock_emitted = False

    def _fresh_ssa(self, sort: str, expr_code: str, prefix: str = "cand_ssa") -> SMVExpr:
        name = f"{prefix}_{self._ssa_counter}"
        self._ssa_counter += 1
        self.define_clauses.append(f"  {name} := {expr_code};")
        return SMVExpr(sort=sort, code=name)

    def _coerce(self, expr: SMVExpr, target_sort: str) -> SMVExpr:
        if expr.sort == target_sort:
            return expr
        if target_sort == "bool" and expr.sort in ("int", "subrange"):
            return SMVExpr("bool", f"(({expr.code}) != 0)")
        if target_sort in ("int", "subrange") and expr.sort == "bool":
            return SMVExpr(target_sort, f"(({expr.code}) ? 1 : 0)")
        if target_sort == "int" and expr.sort == "subrange":
            return SMVExpr("int", expr.code)
        if target_sort == "subrange" and expr.sort == "int":
            return SMVExpr("subrange", expr.code)
        if target_sort == "real" and expr.sort in ("int", "subrange"):
            return SMVExpr("real", f"toint({expr.code})" if False else expr.code)
        if target_sort.startswith("word[") and expr.sort in ("int", "subrange"):
            bits = int(target_sort[5:-1])
            return SMVExpr(target_sort, f"uwconst({expr.code}, {bits})")
        return SMVExpr(target_sort, expr.code)

    def _smv_type_str(self, st_type: STType) -> tuple[str, str]:
        """Return (smv_decl_type, internal_sort) for a scalar STType."""
        if st_type.kind == "BOOL":
            return "boolean", "bool"
        if st_type.kind == "REAL":
            return "real", "real"
        if st_type.kind == "WORD":
            bits = st_type.bitwidth or 32
            return f"unsigned word[{bits}]", f"word[{bits}]"
        if st_type.kind == "TIME":
            return "integer", "int"
        if st_type.kind in ("INT_UNBOUNDED", "ENUM"):
            if self.force_smt_integers:
                return "integer", "int"
            return "-128..255", "subrange"
        if st_type.kind == "INT_SUBRANGE":
            if self.force_smt_integers:
                return "integer", "int"
            lo = 0 if st_type.low is None else st_type.low
            hi = 255 if st_type.high is None else st_type.high
            if (hi - lo) <= 65536 and lo >= -128 and hi <= 255:
                return f"{lo}..{hi}", "subrange"
            return "integer", "int"
        raise UnsupportedSTConstructError(f"Cannot convert scalar type {st_type.base_name} to SMV")

    def _ensure_clock_symbols(self) -> tuple[str, str, str]:
        """Ensure (dt_ms_sym, first_scan_sym, clk_now_sym) exist for TON/TOF/TP timers."""
        self._timer_used = True
        if self.observer_clk_symbols is not None:
            return self.observer_clk_symbols
        if not self._local_clock_emitted:
            self._local_clock_emitted = True
            self.var_decls.extend(
                [
                    "  cand_dt_ms : integer;",
                    "  cand_first_scan : boolean;",
                    "  cand_clk : integer;",
                ]
            )
            self.init_clauses.extend(["cand_first_scan", "cand_clk = 0"])
            self.invar_clauses.extend(["cand_dt_ms >= 0", "cand_clk >= 0"])
            self.assign_clauses.extend(
                [
                    "  next(cand_first_scan) := FALSE;",
                    "  next(cand_clk) := cand_clk_now;",
                ]
            )
            self.define_clauses.append("  cand_clk_now := cand_first_scan ? 0 : cand_clk + cand_dt_ms;")
        return "cand_dt_ms", "cand_first_scan", "cand_clk_now"

    def _flatten_type_leaves(
        self,
        prefix: str,
        st_type: STType,
        section: str,
        init_expr: Any = None,
    ) -> list[tuple[tuple[Any, ...], STType, Any]]:
        """Flatten scalars, arrays, and structs into concrete leaf cells."""
        if st_type.kind == "FB":
            return []
        if st_type.kind == "STRUCT":
            leaves: list[tuple[tuple[Any, ...], STType, Any]] = []
            for fname, ftype in st_type.fields:
                leaves.extend(self._flatten_type_leaves(f"{prefix}.{fname}", ftype, section, None))
            return leaves
        if st_type.kind == "ARRAY":
            leaves = []
            init_items = init_expr if isinstance(init_expr, list) else []
            for idx_offset, idx in enumerate(range(st_type.arr_low, st_type.arr_high + 1)):
                elem_init = init_items[idx_offset] if idx_offset < len(init_items) else None
                leaves.extend(self._flatten_type_leaves(f"{prefix}[{idx}]", st_type.elem_type, section, elem_init))
            return leaves
        return [(self._path_key(prefix), st_type, init_expr)]

    @staticmethod
    def _path_key(path: str) -> tuple[Any, ...]:
        parts = re.split(r"(\.|\[|\])", path)
        out: list[Any] = []
        i = 0
        while i < len(parts):
            tok = parts[i]
            if tok in ("", ".", "]"):
                i += 1
                continue
            if tok == "[":
                out.append(int(parts[i + 1]))
                i += 2
                continue
            out.append(tok.lower())
            i += 1
        return tuple(out)

    @staticmethod
    def _sanitized_smv_id(key: tuple[Any, ...]) -> str:
        return "_".join(str(x) for x in key)

    def _default_smv_literal(self, st_type: STType, sort: str, init_expr: Any = None) -> SMVExpr:
        val = default_python_value(st_type, self.program.enums, init_expr)
        if sort == "bool":
            return SMVExpr("bool", "TRUE" if val else "FALSE")
        if sort == "real":
            s = str(val)
            if "." not in s and "e" not in s.lower():
                s += ".0"
            return SMVExpr("real", s)
        if sort.startswith("word["):
            bits = int(sort[5:-1])
            return SMVExpr(sort, f"0ud{bits}_{int(val)}")
        return SMVExpr(sort, str(int(val)))

    def compile(
        self,
        unmapped_input_strategy: str = "declare",
        external_out_prefix: str = "cand_out_",
    ) -> dict[str, Any]:
        """Compile the full single-scan step into SMV declarations & transitions."""
        state_env: dict[tuple[Any, ...], SMVExpr] = {}
        state_meta: dict[tuple[Any, ...], tuple[STType, STVarDecl, str]] = {}
        post_exprs: dict[str, SMVExpr] = {}

        # 1. Declare state & input symbols
        for decl in self.program.decls:
            if decl.st_type.kind == "FB":
                self._setup_fb_instance(decl.name, decl.st_type.fb_type or decl.st_type.base_name)
                continue

            leaves = self._flatten_type_leaves(decl.name, decl.st_type, decl.section, decl.init_expr)
            for key, leaf_type, leaf_init in leaves:
                smv_type_str, sort = self._smv_type_str(leaf_type)
                key_id = self._sanitized_smv_id(key)
                if key_id in self.mapped_inputs:
                    m_sort, m_sym = self.mapped_inputs[key_id]
                    init_state_expr = SMVExpr(m_sort, m_sym)
                    state_env[key] = init_state_expr
                    state_meta[key] = (leaf_type, decl, m_sym)
                    continue

                if decl.section == "CONSTANT":
                    state_env[key] = self._default_smv_literal(leaf_type, sort, leaf_init)
                    continue

                if decl.section == "INPUT":
                    sym = f"cand_in_{key_id}"
                    if unmapped_input_strategy == "declare":
                        self.var_decls.append(f"  {sym} : {smv_type_str};")
                    state_env[key] = SMVExpr(sort, sym)
                    state_meta[key] = (leaf_type, decl, sym)
                    continue

                if decl.section == "VAR_TEMP":
                    state_env[key] = self._default_smv_literal(leaf_type, sort, leaf_init)
                    continue

                # VAR, VAR_OUTPUT, VAR_IN_OUT (stateful across scans)
                sym = f"cand_state_{key_id}"
                lit = self._default_smv_literal(leaf_type, sort, leaf_init)
                self.var_decls.append(f"  {sym} : {smv_type_str};")
                self.assign_clauses.append(f"  init({sym}) := {lit.code};")
                state_env[key] = SMVExpr(sort, sym)
                state_meta[key] = (leaf_type, decl, sym)

        # 2. Execute scan statements symbolically from initial pre-scan env
        final_env, _, _ = self._exec_stmts(self.program.statements, dict(state_env), active_cond=None)

        # Freeze uncalled stateful FBs so their state variables never remain free nondeterministic inputs
        for fb_meta in self._fb_state_vars.values():
            if fb_meta.get("called") == "0":
                for sv in fb_meta.get("state_vars", ()):
                    self.assign_clauses.append(f"  next({sv}) := {sv};")

        # 3. Emit next-state updates and output DEFINEs
        for key, (leaf_type, decl, state_sym) in state_meta.items():
            if decl.section in ("INPUT", "VAR_TEMP", "CONSTANT"):
                continue
            key_id = self._sanitized_smv_id(key)
            final_val = final_env[key]
            # Wrap subrange integer arithmetic ONLY if subrange is 0..255 etc.
            _, target_sort = self._smv_type_str(leaf_type)
            coerced = self._coerce(final_val, target_sort)
            coerced = self._guard_subrange_expr(coerced, leaf_type)

            if decl.section in ("OUTPUT", "IN_OUT"):
                suffix = self._canonical_out_suffix(decl.name, key)
                out_sym = f"{external_out_prefix}{suffix}"
                self.define_clauses.append(f"  {out_sym} := {coerced.code};")
                post_exprs[suffix.lower()] = SMVExpr(coerced.sort, out_sym)
                if key_id not in self.mapped_inputs:
                    self.assign_clauses.append(f"  next({state_sym}) := {out_sym};")
            else:
                post_sym = f"cand_post_{key_id}"
                self.define_clauses.append(f"  {post_sym} := {coerced.code};")
                self.assign_clauses.append(f"  next({state_sym}) := {post_sym};")

        return {
            "var_decls": self.var_decls,
            "init_clauses": self.init_clauses,
            "invar_clauses": self.invar_clauses,
            "assign_clauses": self.assign_clauses,
            "define_clauses": self.define_clauses,
            "post_exprs": post_exprs,
            "uses_smt": self.force_smt_integers
            or self._timer_used
            or any("integer" in v or "real" in v or "word" in v for v in self.var_decls),
        }

    def _guard_subrange_expr(self, expr: SMVExpr, leaf_type: STType) -> SMVExpr:
        if expr.sort != "subrange" or self.force_smt_integers:
            return expr
        # Protect NuSMV BDD from out-of-range crash on buggy arithmetic
        if leaf_type.kind == "INT_SUBRANGE" and leaf_type.low == 0 and leaf_type.high in (255, 65535):
            mod_n = leaf_type.high + 1
            if expr.code.isdigit() and 0 <= int(expr.code) <= leaf_type.high:
                return expr
            return self._fresh_ssa(
                "subrange",
                f"(({expr.code}) >= 0 ? (({expr.code}) mod {mod_n}) : (((({expr.code}) mod {mod_n}) + {mod_n}) mod {mod_n}))",
                prefix="cand_w",
            )
        if leaf_type.kind == "INT_SUBRANGE":
            lo = -128 if leaf_type.low is None else leaf_type.low
            hi = 255 if leaf_type.high is None else leaf_type.high
        elif leaf_type.kind in ("INT_UNBOUNDED", "ENUM"):
            lo, hi = -128, 255
        else:
            return expr
        if re.fullmatch(r"-?\d+", expr.code) and lo <= int(expr.code) <= hi:
            return expr
        return self._fresh_ssa(
            "subrange",
            f"((({expr.code}) < {lo}) ? {lo} : ((({expr.code}) > {hi}) ? {hi} : ({expr.code})))",
            prefix="cand_w",
        )

    @staticmethod
    def _canonical_out_suffix(decl_name: str, key: tuple[Any, ...]) -> str:
        if len(key) == 1:
            return decl_name
        return "_".join([decl_name] + [str(k) for k in key[1:]])

    def _setup_fb_instance(self, inst_name: str, fb_type: str) -> None:
        lk = inst_name.lower()
        p = f"cand_fb_{inst_name}"
        if fb_type == "TON":
            self._ensure_clock_symbols()
            self.var_decls.extend(
                [
                    f"  {p}_active : boolean;",
                    f"  {p}_since : integer;",
                    f"  {p}_Q : boolean;",
                    f"  {p}_ET : integer;",
                ]
            )
            self.assign_clauses.extend(
                [
                    f"  init({p}_active) := FALSE;",
                    f"  init({p}_since) := 0;",
                    f"  init({p}_Q) := FALSE;",
                    f"  init({p}_ET) := 0;",
                ]
            )
            self._fb_state_vars[lk] = {
                "type": "TON",
                "prefix": p,
                "active": f"{p}_active",
                "since": f"{p}_since",
                "Q": f"{p}_Q",
                "ET": f"{p}_ET",
                "state_vars": [f"{p}_active", f"{p}_since", f"{p}_Q", f"{p}_ET"],
                "called": "0",
            }
        elif fb_type == "TOF":
            self._ensure_clock_symbols()
            self.var_decls.extend(
                [
                    f"  {p}_active : boolean;",
                    f"  {p}_since : integer;",
                    f"  {p}_prev_in : boolean;",
                    f"  {p}_Q : boolean;",
                    f"  {p}_ET : integer;",
                ]
            )
            self.assign_clauses.extend(
                [
                    f"  init({p}_active) := FALSE;",
                    f"  init({p}_since) := 0;",
                    f"  init({p}_prev_in) := FALSE;",
                    f"  init({p}_Q) := FALSE;",
                    f"  init({p}_ET) := 0;",
                ]
            )
            self._fb_state_vars[lk] = {
                "type": "TOF",
                "prefix": p,
                "Q": f"{p}_Q",
                "ET": f"{p}_ET",
                "state_vars": [f"{p}_active", f"{p}_since", f"{p}_prev_in", f"{p}_Q", f"{p}_ET"],
                "called": "0",
            }
        elif fb_type == "TP":
            self._ensure_clock_symbols()
            self.var_decls.extend(
                [
                    f"  {p}_active : boolean;",
                    f"  {p}_since : integer;",
                    f"  {p}_prev_in : boolean;",
                    f"  {p}_Q : boolean;",
                    f"  {p}_ET : integer;",
                ]
            )
            self.assign_clauses.extend(
                [
                    f"  init({p}_active) := FALSE;",
                    f"  init({p}_since) := 0;",
                    f"  init({p}_prev_in) := FALSE;",
                    f"  init({p}_Q) := FALSE;",
                    f"  init({p}_ET) := 0;",
                ]
            )
            self._fb_state_vars[lk] = {
                "type": "TP",
                "prefix": p,
                "Q": f"{p}_Q",
                "ET": f"{p}_ET",
                "state_vars": [f"{p}_active", f"{p}_since", f"{p}_prev_in", f"{p}_Q", f"{p}_ET"],
                "called": "0",
            }
        elif fb_type in ("R_TRIG", "F_TRIG"):
            self.var_decls.extend(
                [
                    f"  {p}_m : boolean;",
                    f"  {p}_Q : boolean;",
                ]
            )
            init_m = "FALSE"
            self.assign_clauses.extend(
                [
                    f"  init({p}_m) := {init_m};",
                    f"  init({p}_Q) := FALSE;",
                ]
            )
            self._fb_state_vars[lk] = {
                "type": fb_type,
                "prefix": p,
                "Q": f"{p}_Q",
                "state_vars": [f"{p}_m", f"{p}_Q"],
                "called": "0",
            }
        elif fb_type in ("SR", "RS"):
            self.var_decls.append(f"  {p}_Q1 : boolean;")
            self.assign_clauses.append(f"  init({p}_Q1) := FALSE;")
            self._fb_state_vars[lk] = {
                "type": fb_type,
                "prefix": p,
                "Q1": f"{p}_Q1",
                "state_vars": [f"{p}_Q1"],
                "called": "0",
            }
        elif fb_type == "CTU":
            self.var_decls.extend(
                [
                    f"  {p}_prev_cu : boolean;",
                    f"  {p}_CV : integer;",
                    f"  {p}_Q : boolean;",
                ]
            )
            self.assign_clauses.extend(
                [
                    f"  init({p}_prev_cu) := FALSE;",
                    f"  init({p}_CV) := 0;",
                    f"  init({p}_Q) := FALSE;",
                ]
            )
            self._fb_state_vars[lk] = {
                "type": "CTU",
                "prefix": p,
                "Q": f"{p}_Q",
                "CV": f"{p}_CV",
                "state_vars": [f"{p}_prev_cu", f"{p}_CV", f"{p}_Q"],
                "called": "0",
            }
        elif fb_type == "CTD":
            self.var_decls.extend(
                [
                    f"  {p}_prev_cd : boolean;",
                    f"  {p}_CV : integer;",
                    f"  {p}_Q : boolean;",
                ]
            )
            self.assign_clauses.extend(
                [
                    f"  init({p}_prev_cd) := FALSE;",
                    f"  init({p}_CV) := 0;",
                    f"  init({p}_Q) := FALSE;",
                ]
            )
            self._fb_state_vars[lk] = {
                "type": "CTD",
                "prefix": p,
                "Q": f"{p}_Q",
                "CV": f"{p}_CV",
                "state_vars": [f"{p}_prev_cd", f"{p}_CV", f"{p}_Q"],
                "called": "0",
            }
        else:
            raise UnsupportedSTConstructError(f"Unsupported standard function block type {fb_type}")

    # --- Symbolic Execution of Statements ---

    def _exec_stmts(
        self,
        stmts: list[Any],
        env: dict[tuple[Any, ...], SMVExpr],
        active_cond: SMVExpr | None,
    ) -> tuple[dict[tuple[Any, ...], SMVExpr], dict[tuple[Any, ...], SMVExpr] | None, SMVExpr | None]:
        cur = env
        for stmt in stmts:
            if isinstance(stmt, AssignStmt):
                cur = self._exec_assign(stmt.target, stmt.expr, cur)
            elif isinstance(stmt, IfStmt):
                cur = self._exec_if(stmt, cur, active_cond)
            elif isinstance(stmt, CaseStmt):
                cur = self._exec_case(stmt, cur, active_cond)
            elif isinstance(stmt, ForStmt):
                cur = self._exec_for(stmt, cur, active_cond)
            elif isinstance(stmt, FBCallStmt):
                cur = self._exec_fb_call(stmt, cur, active_cond)
            elif isinstance(stmt, ExitStmt):
                raise UnsupportedSTConstructError("EXIT inside loop is not supported unless unrolled without break")
            else:
                raise UnsupportedSTConstructError(f"Unsupported statement {type(stmt).__name__}")
        return cur, None, None

    def _exec_assign(
        self,
        target: Any,
        expr: Any,
        env: dict[tuple[Any, ...], SMVExpr],
    ) -> dict[tuple[Any, ...], SMVExpr]:
        # Handle FB input pin assignment before invocation e.g. timer.IN := ...;
        if isinstance(target, FieldRef) and isinstance(target.base, VarRef):
            inst_k = target.base.name.lower()
            if inst_k in self._fb_state_vars:
                val = self._eval_expr(expr, env)
                self._fb_pending_inputs.setdefault(inst_k, {})[target.field_name.upper()] = val
                return env

        val = self._eval_expr(expr, env)
        resolved = self._resolve_lvalue_keys(target, env)
        if len(resolved) == 1:
            key, cond = resolved[0]
            if cond is None:
                prev = env.get(key)
                if prev is not None:
                    val = self._coerce(val, prev.sort)
                env = dict(env)
                env[key] = self._materialise_if_complex(val)
                return env
        # Dynamic index write across multiple candidate cells
        env = dict(env)
        for key, cond in resolved:
            prev = env[key]
            cval = self._coerce(val, prev.sort)
            merged = self._fresh_ssa(prev.sort, f"(({cond.code}) ? ({cval.code}) : ({prev.code}))")
            env[key] = merged
        return env

    def _materialise_if_complex(self, expr: SMVExpr) -> SMVExpr:
        if len(expr.code) <= 32 and "?" not in expr.code:
            return expr
        return self._fresh_ssa(expr.sort, expr.code)

    def _resolve_lvalue_keys(
        self,
        target: Any,
        env: dict[tuple[Any, ...], SMVExpr],
    ) -> list[tuple[tuple[Any, ...], SMVExpr | None]]:
        """Resolve an lvalue AST into concrete flattened keys (plus optional guard for dynamic index)."""
        if isinstance(target, VarRef):
            key = (target.name.lower(),)
            if key not in env:
                raise UnsupportedSTConstructError(f"Undeclared assignment target {target.name}")
            return [(key, None)]
        if isinstance(target, FieldRef):
            base_keys = self._resolve_prefix(target.base, env)
            out: list[tuple[tuple[Any, ...], SMVExpr | None]] = []
            for pkey, gcond in base_keys:
                full = pkey + (target.field_name.lower(),)
                if full not in env:
                    raise UnsupportedSTConstructError(f"Unknown struct field {target.field_name}")
                out.append((full, gcond))
            return out
        if isinstance(target, IndexRef):
            base_keys = self._resolve_prefix(target.base, env)
            static_idx = self._try_eval_const_int(target.index, env)
            if static_idx is not None:
                out = [(pkey + (static_idx,), gcond) for pkey, gcond in base_keys if (pkey + (static_idx,)) in env]
                if not out:
                    raise UnsupportedSTConstructError(f"Array index {static_idx} is out of declared ARRAY bounds")
                return out
            idx_expr = self._eval_expr(target.index, env)
            out = []
            for pkey, gcond in base_keys:
                matching = [
                    k[len(pkey)]
                    for k in env
                    if len(k) > len(pkey) and k[: len(pkey)] == pkey and isinstance(k[len(pkey)], int)
                ]
                for elem_idx in sorted(set(matching)):
                    eq = SMVExpr("bool", f"(({idx_expr.code}) = {elem_idx})")
                    comb = eq if gcond is None else SMVExpr("bool", f"(({gcond.code}) & ({eq.code}))")
                    out.append((pkey + (elem_idx,), comb))
            if not out:
                raise UnsupportedSTConstructError("Dynamic index applied to non-array or empty range")
            return out
        raise UnsupportedSTConstructError(f"Unsupported assignment target {target}")

    def _resolve_prefix(
        self,
        node: Any,
        env: dict[tuple[Any, ...], SMVExpr],
    ) -> list[tuple[tuple[Any, ...], SMVExpr | None]]:
        if isinstance(node, VarRef):
            return [((node.name.lower(),), None)]
        if isinstance(node, FieldRef):
            return [(p + (node.field_name.lower(),), g) for p, g in self._resolve_prefix(node.base, env)]
        if isinstance(node, IndexRef):
            static_idx = self._try_eval_const_int(node.index, env)
            base_list = self._resolve_prefix(node.base, env)
            if static_idx is not None:
                out = [
                    (p + (static_idx,), g)
                    for p, g in base_list
                    if any(len(k) >= len(p) + 1 and k[: len(p) + 1] == (p + (static_idx,)) for k in env)
                ]
                if not out:
                    raise UnsupportedSTConstructError(f"Array index {static_idx} is out of declared ARRAY bounds")
                return out
            idx_expr = self._eval_expr(node.index, env)
            out = []
            for p, g in base_list:
                matching = [
                    k[len(p)] for k in env if len(k) > len(p) and k[: len(p)] == p and isinstance(k[len(p)], int)
                ]
                for elem_idx in sorted(set(matching)):
                    eq = SMVExpr("bool", f"(({idx_expr.code}) = {elem_idx})")
                    comb = eq if g is None else SMVExpr("bool", f"(({g.code}) & ({eq.code}))")
                    out.append((p + (elem_idx,), comb))
            if not out:
                raise UnsupportedSTConstructError("Dynamic index applied to non-array or empty range")
            return out
        raise UnsupportedSTConstructError("Unsupported base expression in lvalue")

    def _exec_if(
        self,
        stmt: IfStmt,
        env: dict[tuple[Any, ...], SMVExpr],
        active_cond: SMVExpr | None,
    ) -> dict[tuple[Any, ...], SMVExpr]:
        # Build nested right-to-left conditional merges while propagating non-None active_cond
        cond_exprs: list[SMVExpr] = []
        branch_envs: list[dict[tuple[Any, ...], SMVExpr]] = []
        prior_neg_conds: list[str] = []
        for cond_ast, body in stmt.branches:
            c = self._coerce(self._eval_expr(cond_ast, env), "bool")
            c_ssa = self._fresh_ssa("bool", c.code, prefix="cand_c")
            cond_exprs.append(c_ssa)
            eff = f"({c_ssa.code} & {' & '.join(prior_neg_conds)})" if prior_neg_conds else c_ssa.code
            if active_cond is not None:
                eff = f"(({active_cond.code}) & {eff})"
            b_env, _, _ = self._exec_stmts(body, dict(env), SMVExpr("bool", eff))
            branch_envs.append(b_env)
            prior_neg_conds.append(f"!({c_ssa.code})")
        else_eff = " & ".join(prior_neg_conds) if prior_neg_conds else "TRUE"
        if active_cond is not None:
            else_eff = f"(({active_cond.code}) & {else_eff})"
        cur_env, _, _ = self._exec_stmts(stmt.else_stmts, dict(env), SMVExpr("bool", else_eff))

        for cond_ssa, then_env in reversed(list(zip(cond_exprs, branch_envs))):
            cur_env = self._merge_envs(cond_ssa, then_env, cur_env)
        return cur_env

    def _merge_envs(
        self,
        cond_ssa: SMVExpr,
        then_env: dict[tuple[Any, ...], SMVExpr],
        else_env: dict[tuple[Any, ...], SMVExpr],
    ) -> dict[tuple[Any, ...], SMVExpr]:
        merged = dict(else_env)
        for key, t_val in then_env.items():
            e_val = else_env.get(key)
            if e_val is None:
                merged[key] = t_val
                continue
            if t_val.code == e_val.code:
                continue
            target_sort = (
                t_val.sort if t_val.sort == e_val.sort else ("int" if "int" in (t_val.sort, e_val.sort) else t_val.sort)
            )
            t_c = self._coerce(t_val, target_sort)
            e_c = self._coerce(e_val, target_sort)
            merged[key] = self._fresh_ssa(
                target_sort,
                f"(({cond_ssa.code}) ? ({t_c.code}) : ({e_c.code}))",
            )
        return merged

    def _exec_case(
        self,
        stmt: CaseStmt,
        env: dict[tuple[Any, ...], SMVExpr],
        active_cond: SMVExpr | None,
    ) -> dict[tuple[Any, ...], SMVExpr]:
        sel = self._eval_expr(stmt.expr, env)
        sel_ssa = self._fresh_ssa(sel.sort, sel.code, prefix="cand_sel")
        conds: list[SMVExpr] = []
        branch_envs: list[dict[tuple[Any, ...], SMVExpr]] = []
        case_neg_conds: list[str] = []
        for labels, arm_stmts in stmt.arms:
            parts: list[str] = []
            for lo, hi in labels:
                if hi is None:
                    parts.append(f"({sel_ssa.code} = {lo})")
                else:
                    parts.append(f"({sel_ssa.code} >= {lo} & {sel_ssa.code} <= {hi})")
            c_ssa = self._fresh_ssa("bool", " | ".join(parts), prefix="cand_c")
            conds.append(c_ssa)
            arm_eff = c_ssa.code if active_cond is None else f"(({active_cond.code}) & {c_ssa.code})"
            b_env, _, _ = self._exec_stmts(arm_stmts, dict(env), SMVExpr("bool", arm_eff))
            branch_envs.append(b_env)
            case_neg_conds.append(f"!({c_ssa.code})")
        else_eff = " & ".join(case_neg_conds) if case_neg_conds else "TRUE"
        if active_cond is not None:
            else_eff = f"(({active_cond.code}) & {else_eff})"
        cur_env, _, _ = self._exec_stmts(stmt.else_stmts, dict(env), SMVExpr("bool", else_eff))
        for c_ssa, then_env in reversed(list(zip(conds, branch_envs))):
            cur_env = self._merge_envs(c_ssa, then_env, cur_env)
        return cur_env

    def _exec_for(
        self,
        stmt: ForStmt,
        env: dict[tuple[Any, ...], SMVExpr],
        active_cond: SMVExpr | None,
    ) -> dict[tuple[Any, ...], SMVExpr]:
        start = self._try_eval_const_int(stmt.start_expr, env)
        end = self._try_eval_const_int(stmt.end_expr, env)
        step = 1 if stmt.step_expr is None else self._try_eval_const_int(stmt.step_expr, env)
        if start is None or end is None or step is None or step == 0:
            raise UnsupportedSTConstructError("FOR loop bounds/step must be compile-time integer constants")

        values: list[int] = []
        cur_i = start
        while (cur_i <= end) if step > 0 else (cur_i >= end):
            values.append(cur_i)
            if len(values) > 256:
                raise UnsupportedSTConstructError("FOR loop iteration bound exceeded 256")
            cur_i += step

        loop_key = (stmt.var_name.lower(),)
        cur_env = dict(env)
        self._loop_depth += 1
        try:
            for iv in values:
                cur_env[loop_key] = SMVExpr("int", str(iv))
                cur_env, _, _ = self._exec_stmts(stmt.body, cur_env, active_cond)
        finally:
            self._loop_depth -= 1
        # After normal loop termination in IEC ST, loop variable holds last+step (or final value)
        cur_env[loop_key] = SMVExpr("int", str(cur_i))
        return cur_env

    def _exec_fb_call(
        self,
        stmt: FBCallStmt,
        env: dict[tuple[Any, ...], SMVExpr],
        active_cond: SMVExpr | None,
    ) -> dict[tuple[Any, ...], SMVExpr]:
        lk = stmt.inst_name.lower()
        fb_meta = self._fb_state_vars.get(lk)
        if fb_meta is None:
            raise UnsupportedSTConstructError(f"Unsupported function block call {stmt.inst_name}(...)")
        if active_cond is not None or self._loop_depth > 0:
            raise UnsupportedSTConstructError(
                f"Conditional or looped invocation of stateful FUNCTION_BLOCK '{stmt.inst_name}' "
                f"inside IF/CASE/FOR is outside the sound synchronous scan fragment; invoke "
                f"'{stmt.inst_name}(...)' unconditionally once per scan and pass conditions via input pins"
            )
        if fb_meta["called"] == "1":
            raise UnsupportedSTConstructError(
                f"Multiple calls to the same FB instance {stmt.inst_name} per scan are unsupported"
            )
        fb_meta["called"] = "1"

        fb_type = fb_meta["type"]
        p = fb_meta["prefix"]
        inputs = dict(self._fb_pending_inputs.get(lk, {}))
        pos_names = {
            "TON": ["IN", "PT"],
            "TOF": ["IN", "PT"],
            "TP": ["IN", "PT"],
            "R_TRIG": ["CLK"],
            "F_TRIG": ["CLK"],
            "SR": ["SET1", "RESET"],
            "RS": ["SET", "RESET1"],
            "CTU": ["CU", "RESET", "PV"],
            "CTD": ["CD", "LOAD", "PV"],
        }[fb_type]
        out_bindings: list[tuple[str, Any]] = []
        pos_idx = 0
        for pname, node, is_arrow in stmt.args:
            if is_arrow:
                assert pname is not None
                out_bindings.append((pname.upper(), node))
            else:
                key_name = (
                    pname.upper() if pname else (pos_names[pos_idx] if pos_idx < len(pos_names) else f"ARG{pos_idx}")
                )
                if pname is None:
                    pos_idx += 1
                inputs[key_name] = self._eval_expr(node, env)

        cur_env = dict(env)
        if fb_type == "TON":
            dt_sym, first_sym, clk_sym = self._ensure_clock_symbols()
            in_e = self._coerce(inputs.get("IN", SMVExpr("bool", "FALSE")), "bool")
            pt_e = self._coerce(inputs.get("PT", SMVExpr("int", "0")), "int")
            in_ssa = self._fresh_ssa("bool", in_e.code, prefix=f"{p}_in")
            since_now = self._fresh_ssa(
                "int",
                f"(({in_ssa.code}) ? (({p}_active) ? {p}_since : {clk_sym}) : 0)",
                prefix=f"{p}_since_now",
            )
            et_raw = self._fresh_ssa(
                "int",
                f"(({in_ssa.code}) ? (({p}_active) ? ({clk_sym} - {p}_since) : 0) : 0)",
                prefix=f"{p}_et_raw",
            )
            et_now = self._fresh_ssa(
                "int",
                f"(({in_ssa.code}) ? (({et_raw.code} >= {pt_e.code}) ? {pt_e.code} : {et_raw.code}) : 0)",
                prefix=f"{p}_et_now",
            )
            q_now = self._fresh_ssa(
                "bool",
                f"(({in_ssa.code}) & (({et_raw.code}) >= ({pt_e.code})))",
                prefix=f"{p}_q_now",
            )
            self.assign_clauses.extend(
                [
                    f"  next({p}_active) := {in_ssa.code};",
                    f"  next({p}_since) := {since_now.code};",
                    f"  next({p}_Q) := {q_now.code};",
                    f"  next({p}_ET) := {et_now.code};",
                ]
            )
            cur_env[(lk, "q")] = q_now
            cur_env[(lk, "et")] = et_now
        elif fb_type == "TOF":
            dt_sym, first_sym, clk_sym = self._ensure_clock_symbols()
            in_e = self._coerce(inputs.get("IN", SMVExpr("bool", "FALSE")), "bool")
            pt_e = self._coerce(inputs.get("PT", SMVExpr("int", "0")), "int")
            in_ssa = self._fresh_ssa("bool", in_e.code, prefix=f"{p}_in")
            falling = self._fresh_ssa("bool", f"(!{in_ssa.code} & {p}_prev_in)", prefix=f"{p}_fall")
            active_now = self._fresh_ssa(
                "bool", f"(!{in_ssa.code} & ({p}_active | {falling.code}))", prefix=f"{p}_act_now"
            )
            since_now = self._fresh_ssa(
                "int",
                f"({in_ssa.code} ? 0 : ({falling.code} ? {clk_sym} : ({p}_active ? {p}_since : 0)))",
                prefix=f"{p}_since_now",
            )
            et_raw = self._fresh_ssa(
                "int",
                f"({active_now.code} ? ({clk_sym} - {since_now.code}) : 0)",
                prefix=f"{p}_et_raw",
            )
            q_now = self._fresh_ssa(
                "bool",
                f"({in_ssa.code} | ({active_now.code} & ({et_raw.code} < {pt_e.code})))",
                prefix=f"{p}_q_now",
            )
            self.assign_clauses.extend(
                [
                    f"  next({p}_prev_in) := {in_ssa.code};",
                    f"  next({p}_active) := {active_now.code};",
                    f"  next({p}_since) := {since_now.code};",
                    f"  next({p}_Q) := {q_now.code};",
                    f"  next({p}_ET) := {et_raw.code};",
                ]
            )
            cur_env[(lk, "q")] = q_now
            cur_env[(lk, "et")] = et_raw
        elif fb_type == "TP":
            dt_sym, first_sym, clk_sym = self._ensure_clock_symbols()
            in_e = self._coerce(inputs.get("IN", SMVExpr("bool", "FALSE")), "bool")
            pt_e = self._coerce(inputs.get("PT", SMVExpr("int", "0")), "int")
            in_ssa = self._fresh_ssa("bool", in_e.code, prefix=f"{p}_in")
            trig = self._fresh_ssa("bool", f"({in_ssa.code} & !{p}_prev_in & !{p}_active)", prefix=f"{p}_trig")
            since_now = self._fresh_ssa(
                "int",
                f"({trig.code} ? {clk_sym} : ({p}_active ? {p}_since : 0))",
                prefix=f"{p}_since_now",
            )
            et_now = self._fresh_ssa(
                "int",
                f"({trig.code} ? 0 : ({p}_active ? ({clk_sym} - {p}_since) : 0))",
                prefix=f"{p}_et_now",
            )
            q_now = self._fresh_ssa(
                "bool",
                f"(({trig.code} | {p}_active) & ({et_now.code} < {pt_e.code}))",
                prefix=f"{p}_q_now",
            )
            self.assign_clauses.extend(
                [
                    f"  next({p}_prev_in) := {in_ssa.code};",
                    f"  next({p}_active) := {q_now.code};",
                    f"  next({p}_since) := {since_now.code};",
                    f"  next({p}_Q) := {q_now.code};",
                    f"  next({p}_ET) := {et_now.code};",
                ]
            )
            cur_env[(lk, "q")] = q_now
            cur_env[(lk, "et")] = et_now
        elif fb_type == "R_TRIG":
            clk_e = self._coerce(inputs.get("CLK", SMVExpr("bool", "FALSE")), "bool")
            clk_ssa = self._fresh_ssa("bool", clk_e.code, prefix=f"{p}_clk")
            q_now = self._fresh_ssa("bool", f"({clk_ssa.code} & !{p}_m)", prefix=f"{p}_q_now")
            self.assign_clauses.extend(
                [
                    f"  next({p}_m) := {clk_ssa.code};",
                    f"  next({p}_Q) := {q_now.code};",
                ]
            )
            cur_env[(lk, "q")] = q_now
        elif fb_type == "F_TRIG":
            clk_e = self._coerce(inputs.get("CLK", SMVExpr("bool", "FALSE")), "bool")
            clk_ssa = self._fresh_ssa("bool", clk_e.code, prefix=f"{p}_clk")
            q_now = self._fresh_ssa("bool", f"(!{clk_ssa.code} & {p}_m)", prefix=f"{p}_q_now")
            self.assign_clauses.extend(
                [
                    f"  next({p}_m) := {clk_ssa.code};",
                    f"  next({p}_Q) := {q_now.code};",
                ]
            )
            cur_env[(lk, "q")] = q_now
        elif fb_type == "SR":
            s1 = self._coerce(inputs.get("SET1", SMVExpr("bool", "FALSE")), "bool")
            r = self._coerce(inputs.get("RESET", SMVExpr("bool", "FALSE")), "bool")
            q_now = self._fresh_ssa("bool", f"(({s1.code}) | (!({r.code}) & {p}_Q1))", prefix=f"{p}_q_now")
            self.assign_clauses.append(f"  next({p}_Q1) := {q_now.code};")
            cur_env[(lk, "q1")] = q_now
        elif fb_type == "RS":
            s = self._coerce(inputs.get("SET", SMVExpr("bool", "FALSE")), "bool")
            r1 = self._coerce(inputs.get("RESET1", SMVExpr("bool", "FALSE")), "bool")
            q_now = self._fresh_ssa("bool", f"(!({r1.code}) & (({s.code}) | {p}_Q1))", prefix=f"{p}_q_now")
            self.assign_clauses.append(f"  next({p}_Q1) := {q_now.code};")
            cur_env[(lk, "q1")] = q_now
        elif fb_type == "CTU":
            cu = self._coerce(inputs.get("CU", SMVExpr("bool", "FALSE")), "bool")
            rst = self._coerce(inputs.get("RESET", inputs.get("R", SMVExpr("bool", "FALSE"))), "bool")
            pv = self._coerce(inputs.get("PV", SMVExpr("int", "0")), "int")
            cu_ssa = self._fresh_ssa("bool", cu.code, prefix=f"{p}_cu")
            cv_now = self._fresh_ssa(
                "int",
                f"(({rst.code}) ? 0 : (({cu_ssa.code} & !{p}_prev_cu) ? ({p}_CV + 1) : {p}_CV))",
                prefix=f"{p}_cv_now",
            )
            q_now = self._fresh_ssa("bool", f"({cv_now.code} >= ({pv.code}))", prefix=f"{p}_q_now")
            self.assign_clauses.extend(
                [
                    f"  next({p}_prev_cu) := {cu_ssa.code};",
                    f"  next({p}_CV) := {cv_now.code};",
                    f"  next({p}_Q) := {q_now.code};",
                ]
            )
            cur_env[(lk, "q")] = q_now
            cur_env[(lk, "cv")] = cv_now
        elif fb_type == "CTD":
            cd = self._coerce(inputs.get("CD", SMVExpr("bool", "FALSE")), "bool")
            ld = self._coerce(inputs.get("LOAD", inputs.get("LD", SMVExpr("bool", "FALSE"))), "bool")
            pv = self._coerce(inputs.get("PV", SMVExpr("int", "0")), "int")
            cd_ssa = self._fresh_ssa("bool", cd.code, prefix=f"{p}_cd")
            cv_now = self._fresh_ssa(
                "int",
                f"(({ld.code}) ? ({pv.code}) : (({cd_ssa.code} & !{p}_prev_cd) ? ({p}_CV - 1) : {p}_CV))",
                prefix=f"{p}_cv_now",
            )
            q_now = self._fresh_ssa("bool", f"(({cv_now.code}) <= 0)", prefix=f"{p}_q_now")
            self.assign_clauses.extend(
                [
                    f"  next({p}_prev_cd) := {cd_ssa.code};",
                    f"  next({p}_CV) := {cv_now.code};",
                    f"  next({p}_Q) := {q_now.code};",
                ]
            )
            cur_env[(lk, "q")] = q_now
            cur_env[(lk, "cv")] = cv_now

        for pin_name, dest_lval in out_bindings:
            val = cur_env.get((lk, pin_name.lower()))
            if val is not None:
                cur_env = self._assign_smv_val(dest_lval, val, cur_env)
        return cur_env

    def _assign_smv_val(
        self, target: Any, val: SMVExpr, env: dict[tuple[Any, ...], SMVExpr]
    ) -> dict[tuple[Any, ...], SMVExpr]:
        resolved = self._resolve_lvalue_keys(target, env)
        env = dict(env)
        for key, cond in resolved:
            prev = env[key]
            cval = self._coerce(val, prev.sort)
            if cond is None:
                env[key] = cval
            else:
                env[key] = self._fresh_ssa(prev.sort, f"(({cond.code}) ? ({cval.code}) : ({prev.code}))")
        return env

    # --- Symbolic Expression Evaluation ---

    def _try_eval_const_int(self, node: Any, env: dict[tuple[Any, ...], SMVExpr]) -> int | None:
        if isinstance(node, IntLit):
            return node.value
        if isinstance(node, VarRef):
            k = (node.name.lower(),)
            val = env.get(k)
            if val is not None and re.fullmatch(r"-?\d+", val.code):
                return int(val.code)
            return None
        if isinstance(node, UnaryOp):
            v = self._try_eval_const_int(node.operand, env)
            if v is None:
                return None
            return -v if node.op == "-" else (v if node.op == "+" else None)
        if isinstance(node, BinOp):
            l = self._try_eval_const_int(node.left, env)
            r = self._try_eval_const_int(node.right, env)
            if l is None or r is None:
                return None
            if node.op == "+":
                return l + r
            if node.op == "-":
                return l - r
            if node.op == "*":
                return l * r
            if node.op == "/" and r != 0:
                return int(l / r)
            if node.op == "MOD" and r != 0:
                return l % r
        return None

    def _eval_expr(self, node: Any, env: dict[tuple[Any, ...], SMVExpr]) -> SMVExpr:
        if isinstance(node, BoolLit):
            return SMVExpr("bool", "TRUE" if node.value else "FALSE")
        if isinstance(node, IntLit):
            return SMVExpr("int", str(node.value))
        if isinstance(node, RealLit):
            return SMVExpr("real", node.value)
        if isinstance(node, TimeLit):
            return SMVExpr("int", str(node.ms))
        if isinstance(node, VarRef):
            key = (node.name.lower(),)
            if key in env:
                return env[key]
            raise UnsupportedSTConstructError(f"Undeclared identifier {node.name}")
        if isinstance(node, (FieldRef, IndexRef)):
            return self._eval_access(node, env)
        if isinstance(node, UnaryOp):
            inner = self._eval_expr(node.operand, env)
            if node.op == "NOT":
                if inner.sort == "bool" or inner.sort.startswith("word["):
                    return SMVExpr(inner.sort, f"!({inner.code})")
                return SMVExpr("bool", f"!({self._coerce(inner, 'bool').code})")
            if node.op == "-":
                if inner.sort == "bool":
                    raise UnsupportedSTConstructError("Cannot negate BOOL")
                return SMVExpr(inner.sort, f"-({inner.code})")
            if node.op == "+":
                return inner
        if isinstance(node, BinOp):
            return self._eval_binop(node, env)
        if isinstance(node, CallExpr):
            return self._eval_call(node, env)
        raise UnsupportedSTConstructError(f"Unsupported expression node {type(node).__name__}")

    def _eval_access(self, node: Any, env: dict[tuple[Any, ...], SMVExpr]) -> SMVExpr:
        # Handle FB pin access before invocation e.g. timer.Q
        if isinstance(node, FieldRef) and isinstance(node.base, VarRef):
            fb_k = (node.base.name.lower(), node.field_name.lower())
            if fb_k in env:
                return env[fb_k]
            inst_k = node.base.name.lower()
            if inst_k in self._fb_state_vars:
                meta = self._fb_state_vars[inst_k]
                fld = node.field_name.upper()
                if fld in meta:
                    return SMVExpr("bool" if fld in ("Q", "Q1") else "int", meta[fld])
        resolved = self._resolve_lvalue_keys(node, env)
        if len(resolved) == 1 and resolved[0][1] is None:
            key = resolved[0][0]
            if key in env:
                return env[key]
            raise UnsupportedSTConstructError(f"Unknown cell {key}")
        # Dynamic index lookup: nested ternary over candidate leaves
        base_sort = env[resolved[-1][0]].sort
        acc = env[resolved[-1][0]].code
        for key, cond in reversed(resolved[:-1]):
            if cond is None:
                return env[key]
            acc = f"(({cond.code}) ? ({env[key].code}) : ({acc}))"
        return self._fresh_ssa(base_sort, acc)

    def _eval_binop(self, node: BinOp, env: dict[tuple[Any, ...], SMVExpr]) -> SMVExpr:
        l = self._eval_expr(node.left, env)
        r = self._eval_expr(node.right, env)
        op = node.op

        if op in ("AND", "OR", "XOR"):
            if l.sort.startswith("word[") or r.sort.startswith("word["):
                ws = l.sort if l.sort.startswith("word[") else r.sort
                lc = self._coerce(l, ws)
                rc = self._coerce(r, ws)
                smv_op = {"AND": "&", "OR": "|", "XOR": "xor"}[op]
                return SMVExpr(ws, f"(({lc.code}) {smv_op} ({rc.code}))")
            lc = self._coerce(l, "bool")
            rc = self._coerce(r, "bool")
            if op == "AND":
                return SMVExpr("bool", f"(({lc.code}) & ({rc.code}))")
            if op == "OR":
                return SMVExpr("bool", f"(({lc.code}) | ({rc.code}))")
            return SMVExpr("bool", f"(({lc.code}) xor ({rc.code}))")

        if op in ("=", "<>"):
            smv_op = "=" if op == "=" else "!="
            if l.sort == "bool" and r.sort == "bool":
                if op == "=":
                    return SMVExpr("bool", f"(({l.code}) <-> ({r.code}))")
                return SMVExpr("bool", f"(({l.code}) xor ({r.code}))")
            if l.sort != r.sort:
                target = (
                    "real"
                    if "real" in (l.sort, r.sort)
                    else (l.sort if l.sort.startswith("word[") else (r.sort if r.sort.startswith("word[") else "int"))
                )
                l = self._coerce(l, target)
                r = self._coerce(r, target)
            return SMVExpr("bool", f"(({l.code}) {smv_op} ({r.code}))")

        if op in ("<", "<=", ">", ">="):
            if l.sort != r.sort:
                target = (
                    "real"
                    if "real" in (l.sort, r.sort)
                    else (l.sort if l.sort.startswith("word[") else (r.sort if r.sort.startswith("word[") else "int"))
                )
                l = self._coerce(l, target)
                r = self._coerce(r, target)
            return SMVExpr("bool", f"(({l.code}) {op} ({r.code}))")

        if op in ("+", "-", "*", "/", "MOD"):
            if op in ("/", "MOD"):
                r_const = self._try_eval_const_int(node.right, env)
                if r_const == 0:
                    raise UnsupportedSTConstructError("Division or modulo by constant zero")
                if isinstance(node.right, RealLit) and float(node.right.value) == 0.0:
                    raise UnsupportedSTConstructError("Division by constant zero")
            target = (
                "real"
                if "real" in (l.sort, r.sort)
                else (l.sort if l.sort.startswith("word[") else (r.sort if r.sort.startswith("word[") else "int"))
            )
            lc = self._coerce(l, target)
            rc = self._coerce(r, target)
            if op == "MOD":
                return SMVExpr(target, f"(({lc.code}) mod ({rc.code}))")
            return SMVExpr(target, f"(({lc.code}) {op} ({rc.code}))")

        raise UnsupportedSTConstructError(f"Unsupported binary operator {op}")

    def _eval_call(self, node: CallExpr, env: dict[tuple[Any, ...], SMVExpr]) -> SMVExpr:
        fn = node.func.upper()
        vals = [self._eval_expr(a, env) for _, a in node.args]
        if fn == "ABS" and len(vals) == 1:
            x = vals[0]
            return self._fresh_ssa(x.sort, f"(({x.code}) >= 0 ? ({x.code}) : -({x.code}))")
        if fn == "MIN" and len(vals) == 2:
            a, b = vals
            return self._fresh_ssa(a.sort, f"(({a.code}) <= ({b.code}) ? ({a.code}) : ({b.code}))")
        if fn == "MAX" and len(vals) == 2:
            a, b = vals
            return self._fresh_ssa(a.sort, f"(({a.code}) >= ({b.code}) ? ({a.code}) : ({b.code}))")
        if fn == "LIMIT" and len(vals) == 3:
            mn, x, mx = vals
            return self._fresh_ssa(
                x.sort,
                f"(({x.code}) < ({mn.code}) ? ({mn.code}) : (({x.code}) > ({mx.code}) ? ({mx.code}) : ({x.code})))",
            )
        if fn == "SEL" and len(vals) == 3:
            g, in0, in1 = vals
            gc = self._coerce(g, "bool")
            return self._fresh_ssa(in1.sort, f"(({gc.code}) ? ({in1.code}) : ({in0.code}))")
        if fn == "SHL" and len(vals) == 2:
            val, nbits = vals
            if val.sort.startswith("word[") and re.fullmatch(r"\d+", nbits.code):
                return SMVExpr(val.sort, f"(({val.code}) << {nbits.code})")
        if fn == "SHR" and len(vals) == 2:
            val, nbits = vals
            if val.sort.startswith("word[") and re.fullmatch(r"\d+", nbits.code):
                return SMVExpr(val.sort, f"(({val.code}) >> {nbits.code})")
        if (
            fn
            in (
                "INT_TO_DINT",
                "DINT_TO_INT",
                "USINT_TO_INT",
                "INT_TO_USINT",
                "UINT_TO_INT",
                "INT_TO_UINT",
                "SINT_TO_INT",
                "INT_TO_SINT",
                "BOOL_TO_INT",
                "TIME_TO_DINT",
                "TIME_TO_INT",
            )
            and len(vals) == 1
        ):
            return self._coerce(vals[0], "int")
        if fn in ("INT_TO_BOOL", "DINT_TO_BOOL", "USINT_TO_BOOL") and len(vals) == 1:
            return self._coerce(vals[0], "bool")
        raise UnsupportedSTConstructError(f"Unsupported built-in function call {node.func}(...)")


# ---------------------------------------------------------------------------
# Observer SMV Parsing & Coupling
# ---------------------------------------------------------------------------


def discover_observer_smv(task_id: str) -> Path | None:
    """Locate the authoritative hand-audited SMV observer model for task_id."""
    models_dir = ROOT / "models"
    for suffix in ("_complete.smv", "_reference.smv"):
        candidate = models_dir / f"{task_id}{suffix}"
        if candidate.exists():
            return candidate
    return None


@dataclass
class ParsedObserverSMV:
    var_stmts: list[str]
    init_stmts: list[str]
    invar_stmts: list[str]
    assign_stmts: list[str]
    define_stmts: list[str]
    spec_stmts: list[str]
    var_types: dict[str, str]
    define_map: dict[str, str]
    uses_smt: bool


def _strip_smv_comments(text: str) -> str:
    return "\n".join(re.split(r"--", line, maxsplit=1)[0] for line in text.splitlines())


def _split_smv_statements(body: str) -> list[str]:
    """Split an SMV section body on `;` only when outside `case ... esac` blocks."""
    parts: list[str] = []
    cur: list[str] = []
    case_depth = 0
    i = 0
    n = len(body)
    while i < n:
        if body[i] == ";" and case_depth == 0:
            stmt = "".join(cur).strip()
            if stmt:
                parts.append(stmt)
            cur = []
            i += 1
            continue
        m_kw = re.match(r"\b(case|esac)\b", body[i:])
        if m_kw and (i == 0 or not (body[i - 1].isalnum() or body[i - 1] == "_")):
            kw = m_kw.group(1)
            if kw == "case":
                case_depth += 1
            elif case_depth > 0:
                case_depth -= 1
            cur.append(kw)
            i += len(kw)
            continue
        cur.append(body[i])
        i += 1
    tail = "".join(cur).strip()
    if tail:
        parts.append(tail)
    return parts


def _parse_observer_smv(smv_text: str) -> ParsedObserverSMV:
    stripped = _strip_smv_comments(smv_text)
    section_re = re.compile(r"(?m)^\s*(MODULE\b.*|VAR\b|INIT\b|INVAR\b|ASSIGN\b|DEFINE\b|LTLSPEC\b|INVARSPEC\b)")
    matches = list(section_re.finditer(stripped))

    var_stmts: list[str] = []
    init_stmts: list[str] = []
    invar_stmts: list[str] = []
    assign_stmts: list[str] = []
    define_stmts: list[str] = []
    spec_stmts: list[str] = []
    var_types: dict[str, str] = {}
    define_map: dict[str, str] = {}

    for idx, m in enumerate(matches):
        kw = m.group(1).split()[0]
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(stripped)
        body = stripped[start:end].strip()

        if kw == "MODULE":
            continue
        if kw in ("LTLSPEC", "INVARSPEC"):
            spec_text = stripped[m.start() : end].strip()
            for part in _split_smv_statements(spec_text):
                spec_stmts.append(part + ";")
            continue

        parts = _split_smv_statements(body)
        if kw == "VAR":
            for p in parts:
                var_stmts.append(p + ";")
                if ":" in p:
                    lhs, rhs = p.split(":", 1)
                    for vn in lhs.split(","):
                        var_types[vn.strip()] = rhs.strip()
        elif kw == "INIT":
            init_stmts.extend(parts)
        elif kw == "INVAR":
            invar_stmts.extend(parts)
        elif kw == "ASSIGN":
            for p in parts:
                assign_stmts.append(p + ";")
        elif kw == "DEFINE":
            for p in parts:
                define_stmts.append(p + ";")
                if ":=" in p:
                    lhs, rhs = p.split(":=", 1)
                    define_map[lhs.strip()] = rhs.strip()

    uses_smt = bool(re.search(r"\b(integer|real|word)\b", stripped))
    return ParsedObserverSMV(
        var_stmts=var_stmts,
        init_stmts=init_stmts,
        invar_stmts=invar_stmts,
        assign_stmts=assign_stmts,
        define_stmts=define_stmts,
        spec_stmts=spec_stmts,
        var_types=var_types,
        define_map=define_map,
        uses_smt=uses_smt,
    )


def _var_type_to_sort(type_str: str) -> str:
    low = type_str.strip().lower()
    if low == "boolean":
        return "bool"
    if low == "real":
        return "real"
    if "word" in low:
        m = re.search(r"word\[(\d+)\]", low)
        return f"word[{m.group(1)}]" if m else "word[32]"
    if ".." in low:
        return "subrange"
    return "int"


def _detect_mapped_inputs_and_outputs(
    program: STProgram,
    task: dict[str, Any],
    obs: ParsedObserverSMV,
) -> tuple[dict[str, tuple[str, str]], dict[str, str], set[str]]:
    """Map task interface & special IN_OUT arrays (e.g. PUB007) onto observer SMV symbols."""
    mapped_inputs: dict[str, tuple[str, str]] = {}
    output_bindings: dict[str, str] = {}  # observer_define_name -> candidate_out_suffix
    expected_outputs: set[str] = set()

    for item in task.get("interface", []):
        if not isinstance(item, dict):
            continue
        name = item.get("name", "")
        direction = item.get("direction", "")
        if not name:
            continue
        if direction == "INPUT":
            if name in obs.var_types:
                mapped_inputs[name.lower()] = (_var_type_to_sort(obs.var_types[name]), name)
            elif name in obs.define_map:
                mapped_inputs[name.lower()] = ("int", name)
        elif direction == "OUTPUT":
            expected_outputs.add(name)
            if name in obs.define_map:
                output_bindings[name] = name
        elif direction == "IN_OUT":
            decl = program.decls_by_lower.get(name.lower())
            if (
                decl
                and decl.st_type.kind == "ARRAY"
                and decl.st_type.elem_type
                and decl.st_type.elem_type.kind == "STRUCT"
            ):
                # Match PUB007-style flattened struct array observer (p{i}_pri, p{i}_sel, run{i} / post_run{i}, out_p{i}_pri)
                elem_fields = [f for f, _ in decl.st_type.elem_type.fields]
                for idx in range(decl.st_type.arr_low, decl.st_type.arr_high + 1):
                    for fn in elem_fields:
                        fn_l = fn.lower()
                        key_id = f"{name.lower()}_{idx}_{fn_l}"
                        cand_suffix = f"{name}_{idx}_{fn}"
                        # Heuristic matching against observer pre/post names
                        obs_in = None
                        obs_out = None
                        if f"p{idx}_{fn_l}" in obs.var_types:
                            obs_in = f"p{idx}_{fn_l}"
                        elif f"p{idx}_{fn_l[:3]}" in obs.var_types:
                            obs_in = f"p{idx}_{fn_l[:3]}"
                        elif fn_l.startswith("run") and f"run{idx}" in obs.var_types:
                            obs_in = f"run{idx}"
                        if obs_in:
                            mapped_inputs[key_id] = (_var_type_to_sort(obs.var_types[obs_in]), obs_in)
                        if f"post_run{idx}" in obs.define_map and fn_l.startswith("run"):
                            obs_out = f"post_run{idx}"
                        elif f"out_p{idx}_{fn_l}" in obs.define_map:
                            obs_out = f"out_p{idx}_{fn_l}"
                        elif f"out_p{idx}_{fn_l[:3]}" in obs.define_map:
                            obs_out = f"out_p{idx}_{fn_l[:3]}"
                        if obs_out:
                            expected_outputs.add(obs_out)
                            output_bindings[obs_out] = cand_suffix

    return mapped_inputs, output_bindings, expected_outputs


def _expr_has_out_of_bdd_int_lit(node: Any) -> bool:
    if node is None:
        return False
    if isinstance(node, list):
        return any(_expr_has_out_of_bdd_int_lit(item) for item in node)
    if isinstance(node, IntLit):
        return node.value < -128 or node.value > 255
    if isinstance(node, UnaryOp):
        return _expr_has_out_of_bdd_int_lit(node.operand)
    if isinstance(node, BinOp):
        return _expr_has_out_of_bdd_int_lit(node.left) or _expr_has_out_of_bdd_int_lit(node.right)
    if isinstance(node, IndexRef):
        return _expr_has_out_of_bdd_int_lit(node.base) or _expr_has_out_of_bdd_int_lit(node.index)
    if isinstance(node, FieldRef):
        return _expr_has_out_of_bdd_int_lit(node.base)
    if isinstance(node, CallExpr):
        return any(_expr_has_out_of_bdd_int_lit(arg) for _, arg in node.args)
    return False


def _expr_has_arithmetic(node: Any) -> bool:
    if node is None:
        return False
    if isinstance(node, UnaryOp):
        return node.op == "-" or _expr_has_arithmetic(node.operand)
    if isinstance(node, BinOp):
        if node.op in ("+", "-", "*", "/", "MOD"):
            return True
        return _expr_has_arithmetic(node.left) or _expr_has_arithmetic(node.right)
    if isinstance(node, IndexRef):
        return _expr_has_arithmetic(node.base) or _expr_has_arithmetic(node.index)
    if isinstance(node, FieldRef):
        return _expr_has_arithmetic(node.base)
    if isinstance(node, CallExpr):
        return any(_expr_has_arithmetic(arg) for _, arg in node.args)
    return False


def _root_var_name(target: Any) -> str | None:
    cur = target
    while isinstance(cur, (IndexRef, FieldRef)):
        cur = cur.base
    return cur.name if isinstance(cur, VarRef) else None


def _stmts_need_unbounded_integers(stmts: list[Any], program: STProgram) -> bool:
    for stmt in stmts:
        if isinstance(stmt, AssignStmt):
            if _expr_has_out_of_bdd_int_lit(stmt.target) or _expr_has_out_of_bdd_int_lit(stmt.expr):
                return True
            root_name = _root_var_name(stmt.target)
            if root_name:
                decl = program.decls_by_lower.get(root_name.lower())
                if decl is not None and decl.st_type.kind == "INT_UNBOUNDED" and _expr_has_arithmetic(stmt.expr):
                    return True
        elif isinstance(stmt, IfStmt):
            for cond, body in stmt.branches:
                if _expr_has_out_of_bdd_int_lit(cond) or _stmts_need_unbounded_integers(body, program):
                    return True
            if _stmts_need_unbounded_integers(stmt.else_stmts, program):
                return True
        elif isinstance(stmt, CaseStmt):
            if _expr_has_out_of_bdd_int_lit(stmt.expr):
                return True
            for labels, arm_stmts in stmt.arms:
                for lo, hi in labels:
                    if lo < -128 or lo > 255 or (hi is not None and (hi < -128 or hi > 255)):
                        return True
                if _stmts_need_unbounded_integers(arm_stmts, program):
                    return True
            if _stmts_need_unbounded_integers(stmt.else_stmts, program):
                return True
        elif isinstance(stmt, ForStmt):
            if (
                _expr_has_out_of_bdd_int_lit(stmt.start_expr)
                or _expr_has_out_of_bdd_int_lit(stmt.end_expr)
                or _expr_has_out_of_bdd_int_lit(stmt.step_expr)
                or _stmts_need_unbounded_integers(stmt.body, program)
            ):
                return True
        elif isinstance(stmt, FBCallStmt):
            for _, arg, _ in stmt.args:
                if _expr_has_out_of_bdd_int_lit(arg):
                    return True
    return False


def _ast_needs_unbounded_integers(program: STProgram) -> bool:
    """Return True when finite -128..255 BDD encoding would lose arithmetic soundness."""
    for decl in program.decls:
        if decl.section == "CONSTANT":
            continue
        if decl.st_type.kind == "INT_SUBRANGE" and (
            (decl.st_type.low is not None and decl.st_type.low < -128)
            or (decl.st_type.high is not None and decl.st_type.high > 255)
        ):
            return True
        if _expr_has_out_of_bdd_int_lit(decl.init_expr):
            return True
    return _stmts_need_unbounded_integers(program.statements, program)


def compile_st_to_smv(
    candidate: dict[str, Any] | str,
    task: dict[str, Any],
    observer_smv_path: Path | None = None,
) -> dict[str, Any]:
    """Compile an ST FUNCTION_BLOCK candidate into a verifiable SMV model.

    If an observer SMV exists for the task, rewrites its output DEFINEs to read
    directly from the symbolically compiled ST candidate scan transition.
    """
    program = parse_st_function_block(candidate)
    task_id = str(task.get("id") or "")
    if observer_smv_path is None and task_id:
        observer_smv_path = discover_observer_smv(task_id)

    if observer_smv_path is None or not observer_smv_path.exists():
        raise UnsupportedSTConstructError(f"No observer SMV specification available for task {task_id}")

    obs = _parse_observer_smv(observer_smv_path.read_text(encoding="utf-8"))
    mapped_inputs, output_bindings, expected_outputs = _detect_mapped_inputs_and_outputs(program, task, obs)

    missing_outs = [o for o in expected_outputs if o not in output_bindings]
    if missing_outs:
        raise UnsupportedSTConstructError(
            f"Observer SMV {observer_smv_path.name} missing output definitions for {missing_outs}"
        )

    # Check if observer has clk_now / first_scan / dt_ms for TON/TOF/TP timers
    obs_clk_symbols: tuple[str, str, str] | None = None
    if "clk_now" in obs.define_map and "first_scan" in obs.var_types and "dt_ms" in obs.var_types:
        obs_clk_symbols = ("dt_ms", "first_scan", "clk_now")

    # Decide integer encoding: use integer SMT when observer uses SMT, when candidate uses
    # REAL/TIME/WORD/timers, or when AST arithmetic / literals exceed safe -128..255 BDD bounds.
    cand_needs_int_smt = (
        obs.uses_smt
        or _ast_needs_unbounded_integers(program)
        or any(
            d.st_type.kind in ("REAL", "TIME", "WORD")
            or (d.st_type.kind == "FB" and (d.st_type.fb_type or "").upper() in ("TON", "TOF", "TP", "CTU", "CTD"))
            for d in program.decls
            if d.section not in ("CONSTANT",)
        )
    )

    compiler = _STToSMVCompiler(
        program=program,
        force_smt_integers=cand_needs_int_smt,
        observer_clk_symbols=obs_clk_symbols,
        mapped_inputs=mapped_inputs,
    )
    compiled = compiler.compile(unmapped_input_strategy="declare", external_out_prefix="cand_out_")

    # Verify every observer-expected output was actually emitted by the candidate FB
    emitted_post = compiled["post_exprs"]
    for obs_out, cand_suffix in output_bindings.items():
        if cand_suffix.lower() not in emitted_post:
            raise UnsupportedSTConstructError(f"Candidate ST FUNCTION_BLOCK missing expected OUTPUT {cand_suffix}")

    # Widen any observer latch `qVar : lo..hi` that tracks a replaced candidate output via `next(qVar) := Out;`
    # so out-of-spec candidate values produce clean LTL/INVAR counterexamples instead of SMV runtime range errors.
    widen_vars: dict[str, str] = {}
    for stmt in obs.assign_stmts:
        m_next = re.match(r"next\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s*:=\s*([^;]+);", stmt)
        if not m_next:
            continue
        qvar, rhs = m_next.group(1), m_next.group(2)
        for obs_out in output_bindings:
            if re.search(rf"\b{re.escape(obs_out)}\b", rhs) and qvar in obs.var_types:
                tstr = obs.var_types[qvar].strip()
                if ".." in tstr:
                    widen_vars[qvar] = "integer" if (cand_needs_int_smt or compiled["uses_smt"]) else "0..255"

    # Assemble coupled SMV module
    lines: list[str] = [
        f"-- Generated by self-developed ST->SMV Formal Verifier for task {task_id}",
        f"-- Coupled observer: {observer_smv_path.name}",
        "MODULE main",
        "VAR",
    ]
    for vstmt in obs.var_stmts:
        m_v = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([^;]+);", vstmt)
        if m_v and m_v.group(1) in widen_vars:
            lines.append(f"  {m_v.group(1)} : {widen_vars[m_v.group(1)]};")
        else:
            lines.append(f"  {vstmt}")
    lines.extend(compiled["var_decls"])

    all_inits = list(obs.init_stmts) + list(compiled["init_clauses"])
    if all_inits:
        lines.append("")
        lines.append("INIT " + " & ".join(f"({c})" for c in all_inits) + ";")

    all_invars = list(obs.invar_stmts) + list(compiled["invar_clauses"])
    if all_invars:
        lines.append("")
        lines.append("INVAR " + " & ".join(f"({c})" for c in all_invars) + ";")

    all_assigns = list(obs.assign_stmts) + list(compiled["assign_clauses"])
    if all_assigns:
        lines.append("")
        lines.append("ASSIGN")
        lines.extend(f"  {a.lstrip()}" for a in all_assigns)

    lines.append("")
    lines.append("DEFINE")
    # Rewritten DEFINEs: replace observer output DEFINEs with cand_out_<suffix>,
    # keeping non-output observer helper DEFINEs (nextMode, qRunning, clk_now, etc.).
    replaced_obs_defs: set[str] = set()
    for dstmt in obs.define_stmts:
        if ":=" in dstmt:
            lhs = dstmt.split(":=", 1)[0].strip()
            if lhs in output_bindings:
                cand_suffix = output_bindings[lhs]
                cand_out_expr = emitted_post[cand_suffix.lower()].code
                lines.append(f"  {lhs} := {cand_out_expr};")
                replaced_obs_defs.add(lhs)
                continue
        lines.append(f"  {dstmt.lstrip()}")

    lines.extend(compiled["define_clauses"])
    for obs_out, cand_suffix in output_bindings.items():
        if obs_out not in replaced_obs_defs:
            cand_out_expr = emitted_post[cand_suffix.lower()].code
            lines.append(f"  {obs_out} := {cand_out_expr};")

    lines.append("")
    lines.extend(obs.spec_stmts)

    smv_text = "\n".join(lines) + "\n"
    return {
        "smv_text": smv_text,
        "observer_smv": str(observer_smv_path),
        "input_names": sorted(
            {
                item["name"]
                for item in task.get("interface", [])
                if isinstance(item, dict) and item.get("direction") in ("INPUT", "IN_OUT") and item.get("name")
            }
        ),
        "output_names": sorted(expected_outputs),
        "candidate_state_names": [
            line.split(":")[0].strip()
            for line in compiled["var_decls"]
            if line.split(":")[0].strip().startswith("cand_")
        ],
        "expected_spec_count": len(obs.spec_stmts),
        "uses_smt": bool(cand_needs_int_smt or compiled["uses_smt"]),
        "program": program,
    }


# ---------------------------------------------------------------------------
# Counterexample Parser & WebUI Waveform Converter
# ---------------------------------------------------------------------------


def _parse_smv_scalar(val_str: str) -> Any:
    s = val_str.strip()
    if s == "TRUE":
        return True
    if s == "FALSE":
        return False
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    m_uw = re.match(r"0[us]d\d+_(\d+)$", s)
    if m_uw:
        return int(m_uw.group(1))
    return s


def parse_counterexamples(
    stdout: str,
    input_names: list[str],
    output_names: list[str],
    state_names: list[str],
    include_expected_observer: bool = True,
) -> list[dict[str, Any]]:
    """Parse NuSMV/nuXmv counterexample execution traces into per-scan dicts."""
    # Exclude SBMC intermediate phase output if nuXmv emitted IC3 phase output
    filtered_stdout = stdout
    if SBMC_START_MARKER in stdout and LTL_RESULTS_MARKER in stdout:
        before_sbmc = stdout.split(SBMC_START_MARKER, 1)[0]
        after_ltl = stdout.split(LTL_RESULTS_MARKER, 1)[1]
        filtered_stdout = before_sbmc + "\n" + after_ltl

    header_re = re.compile(
        r"^--\s+(?:specification|invariant)\s+(.+?)\s+is\s+false\b",
        re.MULTILINE,
    )
    matches = list(header_re.finditer(filtered_stdout))
    if not matches and SBMC_START_MARKER in stdout and LTL_RESULTS_MARKER in stdout:
        # Fall back to full stdout if only SBMC printed the counterexample
        filtered_stdout = stdout
        matches = list(header_re.finditer(filtered_stdout))

    counterexamples: list[dict[str, Any]] = []
    relevant_inputs = set(input_names) | {"dt_ms"}
    relevant_outputs = set(output_names)
    relevant_states = set(state_names)

    for idx, m in enumerate(matches):
        spec_expr = m.group(1).strip()
        block_start = m.end()
        block_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(filtered_stdout)
        block = filtered_stdout[block_start:block_end]

        state_matches = list(re.finditer(r"^\s*->\s*State:\s*(\d+)\.(\d+)\s*<-", block, re.MULTILINE))
        if not state_matches:
            continue

        raw_steps: list[dict[str, Any]] = []
        current_vars: dict[str, Any] = {}
        loop_start_step: int | None = None

        for s_idx, sm in enumerate(state_matches):
            s_start = sm.end()
            s_end = state_matches[s_idx + 1].start() if s_idx + 1 < len(state_matches) else len(block)
            s_body = block[s_start:s_end]
            if (
                "-- Loop starts here"
                in block[block_start if s_idx == 0 else state_matches[s_idx - 1].end() : sm.start()]
            ):
                loop_start_step = s_idx
            for line in s_body.splitlines():
                ls = line.strip()
                if not ls or ls.startswith("--"):
                    continue
                if "=" in ls:
                    k, v = ls.split("=", 1)
                    current_vars[k.strip()] = _parse_smv_scalar(v)

            inputs_snap = {k: current_vars[k] for k in sorted(relevant_inputs) if k in current_vars}
            outputs_snap = {k: current_vars[k] for k in sorted(relevant_outputs) if k in current_vars}
            states_snap = {k: current_vars[k] for k in sorted(relevant_states) if k in current_vars}
            step_entry: dict[str, Any] = {
                "step": s_idx,
                "inputs": inputs_snap,
                "observed": outputs_snap,
                "internal_state": states_snap,
            }
            if include_expected_observer:
                obs_extra = {
                    k: v
                    for k, v in current_vars.items()
                    if k not in inputs_snap and k not in outputs_snap and k not in states_snap
                }
                if obs_extra:
                    step_entry["observer_vars"] = obs_extra
            raw_steps.append(step_entry)

        # Extract property name/index hint from spec text or task ltl if possible
        counterexamples.append(
            {
                "property": spec_expr,
                "loop_start_step": loop_start_step,
                "trace": raw_steps,
            }
        )

    return counterexamples


def sanitize_counterexamples_for_agent(counterexamples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Strip reference/observer internals before returning counterexamples to an LLM agent."""
    sanitized: list[dict[str, Any]] = []
    for ce in counterexamples[:4]:
        sanitized_trace = []
        for step in ce.get("trace", [])[:10]:
            sanitized_trace.append(
                {
                    "step": step.get("step"),
                    "inputs": step.get("inputs", {}),
                    "observed": step.get("observed", {}),
                }
            )
        sanitized.append(
            {
                "property": ce.get("property"),
                "loop_start_step": ce.get("loop_start_step"),
                "trace": sanitized_trace,
            }
        )
    return sanitized


def build_counterexample_waveform(
    counterexamples: list[dict[str, Any]],
    task_id: str,
) -> dict[str, Any] | None:
    """Convert the first parsed counterexample trace into WebUI waveform payload."""
    if not counterexamples:
        return None
    ce = counterexamples[0]
    trace = ce.get("trace") or []
    if not trace:
        return None

    in_keys: list[str] = []
    out_keys: list[str] = []
    for step in trace:
        for k in step.get("inputs") or {}:
            if k not in in_keys:
                in_keys.append(k)
        for k in step.get("observed") or {}:
            if k not in out_keys:
                out_keys.append(k)

    signals: list[dict[str, Any]] = []
    for name in in_keys:
        vals = [(s.get("inputs") or {}).get(name) for s in trace]
        sig_type = "BOOL" if all(isinstance(v, bool) or v is None for v in vals) else "INT"
        signals.append({"name": name, "role": "INPUT", "type": sig_type, "values": vals})
    for name in out_keys:
        vals = [(s.get("observed") or {}).get(name) for s in trace]
        sig_type = "BOOL" if all(isinstance(v, bool) or v is None for v in vals) else "INT"
        signals.append({"name": name, "role": "OUTPUT", "type": sig_type, "values": vals})

    return {
        "name": f"Counterexample: {ce.get('property', 'LTL violation')}",
        "task_id": task_id,
        "steps": [s.get("step", idx) for idx, s in enumerate(trace)],
        "loop_start_step": ce.get("loop_start_step"),
        "signals": signals,
    }


# ---------------------------------------------------------------------------
# Public Entry Point: verify_candidate_st
# ---------------------------------------------------------------------------


def _extract_smv_specs_by_kind(smv_text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Split SMV model into (non_spec_prefix, [(kind, name_or_idx, expr_body), ...])."""
    prefix_lines: list[str] = []
    specs: list[tuple[str, str, str]] = []
    cur_lines: list[str] = []
    in_spec = False
    for line in smv_text.splitlines():
        stripped = line.strip()
        if not in_spec and re.match(r"^(LTLSPEC|INVARSPEC)\b", stripped):
            in_spec = True
            cur_lines = [line]
        elif in_spec:
            cur_lines.append(line)
        else:
            prefix_lines.append(line)
            continue

        joined = "\n".join(cur_lines)
        if ";" in joined:
            stmt = joined.split(";", 1)[0].strip()
            m = re.match(r"^(LTLSPEC|INVARSPEC)\s+(?:NAME\s+([A-Za-z_][A-Za-z0-9_]*)\s*:=\s*)?(.+)$", stmt, re.S)
            if m:
                kind, sname, body = m.group(1), m.group(2) or f"PROP_{len(specs)}", m.group(3).strip()
                specs.append((kind, sname, body))
            in_spec = False
            cur_lines = []
    return "\n".join(prefix_lines), specs


def _run_conjunction_smt_verification(
    smv_text: str,
    out: Path,
    timeout: int,
    executable: str | None,
    tool: str,
    bmc_bound: int,
) -> dict[str, Any] | None:
    """For SMT models whose independent INVARSPECs need relational predicates, prove the conjunction first."""
    prefix, specs = _extract_smv_specs_by_kind(smv_text)
    invars = [(sname, body) for kind, sname, body in specs if kind == "INVARSPEC"]
    ltls = [(sname, body) for kind, sname, body in specs if kind == "LTLSPEC"]
    if len(invars) < 2:
        return None

    conj_body = " & ".join(f"({body})" for _, body in invars)
    conj_lines = [prefix, "", f"INVARSPEC NAME __CONJ_INVAR__ := {conj_body};"]
    for sname, body in ltls:
        conj_lines.append(f"LTLSPEC NAME {sname} := {body};")
    conj_dir = out / "smt_conjunction"
    conj_dir.mkdir(parents=True, exist_ok=True)
    conj_smv = conj_dir / "model.smv"
    conj_smv.write_text("\n".join(conj_lines) + "\n", encoding="utf-8")

    mc_conj = check_model(
        model=conj_smv,
        out_dir=conj_dir,
        executable=executable,
        timeout=timeout,
        tool=tool,
        engine="smt",
        bmc_bound=bmc_bound,
    )
    conj_props = mc_conj.get("property_results") or []
    # In nuXmv SMT scripts, check_invar_ic3 runs before check_ltlspec_ic3, so with 1
    # conjunction INVARSPEC + len(ltls) LTLSPECs, index 0 is __CONJ_INVAR__.
    if len(conj_props) == 1 + len(ltls):
        invar_result_items = [conj_props[0]]
        ltl_result_items = conj_props[1:]
    else:
        invar_result_items = [
            pr for pr in conj_props if any(b[:16] in str(pr.get("expression", "")) for _, b in invars)
        ]
        ltl_result_items = [pr for pr in conj_props if pr not in invar_result_items]
    conj_invar_ok = bool(invar_result_items) and all(bool(pr.get("holds")) for pr in invar_result_items)

    if mc_conj.get("status") == "MODEL_PROPERTIES_TRUE" and conj_invar_ok and len(ltl_result_items) == len(ltls):
        expanded_results: list[dict[str, Any]] = []
        for sname, body in invars:
            expanded_results.append({"expression": f"{sname} := {body}", "holds": True, "status": "PASS"})
        for (sname, body), pr in zip(ltls, ltl_result_items):
            holds = pr.get("holds") is True
            expanded_results.append(
                {
                    "expression": f"{sname} := {body}",
                    "holds": holds,
                    "status": "PASS" if holds else "FAIL",
                }
            )
        return {
            **mc_conj,
            "status": "MODEL_PROPERTIES_TRUE",
            "expected_properties": len(specs),
            "checked_properties": len(specs),
            "unknown_properties": 0,
            "property_results": expanded_results,
            "stdout_path": str(conj_dir / Path(mc_conj["stdout_path"]).name) if mc_conj.get("stdout_path") else None,
            "stderr_path": str(conj_dir / Path(mc_conj["stderr_path"]).name) if mc_conj.get("stderr_path") else None,
        }

    # If conjunction failed OR returned TIMEOUT/INCONCLUSIVE/TOOL_ERROR, check individual specs honestly
    indiv_results: list[dict[str, Any]] = []
    combined_stdout_parts: list[str] = []
    if mc_conj.get("stdout_path"):
        sp = conj_dir / Path(mc_conj["stdout_path"]).name
        if sp.exists():
            combined_stdout_parts.append(sp.read_text(encoding="utf-8", errors="replace"))

    any_false = mc_conj.get("status") == "COUNTEREXAMPLE"
    any_timeout = False
    any_inconclusive = False
    any_tool_error = False
    for idx, (kind, sname, body) in enumerate(specs):
        sub_dir = conj_dir / f"spec_{idx:02d}_{sname}"
        sub_dir.mkdir(parents=True, exist_ok=True)
        sub_smv = sub_dir / "model.smv"
        sub_smv.write_text(f"{prefix}\n\n{kind} NAME {sname} := {body};\n", encoding="utf-8")
        sub_mc = check_model(
            model=sub_smv,
            out_dir=sub_dir,
            executable=executable,
            timeout=max(4, min(8, timeout // max(1, len(specs)))),
            tool=tool,
            engine="smt",
            bmc_bound=bmc_bound,
        )
        sub_sp = sub_dir / Path(sub_mc["stdout_path"]).name if sub_mc.get("stdout_path") else None
        if sub_sp and sub_sp.exists():
            combined_stdout_parts.append(sub_sp.read_text(encoding="utf-8", errors="replace"))
        sub_status = sub_mc.get("status")
        sub_prs = sub_mc.get("property_results") or []
        if sub_status == "MODEL_PROPERTIES_TRUE" and sub_prs and sub_prs[0].get("holds") is True:
            indiv_results.append({"expression": f"{sname} := {body}", "holds": True, "status": "PASS"})
        elif sub_status == "COUNTEREXAMPLE" and sub_prs and sub_prs[0].get("holds") is False:
            indiv_results.append({"expression": f"{sname} := {body}", "holds": False, "status": "FAIL"})
            any_false = True
        else:
            indiv_results.append({"expression": f"{sname} := {body}", "holds": None, "status": "UNKNOWN"})
            if sub_status == "TIMEOUT":
                any_timeout = True
            elif sub_status == "TOOL_ERROR":
                any_tool_error = True
            else:
                any_inconclusive = True

    if any_false:
        comb_status = "COUNTEREXAMPLE"
    elif any_tool_error and not (any_timeout or any_inconclusive):
        comb_status = "TOOL_ERROR"
    elif any_timeout:
        comb_status = "TIMEOUT"
    elif any_inconclusive:
        comb_status = "INCONCLUSIVE"
    else:
        comb_status = "MODEL_PROPERTIES_TRUE"

    merged_stdout = conj_dir / "merged_stdout.txt"
    merged_stdout.write_text("\n".join(combined_stdout_parts), encoding="utf-8")
    return {
        **mc_conj,
        "status": comb_status,
        "expected_properties": len(specs),
        "checked_properties": len(indiv_results),
        "unknown_properties": sum(1 for r in indiv_results if r.get("holds") is None),
        "property_results": indiv_results,
        "stdout_path": str(merged_stdout),
    }


def _map_ltl_ids(task: dict[str, Any], prop_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Annotate checked SMV property results with human-readable LTL IDs from task['ltl']."""
    ltl_by_id = {str(p.get("id", "")): p for p in task.get("ltl", []) if isinstance(p, dict) and p.get("id")}
    enriched: list[dict[str, Any]] = []
    for idx, pr in enumerate(prop_results):
        expr = str(pr.get("expression", ""))
        raw_holds = pr.get("holds")
        holds = True if raw_holds is True else (False if raw_holds is False else None)
        matched_id = f"SMV_{idx + 1}"
        # Check NAME P1_... / PUB001.P1 / SELF001.COMPLETE / legacy V2_* prefix match
        m_ltl_id = re.search(r"\b((?:(?:PUB|SELF)\d+\.)?(?:P\d+|P_init|COMPLETE)|V2_[A-Za-z0-9_]+)\b", expr)
        if m_ltl_id and m_ltl_id.group(1) in ltl_by_id:
            matched_id = m_ltl_id.group(1)
        item = {
            "id": matched_id,
            "expression": expr,
            "holds": holds,
            "status": "PASS" if holds is True else ("FAIL" if holds is False else "UNKNOWN"),
        }
        if matched_id in ltl_by_id:
            item["explanation"] = ltl_by_id[matched_id].get("explanation", "")
        enriched.append(item)
    return enriched


def verify_candidate_st(
    task: dict[str, Any],
    candidate: dict[str, Any] | str,
    out_dir: str | Path,
    timeout: int = 60,
    executable: str | None = None,
    tool: str = "auto",
    engine: str = "auto",
    bmc_bound: int = 25,
    include_expected_observer: bool = True,
) -> dict[str, Any]:
    """Compile candidate ST into SMV, run NuSMV/nuXmv, and return structured formal verification evidence.

    Status outcomes (honestly separated per infrastructure vs verification results):
    - PASS: ST compiled cleanly to SMV, INITIAL_INSTANCE passed, and all SMV specs proved TRUE.
    - COUNTEREXAMPLE: At least one INITIAL_INSTANCE or LTL/INVAR property is violated with a witness trace.
    - INCONCLUSIVE: At least one property could not be decided (e.g. nuXmv IC3 'is unknown') without falsification.
    - TIMEOUT: Model checker exceeded timeout without a falsifying counterexample.
    - UNSUPPORTED_ST: ST code uses a construct outside the bounded symbolic compiler fragment.
    - TOOL_ERROR: NuSMV/nuXmv missing, crashed, internal error, or failed to evaluate expected properties.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    task_id = str(task.get("id") or "")

    # 1. Compile candidate ST into coupled SMV and check INITIAL_INSTANCE pre-scan conditions
    try:
        compiled = compile_st_to_smv(candidate=candidate, task=task)
        smv_path = out / "candidate_coupled.smv"
        smv_path.write_text(compiled["smv_text"], encoding="utf-8")
        init_failures = check_st_initial_instance(compiled["program"], task)
    except UnsupportedSTConstructError as exc:
        result = {
            "task_id": task_id,
            "verifier": "self_developed_st_to_smv",
            "status": "UNSUPPORTED_ST",
            "verified": False,
            "candidate_st_verified": False,
            "reason": str(exc),
            "total_properties": len(task.get("ltl", [])),
            "passed_properties": 0,
            "failed_properties": 0,
            "unknown_properties": 0,
            "property_pass_ratio": None,
            "property_results": [],
            "counterexamples": [],
            "waveform": None,
            "checked_utc": now(),
        }
        write_json(out / "verification_result.json", result)
        return result
    except (KeyError, IndexError, TypeError, ValueError, RecursionError) as exc:
        result = {
            "task_id": task_id,
            "verifier": "self_developed_st_to_smv",
            "status": "TOOL_ERROR",
            "verified": False,
            "candidate_st_verified": False,
            "reason": f"Internal verifier error ({type(exc).__name__}): {exc}",
            "total_properties": len(task.get("ltl", [])),
            "passed_properties": 0,
            "failed_properties": 0,
            "unknown_properties": 0,
            "property_pass_ratio": None,
            "property_results": [],
            "counterexamples": [],
            "waveform": None,
            "checked_utc": now(),
        }
        write_json(out / "verification_result.json", result)
        return result

    # 2. Check NuSMV/nuXmv availability before launching
    if not executable and not (find_nusmv() or find_nuxmv()):
        result = {
            "task_id": task_id,
            "verifier": "self_developed_st_to_smv",
            "status": "TOOL_ERROR",
            "verified": False,
            "candidate_st_verified": False,
            "reason": "Neither NuSMV nor nuXmv executable is available locally",
            "smv_path": str(smv_path),
            "total_properties": compiled["expected_spec_count"],
            "passed_properties": 0,
            "failed_properties": 0,
            "unknown_properties": 0,
            "property_pass_ratio": None,
            "property_results": [],
            "counterexamples": [],
            "waveform": None,
            "checked_utc": now(),
        }
        write_json(out / "verification_result.json", result)
        return result

    # 3. Run model checker (use short initial probe on multi-INVAR SMT models so relational
    # INVAR conjunctions like PUB006 solve in <4s instead of waiting out the full timeout).
    _, parsed_specs = _extract_smv_specs_by_kind(compiled["smv_text"])
    multi_invar_smt = bool(compiled["uses_smt"] and sum(1 for k, _, _ in parsed_specs if k == "INVARSPEC") >= 2)
    initial_timeout = min(timeout, 3) if multi_invar_smt and timeout > 3 else timeout
    mc = check_model(
        model=smv_path,
        out_dir=out,
        executable=executable,
        timeout=initial_timeout,
        tool=tool,
        engine=engine,
        bmc_bound=bmc_bound,
    )
    if mc.get("status") == "TIMEOUT" and multi_invar_smt:
        conj_mc = _run_conjunction_smt_verification(
            smv_text=compiled["smv_text"],
            out=out,
            timeout=max(8, timeout - initial_timeout),
            executable=executable,
            tool=tool,
            bmc_bound=bmc_bound,
        )
        if conj_mc is not None:
            mc = conj_mc

    prop_results = _map_ltl_ids(task, mc.get("property_results") or [])
    total_props = int(mc.get("expected_properties") or len(prop_results) or 0) + (1 if init_failures else 0)
    passed_props = sum(1 for pr in prop_results if pr.get("holds") is True)
    failed_props = sum(1 for pr in prop_results if pr.get("holds") is False) + len(init_failures)
    unknown_props = sum(1 for pr in prop_results if pr.get("holds") is None)

    def _resolve_mc_file(raw_path: str | None) -> Path | None:
        if not raw_path:
            return None
        p = Path(raw_path)
        if p.exists():
            return p
        alt = out / p.name
        return alt if alt.exists() else p

    stdout_path = _resolve_mc_file(mc.get("stdout_path"))
    stderr_path = _resolve_mc_file(mc.get("stderr_path"))
    stdout_text = (
        stdout_path.read_text(encoding="utf-8", errors="replace") if stdout_path and stdout_path.exists() else ""
    )

    counterexamples = parse_counterexamples(
        stdout=stdout_text,
        input_names=compiled["input_names"],
        output_names=compiled["output_names"],
        state_names=compiled["candidate_state_names"],
        include_expected_observer=include_expected_observer,
    )
    for init_err in init_failures:
        counterexamples.insert(
            0,
            {
                "property": f"INITIAL_INSTANCE: {init_err}",
                "loop_start_step": None,
                "trace": [{"step": -1, "inputs": {}, "observed": {}, "note": init_err}],
            },
        )
        prop_results.insert(0, {"id": "P_init", "expression": init_err, "holds": False, "status": "FAIL"})

    mc_status = mc.get("status", "TOOL_ERROR")
    if mc_status == "COUNTEREXAMPLE" or init_failures or failed_props > 0:
        status = "COUNTEREXAMPLE"
        verified = False
    elif mc_status == "TIMEOUT":
        status = "TIMEOUT"
        verified = False
    elif mc_status == "INCONCLUSIVE" or unknown_props > 0:
        status = "INCONCLUSIVE"
        verified = False
    elif mc_status == "TOOL_ERROR":
        status = "TOOL_ERROR"
        verified = False
    elif (
        mc_status == "MODEL_PROPERTIES_TRUE"
        and total_props > 0
        and passed_props == total_props
        and failed_props == 0
        and unknown_props == 0
    ):
        status = "PASS"
        verified = True
    else:
        status = "TOOL_ERROR"
        verified = False

    ratio = (
        (passed_props / total_props)
        if (total_props > 0 and status in ("PASS", "COUNTEREXAMPLE") and unknown_props == 0)
        else None
    )
    waveform = build_counterexample_waveform(counterexamples, task_id=task_id)

    reason = (
        str(stderr_path)
        if status == "TOOL_ERROR" and stderr_path
        else (
            init_failures[0]
            if init_failures
            else (
                f"{unknown_props} property/properties returned UNKNOWN (inconclusive under {mc.get('tool') or 'solver'})"
                if status == "INCONCLUSIVE"
                else None
            )
        )
    )

    result = {
        "task_id": task_id,
        "verifier": "self_developed_st_to_smv",
        "status": status,
        "verified": verified,
        "candidate_st_verified": verified,
        "observer_smv": compiled["observer_smv"],
        "smv_path": str(smv_path),
        "smv_sha256": mc.get("model_sha256") or digest(compiled["smv_text"]),
        "tool": mc.get("tool"),
        "engine": mc.get("engine"),
        "tool_exe_sha256": mc.get("tool_exe_sha256"),
        "total_properties": total_props,
        "passed_properties": passed_props,
        "failed_properties": failed_props,
        "unknown_properties": unknown_props,
        "property_pass_ratio": ratio,
        "property_results": prop_results,
        "initial_instance_failures": init_failures,
        "counterexamples": counterexamples,
        "waveform": waveform,
        "stdout_path": str(stdout_path) if stdout_path else mc.get("stdout_path"),
        "stderr_path": str(stderr_path) if stderr_path else mc.get("stderr_path"),
        "timed_out": mc.get("timed_out", False),
        "reason": reason,
        "checked_utc": now(),
    }
    write_json(out / "verification_result.json", result)
    return result
