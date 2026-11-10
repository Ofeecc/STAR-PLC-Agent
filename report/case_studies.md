# Case studies from preserved CODESYS runs

These examples use active records from campaign `campaign_2026-10-25T121252267365+0000`. They are observations of one run per condition and task. A successful build establishes compilation only; functional results must be read from the separately acquired CODESYS traces and the recalculated analysis.

## 1. A real compiler-guided repair: E1/PUB014

The public task asks for strict dotted-decimal IPv4 parsing into a network-order `UDINT`, with zero returned for malformed input. E1 used the unmodified smolagents 1.26.0 `ToolCallingAgent` with relay model ID `deepseek-v4.1-flash`.

The first candidate declared a local integer `len` and called `LEN(ipText)`. CODESYS rejected the build with two errors:

```text
Cannot convert type 'Unknown type: 'LEN(ipText)'' to type 'INT'
Program name, function or function block instance expected instead of 'LEN'
```

The diagnostic's related declaration is line 10, the local `len`. The likely cause is the local identifier hiding the case-insensitive `LEN` function; this is an interpretation of the observed declaration and diagnostics. The model's next candidate removed that variable and changed the bounded string scan:

```iecst
(* Initial candidate: local len : INT; *)
len := LEN(ipText);
FOR i := 1 TO len DO
    c := ipText[i];
    (* segment validation *)
END_FOR

(* Repaired candidate: no local len variable *)
i := 1;
WHILE (i <= 254) AND ok DO
    c := ipText[i];
    IF c = 0 THEN
        EXIT;
    END_IF
    (* segment validation *)
    i := i + 1;
END_WHILE
```

The second real build reported **0 errors and 0 warnings**, after **one repair**, compared with two errors initially. Both compiler processes exited with code zero, which illustrates why our wrapper reads actual CODESYS error messages instead of relying on the process exit code. The source digests changed from `b6638e0b22e5635b...` to `3b43179efdf7cdb5...`; each build also has its own request nonce, isolated project and complete compiler evidence.

The baseline generated three model requests: initial tool call, repaired tool call and final answer. Its final answer explicitly disclosed that compiler validation alone had been performed at generation time. Later functional testing is evaluated independently and must not be inferred from that answer.

Evidence, relative to the project root:

- [Active result](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB014/run_2026-10-26T132023836291+0000/result.json)
- [Initial candidate](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB014/run_2026-10-26T132023836291+0000/version_00.json) and [repaired candidate](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB014/run_2026-10-26T132023836291+0000/version_01.json)
- [Initial compiler evidence](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB014/run_2026-10-26T132023836291+0000/compile_00/codesys_evidence.json) and [repaired compiler evidence](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB014/run_2026-10-26T132023836291+0000/compile_01/codesys_evidence.json)

## 2. A build success with unresolved task fidelity: E1/PUB018

The official FIFO task exposes caller-owned `item : VARIANT` and `buffer : VARIANT` storage and requires behavior across different element types and array bounds. Its initial E1 candidate produced **38 CODESYS errors**, including unknown `VARIANT` types and invalid conversion/pointer-expression syntax.

After compiler feedback, the model added a supporting data type and rewrote the byte-copy loops. The substitute type was:

```iecst
TYPE VARIANT :
STRUCT
    pData : POINTER TO BYTE;
    udiSize : UDINT;
END_STRUCT
END_TYPE
```

The second build had **0 errors and 0 warnings**. It is therefore a verified final compilation success under the stated build metric. However, the caller must now provide a custom pointer-and-byte-size structure. Keeping the identifier `VARIANT` does not establish native generic parameter compatibility, array-bound handling or FIFO runtime correctness. The model disclosed the substitution in its final answer. Our automatic runtime adapter does not support this IN_OUT/composite case, so the result must remain functionally unverified unless a separately validated caller adapter and actual traces are supplied.

This case explains the separation between build success, task-interface fidelity and functional correctness. It must not be described as a fully verified generic FIFO implementation, and the reported compilation count must not be silently recoded as a functional pass.

Evidence:

- [Active result](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T132336730837+0000/result.json)
- [Initial candidate](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T132336730837+0000/version_00.json), [repaired candidate and DUT](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T132336730837+0000/version_01.json), and [explicit model disclosure](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T132336730837+0000/agent_final_answer.json)
- [Initial compiler evidence](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T132336730837+0000/compile_00/codesys_evidence.json) and [repaired compiler evidence](../experiments/E1/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T132336730837+0000/compile_01/codesys_evidence.json)

## 3. Early termination after a real compile failure: E2/PUB018

For the same FIFO task, E2 used smolagents with `kimi-k3.1-pro`. CODESYS reported **two unknown-type errors**, one for each official `VARIANT` parameter. The agent then called `final_answer` and explained that it would not substitute an adapter. There was **one compiler attempt and zero repairs**. The maximum of three compiler attempts was available; it was **not exhausted**. The result is `COMPILE_FAIL` because no successfully compiled candidate was produced.

The generic wording in the result row says errors remain after the available steps/budget. The detailed tool records show the more precise explanation: the agent chose to stop early. The initial implementation also contains only partial queue bookkeeping and no data-copy implementation; the type failure is not evidence that an otherwise complete FIFO would have worked. We do not classify this as a transport outage or count the stated limitation as a correct solution.

Evidence:

- [Active result](../experiments/E2/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T134919626803+0000/result.json)
- [Only candidate](../experiments/E2/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T134919626803+0000/version_00.json), [compiler evidence](../experiments/E2/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T134919626803+0000/compile_00/codesys_evidence.json), and [final-answer explanation](../experiments/E2/campaign_2026-10-25T121252267365+0000/PUB018/run_2026-10-26T134919626803+0000/agent_final_answer.json)

## 4. A real self-harness repair: E4/SELF012

The self-built task is a fault-recovery controller with a bounded automatic restart count and persistent lockout. E4 used our self-developed harness with relay model ID `kimi-k3.1-pro`. Its last generation run provided a direct example of the harness's compiler-feedback loop.

The first candidate exposed `Locked : BOOL` and declared the enum literals `IDLE`, `RUNNING`, `WAIT` and `LOCKED`. The use of `LOCKED` then conflicted with the case-insensitive output identifier. CODESYS reported three actual errors:

```text
Line 5, Column 1 (Impl): Cannot compare type 'INT' with type 'BOOL'
Line 23, Column 1 (Impl): Cannot convert type 'BOOL' to type 'E_TASKSTATE'
Line 40, Column 1 (Impl): Cannot compare type 'INT' with type 'BOOL'
```

The colliding names and rejected uses were present in the original source:

```iecst
(* Initial declaration and representative uses *)
VAR_OUTPUT
    Locked : BOOL;
END_VAR
TYPE E_TaskState : (IDLE, RUNNING, WAIT, LOCKED); END_TYPE

ELSIF State = LOCKED THEN
    RecoveryFreeScans := 0;
(* ... later in the fault-handling branch ... *)
State := LOCKED;
(* ... final output assignment ... *)
Locked := State = LOCKED;
```

The next candidate gave every enum literal a distinct `TASK_` prefix and updated the comparisons, assignments, CASE labels and initializer. Representative repaired code was:

```iecst
TYPE E_TaskState :
    (TASK_IDLE, TASK_RUNNING, TASK_WAIT, TASK_LOCKED);
END_TYPE

ELSIF State = TASK_LOCKED THEN
    RecoveryFreeScans := 0;
(* ... later in the fault-handling branch ... *)
State := TASK_LOCKED;
(* ... final output assignment ... *)
Locked := (State = TASK_LOCKED);
```

The repair also added an explicit `TASK_LOCKED` CASE branch that clears `RecoveryFreeScans`. It preserved the official input/output interface. CODESYS then reported **0 errors and 0 warnings**: **one repair converted a three-error build into a successful build**. The initial candidate SHA-256 was `6337eb8fb5e63ea60bb82f4a90fb7dcc7f1aa9cba5d6074392eda0ed37dd6f1d`; the repaired candidate was `7c914ea2dd50a9c4575cd52f8edf73a6351a43b60589000f1fa3352160d74320`. These are the structured candidate digests verified by the compiler wrapper, not merely hashes of the displayed excerpts.

This example belongs to **our harness**, unlike the E1 repairs above. It demonstrates actual generation, compiler diagnostics, focused regeneration and recompilation. Its functional correctness must still be assessed from the later actual simulator trace; compilation alone does not verify recovery timing, retry limits or reset priority.

Evidence:

- [Active result](../experiments/E4/campaign_2026-10-25T121252267365+0000/SELF012/run_2026-10-26T170424805779+0000/result.json)
- [Initial candidate](../experiments/E4/campaign_2026-10-25T121252267365+0000/SELF012/run_2026-10-26T170424805779+0000/version_00.json) and [repaired candidate](../experiments/E4/campaign_2026-10-25T121252267365+0000/SELF012/run_2026-10-26T170424805779+0000/version_01.json)
- [Initial compiler evidence](../experiments/E4/campaign_2026-10-25T121252267365+0000/SELF012/run_2026-10-26T170424805779+0000/compile_00/codesys_evidence.json) and [repaired compiler evidence](../experiments/E4/campaign_2026-10-25T121252267365+0000/SELF012/run_2026-10-26T170424805779+0000/compile_01/codesys_evidence.json)

## 5. Infrastructure failure is not a compiler rejection: E3/PUB010

E3/PUB010 saved a real model request, but the relay stream ended with an `internal_server_error` stating that the upstream stream closed before a terminal event. No complete response or candidate was accepted, and **no compiler call occurred**. The row is `TOOL_ERROR`, with null first-pass/final compilation observations. The task stays in the fixed denominator of 32 when computing campaign compilation rates, while the compiler-coverage metric shows that no compiler evaluation happened.

This failure also exposes a resource-accounting difference: the self harness's stored `llm_calls` is zero because it increments after a successful response. A saved `llm_00/request.json` proves one attempted request. The independent analysis therefore counts saved requests for both frameworks and marks missing provider token usage as unknown. A stream failure does not prove whether the upstream computation was charged, nor whether the configured output limit caused the interruption.

Evidence:

- [Active result](../experiments/E3/campaign_2026-10-25T121252267365+0000/PUB010/run_2026-10-26T140616445638+0000/result.json)
- [Saved request](../experiments/E3/campaign_2026-10-25T121252267365+0000/PUB010/run_2026-10-26T140616445638+0000/llm_00/request.json) and [raw response events](../experiments/E3/campaign_2026-10-25T121252267365+0000/PUB010/run_2026-10-26T140616445638+0000/llm_00/events.json)

## Boundaries of the case evidence

The first two repaired builds belong to the existing-agent baseline; E4/SELF012 belongs to the self-developed harness. The compiler preflight separately establishes a valid-invalid-repaired sequence for the shared backend. These examples demonstrate observed compiler-feedback behavior and limits of build-only metrics. They are not controlled ablations of the repair policy, formal LTL proofs, evidence of statistical superiority, or substitutes for actual runtime traces.
