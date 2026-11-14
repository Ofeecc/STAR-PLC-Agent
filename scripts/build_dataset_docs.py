"""Render deterministic human-readable dataset documentation, not experiment results."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2)

def table_escape(text):
    return str(text).replace('|', '\\|').replace('\n', '<br>')

def main():
    paths = sorted((ROOT/'dataset/public').glob('PUB*.json'))+sorted((ROOT/'dataset/self_built').glob('SELF*.json'))
    tasks = [json.loads(p.read_text(encoding='utf-8-sig')) for p in paths]
    catalog = ['# Dataset source specifications and test catalog',
        'This document is generated from the task JSON files. It records requirements, provenance, formal specifications and planned test expectations. It contains no actual CODESYS execution results.',
        'Regenerate after a deliberate dataset revision with `python scripts/build_dataset_docs.py`, then prepare a new campaign when the frozen hash has changed.',
        '| ID | Origin | Difficulty | Title | LTL properties | Cases | Scan observations |',
        '| --- | --- | --- | --- | ---: | ---: | ---: |']
    manual = ['# Fixed manual functional tests',
        'These are the complete planned input sequences and expected observations, not measured runtime outputs. Follow docs/functional_testing.md and preserve actual observations separately.',
        'Before each case, initialize a fresh FB instance and its caller storage. Before each step, apply all listed sampled inputs, invoke the generated FB exactly once at the prescribed timing, then observe outputs at the end of that call. Only listed expected outputs are constrained. Never copy an expected output into an actual trace without running the program.',
        'A `$binding` input object means the same caller-owned IN_OUT storage reference is retained; it is not a new data assignment per scan. Binding definitions and timing conventions appear in each task and the testing guide.']
    for t in tasks:
        catalog.append('| '+' | '.join(map(table_escape,[t['id'],t['kind'],t['difficulty'],t['title'],len(t['ltl']),len(t['tests']),sum(len(c['steps']) for c in t['tests'])]))+' |')
    for t in tasks:
        catalog.extend(['',f"## {t['id']} {t['title']}",'',f"Origin: {t['kind']}. Difficulty: {t['difficulty']}.",'','### Source and adaptation','', '```json',dump(t['provenance']),'```','','### Natural language source','',t['requirements'],'','### Scenario','',t['scenario'],'','### Normalized interface','', '| Direction | Name | Type | Description |','| --- | --- | --- | --- |'])
        for v in t['interface']:
            catalog.append('| '+' | '.join(table_escape(v[k]) for k in ('direction','name','type','description'))+' |')
        catalog.extend(['','### Initial conditions','','```json',dump(t['initial_conditions']),'```','','### Scan semantics','',t['scan_semantics'],'','### Safety and priorities',''])
        catalog.extend('- '+s for s in t['safety_priority'])
        catalog.extend(['','### Explicit assumptions',''])
        catalog.extend('- '+s for s in t['assumptions'])
        for key in ('data_types','supporting_types','test_bindings','portability'):
            if key in t:
                catalog.extend(['',f'### {key.replace("_"," ").capitalize()}','','```json',dump(t[key]),'```'])
        catalog.extend(['','### Atomic propositions and monitor predicates',''])
        catalog.extend(f"- `{name}`: {definition}" for name,definition in t['atomic_propositions'].items())
        catalog.extend(['','### LTL properties',''])
        if 'normalized_specification' in t:
            catalog.extend(['**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.','','### Normalized state, observation and predicate definitions','','```json',dump(t['normalized_specification']),'```',''])
        for p in t['ltl']:
            catalog.extend([f"**{p['id']}** {p.get('name','')}".rstrip(),'','```text',p['formula'],'```','',p['explanation'],''])
        catalog.extend(['### Fixed test index','', '| Case | Purpose | Steps |','| --- | --- | ---: |'])
        for c in t['tests']:
            catalog.append('| '+' | '.join(map(table_escape,[c['id'],c.get('purpose') or c.get('name', c['id']),len(c['steps'])]))+' |')
        catalog.extend(['','Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.'])
        manual.extend(['',f"## {t['id']} {t['title']}",'','Scan convention: '+t['scan_semantics'],'','Initial state:','','```json',dump(t['initial_conditions']),'```'])
        if 'test_bindings' in t:
            manual.extend(['','Caller bindings:','','```json',dump(t['test_bindings']),'```'])
        for c in t['tests']:
            manual.extend(['',f"### {c['id']} {c.get('name','')}".rstrip(),'',c.get('purpose') or c.get('name',''),''])
            for key,value in c.items():
                if key not in ('id','name','purpose','steps'):
                    manual.extend([f"{key}: {value if isinstance(value,str) else dump(value)}",''])
            for i,s in enumerate(c['steps']):
                manual.extend([f'**Step {i}**'+(f"; elapsed interval `{s['dt_ms']} ms`." if 'dt_ms' in s else '.'),'','```json',dump(s),'```',''])
    (ROOT/'dataset/specifications/catalog.md').write_text('\n'.join(catalog)+'\n',encoding='utf-8')
    (ROOT/'dataset/test_cases/manual_tests.md').write_text('\n'.join(manual)+'\n',encoding='utf-8')
    print(dump({'tasks':len(tasks),'cases':sum(len(t['tests']) for t in tasks),'steps':sum(len(c['steps']) for t in tasks for c in t['tests'])}))

if __name__=='__main__':
    main()
