/* STAR-PLC v2 WebUI Controller */
'use strict';

let gTasks = [];
let gReviews = [];
let gPilotReview = [];
let gCheckerAvail = null;
let gCurrentTask = null;
let gLang = 'en';
let gWaveforms = [];
let gRuns = [];
let gCurrentRunTrace = null;
let gExperiments = null;
let gSelectedStageId = null;
let gSelectedVersionIdx = 0;
let gVersionViewMode = 'st';
let gTraceWaveforms = [];
let gLivePollTimer = null;
let gCurrentTab = 'explorer';
let gBootstrapped = false;

const PILOT_IDS = new Set(['PUB001', 'PUB003', 'PUB009', 'PUB010', 'PUB015', 'PUB016']);
const BRACKET_COLORS = ['#09090b', '#047857', '#b45309', '#991b1b', '#52525b'];
const RESERVED_TOKENS = new Set(['TRUE', 'FALSE', 'AND', 'OR', 'NOT']);
const LTL_OPERATORS = new Set(['G', 'F', 'X', 'U', 'R', 'V', 'W']);

const ST_BLOCK_KW = new Set([
  'FUNCTION_BLOCK',
  'END_FUNCTION_BLOCK',
  'PROGRAM',
  'END_PROGRAM',
  'FUNCTION',
  'END_FUNCTION',
  'TYPE',
  'END_TYPE',
  'STRUCT',
  'END_STRUCT',
  'VAR_INPUT',
  'VAR_OUTPUT',
  'VAR_IN_OUT',
  'VAR_TEMP',
  'VAR_GLOBAL',
  'VAR',
  'END_VAR',
  'CONSTANT',
  'RETAIN',
  'PERSISTENT',
]);
const ST_CTRL_KW = new Set([
  'IF',
  'THEN',
  'ELSIF',
  'ELSE',
  'END_IF',
  'CASE',
  'OF',
  'END_CASE',
  'FOR',
  'TO',
  'BY',
  'DO',
  'END_FOR',
  'WHILE',
  'END_WHILE',
  'REPEAT',
  'UNTIL',
  'END_REPEAT',
  'EXIT',
  'RETURN',
  'CONTINUE',
  'AND',
  'OR',
  'NOT',
  'XOR',
  'MOD',
]);
const ST_TYPE_KW = new Set([
  'BOOL',
  'BYTE',
  'WORD',
  'DWORD',
  'LWORD',
  'SINT',
  'USINT',
  'INT',
  'UINT',
  'DINT',
  'UDINT',
  'LINT',
  'ULINT',
  'REAL',
  'LREAL',
  'TIME',
  'STRING',
  'WSTRING',
  'ARRAY',
  'TON',
  'TOF',
  'TP',
  'CTU',
  'CTD',
  'CTUD',
  'R_TRIG',
  'F_TRIG',
  'SR',
  'RS',
]);

const I18N = {
  en: {
    'doc.title': 'STAR-PLC v2 | Agent Workflow, Benchmark & Waveform Inspector',
    'app.brandTitle': 'CODESYS STAR v2',
    'nav.explorer': 'Dataset & Specs',
    'nav.trace': 'Workflow & Benchmark',
    'nav.sandbox': 'Sandbox & Waveform Lab',
    'explorer.title': 'Benchmark Tasks & Specifications',
    'explorer.interfaceTitle': 'Interface Contract',
    'explorer.ltlTitle': 'Formal LTL Properties',
    'explorer.testsTitle': 'Test Cases & Signal Sequences',
    'filter.kind': 'Dataset Split',
    'filter.allSplits': 'All (32)',
    'filter.public': 'Public (20)',
    'filter.selfBuilt': 'Self-built (12)',
    'filter.difficulty': 'Difficulty',
    'filter.allDiff': 'All',
    'filter.easy': 'Easy',
    'filter.medium': 'Medium',
    'filter.hard': 'Hard',
    'filter.search': 'Search ID / Title',
    'filter.searchPlaceholder': 'PUB001, timer, pump...',
    'filter.taskSelect': 'Active Task',
    'filter.pilotOnly': 'Pilot 6 tasks only',
    'trace.title': 'Agent Workflow & Execution Replay',
    'trace.autoPoll': 'Auto-refresh (2s)',
    'trace.refresh': 'Refresh',
    'trace.selectRun': 'Run Record',
    'trace.sendToSandbox': 'Open Candidate in Sandbox Lab',
    'trace.versionsTitle': 'Candidate Versions & ST Diff',
    'trace.timelineTitle': 'Execution Event Timeline',
    'trace.waveformTitle': 'Recorded Execution Waveform',
    'bench.title': 'Benchmark Condition Matrix',
    'sandbox.title': 'Compile, Simulation & Waveform Lab',
    'sandbox.loadSkeleton': 'Load Interface Skeleton',
    'sandbox.loadReference': 'Load Reference ST',
    'sandbox.loadRunCandidate': 'Load Run Candidate',
    'sandbox.includeRandom': 'Include random boundary tests',
    'sandbox.runEval': 'Compile & Simulate',
    'sandbox.exportVerify': 'Export NuSMV Bundle',
    'sandbox.editorLabel': 'Structured Text (ST)',
    'sandbox.consoleLabel': 'Compiler Diagnostics & Verification Output',
    'wave.title': 'Timing & Signal Divergence Comparator',
    'wave.caseSelect': 'Test Case',
  },
  zh: {
    'doc.title': 'STAR-PLC v2 | Agent 动态工作流、评测与波形平台',
    'app.brandTitle': 'CODESYS STAR v2',
    'nav.explorer': '数据集与规约',
    'nav.trace': '工作流与基准评测',
    'nav.sandbox': '仿真与波形实验台',
    'explorer.title': '基准任务集与规约',
    'explorer.interfaceTitle': '接口契约',
    'explorer.ltlTitle': 'LTL 时序规约',
    'explorer.testsTitle': '测试用例与信号表',
    'filter.kind': '数据来源',
    'filter.allSplits': '全部（32 题）',
    'filter.public': '公开基准（20 题）',
    'filter.selfBuilt': '自建扩展（12 题）',
    'filter.difficulty': '难度分级',
    'filter.allDiff': '全部难度',
    'filter.easy': '简单 (Easy)',
    'filter.medium': '中等 (Medium)',
    'filter.hard': '困难 (Hard)',
    'filter.search': '搜索题号 / 名称',
    'filter.searchPlaceholder': '输入 PUB001、timer、pump...',
    'filter.taskSelect': '当前任务',
    'filter.pilotOnly': '仅显示核心试跑 6 题',
    'trace.title': 'Agent 动态工作流与轨迹回放',
    'trace.autoPoll': '实时刷新（2s）',
    'trace.refresh': '刷新',
    'trace.selectRun': '运行记录',
    'trace.sendToSandbox': '载入候选代码到实验台',
    'trace.versionsTitle': '候选版本演进与 ST 高亮 / Diff',
    'trace.timelineTitle': '模型调用与编译仿真时间线',
    'trace.waveformTitle': '执行记录波形对比',
    'bench.title': '基准实验条件矩阵',
    'sandbox.title': 'ST 编译、仿真与波形实验台',
    'sandbox.loadSkeleton': '载入接口骨架',
    'sandbox.loadReference': '加载参考 ST',
    'sandbox.loadRunCandidate': '加载轨迹候选代码',
    'sandbox.includeRandom': '附加随机边界测试',
    'sandbox.runEval': '编译并运行仿真',
    'sandbox.exportVerify': '导出 NuSMV 验证包',
    'sandbox.editorLabel': 'Structured Text (ST) 源码',
    'sandbox.consoleLabel': '编译器诊断与导出输出',
    'wave.title': '逐周期时序信号与偏差定位表',
    'wave.caseSelect': '测试用例',
  },
};

function t(enText, zhText) {
  return gLang === 'zh' ? zhText : enText;
}

function escapeHtml(raw) {
  return String(raw == null ? '' : raw)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function isBoolLike(v) {
  return typeof v === 'boolean' || v === 0 || v === 1;
}

function formatSignalValue(v) {
  if (v === true) return '1';
  if (v === false) return '0';
  if (v === null || v === undefined) return '—';
  if (typeof v === 'object') return JSON.stringify(v);
  return String(v);
}

/* ================= IEC 61131-3 ST Syntax Highlighter ================= */
function highlightST(source) {
  const code = String(source || '');
  const tokRe =
    /\(\*[\s\S]*?\*\)|\/\/[^\n]*|'(?:\\.|[^'\n])*'|T#[0-9A-Za-z_.]+|TIME#[0-9A-Za-z_.]+|16#[0-9A-Fa-f_]+|2#[01_]+|\b\d+(?:\.\d+)?\b|:=|=>|<=|>=|<>|[A-Za-z_][A-Za-z_0-9]*/gi;
  let out = '';
  let lastIdx = 0;
  let m;
  while ((m = tokRe.exec(code)) !== null) {
    if (m.index > lastIdx) {
      out += escapeHtml(code.slice(lastIdx, m.index));
    }
    const tok = m[0];
    const upper = tok.toUpperCase();
    if (tok.startsWith('//') || tok.startsWith('(*')) {
      out += `<span class="st-comment">${escapeHtml(tok)}</span>`;
    } else if (
      tok.startsWith("'") ||
      /^T(?:IME)?#/i.test(tok) ||
      /^(?:16|2)#/.test(tok) ||
      /^\d/.test(tok) ||
      upper === 'TRUE' ||
      upper === 'FALSE'
    ) {
      out += `<span class="st-literal">${escapeHtml(tok)}</span>`;
    } else if (tok === ':=' || tok === '=>' || tok === '<=' || tok === '>=' || tok === '<>') {
      out += `<span class="st-op">${escapeHtml(tok)}</span>`;
    } else if (ST_BLOCK_KW.has(upper)) {
      out += `<span class="st-kw-block">${escapeHtml(tok)}</span>`;
    } else if (ST_CTRL_KW.has(upper)) {
      out += `<span class="st-kw-ctrl">${escapeHtml(tok)}</span>`;
    } else if (ST_TYPE_KW.has(upper)) {
      out += `<span class="st-kw-type">${escapeHtml(tok)}</span>`;
    } else {
      out += escapeHtml(tok);
    }
    lastIdx = tokRe.lastIndex;
  }
  if (lastIdx < code.length) {
    out += escapeHtml(code.slice(lastIdx));
  }
  return out;
}

function syncEditorHighlight() {
  const ta = document.getElementById('st-source-code');
  const codeEl = document.getElementById('st-highlight-code');
  if (!ta || !codeEl) return;
  const val = ta.value || '';
  codeEl.innerHTML = highlightST(val.endsWith('\n') ? `${val} ` : val);
  syncEditorScroll();
}

function syncEditorScroll() {
  const ta = document.getElementById('st-source-code');
  const layer = document.getElementById('st-highlight-layer');
  if (!ta || !layer) return;
  layer.scrollTop = ta.scrollTop;
  layer.scrollLeft = ta.scrollLeft;
}

function setSandboxCode(val) {
  const ta = document.getElementById('st-source-code');
  if (ta) ta.value = val || '';
  syncEditorHighlight();
}

/* ================= Static Bilingual Chrome ================= */
function applyStaticLanguage() {
  const dict = I18N[gLang] || I18N.en;
  if (typeof document !== 'undefined') {
    document.title = dict['doc.title'] || document.title;
    if (document.documentElement) {
      document.documentElement.lang = gLang === 'zh' ? 'zh-CN' : 'en';
    }
    const nodes = document.querySelectorAll('[data-i18n]');
    for (let i = 0; i < nodes.length; i += 1) {
      const el = nodes[i];
      const key = el.getAttribute('data-i18n');
      if (key && dict[key] !== undefined) el.textContent = dict[key];
    }
    const phNodes = document.querySelectorAll('[data-i18n-placeholder]');
    for (let j = 0; j < phNodes.length; j += 1) {
      const el = phNodes[j];
      const key = el.getAttribute('data-i18n-placeholder');
      if (key && dict[key] !== undefined) el.setAttribute('placeholder', dict[key]);
    }
  }
}

function changeLanguage(lang) {
  gLang = lang === 'zh' ? 'zh' : 'en';
  try {
    if (typeof localStorage !== 'undefined' && localStorage.setItem) {
      localStorage.setItem('star_plc_lang', gLang);
    }
  } catch (e) {}
  const sel = document.getElementById('language-select');
  if (sel) sel.value = gLang;
  applyStaticLanguage();
  renderSystemStatus();
  renderTaskList(false);
  if (gCurrentTask) {
    renderTaskDetails(gCurrentTask);
    renderReviewDetails(gCurrentTask);
    renderWaveformPanel(
      gWaveforms,
      document.getElementById('waveform-case-select'),
      document.getElementById('waveform-display')
    );
  }
  renderRunSelect();
  if (gCurrentRunTrace) renderRunTrace(gCurrentRunTrace);
  renderBenchmarkPanel();
}

function switchTab(tabName) {
  const normalized = tabName === 'waveform' ? 'sandbox' : tabName;
  gCurrentTab = normalized;
  const panels = document.querySelectorAll('.tab-panel');
  for (let i = 0; i < panels.length; i += 1) {
    panels[i].hidden = panels[i].id !== 'tab-' + normalized;
  }
  const btns = document.querySelectorAll('.nav-tab');
  for (let i = 0; i < btns.length; i += 1) {
    btns[i].classList.toggle('active', btns[i].getAttribute('data-tab') === normalized);
  }
  try {
    const u = new URL(window.location.href);
    u.searchParams.set('tab', normalized);
    if (window.history && window.history.replaceState) {
      window.history.replaceState({}, '', u.toString());
    }
  } catch (e) {}
  if (normalized === 'trace') {
    refreshWorkflowData(true);
  }
  if (normalized === 'sandbox') {
    syncEditorHighlight();
  }
}

function renderSystemStatus() {
  const box = document.getElementById('system-status');
  if (!box) return;
  const parts = [];
  const activeRuns = (gRuns || []).filter(r => r.state === 'running');
  if (activeRuns.length > 0) {
    parts.push(
      `<span class="pill pill--live"><span class="pulse-dot"></span>${escapeHtml(String(activeRuns.length))} LIVE</span>`
    );
  }
  if (gCheckerAvail) {
    const hasNusmv = !!gCheckerAvail.nusmv_available;
    const hasNuxmv = !!gCheckerAvail.nuxmv_available;
    if (hasNusmv || hasNuxmv || gCheckerAvail.available) {
      const label = hasNusmv && hasNuxmv ? 'NuSMV / nuXmv' : hasNuxmv ? 'nuXmv' : 'NuSMV';
      parts.push(`<span class="pill pill--pass">${escapeHtml(label)}</span>`);
    } else {
      parts.push(`<span class="pill">${escapeHtml(t('SMV Offline', 'SMV 离线'))}</span>`);
    }
  }
  box.innerHTML = parts.join('');
}

function smvSummaryBadge(smvStatus) {
  if (!smvStatus) return `<span class="pill">UNVERIFIED</span>`;
  const st = smvStatus.verification_status || 'UNVERIFIED';
  if (st === 'VERIFIED_BOTH' || st === 'VERIFIED_REFERENCE') {
    return `<span class="pill pill--pass">${escapeHtml(t('SMV Ready', 'SMV 就绪'))}</span>`;
  }
  if (st === 'STALE')
    return `<span class="pill pill--warn">${escapeHtml(t('SMV Stale', 'SMV 过期'))}</span>`;
  if (st === 'FAILED')
    return `<span class="pill pill--fail">${escapeHtml(t('SMV Failed', 'SMV 失败'))}</span>`;
  return `<span class="pill">${escapeHtml(st)}</span>`;
}

/* ================= Tab 1: Dataset & Specs ================= */
function renderTaskList(autoSelect) {
  const kindFilter = (document.getElementById('kind-filter') || {}).value || 'all';
  const diffFilter = (document.getElementById('difficulty-filter') || {}).value || 'all';
  const searchVal = ((document.getElementById('task-search') || {}).value || '')
    .trim()
    .toLowerCase();
  const pilotOnly = !!(document.getElementById('pilot-only') || {}).checked;

  const reviewById = {};
  for (let i = 0; i < (gReviews || []).length; i += 1) {
    reviewById[gReviews[i].id] = gReviews[i];
  }

  const filtered = (gTasks || []).filter(item => {
    if (kindFilter !== 'all' && item.kind !== kindFilter) return false;
    if (diffFilter !== 'all' && item.difficulty !== diffFilter) return false;
    if (pilotOnly && !PILOT_IDS.has(item.id)) return false;
    if (searchVal) {
      const rev = reviewById[item.id] || {};
      const hay = `${item.id} ${item.title || ''} ${rev.title_zh || ''}`.toLowerCase();
      if (!hay.includes(searchVal)) return false;
    }
    return true;
  });

  const totalBadge = document.getElementById('pilot-total');
  if (totalBadge) {
    totalBadge.textContent = t(
      `${filtered.length} / ${gTasks.length} Human Reviewed`,
      `${filtered.length} / ${gTasks.length} 已完成人工审阅`
    );
  }

  const grid = document.getElementById('pilot-grid');
  const sel = document.getElementById('task-select');
  const activeId = gCurrentTask && gCurrentTask.task ? gCurrentTask.task.id : '';

  if (grid) {
    grid.innerHTML = filtered
      .map(item => {
        const rev = reviewById[item.id] || {};
        const title =
          gLang === 'zh' ? rev.title_zh || item.title || item.id : item.title || item.id;
        const kindLabel =
          item.kind === 'self_built' ? t('Self-built', '自建') : t('Public', '公开');
        const activeCls = item.id === activeId ? ' active' : '';
        return (
          `<button type="button" class="pilot-card${activeCls}" data-task-id="${escapeHtml(item.id)}" onclick="selectTask('${escapeHtml(item.id)}')">` +
          `<div class="pilot-card-top">` +
          `<span class="pilot-card-id">${escapeHtml(item.id)}</span>` +
          `<span class="pill pill--pass">${escapeHtml(t('Human reviewed', '已完成人工审阅'))}</span>` +
          `</div>` +
          `<div class="pilot-card-title">${escapeHtml(title)}</div>` +
          `<div class="pilot-card-meta">` +
          `<span class="pill">${escapeHtml(kindLabel)} · ${escapeHtml(item.difficulty || '')}</span>` +
          `<span class="pill">${escapeHtml(String(item.tests_count || 0))} ${escapeHtml(t('cases', '用例'))} / ${escapeHtml(String(item.properties_count || 0))} LTL</span>` +
          `<span class="pilot-card-smv">${smvSummaryBadge(item.smv_status)}</span>` +
          `</div>` +
          `</button>`
        );
      })
      .join('');
  }

  if (sel) {
    sel.innerHTML = filtered
      .map(item => {
        const rev = reviewById[item.id] || {};
        const title = gLang === 'zh' ? rev.title_zh || item.title : item.title;
        const selectedAttr = item.id === activeId ? ' selected' : '';
        return `<option value="${escapeHtml(item.id)}"${selectedAttr}>${escapeHtml(item.id)} — ${escapeHtml(title)}</option>`;
      })
      .join('');
  }

  if (autoSelect && filtered.length > 0 && (!activeId || !filtered.some(x => x.id === activeId))) {
    selectTask(filtered[0].id);
  }
}

async function selectTask(taskId) {
  if (!taskId) return;
  try {
    const resp = await fetch(`/api/task?id=${encodeURIComponent(taskId)}`);
    if (!resp.ok) return;
    const detail = await resp.json();
    gCurrentTask = detail;
    renderTaskList(false);
    renderTaskDetails(detail);
    renderReviewDetails(detail);
    populateSandboxTemplate(detail);
    const url = new URL(window.location.href);
    url.searchParams.set('task', taskId);
    if (window.history && window.history.replaceState) {
      window.history.replaceState({}, '', url.toString());
    }
  } catch (e) {
    console.error('Failed to load task:', e);
  }
}

function renderSmvModelRow(label, modelInfo, variant) {
  const info = modelInfo || {};
  const st = info.status || 'UNVERIFIED';
  const staleNote = info.stale ? ` (${t('stale', '过期')})` : '';
  const cls = st === 'PASS' ? 'pill--pass' : st === 'FAIL' ? 'pill--fail' : 'pill--warn';
  return (
    `<tr>` +
    `<td class="mono">${escapeHtml(label)}</td>` +
    `<td><span class="pill ${cls}">${escapeHtml(st + staleNote)}</span></td>` +
    `<td class="mono" style="font-size:11px;color:var(--text-secondary);">${escapeHtml((info.model_sha256 || '—').slice(0, 12))}</td>` +
    `<td><button class="btn btn-sm" type="button" onclick="runSmvCheck('${escapeHtml(variant)}')">${escapeHtml(t('Verify', '重验'))}</button></td>` +
    `</tr>`
  );
}

function renderTaskDetails(detail) {
  if (!detail || !detail.task) return;
  const task = detail.task;
  const review = detail.review || {};
  const glossary = detail.symbol_glossary || {};
  const smv = detail.smv_status || {};
  const titleText = gLang === 'zh' ? review.title_zh || task.title : task.title;
  const promptText =
    gLang === 'zh' && review.translation_zh ? review.translation_zh : task.prompt || '';

  const overview = document.getElementById('task-overview');
  if (overview) {
    const models = smv.models || {};
    const stepTotal = (task.tests || []).reduce((a, c) => a + (c.steps || []).length, 0);
    overview.innerHTML =
      `<div class="card-head">` +
      `<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">` +
      `<h2 class="card-title">${escapeHtml(task.id)} — ${escapeHtml(titleText || '')}</h2>` +
      `<span class="pill pill--pass">${escapeHtml(t('Reviewed', '已审阅'))}</span>` +
      `<span class="pill">${escapeHtml(task.kind || '')} · ${escapeHtml(task.difficulty || '')}</span>` +
      `<span class="pill mono">${escapeHtml((detail.task_sha256 || '').slice(0, 10))}</span>` +
      `</div>` +
      `<button class="btn btn-primary btn-sm" type="button" onclick="switchTab('sandbox')">${escapeHtml(t('Open in Sandbox Lab', '在实验台运行'))}</button>` +
      `</div>` +
      `<div class="overview-grid">` +
      `<div class="metric-box"><div class="metric-label">${escapeHtml(t('Fixed Cases / Steps', '固定用例 / 步数'))}</div><div class="metric-val">${(task.tests || []).length} / ${stepTotal}</div></div>` +
      `<div class="metric-box"><div class="metric-label">${escapeHtml(t('Random Boundary Cases', '随机边界用例'))}</div><div class="metric-val">${(detail.random_cases || []).length}</div></div>` +
      `<div class="metric-box"><div class="metric-label">${escapeHtml(t('LTL Properties', 'LTL 性质'))}</div><div class="metric-val">${(task.ltl || []).length}</div></div>` +
      `</div>` +
      `<div class="prompt-box">${escapeHtml(promptText)}</div>` +
      `<div id="overview-smv-box" class="card-subtle" style="margin-top:12px;">` +
      `<div class="card-head" style="margin-bottom:6px;">` +
      `<strong>${escapeHtml(t('Reference SMV Check', '参考模型 SMV 核验'))}</strong>` +
      `${smvSummaryBadge(smv)}` +
      `</div>` +
      `<table class="clean-table"><thead><tr><th>${escapeHtml(t('Model', '模型'))}</th><th>${escapeHtml(t('Status', '状态'))}</th><th>SHA256</th><th>${escapeHtml(t('Action', '操作'))}</th></tr></thead><tbody>` +
      renderSmvModelRow('reference.smv', models.reference, 'reference') +
      renderSmvModelRow('complete.smv', models.complete, 'complete') +
      renderSmvModelRow('mutant.smv', models.mutant, 'mutant') +
      `</tbody></table>` +
      `</div>`;
  }

  const pinsBox = document.getElementById('interface-pins-container');
  if (pinsBox) {
    const interfaceZh = review.interface_zh || {};
    const rows = (task.interface || [])
      .map(pin => {
        const entry = glossary[pin.name] || {};
        const dir = pin.direction || 'INPUT';
        const isPersistent = dir === 'IN_OUT';
        const dirCls = isPersistent ? 'pill--persist' : '';
        const desc =
          gLang === 'zh'
            ? interfaceZh[pin.name] || entry.definition_zh || ''
            : entry.definition_en || pin.description || '';
        const persistBadge = isPersistent
          ? `<div style="margin-top:4px;"><span class="pill pill--persist">${escapeHtml(t('VAR_IN_OUT persistent', 'VAR_IN_OUT 跨周期保持'))}</span></div>`
          : '';
        return (
          `<tr>` +
          `<td class="mono"><strong>${escapeHtml(pin.name)}</strong></td>` +
          `<td><span class="pill ${dirCls}">${escapeHtml(dir)}</span></td>` +
          `<td class="mono">${escapeHtml(pin.type || '')}</td>` +
          `<td>${escapeHtml(desc)}${persistBadge}</td>` +
          `</tr>`
        );
      })
      .join('');
    pinsBox.innerHTML =
      `<table class="clean-table"><thead><tr>` +
      `<th>${escapeHtml(t('Pin', '变量名'))}</th>` +
      `<th>${escapeHtml(t('Direction', '方向'))}</th>` +
      `<th>${escapeHtml(t('Type', '类型'))}</th>` +
      `<th>${escapeHtml(t('Description', '说明'))}</th>` +
      `</tr></thead><tbody>${rows}</tbody></table>` +
      renderGlossaryPanel(glossary, task);
  }

  const ltlBox = document.getElementById('ltl-container');
  if (ltlBox) {
    const propsZh = review.properties_zh || {};
    ltlBox.innerHTML = (task.ltl || [])
      .map(prop => {
        const zhItem = propsZh[prop.id] || {};
        const desc =
          gLang === 'zh'
            ? zhItem.description || prop.description || prop.name || ''
            : prop.description || prop.name || '';
        return (
          `<div class="ltl-item">` +
          `<div class="ltl-head">` +
          `<span class="mono" style="font-weight:700;">${escapeHtml(prop.id)}</span>` +
          `<span class="pill">${escapeHtml(prop.category || 'property')}</span>` +
          `</div>` +
          `<div class="spec-code">${formatSpec(prop.formula || '', glossary)}</div>` +
          (desc
            ? `<div class="muted" style="margin-top:6px;font-size:12.5px;">${escapeHtml(desc)}</div>`
            : '') +
          `</div>`
        );
      })
      .join('');
  }

  const testsBox = document.getElementById('tests-container');
  if (testsBox) {
    const testsZh = review.tests_zh || {};
    const buildTestCard = (c, isRandom) => {
      const steps = c.steps || [];
      const zhEntry = testsZh[c.id] || {};
      const nameText =
        gLang === 'zh'
          ? zhEntry.description_zh || zhEntry.name_zh || c.purpose || c.name || c.id
          : c.purpose || c.name || c.id;
      const previewSteps = steps.map((st, idx) => ({
        step: idx,
        inputs: st.inputs || {},
        expected: st.expected || {},
        observed: null,
        dt_ms: st.dt_ms,
        match: null,
        divergence: null,
      }));
      const inlineTable = buildWaveTableHtml(previewSteps);
      const badgeLabel = isRandom
        ? `${t('Random', '随机边界')} · ${steps.length} ${t('steps', '步')}`
        : `${t('Fixed Test', '固定测试')} · ${steps.length} ${t('steps', '步')}`;
      return (
        `<div class="ltl-item">` +
        `<div class="ltl-head">` +
        `<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">` +
        `<span class="mono" style="font-weight:700;">${escapeHtml(c.id)}</span>` +
        `<span class="pill ${isRandom ? '' : 'pill--dark'}">${escapeHtml(badgeLabel)}</span>` +
        `</div>` +
        `<button type="button" class="btn btn-sm" onclick="openTestWaveform('${escapeHtml(c.id)}')">${escapeHtml(t('Signal Table', '波形详情'))} ↗</button>` +
        `</div>` +
        (nameText && nameText !== c.id
          ? `<div style="font-size:12.5px;font-weight:600;margin-bottom:6px;">${escapeHtml(nameText)}</div>`
          : '') +
        `<details class="details-accordion">` +
        `<summary>${escapeHtml(t(`Expand Signal Table (${steps.length} steps)`, `展开信号时序表（${steps.length} 步）`))}</summary>` +
        `<div style="margin-top:8px;">${inlineTable}</div>` +
        `</details>` +
        `</div>`
      );
    };

    const fixedHtml = (task.tests || []).map(c => buildTestCard(c, false)).join('');
    const randCases = detail.random_cases || [];
    const randHtml = randCases.length
      ? `<details class="details-accordion" style="margin-top:10px;"><summary>${escapeHtml(t(`Random Boundary Cases (${randCases.length})`, `随机边界用例（${randCases.length} 组）`))}</summary><div style="margin-top:8px;">` +
        randCases.map(rc => buildTestCard(rc, true)).join('') +
        `</div></details>`
      : '';
    testsBox.innerHTML = fixedHtml + randHtml;
  }
}

function openTestWaveform(caseId) {
  if (!caseId) return;
  switchTab('sandbox');
  const sel = document.getElementById('waveform-case-select');
  renderWaveformPanel(gWaveforms, sel, document.getElementById('waveform-display'));
  if (sel) {
    sel.value = caseId;
    renderWaveformPanel(gWaveforms, sel, document.getElementById('waveform-display'));
  }
  const wfView = document.getElementById('waveform-view');
  if (wfView && wfView.scrollIntoView) {
    wfView.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function renderGlossaryPanel(glossary, task) {
  const entries = Object.keys(glossary || {});
  if (!entries.length) return '';
  const rows = entries
    .slice(0, 18)
    .map(sym => {
      const e = glossary[sym] || {};
      const cat = gLang === 'zh' ? e.category_zh || e.category : e.category_en || e.category;
      const typ = gLang === 'zh' ? e.type_zh || e.type : e.type_en || e.type;
      const def =
        gLang === 'zh'
          ? e.definition_zh || e.definition_en || ''
          : e.definition_en || e.definition_zh || '';
      const cls = e.is_persistent ? 'pill--persist' : '';
      return (
        `<tr>` +
        `<td class="mono"><button type="button" class="spec-tok ${e.is_persistent ? 'spec-tok--persist' : 'spec-tok--symbol'}" onclick="showSpecPopover(this, '${escapeHtml(sym)}', true)">${escapeHtml(sym)}</button></td>` +
        `<td><span class="pill ${cls}">${escapeHtml(cat || '')}</span></td>` +
        `<td class="mono" style="font-size:12px;">${escapeHtml(typ || '')}</td>` +
        `<td>${escapeHtml(def)}</td>` +
        `</tr>`
      );
    })
    .join('');
  return (
    `<details class="details-accordion" style="margin-top:12px;">` +
    `<summary>${escapeHtml(t(`Symbol Glossary (${entries.length})`, `符号词表（${entries.length}）`))}</summary>` +
    `<div style="margin-top:8px;overflow-x:auto;">` +
    `<table class="clean-table"><thead><tr><th>${escapeHtml(t('Symbol', '符号'))}</th><th>${escapeHtml(t('Category', '类别'))}</th><th>${escapeHtml(t('Type', '类型'))}</th><th>${escapeHtml(t('Definition', '解释'))}</th></tr></thead><tbody>${rows}</tbody></table>` +
    `</div></details>`
  );
}

function renderReviewDetails(detail) {
  const container = document.getElementById('review-details');
  if (!container || !detail) return;
  const rev = detail.review || {};
  const task = detail.task || {};
  const norm = task.normalized_specification || {};

  if (gLang === 'zh') {
    const items = [];
    if (rev.assumptions_zh)
      items.push(
        `<div class="card-subtle"><strong>假设与约束：</strong><div>${escapeHtml(rev.assumptions_zh)}</div></div>`
      );
    if (rev.coverage_zh)
      items.push(
        `<div class="card-subtle"><strong>测试覆盖：</strong><div>${escapeHtml(rev.coverage_zh)}</div></div>`
      );
    if (rev.review_points_zh)
      items.push(
        `<div class="card-subtle"><strong>复核要点：</strong><div>${escapeHtml(rev.review_points_zh)}</div></div>`
      );
    container.innerHTML = `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;font-size:12.5px;">${items.join('')}</div>`;
  } else {
    const enRules =
      Array.isArray(norm.rules) && norm.rules.length
        ? norm.rules
            .slice(0, 3)
            .map(r => (typeof r === 'string' ? r : r.id || ''))
            .filter(Boolean)
            .join('; ')
        : 'Single-scan transition contract with explicit timing semantics.';
    container.innerHTML =
      `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;font-size:12.5px;">` +
      `<div class="card-subtle"><strong>Contract Rules</strong><div>${escapeHtml(enRules)}</div></div>` +
      `<div class="card-subtle"><strong>Timing &amp; Coverage</strong><div>${escapeHtml(norm.timing_unit || 'scan / ms')} · ${(task.tests || []).length} fixed + ${(detail.random_cases || []).length} random cases</div></div>` +
      `</div>`;
  }
}

function formatSpec(formula, glossary) {
  const text = String(formula || '');
  const parts = [];
  const tokenRe = /[A-Za-z_][A-Za-z_0-9.]*|\d+|[()\[\]]|->|<->|==|!=|<=|>=|[&|!<>+\-*/=,;:\s]+/g;
  let depth = 0;
  let m;
  while ((m = tokenRe.exec(text)) !== null) {
    const tok = m[0];
    if (/^\s+$/.test(tok)) {
      parts.push(escapeHtml(tok));
      continue;
    }
    if (tok === '(' || tok === '[') {
      const col = BRACKET_COLORS[depth % BRACKET_COLORS.length];
      depth += 1;
      parts.push(`<span style="color:${col};font-weight:700;">${escapeHtml(tok)}</span>`);
      continue;
    }
    if (tok === ')' || tok === ']') {
      depth = Math.max(0, depth - 1);
      const col = BRACKET_COLORS[depth % BRACKET_COLORS.length];
      parts.push(`<span style="color:${col};font-weight:700;">${escapeHtml(tok)}</span>`);
      continue;
    }
    if (/^\d+$/.test(tok)) {
      parts.push(`<span class="spec-tok--num">${escapeHtml(tok)}</span>`);
      continue;
    }
    if (!/^[A-Za-z_]/.test(tok)) {
      parts.push(`<span class="spec-tok--logic">${escapeHtml(tok)}</span>`);
      continue;
    }
    if (LTL_OPERATORS.has(tok)) {
      parts.push(
        `<span class="spec-tok spec-tok--ltl" onclick="showSpecPopover(this, '${escapeHtml(tok)}', true)">${escapeHtml(tok)}</span>`
      );
      continue;
    }
    if (RESERVED_TOKENS.has(tok)) {
      parts.push(
        `<span class="spec-tok spec-tok--logic" onclick="showSpecPopover(this, '${escapeHtml(tok)}', true)">${escapeHtml(tok)}</span>`
      );
      continue;
    }
    const entry = (glossary || {})[tok];
    let cls = 'spec-tok--symbol';
    if (entry) {
      if (entry.is_persistent) cls = 'spec-tok--persist';
      else if (entry.category === 'input') cls = 'spec-tok--input';
      else if (entry.category === 'output') cls = 'spec-tok--output';
      else if (entry.category === 'timer') cls = 'spec-tok--timer';
    }
    parts.push(
      `<span class="spec-tok ${cls}" onclick="showSpecPopover(this, '${escapeHtml(tok)}', true)">${escapeHtml(tok)}</span>`
    );
  }
  return parts.join('');
}

function showSpecPopover(anchorEl, token, keepOpen) {
  const pop = document.getElementById('spec-popover');
  if (!pop || !token) return;
  const glossary = (gCurrentTask && gCurrentTask.symbol_glossary) || {};
  const entry = glossary[token] || {};
  const cat =
    gLang === 'zh' ? entry.category_zh || entry.category : entry.category_en || entry.category;
  const typ = gLang === 'zh' ? entry.type_zh || entry.type : entry.type_en || entry.type;
  const def =
    gLang === 'zh'
      ? entry.definition_zh || entry.definition_en || ''
      : entry.definition_en || entry.definition_zh || '';
  const warn = gLang === 'zh' ? entry.persistence_warning_zh : entry.persistence_warning_en;

  pop.innerHTML =
    `<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:6px;">` +
    `<strong class="mono">${escapeHtml(token)}</strong>` +
    `<button type="button" class="btn btn-sm" onclick="hideSpecPopover(true)">×</button>` +
    `</div>` +
    (cat || typ
      ? `<div style="margin-bottom:6px;display:flex;gap:6px;flex-wrap:wrap;"><span class="pill ${entry.is_persistent ? 'pill--persist' : ''}">${escapeHtml(cat || 'symbol')}</span>${typ ? `<span class="pill mono">${escapeHtml(typ)}</span>` : ''}</div>`
      : '') +
    `<div>${escapeHtml(def || t('Specification symbol.', '规约符号。'))}</div>` +
    (warn
      ? `<div class="card-subtle" style="margin-top:8px;border-color:var(--persist-border);background:var(--persist-bg);color:var(--persist-ink);">${escapeHtml(warn)}</div>`
      : '');

  if (anchorEl && anchorEl.getBoundingClientRect) {
    const r = anchorEl.getBoundingClientRect();
    const top = Math.min((window.innerHeight || 800) - 180, (r.bottom || 20) + 6);
    const left = Math.min((window.innerWidth || 1280) - 395, Math.max(12, r.left || 16));
    pop.style.top = `${Math.max(12, top)}px`;
    pop.style.left = `${left}px`;
  }
  pop.hidden = false;
  if (keepOpen) pop.dataset.pinned = '1';
}

function hideSpecPopover(force) {
  const pop = document.getElementById('spec-popover');
  if (!pop) return;
  if (force || pop.dataset.pinned !== '1') {
    pop.hidden = true;
    pop.dataset.pinned = '';
  }
}

async function runSmvCheck(variant) {
  if (!gCurrentTask || !gCurrentTask.task) return;
  try {
    const resp = await fetch('/api/check-reference-model', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task_id: gCurrentTask.task.id, variant: variant || null }),
    });
    const data = await resp.json();
    if (data && data.smv_status) {
      gCurrentTask.smv_status = data.smv_status;
      renderTaskDetails(gCurrentTask);
    }
  } catch (e) {
    console.error('SMV check failed:', e);
  }
}

/* ================= Shared Waveform Table Builder ================= */
function buildWaveTableHtml(steps) {
  if (!steps || !steps.length) {
    return `<div class="card-subtle muted">${escapeHtml(t('Zero scan steps.', '无扫描步记录。'))}</div>`;
  }
  const inputKeys = [];
  const outputKeys = [];
  for (let i = 0; i < steps.length; i += 1) {
    const st = steps[i];
    Object.keys(st.inputs || {}).forEach(k => {
      if (!inputKeys.includes(k)) inputKeys.push(k);
    });
    Object.keys(st.expected || {}).forEach(k => {
      if (!outputKeys.includes(k)) outputKeys.push(k);
    });
    if (st.observed && typeof st.observed === 'object') {
      Object.keys(st.observed).forEach(k => {
        if (!outputKeys.includes(k)) outputKeys.push(k);
      });
    }
  }

  const headerCells = steps
    .map(s => {
      const failCls = s.match === false ? 'wave-cell-step-fail' : '';
      const dt =
        s.dt_ms != null
          ? `<div style="font-size:10px;color:var(--text-muted);">${escapeHtml(String(s.dt_ms))}ms</div>`
          : '';
      return `<th class="${failCls}">t${s.step}${dt}</th>`;
    })
    .join('');

  const buildRow = (label, tag, getter, compareExpected) => {
    const cells = steps
      .map(st => {
        const val = getter(st);
        const txt = formatSignalValue(val);
        let cls = '';
        if (compareExpected) {
          const exp = compareExpected(st);
          if (
            val !== undefined &&
            val !== null &&
            st.match === false &&
            st.divergence &&
            st.divergence.field === compareExpected.field
          ) {
            cls = 'wave-cell-bad';
          } else if (
            val !== undefined &&
            val !== null &&
            exp !== undefined &&
            formatSignalValue(val) !== formatSignalValue(exp)
          ) {
            cls = 'wave-cell-bad';
          } else if (isBoolLike(val)) {
            cls = val === true || val === 1 ? 'wave-cell-hi' : 'wave-cell-lo';
          }
        } else if (isBoolLike(val)) {
          cls = val === true || val === 1 ? 'wave-cell-hi' : 'wave-cell-lo';
        }
        return `<td class="${cls}">${escapeHtml(txt)}</td>`;
      })
      .join('');
    return `<tr><td class="wave-sig-col"><span class="pill" style="margin-right:6px;">${escapeHtml(tag)}</span>${escapeHtml(label)}</td>${cells}</tr>`;
  };

  let bodyRows = '';
  inputKeys.forEach(k => {
    bodyRows += buildRow(k, 'IN', st => (st.inputs || {})[k], null);
  });
  outputKeys.forEach(k => {
    bodyRows += buildRow(k, t('EXP', '预期'), st => (st.expected || {})[k], null);
    const hasObs = steps.some(st => st.observed && st.observed[k] !== undefined);
    if (hasObs) {
      const cmp = st => (st.expected || {})[k];
      cmp.field = k;
      bodyRows += buildRow(k, t('OBS', '实测'), st => (st.observed || {})[k], cmp);
    }
  });

  return `<div class="waveform-scroll"><table class="wave-table"><thead><tr><th class="wave-sig-col">${escapeHtml(t('Signal / Step', '信号 / 扫描步'))}</th>${headerCells}</tr></thead><tbody>${bodyRows}</tbody></table></div>`;
}

function renderWaveformPanel(waveforms, selectEl, displayEl, emptyMessage) {
  const list = Array.isArray(waveforms) ? waveforms : [];
  if (selectEl) {
    const prev = selectEl.value;
    selectEl.innerHTML = list
      .map((wf, idx) => {
        const badge = wf.passed === true ? 'PASS' : wf.passed === false ? 'FAIL' : 'SPEC';
        const selAttr = prev
          ? prev === wf.case_id
            ? ' selected'
            : ''
          : idx === 0
            ? ' selected'
            : '';
        return `<option value="${escapeHtml(wf.case_id || '')}"${selAttr}>${escapeHtml(wf.case_id || '')} [${badge}] — ${escapeHtml(wf.name || wf.case_id || '')}</option>`;
      })
      .join('');
  }
  if (!displayEl) return;
  if (!list.length) {
    displayEl.innerHTML = `<div class="card-subtle muted">${escapeHtml(emptyMessage || t('No waveform data available.', '暂无可展示的时序波形数据。'))}</div>`;
    return;
  }
  const activeId = (selectEl && selectEl.value) || list[0].case_id;
  const wf = list.find(item => item.case_id === activeId) || list[0];
  const steps = wf.steps || [];
  const divs = steps.filter(s => s.divergence);
  const divBanner = divs.length
    ? `<div class="card-subtle" style="margin-bottom:10px;border-color:var(--fail-border);background:var(--fail-bg);color:var(--fail-ink);font-size:12.5px;">` +
      `<strong>${escapeHtml(t('Divergence at step', '偏差定位步'))} #${divs[0].step}:</strong> ` +
      `<span class="mono">${escapeHtml(divs[0].divergence.field)}</span> ` +
      `(${escapeHtml(t('expected', '预期'))} <span class="mono">${escapeHtml(formatSignalValue(divs[0].divergence.expected))}</span>, ` +
      `${escapeHtml(t('observed', '实测'))} <span class="mono">${escapeHtml(formatSignalValue(divs[0].divergence.observed))}</span>)` +
      `</div>`
    : '';

  displayEl.innerHTML = divBanner + buildWaveTableHtml(steps);
}

/* ================= Tab 2: Workflow & Benchmark ================= */
async function refreshWorkflowData(forceTraceReload) {
  try {
    const [runsResp, expResp] = await Promise.all([fetch('/api/runs'), fetch('/api/experiments')]);
    if (runsResp.ok) {
      const runsData = await runsResp.json();
      gRuns = runsData.runs || [];
      renderSystemStatus();
      renderRunSelect();
    }
    if (expResp.ok) {
      gExperiments = await expResp.json();
      renderBenchmarkPanel();
    }
    const sel = document.getElementById('run-select');
    const selectedRun = (sel && sel.value) || (gRuns[0] && gRuns[0].run_id);
    if (
      selectedRun &&
      (forceTraceReload ||
        !gCurrentRunTrace ||
        gCurrentRunTrace.run_id === selectedRun ||
        (gCurrentRunTrace && gCurrentRunTrace.state === 'running'))
    ) {
      await loadRunTrace(selectedRun);
    } else if (!selectedRun) {
      renderRunTrace(null);
    }
    updatePollBadge();
  } catch (e) {
    console.error('Workflow refresh error:', e);
  }
}

function updatePollBadge() {
  const badge = document.getElementById('live-poll-badge');
  const toggle = document.getElementById('live-poll-toggle');
  if (!badge) return;
  const activeRuns = (gRuns || []).filter(r => r.state === 'running');
  if (toggle && !toggle.checked) {
    badge.className = 'pill';
    badge.textContent = t('Paused', '已暂停');
    return;
  }
  if (activeRuns.length > 0) {
    badge.className = 'pill pill--live';
    badge.innerHTML = `<span class="pulse-dot"></span>${escapeHtml(t(`Live (${activeRuns.length})`, `实时运行 (${activeRuns.length})`))}`;
  } else {
    badge.className = 'pill';
    badge.textContent = t('Watching (2s)', '监听中 (2s)');
  }
}

function ensureLivePolling() {
  if (typeof setInterval !== 'function') return;
  if (gLivePollTimer && typeof clearInterval === 'function') {
    clearInterval(gLivePollTimer);
    gLivePollTimer = null;
  }
  gLivePollTimer = setInterval(() => {
    const toggle = document.getElementById('live-poll-toggle');
    if (toggle && !toggle.checked) return;
    const hasLive = (gRuns || []).some(r => r.state === 'running');
    if (gCurrentTab === 'trace' || hasLive) {
      refreshWorkflowData(false);
    }
  }, 2000);
}

function renderRunSelect() {
  const sel = document.getElementById('run-select');
  if (!sel) return;
  const prev = sel.value || (gCurrentRunTrace && gCurrentRunTrace.run_id) || '';
  if (!gRuns.length) {
    sel.innerHTML = `<option value="">${escapeHtml(t('No runs found', '暂无运行记录'))}</option>`;
    return;
  }
  sel.innerHTML = gRuns
    .map((r, idx) => {
      const tag = r.state === 'running' ? '[LIVE]' : r.source === 'pilot' ? '[PILOT]' : '[EXP]';
      const cond = r.condition ? `${r.condition} · ` : '';
      const label = `${tag} ${r.task_id} · ${cond}${r.framework} · ${r.status}${r.campaign ? ' (' + r.campaign + ')' : ''}`;
      const isSelected = prev ? prev === r.run_id : idx === 0;
      return `<option value="${escapeHtml(r.run_id)}"${isSelected ? ' selected' : ''}>${escapeHtml(label)}</option>`;
    })
    .join('');
}

async function loadRunTrace(runId) {
  if (!runId) return;
  try {
    const resp = await fetch(`/api/run-trace?run=${encodeURIComponent(runId)}`);
    if (!resp.ok) return;
    const trace = await resp.json();
    gCurrentRunTrace = trace;
    gSelectedVersionIdx = Math.max(0, (trace.versions || []).length - 1);
    if (!gSelectedStageId || !(trace.stages || []).some(s => s.id === gSelectedStageId)) {
      const running = (trace.stages || []).find(s => s.status === 'RUNNING');
      gSelectedStageId =
        (running && running.id) || (trace.stages && trace.stages[0] && trace.stages[0].id) || null;
    }
    renderRunTrace(trace);
  } catch (e) {
    console.error('Failed to inspect run trace:', e);
  }
}

function statusPillClass(status) {
  if (status === 'PASS' || status === 'DONE') return 'pill--pass';
  if (
    status === 'FAIL' ||
    status === 'TEST_FAIL' ||
    status === 'COMPILE_FAIL' ||
    status === 'TOOL_ERROR' ||
    status === 'TIMEOUT'
  )
    return 'pill--fail';
  if (status === 'RUNNING') return 'pill--live';
  if (status === 'UNVERIFIED' || status === 'STALE') return 'pill--warn';
  return '';
}

function renderRunTrace(trace) {
  const sumEl = document.getElementById('trace-summary');
  const pbEl = document.getElementById('trace-playback');
  const verEl = document.getElementById('version-history-panel');
  const tlEl = document.getElementById('trace-timeline-panel');
  const wfMetaEl = document.getElementById('trace-waveform-meta');
  const wfSel = document.getElementById('trace-waveform-case-select');
  const wfDisp = document.getElementById('trace-waveform-display');

  if (!trace) {
    if (sumEl) sumEl.innerHTML = '';
    if (pbEl)
      pbEl.innerHTML = `<div class="card-subtle muted">${escapeHtml(t('No run selected.', '未选择运行记录。'))}</div>`;
    if (verEl) verEl.innerHTML = '';
    if (tlEl) tlEl.innerHTML = '';
    return;
  }

  const tok = trace.token_summary || {};
  if (sumEl) {
    const fwLabel =
      trace.framework_kind === 'star_v2' ? 'STAR v2 (5-Stage)' : `Baseline (${trace.framework})`;
    const tokStr =
      tok.usage_available && tok.total_tokens != null
        ? `${tok.total_tokens} (in:${tok.input_tokens ?? '—'} out:${tok.output_tokens ?? '—'})`
        : '—';
    const elapsedStr =
      trace.elapsed_seconds != null
        ? `${Number(trace.elapsed_seconds).toFixed(1)}s`
        : trace.state === 'running'
          ? t('Running', '运行中')
          : '—';
    sumEl.innerHTML =
      `<div class="metric-box"><div class="metric-label">${escapeHtml(t('Task / Condition', '任务 / 条件'))}</div><div class="metric-val">${escapeHtml(trace.task_id)}${trace.condition ? ' · ' + escapeHtml(trace.condition) : ''}</div></div>` +
      `<div class="metric-box"><div class="metric-label">${escapeHtml(t('Architecture', 'Agent 架构'))}</div><div class="metric-val">${escapeHtml(fwLabel)}</div></div>` +
      `<div class="metric-box"><div class="metric-label">${escapeHtml(t('Status', '状态'))}</div><div class="metric-val"><span class="pill ${statusPillClass(trace.status)}">${trace.state === 'running' ? '<span class="pulse-dot"></span>' : ''}${escapeHtml(trace.status)}</span></div></div>` +
      `<div class="metric-box"><div class="metric-label">Tokens</div><div class="metric-val" style="font-size:13px;">${escapeHtml(tokStr)}</div></div>` +
      `<div class="metric-box"><div class="metric-label">${escapeHtml(t('Elapsed', '耗时'))}</div><div class="metric-val">${escapeHtml(elapsedStr)}</div></div>`;
  }

  if (pbEl) {
    const stages = trace.stages || [];
    const nodesHtml = stages
      .map(st => {
        const label = gLang === 'zh' ? st.label_zh || st.label_en : st.label_en;
        const summary = gLang === 'zh' ? st.summary_zh || st.summary_en : st.summary_en;
        const selCls = st.id === gSelectedStageId ? ' selected' : '';
        const rollbackPill =
          st.metrics && st.metrics.rollback_count > 0
            ? `<span class="pill pill--warn">${escapeHtml(t(`${st.metrics.rollback_count} rollback`, `回滚 ${st.metrics.rollback_count} 次`))}</span>`
            : '';
        return (
          `<button type="button" class="stage-node status-${escapeHtml(st.status)}${selCls}" onclick="selectTraceStage('${escapeHtml(st.id)}')">` +
          `<div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">` +
          `<strong style="font-size:13px;">${escapeHtml(label)}</strong>` +
          `<span class="pill ${statusPillClass(st.status)}">${st.status === 'RUNNING' ? '<span class="pulse-dot"></span>' : ''}${escapeHtml(st.status)}</span>` +
          `</div>` +
          `<div class="muted" style="font-size:12px;">${escapeHtml(summary || '')}</div>` +
          (rollbackPill ? `<div>${rollbackPill}</div>` : '') +
          `</button>`
        );
      })
      .join('');

    const activeStage = stages.find(s => s.id === gSelectedStageId) || stages[0];
    const stageDetailHtml = activeStage
      ? `<div class="card-subtle" style="margin-top:10px;">` +
        `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">` +
        `<strong>${escapeHtml(gLang === 'zh' ? activeStage.label_zh : activeStage.label_en)}</strong>` +
        `<span class="pill ${statusPillClass(activeStage.status)}">${escapeHtml(activeStage.status)}</span>` +
        `</div>` +
        `<pre class="mono" style="margin:0;font-size:11.5px;max-height:220px;overflow:auto;white-space:pre-wrap;">${escapeHtml(JSON.stringify(activeStage.detail || activeStage.metrics || {}, null, 2))}</pre>` +
        `</div>`
      : '';

    pbEl.innerHTML = `<div class="pipeline-rail">${nodesHtml}</div>` + stageDetailHtml;
  }

  if (verEl) {
    const versions = trace.versions || [];
    if (!versions.length) {
      verEl.innerHTML = `<div class="card-subtle muted">${escapeHtml(t('No candidate versions yet.', '暂无候选版本。'))}</div>`;
    } else {
      const idx = Math.min(gSelectedVersionIdx, versions.length - 1);
      const activeVer = versions[idx];
      const pills = versions
        .map((v, i) => {
          const btnCls = i === idx ? 'btn btn-sm btn-primary' : 'btn btn-sm';
          const tag = v.rolled_back
            ? ` [${t('ROLLED BACK', '已回滚')}]`
            : v.is_final
              ? ` [${t('FINAL', '最终')}]`
              : '';
          return `<button type="button" class="${btnCls}" onclick="selectTraceVersion(${i})">${escapeHtml(v.label + tag)}</button>`;
        })
        .join('');
      const hasDiff = (activeVer.diff_from_prev || []).length > 0;
      const showDiff = gVersionViewMode === 'diff' && hasDiff;
      const modeToggle = hasDiff
        ? `<div style="display:flex;gap:4px;"><button type="button" class="btn btn-sm ${!showDiff ? 'btn-primary' : ''}" onclick="setVersionViewMode('st')">ST</button><button type="button" class="btn btn-sm ${showDiff ? 'btn-primary' : ''}" onclick="setVersionViewMode('diff')">Diff</button></div>`
        : '';
      const codeBody = showDiff
        ? (activeVer.diff_from_prev || [])
            .map(line => {
              const cls =
                line.startsWith('+') && !line.startsWith('+++')
                  ? 'diff-line diff-add'
                  : line.startsWith('-') && !line.startsWith('---')
                    ? 'diff-line diff-del'
                    : line.startsWith('@@')
                      ? 'diff-line diff-hdr'
                      : 'diff-line';
              const content =
                (line.startsWith('+') || line.startsWith('-')) &&
                !line.startsWith('+++') &&
                !line.startsWith('---')
                  ? `${escapeHtml(line[0])}${highlightST(line.slice(1))}`
                  : line.startsWith(' ')
                    ? ` ${highlightST(line.slice(1))}`
                    : escapeHtml(line);
              return `<div class="${cls}">${content}</div>`;
            })
            .join('')
        : `<div class="diff-line" style="white-space:pre-wrap;padding:6px 12px;">${highlightST(activeVer.full_st || '')}</div>`;
      verEl.innerHTML =
        `<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">` +
        `<div style="display:flex;gap:6px;flex-wrap:wrap;">${pills}</div>${modeToggle}` +
        `</div>` +
        `<div class="muted" style="font-size:12px;margin-bottom:6px;">` +
        `<strong class="mono">${escapeHtml(activeVer.id)}</strong> · SHA256: <span class="mono">${escapeHtml((activeVer.sha256 || '').slice(0, 12))}</span>` +
        `</div>` +
        `<div class="diff-box">${codeBody}</div>`;
    }
  }

  if (tlEl) {
    const timeline = trace.timeline || [];
    if (!timeline.length) {
      tlEl.innerHTML = `<div class="card-subtle muted">${escapeHtml(t('No events logged.', '暂无事件日志。'))}</div>`;
    } else {
      const rows = timeline
        .map(ev => {
          const lat =
            ev.elapsed_seconds != null ? `${Number(ev.elapsed_seconds).toFixed(2)}s` : '—';
          const tokCell = ev.total_tokens != null ? String(ev.total_tokens) : '—';
          return (
            `<tr>` +
            `<td class="mono" style="font-size:11px;white-space:nowrap;">${escapeHtml((ev.utc || '').replace('T', ' ').slice(0, 19) || '—')}</td>` +
            `<td class="mono" style="font-size:12px;">${escapeHtml(ev.actor || '')}</td>` +
            `<td class="mono" style="font-size:12px;">${escapeHtml(ev.event || '')}</td>` +
            `<td><span class="pill ${statusPillClass(ev.status)}">${escapeHtml(ev.status || '')}</span></td>` +
            `<td class="mono" style="font-size:11.5px;">${escapeHtml(lat)} / ${escapeHtml(tokCell)}</td>` +
            `</tr>`
          );
        })
        .join('');
      tlEl.innerHTML =
        `<div style="max-height:390px;overflow:auto;"><table class="clean-table"><thead><tr>` +
        `<th>UTC</th><th>${escapeHtml(t('Actor', '节点'))}</th><th>${escapeHtml(t('Event', '事件'))}</th><th>${escapeHtml(t('Status', '状态'))}</th><th>${escapeHtml(t('Time / Tok', '耗时/Token'))}</th>` +
        `</tr></thead><tbody>${rows}</tbody></table></div>`;
    }
  }

  gTraceWaveforms = trace.waveforms || [];
  if (wfMetaEl) {
    const ws = trace.waveform_source || {};
    wfMetaEl.innerHTML =
      ws.kind && ws.kind !== 'none'
        ? `<span class="pill ${ws.execution_verified ? 'pill--pass' : 'pill--warn'}">${escapeHtml(ws.kind)} · ${escapeHtml(ws.backend || '')}</span> ` +
          `<span class="mono muted" style="font-size:12px;">${escapeHtml(ws.trace_relpath || '')}</span>`
        : `<span class="pill">${escapeHtml(t('No Trace', '暂无波形'))}</span>`;
  }
  renderWaveformPanel(
    gTraceWaveforms,
    wfSel,
    wfDisp,
    t('No simulation trace recorded for this run.', '该运行暂无仿真波形记录。')
  );
}

function selectTraceStage(stageId) {
  gSelectedStageId = stageId;
  if (gCurrentRunTrace) renderRunTrace(gCurrentRunTrace);
}

function selectTraceVersion(idx) {
  gSelectedVersionIdx = idx;
  if (gCurrentRunTrace) renderRunTrace(gCurrentRunTrace);
}

function setVersionViewMode(mode) {
  gVersionViewMode = mode === 'diff' ? 'diff' : 'st';
  if (gCurrentRunTrace) renderRunTrace(gCurrentRunTrace);
}

function loadRunCandidateIntoSandbox() {
  if (!gCurrentRunTrace || !gCurrentRunTrace.versions || !gCurrentRunTrace.versions.length) return;
  const idx = Math.min(gSelectedVersionIdx, gCurrentRunTrace.versions.length - 1);
  const ver = gCurrentRunTrace.versions[idx];
  setSandboxCode(ver.full_st || '');
  const banner = document.getElementById('sandbox-provenance-banner');
  if (banner) {
    banner.hidden = false;
    banner.innerHTML = `<span class="pill">${escapeHtml(t('Candidate', '候选代码'))}</span> <strong class="mono">${escapeHtml(gCurrentRunTrace.task_id)} / ${escapeHtml(ver.id)}</strong> <span class="mono muted">${escapeHtml(gCurrentRunTrace.run_id)}</span>`;
  }
  if (
    gCurrentRunTrace.task_id &&
    (!gCurrentTask || gCurrentTask.task.id !== gCurrentRunTrace.task_id)
  ) {
    selectTask(gCurrentRunTrace.task_id);
  }
  switchTab('sandbox');
}

function renderBenchmarkPanel() {
  const box = document.getElementById('benchmark-summary-panel');
  const statusBadge = document.getElementById('benchmark-status-badge');
  if (!box) return;
  const exp = gExperiments || {};
  const conditions = exp.conditions || [];
  const metrics = exp.metrics || null;
  const metricConds = (metrics && metrics.conditions) || {};

  if (statusBadge) {
    statusBadge.className = metrics ? 'pill pill--pass' : 'pill';
    statusBadge.textContent = metrics
      ? t('Campaign Aggregate Ready', '汇总数据已就绪')
      : t('Pending Full Campaign', '待全量实测汇总');
  }

  const rows = conditions
    .map(c => {
      const m = metricConds[c.id] || {};
      const runsForCond = (gRuns || []).filter(r => r.condition === c.id);
      const passStr = m.evaluated
        ? `${m.passed || 0}/${m.evaluated}`
        : runsForCond.length
          ? `${runsForCond.filter(r => r.status === 'PASS').length}/${runsForCond.length} (${t('local', '本地')})`
          : '—';
      return (
        `<tr>` +
        `<td class="mono"><strong>${escapeHtml(c.id)}</strong></td>` +
        `<td class="mono">${escapeHtml(c.framework || '')}</td>` +
        `<td class="mono">${escapeHtml(c.model || '')}</td>` +
        `<td>${c.ablation ? `<span class="pill pill--warn">${escapeHtml(c.ablation)}</span>` : c.spec_visible === false ? `<span class="pill">No LTL Spec</span>` : `<span class="pill pill--pass">Full Spec</span>`}</td>` +
        `<td class="mono">${escapeHtml(passStr)}</td>` +
        `</tr>`
      );
    })
    .join('');

  box.innerHTML = rows
    ? `<div style="overflow-x:auto;"><table class="clean-table"><thead><tr><th>ID</th><th>${escapeHtml(t('Framework', '框架'))}</th><th>${escapeHtml(t('Model', '模型'))}</th><th>${escapeHtml(t('Config / Ablation', '条件 / 消融'))}</th><th>PASS</th></tr></thead><tbody>${rows}</tbody></table></div>`
    : `<div class="muted">${escapeHtml(t('No experiment configuration found.', '未找到实验配置文件。'))}</div>`;
}

/* ================= Tab 3: Sandbox & Waveform Lab ================= */
function populateSandboxTemplate(detail) {
  if (!detail || !detail.task) return;
  const task = detail.task;
  const badge = document.getElementById('sandbox-task-badge');
  if (badge) badge.textContent = `${task.id} · ${task.difficulty || ''}`;

  const inputs = [];
  const outputs = [];
  const inouts = [];
  (task.interface || []).forEach(p => {
    const line = `    ${p.name} : ${p.type || 'BOOL'};`;
    if (p.direction === 'OUTPUT') outputs.push(line);
    else if (p.direction === 'IN_OUT') inouts.push(line);
    else inputs.push(line);
  });

  const sections = ['FUNCTION_BLOCK FB_Task'];
  if (inputs.length) sections.push(`VAR_INPUT\n${inputs.join('\n')}\nEND_VAR`);
  if (outputs.length) sections.push(`VAR_OUTPUT\n${outputs.join('\n')}\nEND_VAR`);
  if (inouts.length) sections.push(`VAR_IN_OUT\n${inouts.join('\n')}\nEND_VAR`);
  sections.push('VAR\n    // Internal state or TON timers\nEND_VAR');
  sections.push('\n// Write IEC 61131-3 ST implementation below\n');

  setSandboxCode(sections.join('\n'));

  const banner = document.getElementById('sandbox-provenance-banner');
  if (banner) banner.hidden = true;

  const allCases = (task.tests || []).concat(detail.random_cases || []);
  gWaveforms = allCases.map(c => ({
    case_id: c.id,
    name: c.purpose || c.name || c.id,
    passed: null,
    steps: (c.steps || []).map((st, idx) => ({
      step: idx,
      inputs: st.inputs || {},
      expected: st.expected || {},
      observed: null,
      dt_ms: st.dt_ms,
      match: null,
      divergence: null,
    })),
  }));
  renderWaveformPanel(
    gWaveforms,
    document.getElementById('waveform-case-select'),
    document.getElementById('waveform-display')
  );
}

async function loadReferenceSt() {
  if (!gCurrentTask || !gCurrentTask.task) return;
  const tid = gCurrentTask.task.id;
  const consoleBox = document.getElementById('sandbox-console');
  const banner = document.getElementById('sandbox-provenance-banner');
  try {
    const resp = await fetch(`/api/reference-st?id=${encodeURIComponent(tid)}`);
    const data = await resp.json();
    if (!resp.ok || !data.available) {
      if (banner) {
        banner.hidden = false;
        banner.innerHTML = `<span class="pill pill--warn">${escapeHtml(t('Unavailable', '暂无示例'))}</span> <span class="mono">codesys/examples/${escapeHtml(tid)}.json</span>`;
      }
      return;
    }
    setSandboxCode(`${(data.declaration || '').trim()}\n\n${(data.implementation || '').trim()}\n`);
    if (banner) {
      banner.hidden = false;
      banner.innerHTML = `<span class="pill">${escapeHtml(t('Reference ST', '参考示例'))}</span> <strong class="mono">${escapeHtml(data.source || '')}</strong>`;
    }
    if (consoleBox) {
      consoleBox.textContent = `Loaded ${data.source || tid}.`;
    }
  } catch (e) {
    console.error('Failed to load reference ST:', e);
  }
}

async function runSandboxEvaluate() {
  if (!gCurrentTask || !gCurrentTask.task) return;
  const editor = document.getElementById('st-source-code');
  const consoleBox = document.getElementById('sandbox-console');
  const incRand = !!(document.getElementById('eval-include-random') || {}).checked;
  const code = editor ? editor.value : '';
  if (consoleBox)
    consoleBox.textContent = t(
      'Running CODESYS compile & simulation...',
      '正在调用 CODESYS 编译与仿真...'
    );

  try {
    const resp = await fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        task_id: gCurrentTask.task.id,
        candidate: code,
        include_random: incRand,
      }),
    });
    const data = await resp.json();
    if (resp.status === 503) {
      if (consoleBox) {
        consoleBox.textContent = `[HTTP 503 · ${data.status || 'UNVERIFIED'}]\n${data.error || t('CODESYS unavailable.', 'CODESYS 未配置。')}`;
      }
      return;
    }
    if (consoleBox) {
      const comp = data.compile || {};
      const sim = data.simulation || {};
      const diags = (comp.diagnostics || [])
        .slice(0, 15)
        .map(d => `[${d.severity || ''}] ${d.text || ''}`)
        .join('\n');
      consoleBox.textContent =
        `Backend: ${data.execution_kind || 'UNKNOWN'}\n` +
        `Compile: ${comp.status || 'UNKNOWN'} (success=${comp.success})\n` +
        (sim.status
          ? `Simulation: ${sim.status} (${sim.passed_cases || 0}/${sim.evaluated_cases || 0} passed)\n`
          : '') +
        (diags ? `\n${diags}` : '');
    }
    if (Array.isArray(data.waveform) && data.waveform.length > 0) {
      gWaveforms = data.waveform;
      const sel = document.getElementById('waveform-case-select');
      const firstFail = gWaveforms.find(w => w.passed === false);
      renderWaveformPanel(gWaveforms, sel, document.getElementById('waveform-display'));
      if (firstFail && sel) {
        sel.value = firstFail.case_id;
        renderWaveformPanel(gWaveforms, sel, document.getElementById('waveform-display'));
      }
    }
  } catch (e) {
    if (consoleBox) consoleBox.textContent = `Request failed: ${String(e)}`;
  }
}

async function runExportVerify() {
  if (!gCurrentTask || !gCurrentTask.task) return;
  const editor = document.getElementById('st-source-code');
  const consoleBox = document.getElementById('sandbox-console');
  try {
    const resp = await fetch('/api/export-verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        task_id: gCurrentTask.task.id,
        candidate: editor ? editor.value : '',
      }),
    });
    const data = await resp.json();
    if (consoleBox) {
      consoleBox.textContent =
        `Bundle: ${data.bundle_dir || ''}\n\n` +
        `--- spec.ltl ---\n${data.spec_ltl || ''}\n\n` +
        `--- verification_manifest.json ---\n${JSON.stringify(data.manifest || {}, null, 2)}`;
    }
  } catch (e) {
    if (consoleBox) consoleBox.textContent = `Export failed: ${String(e)}`;
  }
}

async function bootstrapWebUI() {
  if (gBootstrapped) return;
  gBootstrapped = true;
  let initialLang = 'en';
  try {
    const u = new URL(window.location.href);
    const qLang = u.searchParams.get('lang');
    const saved =
      typeof localStorage !== 'undefined' && localStorage.getItem
        ? localStorage.getItem('star_plc_lang')
        : null;
    if (qLang === 'zh' || qLang === 'en') initialLang = qLang;
    else if (saved === 'zh' || saved === 'en') initialLang = saved;
  } catch (e) {}
  gLang = initialLang;
  const langSel = document.getElementById('language-select');
  if (langSel) {
    langSel.value = gLang;
    langSel.addEventListener('change', ev => changeLanguage(ev.target.value));
  }
  applyStaticLanguage();

  const wire = (id, ev, fn) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener(ev, fn);
  };
  wire('kind-filter', 'change', () => renderTaskList(true));
  wire('difficulty-filter', 'change', () => renderTaskList(true));
  wire('task-search', 'input', () => renderTaskList(false));
  wire('pilot-only', 'change', () => renderTaskList(true));
  wire('task-select', 'change', ev => selectTask(ev.target.value));
  wire('st-source-code', 'input', syncEditorHighlight);
  wire('st-source-code', 'scroll', syncEditorScroll);
  wire('waveform-case-select', 'change', () => {
    renderWaveformPanel(
      gWaveforms,
      document.getElementById('waveform-case-select'),
      document.getElementById('waveform-display')
    );
  });
  wire('trace-waveform-case-select', 'change', () => {
    renderWaveformPanel(
      gTraceWaveforms,
      document.getElementById('trace-waveform-case-select'),
      document.getElementById('trace-waveform-display')
    );
  });
  wire('run-select', 'change', ev => loadRunTrace(ev.target.value));
  wire('refresh-runs-btn', 'click', () => refreshWorkflowData(true));
  wire('live-poll-toggle', 'change', () => updatePollBadge());
  wire('btn-load-skeleton', 'click', () => gCurrentTask && populateSandboxTemplate(gCurrentTask));
  wire('btn-load-reference', 'click', () => loadReferenceSt());
  wire('btn-load-run-candidate', 'click', () => loadRunCandidateIntoSandbox());
  wire('btn-load-run-to-sandbox', 'click', () => loadRunCandidateIntoSandbox());

  if (typeof document !== 'undefined' && document.addEventListener) {
    document.addEventListener('keydown', ev => {
      if (ev.key === 'Escape') hideSpecPopover(true);
    });
    document.addEventListener('click', ev => {
      const pop = document.getElementById('spec-popover');
      if (!pop || pop.hidden) return;
      if (
        ev.target &&
        ev.target.closest &&
        (ev.target.closest('#spec-popover') || ev.target.closest('.spec-tok'))
      )
        return;
      hideSpecPopover(true);
    });
  }

  try {
    const resp = await fetch('/api/tasks');
    if (resp.ok) {
      const data = await resp.json();
      gTasks = data.tasks || [];
      gReviews = data.task_review || [];
      gPilotReview = data.pilot_review || [];
      gCheckerAvail = data.checker_availability || null;
      renderSystemStatus();
      renderTaskList(true);
    }
  } catch (e) {
    console.error('Bootstrap /api/tasks failed:', e);
  }

  try {
    const u = new URL(window.location.href);
    const reqTab = u.searchParams.get('tab');
    const reqTask = u.searchParams.get('task');
    if (reqTask) await selectTask(reqTask);
    if (reqTab) switchTab(reqTab);
  } catch (e) {}

  ensureLivePolling();
}

if (typeof document !== 'undefined' && document.addEventListener) {
  document.addEventListener('DOMContentLoaded', bootstrapWebUI);
}
if (typeof window !== 'undefined' && window.addEventListener && window !== document) {
  window.addEventListener('DOMContentLoaded', bootstrapWebUI);
}
