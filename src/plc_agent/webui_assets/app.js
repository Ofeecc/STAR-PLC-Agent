'use strict';
let gTasks=[], gReviews=[], gPilotReview=[], gCurrentTask=null, gLastWaveformData=[];
let gRequestSerial=0, gLastEvaluation=null, gLastExport=null;
const params=new URLSearchParams(location.search);
let gLang=params.get('lang');
if(!['zh','en'].includes(gLang)) {
  try {gLang=localStorage.getItem('star-plc-language');} catch(_) {}
}
if(!['zh','en'].includes(gLang)) gLang='zh';
const tr=(zh,en)=>gLang==='zh'?zh:en;
const esc=value=>String(value==null?'':value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const difficulty=value=>({easy:tr('简单','Easy'),medium:tr('中等','Medium'),hard:tr('困难','Hard')})[value]||value;
const kind=value=>value==='public'?tr('公开题','Public'):tr('自建题','Self-built');
const reviewFor=id=>gReviews.find(r=>r.id===id);
const titleFor=task=>gLang==='zh'&&reviewFor(task.id)?reviewFor(task.id).title_zh:task.title;
const staticPairs=[
 ['CODESYS STAR v2 | 题库审核与实验验证','CODESYS STAR v2 | Auto-Test & Waveform Agent Trace Inspector'],
 ['IEC 61131-3 题库审核与实验证据','IEC 61131-3 TASK REVIEW & EXPERIMENT EVIDENCE'],
 ['📂 题库与规约审核','📂 Task & Dataset Explorer'],['📊 波形与时序对比','📊 Waveform & Timing Comparator'],
 ['🧠 Agent 工作流程','🧠 Agent Trace Playback'],['🧪 编译仿真与验证导出','🧪 Interactive Sandbox & Verifier'],
 ['全题库 · 人工审核','Full Dataset · Human Review'],
 ['32题均可审查；勾选“仅显示本轮六题”可回到原试跑范围。先核对题意，再审补充约定、规约和逐步预期值。','Review all 32 tasks, or filter to the original six-task pilot. Check the requirements, additional assumptions, specifications and expected traces.'],
 ['中文材料为组内整理，均待人工审核。界面中的题库与预期值不代表已通过 Agent 或真实 PLC 测试。','Translations and review notes are group-authored and pending human review. Dataset expectations are not evidence of successful Agent or PLC execution.'],
 ['题目选择与概况','Task Selection & Overview'],['仅显示本轮六题','Original six-task pilot only'],
 ['🔄 刷新','🔄 Refresh'],['正在读取题库…','Loading tasks...'],
 ['在上方选择题目，查看题意、接口、规约和逐步测试。','Select a task above to inspect details, interface pins, specifications, and test cases.'],
 ['接口定义 · 变量与信号','Interface · Variables & Signals'],['规约属性 · 组内编写，待审核','Specifications · Group-authored, Pending Review'],
 ['测试用例 · 组内编写，待审核','Test Cases · Group-authored, Pending Review'],['尚未选择题目。','No task selected.'],
 ['信号波形对比','Signal Waveform Comparator'],['（运行评测后查看波形）','(Run evaluation to view waveforms)'],
 ['⚡ 评测当前代码','⚡ Evaluate Current Task'],
 ['逐步对比输入、预期输出、候选实际输出和 dt_ms。红色表示发现差异；没有运行数据时不推定通过。','Visualizing step-by-step logic signals: comparing input stimuli, expected outputs, candidate observed outputs, and dt_ms intervals. Red blocks indicate first Divergence point where candidate failed.'],
 ['运行候选 ST 后查看实际信号波形。','Select or evaluate a candidate ST to inspect signal waveforms.'],
 ['STAR 流程概览','STAR Pipeline Overview'],['🔄 刷新实验记录','🔄 Refresh Trace Status'],
 ['查看流程结构、方言规则、编译诊断与版本评分；以下流程图是说明，不是实时执行状态。','Inspect the deterministic state graph, dialect cards applied, compiler diagnostic compactions, and ratchet progress.'],
 ['阶段 01','STAGE 01'],['阶段 02','STAGE 02'],['阶段 03','STAGE 03'],['阶段 04','STAGE 04'],['阶段 05','STAGE 05'],
 ['需求与规约分析','Contract Analyzer'],['方言规则','Dialect Cards'],['编译修复循环','Compiler Loop'],['版本择优','Lexicographical Ratchet'],['验证材料导出','Verification Export'],
 ['分析接口、规约约束及初始状态。','Parses interface types, LTL safety constraints, and initial state invariants.'],
 ['提供目标 CODESYS V3.5 的语法、时间字面量及相关规则。','Injects target CODESYS V3.5 syntax rules, TIME literals, and vendor pragmas.'],
 ['无界面编译，记录诊断及行号。','Performs headless build, captures diagnostics, and maps line numbers.'],
 ['在相同自测集上比较版本；此流程图不代表一次真实执行。','Compares versions using the same self-test set; this diagram is not a live execution trace.'],
 ['导出候选 ST 与规约；候选代码的完整模型检查尚未接通。','Exports candidate ST and properties; full candidate model checking is not yet integrated.'],
 ['CODESYS 方言规则示例','CODESYS Dialect Rule Examples'],['规则编号','Rule ID'],['类别','Category'],['IEC 61131-3 标准','IEC 61131-3 Standard'],['CODESYS V3.5 方言要求','CODESYS V3.5 Dialect Requirement'],
 ['时间字面量','Time Literals'],['引用传递变量','In-Out Variables'],['TON/TOF定时器','Ton/Toff Timers'],['数组下标','Array Indices'],
 ['严格时间语法，前缀后无空格；精度依类型。','Strict duration syntax, no space after prefix, microsecond precision'],
 ['按引用传递','passed by reference'],['必须传入可写存储变量，不能传常量。','Requires allocated variable storage, no constants in caller POUs'],
 ['跨扫描保留实例状态，不能每拍创建临时实例。','State persistence across scan cycles; cannot be re-instantiated dynamically'],
 ['可从0或1等下界开始','1-based or 0-based bounds'],['显式数组边界；按声明下界访问。','Explicit'],['边界检查','bounds checking'],
 ['ST 编译仿真与验证导出','IEC Structured Text Sandbox & Verifier'],['加入随机差分测试','Include Random Differential Tests'],
 ['▶ 编译并仿真','▶ Compile & Simulate'],['🛡️ 导出验证材料','🛡️ Export Verification Bundle'],
 ['候选结构化文本（ST）：','CANDIDATE STRUCTURED TEXT (ST):'],['编译与仿真控制台：','COMPILER & SIMULATION CONSOLE:'],
 ['就绪。选择题目并填写完整 ST 后点击“编译并仿真”。','Ready. Select a task or edit Structured Text and press "Compile & Simulate".'],
 ['全部来源','All Sources'],['公开题','Public Tasks'],['自建题','Self-built Tasks'],['全部难度','All Difficulties'],['简单','Easy'],['中等','Medium'],['困难','Hard']
];
const staticNodes=[];
function captureStaticText() {
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  let node;
  while((node=walker.nextNode())) {
    if(node.parentElement.closest('script,style,code,textarea'))continue;
    const text=node.textContent.replace(/\s+/g,' ').trim();
    const pair=staticPairs.find(p=>p.includes(text));
    if(pair) staticNodes.push({node,pair});
  }
}
function applyStaticLanguage() {
  staticNodes.forEach(({node,pair})=>{node.textContent=' '+pair[gLang==='zh'?0:1]+' ';});
  document.documentElement.lang=gLang==='zh'?'zh-CN':'en';
  document.title=tr('STAR PLC · 题库审核与验证','STAR PLC · Task Review & Verification');
  document.getElementById('language-select').value=gLang;
  document.getElementById('task-search').placeholder=tr('搜索题号 / 中英文题名','Search ID or Chinese / English title');
  document.getElementById('st-source-code').placeholder=tr('输入完整 ST 功能块：FUNCTION_BLOCK FB_Task ... END_FUNCTION_BLOCK','Enter complete ST: FUNCTION_BLOCK FB_Task ... END_FUNCTION_BLOCK');
}
function changeLanguage(value) {
  if(!['zh','en'].includes(value))return;
  gLang=value;
  try{localStorage.setItem('star-plc-language',value);}catch(_){}
  const url=new URL(location.href);url.searchParams.set('lang',value);history.replaceState(null,'',url);
  hideSpecPopover(true);applyStaticLanguage();renderTaskList(false);
  if(gCurrentTask){renderTaskDetails(gCurrentTask);renderReviewDetails(gCurrentTask);}
  updateWaveformCaseSelector();
  if(gLastEvaluation)renderEvaluation(gLastEvaluation);
  else if(gLastExport)renderExport(gLastExport);
  updateStatus();
}
function updateStatus(){document.getElementById('system-status').textContent=tr(`题库已载入 · ${gTasks.length}题`,`DATASET READY · ${gTasks.length} TASKS`);}
async function api(path,body) {
  const response=await fetch(path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  const data=await response.json();
  if(!response.ok)throw new Error(data.error||data.reason||`HTTP ${response.status}`);
  return data;
}
function switchTab(name) {
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.toggle('active',b.dataset.tab===name));
  document.querySelectorAll('.tab-pane').forEach(p=>p.classList.toggle('active',p.id==='tab-'+name));
}
function visibleTasks() {
  const only=document.getElementById('pilot-only').checked;
  const ids=new Set(gPilotReview.map(r=>r.id));
  const query=document.getElementById('task-search').value.trim().toLowerCase();
  const source=document.getElementById('kind-filter').value;
  const diff=document.getElementById('difficulty-filter').value;
  return gTasks.filter(t=>(!only||ids.has(t.id))&&(source==='all'||t.kind===source||(source==='self'&&t.kind==='self_built'))&&(diff==='all'||t.difficulty===diff)&&
    `${t.id} ${t.title} ${(reviewFor(t.id)||{}).title_zh||''}`.toLowerCase().includes(query));
}
function renderTaskList(loadSelected=true) {
  const tasks=visibleTasks(), select=document.getElementById('task-select');
  const previous=select.value||new URLSearchParams(location.search).get('task');
  select.innerHTML=tasks.map(t=>`<option value="${esc(t.id)}">${esc(t.id)} · ${esc(titleFor(t))} · ${esc(difficulty(t.difficulty))}</option>`).join('');
  select.value=tasks.some(t=>t.id===previous)?previous:(tasks[0]||{}).id||'';
  document.getElementById('pilot-total').textContent=tr(`${tasks.length}题 · ${tasks.reduce((n,t)=>n+t.tests_count,0)}用例 · ${tasks.reduce((n,t)=>n+t.steps_count,0)}步`,`${tasks.length} tasks · ${tasks.reduce((n,t)=>n+t.tests_count,0)} cases · ${tasks.reduce((n,t)=>n+t.steps_count,0)} steps`);
  const grid=document.getElementById('pilot-grid');
  grid.innerHTML=tasks.map(t=>`<button class="pilot-card" data-task="${esc(t.id)}" aria-pressed="${gCurrentTask?.task.id===t.id}"><div class="pilot-card-head"><strong>${esc(t.id)} · ${esc(titleFor(t))}</strong>${renderCardSmvBadges(t.smv_status)}</div><span>${esc(kind(t.kind))} · ${esc(difficulty(t.difficulty))} · ${t.tests_count} ${tr('用例','cases')} / ${t.steps_count} ${tr('步','steps')} · ${t.properties_count} ${tr('属性','properties')}</span><br><span style="color:var(--amber)">${tr('待人工审核','Pending human review')}</span></button>`).join('')||`<p>${tr('没有匹配题目。','No matching tasks.')}</p>`;
  grid.querySelectorAll('button[data-task]').forEach(b=>b.onclick=()=>onTaskSelected(b.dataset.task));
  const url=new URL(location.href);url.searchParams.set('scope',document.getElementById('pilot-only').checked?'pilot':'all');history.replaceState(null,'',url);
  if(select.value && (loadSelected||gCurrentTask?.task.id!==select.value))onTaskSelected(select.value);
  if(!select.value){gRequestSerial++;gCurrentTask=null;clearTaskDetails();}
}
function clearTaskDetails(){
  ['task-overview','interface-pins-container','ltl-container','tests-container'].forEach(id=>document.getElementById(id).textContent=tr('没有匹配题目。','No matching tasks.'));
  document.getElementById('review-details-card').hidden=true;
}
async function reloadTasks(){
  try{
    const data=await api('/api/tasks');gTasks=data.tasks||[];gReviews=data.task_review||[];gPilotReview=data.pilot_review||[];
    updateStatus();renderTaskList(true);
  }catch(error){document.getElementById('system-status').textContent=tr('题库加载失败：','Failed to load tasks: ')+error.message;}
}
async function onTaskSelected(id){
  if(!id)return;
  document.getElementById('task-select').value=id;
  const serial=++gRequestSerial;
  const changed=gCurrentTask?.task.id!==id;
  if(changed){gCurrentTask=null;gLastWaveformData=[];gLastEvaluation=null;gLastExport=null;updateWaveformCaseSelector();}
  const url=new URL(location.href);url.searchParams.set('task',id);history.replaceState(null,'',url);
  try{
    const data=await api('/api/task?id='+encodeURIComponent(id));if(serial!==gRequestSerial)return;
    gCurrentTask=data;renderTaskDetails(data);renderReviewDetails(data);populateSandboxTemplate(data);
    document.querySelectorAll('.pilot-card').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.task===id)));
  }catch(error){if(serial===gRequestSerial)document.getElementById('task-overview').textContent=tr('读取失败：','Load failed: ')+error.message;}
}
function currentReview(data){return data.review?.source_matches?data.review:null;}
function renderReviewDetails(data){
  const task=data.task, review=currentReview(data), source=task.kind==='public'?tr('老师公开题','Teacher-provided public task'):tr('组内自建题','Group-authored task');
  const block=(title,text)=>`<section class="review-section"><h3>${esc(title)}</h3><div class="review-text">${esc(text)}</div></section>`;
  const raw={initial_conditions:task.initial_conditions,scan_semantics:task.scan_semantics,assumptions:task.assumptions,atomic_propositions:task.atomic_propositions,specification_contract:task.specification_contract};
  document.getElementById('review-details-card').hidden=false;
  let html=`<p><a href="#interface-pins-container">${tr('查看接口','Interface')}</a> · <a href="#ltl-container">${tr('查看规约','Specifications')}</a> · <a href="#tests-container">${tr('查看逐步测试','Step-by-step tests')}</a></p>`;
  if(!review)html+=`<p class="review-note">${tr('中文材料缺失或题目内容已变化，旧译文已停用，请重新审核。','Translation missing or stale; previous review text is withheld until rechecked.')}</p>`;
  html+=block('① '+source+' · '+tr('题意','Requirements'),gLang==='zh'&&review?review.translation_zh:task.requirements);
  html+=`<p class="spec-hint">${tr('中文为组内翻译；补充约定、规约和预期值由组内编写，均需人工确认。','Translations, additional assumptions, properties and expectations are group-authored and require human review.')}</p>`;
  html+=`<details class="review-section"><summary>${tr('查看原始英文题目与接口','Original source requirements & interface')}</summary><pre>${esc(task.requirements)}</pre></details>`;
  html+=block('② '+tr('组内补充约定 · 待认可','Additional assumptions · Pending approval'),gLang==='zh'&&review?review.assumptions_zh:(task.assumptions||[]).join('\n'));
  html+=block('③ '+tr('当前完整行为关系 · 待审核','Complete behavior relation · Pending review'),gLang==='zh'?(review?.complete_behavior_zh||''):tr('','Interpret the properties together with the scan semantics, initial conditions, declared history bindings and assumptions. The original complete relation is included in the source metadata below; no candidate formal proof is claimed.'));
  html+=`<details class="review-section"><summary>${tr('展开初值、扫描语义、原子命题与完整规约原文','Initial state, scan semantics, atomic propositions & source contract')}</summary><pre>${esc(JSON.stringify(raw,null,2))}</pre></details>`;
  html+=block('④ '+tr('现有固定测试覆盖','Current fixed-test scenarios'),gLang==='zh'&&review?review.coverage_zh:data.tests.map(t=>`${t.id}: ${t.purpose||t.name||''} (${t.steps.length} steps)`).join('\n'));
  html+=`<div class="review-note">${block('⑤ '+tr('重点确认 / 建议补测','Review focus / Further checks'),gLang==='zh'&&review?review.review_points_zh:'Check source agreement, strict/equal boundaries, same-scan priorities, retained history, reset behavior and a positive/negative trace for each property. Test counts do not establish complete coverage.')}</div>`;
  html+=`<p class="spec-hint">${tr('每个用例使用新实例。未列出的预期输出不表示FALSE；预期值不是实测值。解释性谓词须编码后才能模型检查。','Each case starts with a fresh instance. An omitted expected output is not implicitly FALSE. Expected values are not observations. Interpreted predicates require explicit encoding for model checking.')}</p>`;
  document.getElementById('review-details').innerHTML=html;
}
let gSymbolGlossary={},gPopoverTimer=null,gPopoverPinned=false;
const SPEC_CAT_ORDER=['input','output','persistent_inout','obs_history','ghost_state','alias'];
const SPEC_CAT_TEXT={
  input:{zh:'输入 INPUT',en:'INPUT'},
  output:{zh:'输出 OUTPUT',en:'OUTPUT'},
  persistent_inout:{zh:'持久化 IN_OUT',en:'Persistent IN_OUT'},
  obs_history:{zh:'上拍输出 O[k-1]',en:'Obs History O[k-1]'},
  ghost_state:{zh:'跨拍参考/幽灵态',en:'Ghost / Ref State'},
  alias:{zh:'别名 / 原子命题',en:'Alias / AP'}
};
function smvTooltip(smv){
  if(!smv)return '';
  const base=gLang==='zh'?(smv.badge_text_zh||''):(smv.badge_text_en||'');
  const note=gLang==='zh'?'仅针对显式 SMV 模型，不证明候选 ST 代码':'Explicit SMV model only; does not verify candidate ST';
  return `${base} · ${note}`;
}
function renderCardSmvBadges(smv){
  if(!smv)return `<div class="pilot-card-smv"><span class="smv-pill smv-tone-muted">${tr('SMV 未记录','No SMV record')}</span></div>`;
  const authText=gLang==='zh'?smv.authoring_text_zh:smv.authoring_text_en;
  const authTone=smv.authored?'cyan':'muted';
  const verText=gLang==='zh'?smv.badge_text_zh:smv.badge_text_en;
  const verTone=smv.badge_tone||'muted';
  return `<div class="pilot-card-smv" title="${esc(smvTooltip(smv))}"><span class="smv-pill smv-tone-${esc(authTone)}">${esc(authText||'SMV')}</span><span class="smv-pill smv-tone-${esc(verTone)}">${esc(verText||'')}</span></div>`;
}
function variantLabel(variant){
  if(gLang==='zh')return ({reference:'参考 SMV',complete:'完备 SMV',mutant:'变异 SMV'})[variant]||variant;
  return ({reference:'Reference SMV',complete:'Complete SMV',mutant:'Mutant SMV'})[variant]||variant;
}
function variantBadgeInfo(variant,vInfo){
  const eff=vInfo?.effective_status||'UNVERIFIED';
  if(eff==='STALE')return {tone:'amber',text:tr('模型变更 · 待重验','Stale · Re-verify')};
  if(eff==='CHECKER_MISSING')return {tone:'amber',text:tr(`缺 ${vInfo.required_tool||'Checker'}`,`Missing ${vInfo.required_tool||'Checker'}`)};
  if(eff==='TOOL_ERROR'||eff==='TIMEOUT')return {tone:'red',text:eff};
  if(eff==='MODEL_PROPERTIES_TRUE'){
    if(variant==='mutant')return {tone:'red',text:tr('变异逃逸 (未捕获)','Mutant escaped')};
    return {tone:'green',text:tr('属性全真','Properties TRUE')};
  }
  if(eff==='COUNTEREXAMPLE'){
    if(variant==='mutant')return {tone:'green',text:tr('变异已检出 (反例)','Mutant caught')};
    return {tone:'red',text:tr('出现反例','Counterexample')};
  }
  return {tone:'muted',text:eff};
}
function renderOverviewSmvBox(task,smv){
  if(!smv)return `<div class="overview-smv-box"><div class="overview-smv-head"><strong>${tr('显式 SMV 状态','Explicit SMV Status')}</strong><span class="smv-pill smv-tone-muted">${tr('未加载','Unavailable')}</span></div></div>`;
  const authText=gLang==='zh'?smv.authoring_text_zh:smv.authoring_text_en;
  const verText=gLang==='zh'?smv.badge_text_zh:smv.badge_text_en;
  const variants=smv.authored_variants||[];
  const rows=variants.map(variant=>{
    const v=smv.models?.[variant];
    if(!v)return '';
    const info=variantBadgeInfo(variant,v);
    const ratio=v.expected_properties!=null?`${v.passed_count??0}/${v.expected_properties}`:'—';
    const stamp=v.checked_utc?v.checked_utc.slice(0,19).replace('T',' ')+'Z':tr('未执行','Never');
    const engineMeta=`${v.required_tool||''} · ${ratio}`;
    const btnTitle=v.checker_missing?tr(`缺失 ${v.required_tool}，点击将记录 CHECKER_MISSING 状态`,`${v.required_tool} missing; clicking records CHECKER_MISSING`):tr('重新运行显式 SMV 验证并持久化结果','Re-run explicit SMV verification and persist result');
    return `<div class="overview-smv-row"><div><strong>${esc(variantLabel(variant))}</strong> <span class="smv-meta">${esc(engineMeta)} · ${esc(stamp)}</span></div><div style="display:flex;gap:6px;align-items:center"><span class="smv-pill smv-tone-${esc(info.tone)}">${esc(info.text)}</span><button type="button" class="btn btn-secondary" style="padding:3px 9px;font-size:.76rem" data-smv-run="${esc(variant)}" title="${esc(btnTitle)}">${tr('重验','Run')}</button></div></div>`;
  }).join('');
  const missingBanner=smv.checker_missing?`<div class="smv-meta" style="color:var(--amber);margin-top:6px">${tr(`环境缺失 ${smv.required_tool}：无法实时重跑，已优先保留哈希匹配的持久化验证记录。`,`${smv.required_tool} not installed: live re-run unavailable; hash-matched persisted records preserved.`)}</div>`:'';
  const attemptBanner=smv.last_run_attempt?.status==='CHECKER_MISSING'?`<div class="smv-meta" style="color:var(--amber);margin-top:4px">${tr('最近重跑尝试：','Last run attempt: ')}${esc(smv.last_run_attempt.variant||'')} · CHECKER_MISSING (${esc((smv.last_run_attempt.attempted_utc||'').slice(0,19).replace('T',' '))}Z)</div>`:'';
  return `<div class="overview-smv-box" id="overview-smv-box"><div class="overview-smv-head"><div><strong>${tr('显式 SMV 编写与验证','Explicit SMV Authoring & Verification')}</strong><div class="smv-meta">${tr('范围：仅显式 SMV 参考/完备/变异模型（不证明候选 ST）','Scope: explicit SMV models only (candidate ST not verified)')}</div></div><div class="pilot-card-smv"><span class="smv-pill smv-tone-${smv.authored?'cyan':'muted'}">${esc(authText)}</span><span class="smv-pill smv-tone-${esc(smv.badge_tone||'muted')}">${esc(verText)}</span></div></div>${rows||`<div class="smv-meta">${tr('本题尚无 SMV 模型文件。','No explicit SMV file for this task.')}</div>`}${missingBanner}${attemptBanner}<div class="overview-smv-actions" id="overview-smv-live-status"></div></div>`;
}
function lookupGlossarySymbol(token,glossary){
  if(!glossary||!token)return null;
  if(glossary[token])return glossary[token];
  if(token.includes('#')){const base=token.split('#')[0];if(glossary[base])return glossary[base];}
  if(token.includes('.')){const base=token.split('.')[0];if(glossary[base])return glossary[base];}
  return null;
}
function hideSpecPopover(force=false){
  if(gPopoverTimer){clearTimeout(gPopoverTimer);gPopoverTimer=null;}
  if(!force&&gPopoverPinned)return;
  gPopoverPinned=false;
  const pop=document.getElementById('spec-popover');
  if(pop)pop.hidden=true;
}
function positionSpecPopover(pop,anchor){
  const rect=anchor.getBoundingClientRect();
  const pad=10,maxW=380;
  pop.hidden=false;
  const popRect=pop.getBoundingClientRect();
  const width=Math.min(maxW,popRect.width||340);
  const height=popRect.height||180;
  let left=rect.left;
  if(left+width+pad>window.innerWidth)left=Math.max(pad,window.innerWidth-width-pad);
  let top=rect.bottom+8;
  if(top+height+pad>window.innerHeight&&rect.top-height-8>pad)top=rect.top-height-8;
  else if(top+height+pad>window.innerHeight)top=Math.max(pad,window.innerHeight-height-pad);
  pop.style.left=`${Math.round(left)}px`;
  pop.style.top=`${Math.round(top)}px`;
}
function showSpecPopover(anchor,symbol,pinned=false){
  const entry=lookupGlossarySymbol(symbol,gSymbolGlossary);
  const pop=document.getElementById('spec-popover');
  if(!entry||!pop)return;
  if(gPopoverTimer){clearTimeout(gPopoverTimer);gPopoverTimer=null;}
  if(pinned)gPopoverPinned=true;
  const catText=SPEC_CAT_TEXT[entry.category]?.zh||entry.category_zh||entry.category;
  const persistPill=entry.is_persistent?`<span class="spec-tok spec-tok--${esc(entry.category)} is-persistent" style="font-size:.72rem">持久化 / 跨拍重点</span>`:'';
  const srcHtml=entry.definition_source&&entry.definition_source!==entry.name&&entry.definition_source!==entry.definition_zh?`<div class="spec-popover-code">来源定义 / 绑定：${esc(entry.definition_source)}</div>`:'';
  const warnHtml=entry.persistence_warning_zh?`<div class="spec-popover-warn">${esc(entry.persistence_warning_zh)}</div>`:'';
  pop.innerHTML=`<div class="spec-popover-head"><span class="spec-tok spec-tok--${esc(entry.category)}${entry.is_persistent?' is-persistent':''}">${esc(entry.name)}</span><span class="spec-popover-cat">${esc(catText)} · ${esc(entry.type||'')}</span>${persistPill}</div><div class="spec-popover-title">${esc(entry.label_zh||entry.name)}</div><div class="spec-popover-desc">${esc(entry.definition_zh||'')}</div>${srcHtml}${warnHtml}`;
  positionSpecPopover(pop,anchor);
}
function attachPopoverEvents(container){
  if(!container)return;
  container.onmouseover=e=>{
    const pair=e.target.closest('.spec-pair');
    if(pair){pair.closest('.spec-formula')?.querySelectorAll('.spec-pair').forEach(n=>{if(n.dataset.pair===pair.dataset.pair)n.classList.add('is-match');});}
    const tok=e.target.closest('.spec-tok[data-symbol]');
    if(tok&&!gPopoverPinned)showSpecPopover(tok,tok.dataset.symbol,false);
  };
  container.onmouseout=e=>{
    const pair=e.target.closest('.spec-pair');
    if(pair){pair.closest('.spec-formula')?.querySelectorAll('.spec-pair').forEach(n=>{if(n.dataset.pair===pair.dataset.pair)n.classList.remove('is-match');});}
    const tok=e.target.closest('.spec-tok[data-symbol]');
    if(tok&&!gPopoverPinned){
      if(gPopoverTimer)clearTimeout(gPopoverTimer);
      gPopoverTimer=setTimeout(()=>hideSpecPopover(false),140);
    }
  };
  container.onfocusin=e=>{
    const tok=e.target.closest('.spec-tok[data-symbol]');
    if(tok)showSpecPopover(tok,tok.dataset.symbol,false);
  };
  container.onfocusout=e=>{
    if(!gPopoverPinned&&!e.relatedTarget?.closest?.('#spec-popover'))hideSpecPopover(false);
  };
  container.onclick=e=>{
    const tok=e.target.closest('.spec-tok[data-symbol]');
    if(!tok)return;
    e.stopPropagation();
    const sameOpen=gPopoverPinned&&!document.getElementById('spec-popover')?.hidden&&document.getElementById('spec-popover')?.querySelector('.spec-popover-head .spec-tok')?.textContent===lookupGlossarySymbol(tok.dataset.symbol,gSymbolGlossary)?.name;
    if(sameOpen)hideSpecPopover(true);
    else showSpecPopover(tok,tok.dataset.symbol,true);
  };
}
const specPopEl=document.getElementById('spec-popover');
if(specPopEl){
  specPopEl.onmouseenter=()=>{if(gPopoverTimer){clearTimeout(gPopoverTimer);gPopoverTimer=null;}};
  specPopEl.onmouseleave=()=>{if(!gPopoverPinned)hideSpecPopover(false);};
}
document.addEventListener('keydown',e=>{if(e.key==='Escape')hideSpecPopover(true);});
document.addEventListener('click',e=>{if(gPopoverPinned&&!e.target.closest?.('.spec-tok[data-symbol]')&&!e.target.closest?.('#spec-popover'))hideSpecPopover(true);});
window.addEventListener('scroll',()=>{if(!gPopoverPinned)hideSpecPopover(false);},{passive:true});

// Token-preserving formula presentation; never rewrite or evaluate source formulas.
function formatSpec(formula,glossary=gSymbolGlossary){
  const tokens=String(formula).match(/<->|->|<=|>=|!=|previous-input|pre-output|[0-9]+#[A-Fa-f0-9]+|[A-Za-z_][A-Za-z_0-9.]*(?:#[A-Za-z0-9_.]+)?|[0-9]+(?:\.[0-9]+)?|[^\s]/g)||[];
  const colors=['#fcd34d','#c4b5fd','#6ee7b7','#fda4af','#93c5fd','#fdba74'];
  let depth=0,serial=0,stack=[],parts=[];
  tokens.forEach(t=>{
    if(t==='('){const pair=serial++;stack.push(pair);parts.push(`<span class="spec-pair" data-pair="${pair}" style="color:${colors[depth%colors.length]}">(</span>`);depth++;}
    else if(t===')'){depth=Math.max(0,depth-1);const pair=stack.length?stack.pop():'unmatched';parts.push(`<span class="spec-pair" data-pair="${pair}" style="color:${colors[depth%colors.length]}">)</span>`);}
    else if(['->','<->','&','|'].includes(t))parts.push('\n'+'  '.repeat(Math.min(depth,8))+`<span class="spec-op">${esc(t)}</span> `);
    else if(/^(G|F|X|U|R|V|W|!)$/.test(t))parts.push(`<span class="spec-op">${esc(t)}</span>`);
    else{
      const meta=lookupGlossarySymbol(t,glossary);
      if(meta){
        parts.push(`<button type="button" class="spec-tok spec-tok--${esc(meta.category)}${meta.is_persistent?' is-persistent':''}" data-symbol="${esc(t)}">${esc(t)}</button>`);
      }else{
        parts.push(esc(t));
      }
    }
  });return parts.join(' ');
}
function renderGlossaryPanel(glossary){
  const entries=Object.values(glossary||{});
  const legendItems=SPEC_CAT_ORDER.map(cat=>{
    const label=gLang==='zh'?SPEC_CAT_TEXT[cat].zh:SPEC_CAT_TEXT[cat].en;
    const persistClass=(cat==='persistent_inout'||cat==='obs_history'||cat==='ghost_state')?' is-persistent':'';
    return `<span class="spec-tok spec-tok--${cat}${persistClass}">${esc(label)}</span>`;
  }).join('');
  const legendHtml=`<div class="spec-legend" aria-label="Symbol Highlight Legend"><strong>${tr('高亮图例（悬停或点击公式符号查看中文浮窗）：','Highlight Legend (hover/click tokens for Chinese popover):')}</strong>${legendItems}</div>`;
  if(!entries.length)return legendHtml;
  const orderMap={persistent_inout:0,obs_history:1,ghost_state:2,input:3,output:4,alias:5};
  const sorted=[...entries].sort((a,b)=>(orderMap[a.category]??9)-(orderMap[b.category]??9)||a.name.localeCompare(b.name));
  const persistentCount=sorted.filter(e=>e.is_persistent).length;
  const aliasCount=sorted.filter(e=>e.category==='alias').length;
  const rows=sorted.map(e=>`<tr><td><button type="button" class="spec-tok spec-tok--${esc(e.category)}${e.is_persistent?' is-persistent':''}" data-symbol="${esc(e.name)}">${esc(e.name)}</button></td><td>${esc(e.category_zh||e.category)}${e.is_persistent?` <span class="smv-pill smv-tone-amber">${tr('持久化/跨拍','Persistent')}</span>`:''}</td><td><strong>${esc(e.label_zh||e.name)}</strong><div class="spec-hint" style="margin-top:2px">${esc(e.definition_zh||'')}</div>${e.persistence_warning_zh?`<div class="spec-hint" style="color:var(--amber);margin-top:2px">${esc(e.persistence_warning_zh)}</div>`:''}</td></tr>`).join('');
  return `${legendHtml}<details class="spec-glossary-box"><summary>${tr(`查看全部接口变量、持久化状态 (${persistentCount}) 与规约别名 (${aliasCount}) 清单`,`Inspect interface pins, persistent states (${persistentCount}) & spec aliases (${aliasCount})`)}</summary><div class="review-table-wrap"><table class="data-table"><thead><tr><th>${tr('符号','Symbol')}</th><th>${tr('分类 / 持久性','Category / Persistence')}</th><th>${tr('中文定义与跨拍注意点','Chinese Definition & Persistence Notes')}</th></tr></thead><tbody>${rows}</tbody></table></div></details>`;
}
function specReviewGuide(task,smv){
  const variants=smv?.authored_variants||[];
  const defaultVariant=variants.includes('reference')?'reference':(variants[0]||'reference');
  const smvControls=variants.length?`<div style="display:flex;gap:8px;flex-wrap:wrap;margin:6px 0">${variants.map(v=>`<button type="button" class="btn btn-secondary" data-smv-run="${esc(v)}">${tr(`${smv?.required_tool||'SMV'}：检查 ${task.id} (${variantLabel(v)})`,`${smv?.required_tool||'SMV'}: Check ${task.id} (${variantLabel(v)})`)}</button>`).join('')}</div><p class="spec-hint">${tr('仅验证 models/ 中的显式 SMV 模型（EXPLICIT_SMV_MODEL_ONLY），不覆盖未编译候选 ST 代码；校验结果会写入 configs/smv_verification_status.json。','Checks explicit SMV models in models/ only (EXPLICIT_SMV_MODEL_ONLY); candidate ST is NOT verified. Results persist to configs/smv_verification_status.json.')}</p><pre id="reference-model-result" class="spec-source">${smv?.last_run_attempt?.status==='CHECKER_MISSING'?esc(JSON.stringify(smv.last_run_attempt,null,2)):''}</pre>`:`<p class="spec-hint">${tr('本题尚无可执行的SMV编码。','No executable SMV encoding is available for this task.')}</p>`;
  return `<details class="spec-help" open><summary>${tr('如何审核规约（组内整理，待人工确认）','How to review a specification (group-authored guidance)')}</summary><p>${tr('符号：G 始终；F 最终（无固定期限）；X 下一拍；! 非；& 同时满足；| 或；→ 如果…那么…；↔ 当且仅当；U 直到。同色括号是一对，悬停可定位；点击或悬停彩色变量/别名可查看中文定义与持久化警示。','Symbols: G always; F eventually (no fixed deadline); X next scan; ! not; & and; | or; → implies; ↔ iff; U until. Matching brackets share a color; hover/click highlighted symbols for Chinese definitions and persistence notes.')}</p><p>${tr('逐条核对：①在原题中找依据；②分开前提和结论，确认本拍/下拍；③检查边界、长按、乱序与优先级；④确认 IN_OUT、O[k-1] 与 Spre/q* 参考幽灵态未被候选内部私有变量混淆；⑤找到触发前提的测试，避免空泛通过。','For each property: find source support; separate premise and conclusion; check current/next-scan observations and boundaries; confirm IN_OUT, O[k-1], and Spre/q* ghost states are distinct from candidate internals; ensure tests activate premises.')}</p>${task.id==='PUB001'?`<p>${tr('PUB001：0空闲→1清洗→2灌装→3旋盖→4包装→5完成。phase是扫描前状态，输出在扫描后观测。P3中Pump_Motor是本拍输出，X(phase=1)是下拍开始阶段；确认全真仍只前进一步。','PUB001 phases: 0 idle → 1 clean → 2 fill → 3 cap → 4 pack → 5 complete. phase is pre-scan; outputs are post-scan. In P3, Pump_Motor is the current observed output and X(phase=1) is the next pre-state. All confirmations together still advance only one phase.')}</p>`:''}<p class="spec-hint">${tr('配色与符号高亮均保持原始公式一字不改；显示规约不等于完成候选 ST 形式证明。','Highlighting preserves source formulas verbatim; displaying properties does not prove candidate ST.')}</p>${smvControls}</details>`;
}
async function checkSmvModel(taskId,variant){
  const target=document.getElementById('reference-model-result');
  const liveBox=document.getElementById('overview-smv-live-status');
  const btns=[...document.querySelectorAll(`[data-smv-run]`)];
  btns.forEach(b=>b.disabled=true);
  if(target)target.textContent=tr(`正在检查 ${taskId} (${variant})…`,`Checking ${taskId} (${variant})…`);
  if(liveBox)liveBox.innerHTML=`<span class="smv-meta">${tr('执行中…','Running…')}</span>`;
  try{
    const resp=await fetch('/api/check-reference-model',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task_id:taskId,variant})});
    const payload=await resp.json();
    if(payload?.smv_status&&gCurrentTask?.task.id===taskId){
      gCurrentTask.smv_status=payload.smv_status;
      gTasks=gTasks.map(t=>t.id===taskId?{...t,smv_status:payload.smv_status}:t);
      renderTaskList(false);
      renderTaskOverview(gCurrentTask);
      bindSmvButtons(taskId);
    }
    if(target)target.textContent=JSON.stringify(payload,null,2);
    const afterLive=document.getElementById('overview-smv-live-status');
    if(afterLive){
      if(payload?.verification_status==='CHECKER_MISSING')afterLive.innerHTML=`<span class="smv-meta" style="color:var(--amber)">${tr('已持久化 CHECKER_MISSING 记录（HTTP 503）','Persisted CHECKER_MISSING attempt (HTTP 503)')}</span>`;
      else if(resp.ok)afterLive.innerHTML=`<span class="smv-meta" style="color:var(--green)">${tr(`已重验 ${variant} 并入库`, `Re-verified ${variant} and persisted`)}</span>`;
      else afterLive.innerHTML=`<span class="smv-meta" style="color:var(--red)">${esc(payload?.error||resp.statusText)}</span>`;
    }
  }catch(error){
    if(target)target.textContent=error.message;
  }finally{
    document.querySelectorAll(`[data-smv-run]`).forEach(b=>b.disabled=false);
  }
}
function checkReferenceModel(){
  if(!gCurrentTask)return;
  const variants=gCurrentTask.smv_status?.authored_variants||[];
  const variant=variants.includes('reference')?'reference':(variants[0]||'reference');
  return checkSmvModel(gCurrentTask.task.id,variant);
}
function bindSmvButtons(taskId){
  document.querySelectorAll('[data-smv-run]').forEach(btn=>{
    btn.onclick=()=>checkSmvModel(taskId,btn.dataset.smvRun);
  });
}
function renderTaskOverview(data){
  const task=data.task,review=currentReview(data);
  document.getElementById('task-overview').innerHTML=`<div class="overview-layout"><div class="overview-main"><p><span class="badge badge-pub">${esc(kind(task.kind))}</span> <span class="badge">${esc(difficulty(task.difficulty))}</span> <strong>${esc(task.id)} · ${esc(gLang==='zh'&&review?review.title_zh:task.title)}</strong></p><p>${data.tests.length} ${tr('固定用例','fixed cases')} · ${data.tests.reduce((n,c)=>n+c.steps.length,0)} ${tr('步','steps')} · ${task.ltl.length} ${tr('条属性','properties')}</p><p class="spec-hint">${tr('安全与错误优先级：详见补充约定及完整行为。','Safety and error priorities: see assumptions and the complete contract.')}</p></div>${renderOverviewSmvBox(task,data.smv_status)}</div>`;
}
function testName(test,review){return gLang==='zh'&&review?.tests_zh[test.id]?review.tests_zh[test.id].name:test.purpose||test.name||test.id;}
function renderTaskDetails(data){
  hideSpecPopover(true);
  const task=data.task,review=currentReview(data);
  gSymbolGlossary=data.symbol_glossary||{};
  renderTaskOverview(data);
  const pinsContainer=document.getElementById('interface-pins-container');
  pinsContainer.innerHTML=`<div class="review-table-wrap"><table class="data-table"><thead><tr>${[tr('变量名','Name'),tr('类型','Type'),tr('方向 / 持久性','Direction / Persistence'),tr('含义','Description')].map(v=>`<th>${v}</th>`).join('')}</tr></thead><tbody>${(task.interface||[]).map(p=>{
    const meta=gSymbolGlossary[p.name];
    const cat=meta?.category||(p.direction==='IN_OUT'?'persistent_inout':(p.direction==='OUTPUT'?'output':'input'));
    const isPersist=Boolean(meta?.is_persistent||p.direction==='IN_OUT');
    const dirZh=({INPUT:'输入 INPUT',OUTPUT:'输出 OUTPUT',IN_OUT:'输入/输出 IN_OUT（持久化存储）'})[p.direction]||p.direction;
    const dirLabel=gLang==='zh'?dirZh:(p.direction==='IN_OUT'?'IN_OUT (Persistent Storage)':p.direction);
    return `<tr><td><button type="button" class="spec-tok spec-tok--${esc(cat)}${isPersist?' is-persistent':''}" data-symbol="${esc(p.name)}">${esc(p.name)}</button></td><td><code>${esc(p.type)}</code></td><td>${esc(dirLabel)}${isPersist?` <span class="smv-pill smv-tone-amber">${tr('持久化','Persistent')}</span>`:''}</td><td>${esc(gLang==='zh'&&review?review.interface_zh[p.name]:p.description||p.comment||'')}</td></tr>`;
  }).join('')}</tbody></table></div>`;
  attachPopoverEvents(pinsContainer);
  const box=document.getElementById('ltl-container');
  const normalized=task.normalized_specification;
  const normalizationHtml=normalized?`<p class="spec-hint">${tr('规范化已完成；人工审核待确认。属性条数统计不代表候选 ST 已被形式证明。','Normalized definitions; human review pending. Property count does not mean candidate ST is proved.')} ${esc(normalized.candidate_formal_verification)}</p><details class="review-section"><summary>${tr('查看精确行为定义、辅助状态初值与历史绑定','Exact behavior, reference initialization and history bindings')}</summary><pre class="review-json">${esc(normalized.rules_zh)}</pre><pre class="review-json">${esc(JSON.stringify({observation:normalized.observation,initial_observed:normalized.initial_observed,reference_state_initial:normalized.reference_state_initial,history_bindings:normalized.history_bindings,auxiliary_state_bindings:normalized.auxiliary_state_bindings,finite_conjunctions:normalized.finite_conjunctions,comparison:normalized.comparison,constrained_fields:normalized.constrained_observed_fields,unconstrained_representation:normalized.unconstrained_representation_fields,transition:normalized.transition,limitations:normalized.limitations},null,2))}</pre></details>`:'';
  box.innerHTML=specReviewGuide(task,data.smv_status)+renderGlossaryPanel(gSymbolGlossary)+normalizationHtml+`<div class="review-table-wrap"><table class="data-table spec-table"><thead><tr><th>${tr('属性','Property')}</th><th>${tr('规约公式 · 括号配色与符号高亮','Formula · Bracket pairs & symbol highlights')}</th><th>${tr('中文含义与审核要点','Meaning & review notes')}</th></tr></thead><tbody>${task.ltl.map(p=>{
    const item=review?.properties_zh[p.id],matched=item?.formula===p.formula;
    const meaning=gLang==='zh'?(matched?item.description:tr('译文缺失或公式已变化，请重新审核。','Translation missing or stale.')):p.explanation||p.description||'';
    return `<tr><td>${esc(p.id)}</td><td><pre class="spec-formula">${formatSpec(p.formula,gSymbolGlossary)}</pre><details><summary>${tr('原始公式','Source formula')}</summary><code class="spec-source">${esc(p.formula)}</code></details></td><td>${esc(meaning)}<p class="spec-hint">${esc(gLang==='zh'&&matched?item.review:tr('','Check premise activation, history binding, boundaries and the complete contract.'))}</p><details><summary>${tr('原英文说明','Original description')}</summary>${esc(p.explanation||p.description||'')}</details></td></tr>`;
  }).join('')}</tbody></table></div>`;
  attachPopoverEvents(box);
  bindSmvButtons(task.id);
  const fixed=data.tests||[],random=data.random_cases||[];
  document.getElementById('tests-container').innerHTML=`<p>${tr('固定测试','Fixed tests')}: ${fixed.length} · ${tr('可生成随机差分用例','Available differential random cases')}: ${random.length}</p><table class="data-table"><thead><tr><th>${tr('用例编号','Case ID')}</th><th>${tr('类别','Kind')}</th><th>${tr('步数','Steps')}</th><th>${tr('场景说明','Scenario')}</th></tr></thead><tbody>${[...fixed,...random].map((t,i)=>`<tr><td>${esc(t.id)}</td><td>${i<fixed.length?tr('固定','Fixed'):tr('随机','Random')}</td><td>${t.steps.length}</td><td>${esc(i<fixed.length?testName(t,review):tr('随机差分输入序列','Random differential input sequence'))}</td></tr>`).join('')}</tbody></table><h3>${tr('固定测试 · 逐步输入与预期输出','Fixed tests · Inputs & expected outputs by step')}</h3><p class="spec-hint">${tr('从0编号；dt_ms为距上次调用时间。预期值供审核，不是实测输出。','Zero-based steps; dt_ms is time since the previous call. Expectations are for review, not observed outputs.')}</p>${fixed.map(t=>`<details class="review-section"><summary>${esc(t.id)} · ${esc(testName(t,review))} · ${t.steps.length} ${tr('步','steps')}</summary><div class="review-table-wrap"><table class="data-table"><thead><tr><th>${tr('步','Step')}</th><th>dt_ms</th><th>${tr('输入','Inputs')}</th><th>${tr('预期输出','Expected outputs')}</th></tr></thead><tbody>${t.steps.map((s,i)=>`<tr><td>${i}</td><td>${s.dt_ms==null?tr('未设置','Not set'):esc(s.dt_ms)}</td><td><pre class="review-json">${esc(JSON.stringify(s.inputs,null,2))}</pre></td><td><pre class="review-json">${esc(JSON.stringify(s.expected,null,2))}</pre></td></tr>`).join('')}</tbody></table></div></details>`).join('')}`;
}
function populateSandboxTemplate(data){
  const area=document.getElementById('st-source-code');if(area.value.trim())return;
  const lines=['FUNCTION_BLOCK FB_Task'];
  for(const [direction,label] of [['INPUT','VAR_INPUT'],['IN_OUT','VAR_IN_OUT'],['OUTPUT','VAR_OUTPUT']]){
    const pins=data.task.interface.filter(p=>p.direction===direction);if(!pins.length)continue;
    lines.push(label,...pins.map(p=>`    ${p.name} : ${p.type};`),'END_VAR');
  }
  lines.push('','(* Implementation *)','','END_FUNCTION_BLOCK');area.value=lines.join('\n');
}
function renderEvaluation(data){
  const c=data.compile||{},s=data.simulation||{};
  document.getElementById('sandbox-console').textContent=`${tr('编译结果','COMPILATION')}: ${c.status} (success=${c.success})\n${tr('诊断原文','Original diagnostics')}:\n${JSON.stringify(c.diagnostics||[],null,2)}\n\n${tr('仿真结果','SIMULATION')}: ${s.status}\n${tr('通过用例','Passed cases')}: ${s.passed_cases||0}/${s.evaluated_cases||0}\n${tr('失败信息','Failures')}:\n${JSON.stringify(s.failures||[],null,2)}\n${tr('证据目录','Evidence directory')}: ${data.evidence_workspace||''}`;
}
async function runSandboxEvaluate(){
  if(!gCurrentTask)return;
  const taskId=gCurrentTask.task.id;
  document.getElementById('sandbox-console').textContent=tr('正在编译并仿真…','Compiling and simulating…');
  try{
    const data=await api('/api/evaluate',{task_id:taskId,candidate:document.getElementById('st-source-code').value,include_random:document.getElementById('eval-include-random').checked});
    if(gCurrentTask?.task.id!==taskId)return;
    gLastEvaluation=data;gLastExport=null;gLastWaveformData=data.waveform||[];renderEvaluation(data);updateWaveformCaseSelector();switchTab('waveform');
  }catch(error){document.getElementById('sandbox-console').textContent=tr('评测失败：','Evaluation failed: ')+error.message;}
}
function waveStatus(w){return w.passed===true?tr('通过','PASS'):w.passed===false?tr('存在差异','DIVERGED'):tr('未验证','UNVERIFIED');}
function updateWaveformCaseSelector(){
  const select=document.getElementById('waveform-case-select'),old=select.value;
  select.innerHTML=gLastWaveformData.map((w,i)=>`<option value="${i}">${esc(w.case_id)} · ${waveStatus(w)} · ${w.steps.length} ${tr('步','steps')}</option>`).join('')||`<option value="">${tr('（暂无实测波形）','(No observed waveform data)')}</option>`;
  if([...select.options].some(o=>o.value===old))select.value=old;renderActiveWaveform();
}
function renderActiveWaveform(){
  const wave=gLastWaveformData[Number.parseInt(document.getElementById('waveform-case-select').value,10)],display=document.getElementById('waveform-display');
  if(!wave){display.textContent=tr('暂无实测波形，运行评测后查看。','No observed waveforms. Run an evaluation first.');return;}
  const steps=wave.steps||[];if(!steps.length){display.textContent=tr('没有步骤。','No steps.');return;}
  let html=`<p>${esc(wave.case_id)} · ${waveStatus(wave)}</p><div class="waveform-timeline" style="grid-template-columns:180px repeat(${steps.length},minmax(65px,1fr))"><div class="sig-label">${tr('信号 / 步','SIGNAL / STEP')}</div>${steps.map((s,i)=>`<div>#${i}${s.dt_ms==null?'':` +${s.dt_ms}ms`}</div>`).join('')}</div>`;
  for(const [field,label,keys] of [['inputs',tr('输入','IN'),Object.keys(steps[0].inputs||{})],['expected',tr('预期','EXP'),Object.keys(steps[0].expected||{})],['observed',tr('实测','OBS'),Object.keys(steps[0].expected||{})]]){
    keys.forEach(k=>{
      html+=`<div class="waveform-signal" style="grid-template-columns:180px repeat(${steps.length},minmax(65px,1fr))"><div class="sig-label" title="${esc(k)}">${label}: ${esc(k)}</div>`;
      steps.forEach(s=>{const value=s[field]?.[k],missing=value===undefined;const cls=missing?'unexecuted':field==='observed'&&s.divergence?.field===k?'mismatch':typeof value==='boolean'?(value?'true':'false'):'';html+=`<div class="sig-cell ${cls}">${missing?tr('未执行','unexecuted'):esc(typeof value==='object'?JSON.stringify(value):value)}</div>`;});
      html+='</div>';
    });
  }display.innerHTML=html;
}
function renderExport(data){document.getElementById('sandbox-console').textContent=`${tr('已导出验证材料（不等于形式验证通过）','Verification bundle exported (not a formal proof)')}\n${tr('目录','Directory')}: ${data.bundle_dir}\n${JSON.stringify(data.manifest,null,2)}\n\n${data.candidate_st||''}\n\n${data.spec_ltl||''}`;}
async function exportFormalVerify(){
  if(!gCurrentTask)return;
  try{const data=await api('/api/export-verify',{task_id:gCurrentTask.task.id,candidate:document.getElementById('st-source-code').value});gLastExport=data;gLastEvaluation=null;renderExport(data);}catch(error){document.getElementById('sandbox-console').textContent=tr('导出失败：','Export failed: ')+error.message;}
}
async function loadTraceDetails(){
  const target=document.getElementById('trace-summary');
  try{const data=await api('/api/experiments');target.textContent=tr('本地汇总记录（不代表下方流程图实时执行）：\n','Local summary records (the diagram below is not live execution):\n')+JSON.stringify(data.summaries?.pilot_pair_latest||data.campaign||{status:'NO_CAMPAIGN'},null,2);}catch(error){target.textContent=error.message;}
}
window.addEventListener('DOMContentLoaded',()=>{
  captureStaticText();applyStaticLanguage();
  document.getElementById('pilot-only').checked=params.get('scope')==='pilot';
  reloadTasks();
});
