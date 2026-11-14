"""Summarize actual six-task evidence, never infer unexecuted stages as passed."""
import csv
import json
from collections import Counter

from plc_agent.common import ROOT, now, read_json, write_json

base = ROOT/'results/raw/six_task_fullflow_20261114'
summary = read_json(base/'summary.json')
rows = summary['results']
totals = {key: sum(int(u.get(key) or 0) for r in rows for u in r['usage'])
          for key in ('input_tokens', 'output_tokens', 'total_tokens')}
summary.update({'compiled_tasks': sum(r['compiled'] for r in rows),
                'fixed_passed_cases': sum(r['functional'].get('passed_cases', 0) for r in rows),
                'fixed_evaluated_cases': sum(r['functional'].get('evaluated_cases', 0) for r in rows),
                'fixed_passed_tasks': sum(r['functional']['status'] == 'PASS' for r in rows),
                'formal_status_counts': dict(Counter(r['verification']['status'] for r in rows)),
                'stage_checks_passed_tasks': sum(bool(r.get('stage_checks_passed')) for r in rows),
                'complete_passed_tasks': sum(r['status'] == 'PASS' for r in rows),
                'llm_calls': sum(r['llm_calls'] for r in rows), 'reported_tokens': totals,
                'report_generated_utc': now()})
write_json(base/'summary.json', summary)
write_json(ROOT/'results/summary/six_task_fullflow_latest.json', summary)
lines = ['# DeepSeek 六题完整流程实测（2026-11-14）', '',
         '模型：`deepseek-v4.1-flash-1017`；框架：STAR/E3；high 思考强度。', '',
         '每题重新生成 ST；最终固定测试与最终形式验证使用同一候选源代码哈希。Agent 自测不是最终固定测试。', '',
         '| 题目 | 难度 | 编译 | 固定用例：通过/已测/计划 | 形式验证 | 完整流程 |',
         '|---|---|---|---|---|---|']
table = []
for r in rows:
    f, v = r['functional'], r['verification']
    row = {'task': r['task_id'], 'difficulty': r['difficulty'], 'compiled': r['compiled'],
           'passed_cases': f.get('passed_cases', 0), 'evaluated_cases': f.get('evaluated_cases', 0),
           'planned_cases': r['planned_cases'], 'formal_status': v['status'], 'fullflow_status': r['status']}
    table.append(row)
    lines.append(f'| {row["task"]} | {row["difficulty"]} | {"PASS" if r["compiled"] else r["generation_status"]} | {row["passed_cases"]}/{row["evaluated_cases"]}/{row["planned_cases"]} | {v["status"]} | {r["status"]} |')
lines += ['', f'完成执行 {len(rows)}/6 题；编译通过 {summary["compiled_tasks"]}/6；固定用例通过 {summary["fixed_passed_cases"]}/50，已执行 {summary["fixed_evaluated_cases"]}/50。',
          '', f'固定测试和已转换性质检查同时通过 {summary["stage_checks_passed_tasks"]}/6；形成完整题库规约证明 {summary["complete_passed_tasks"]}/6。尚未证明不等同于代码错误。',
          '', f'模型请求 {summary["llm_calls"]} 次；提供商返回 token 统计：{json.dumps(totals, ensure_ascii=False)}。',
          '', '只统计本轮六题，修复预检和原批次不计入成绩。PARTIAL/UNSUPPORTED_ST/INCONCLUSIVE/TIMEOUT/TOOL_ERROR 不视为正确或错误程序的证明。', '']
for r in rows:
    tid = r['task_id']; v = r['verification']; f = r['functional']
    lines += [f'## {tid}', '', f'- 生成阶段：{r["generation_status"]}；{r.get("generation_reason")}',
              f'- 固定测试：{f["status"]}；{f.get("reason") or f.get("infrastructure_error") or "详见轨迹"}',
              f'- 形式验证：{v["status"]}；{v.get("reason") or "详见性质结果"}',
              f'- 转换后检查项：通过 {v.get("passed_properties", 0)}/{v.get("total_properties", 0)}（包含辅助检查项，不等同原题库性质条数）。',
              f'- 完整规约覆盖：{v.get("specification_coverage", {}).get("status", "NOT_EVALUATED")}；建模语义：{v.get("modeling_scope", "NOT_EVALUATED")}。',
              f'- 尚未证明或未完成对应的题库性质 ID：`{v.get("specification_coverage", {}).get("unproven_or_unmapped_ids", [])}`。',
              f'- 证据目录：`results/raw/six_task_fullflow_20261114/{tid}/`', '']
(ROOT/'results/summary/six_task_fullflow_20261114.md').write_text('\n'.join(lines), encoding='utf-8')
with (ROOT/'results/summary/six_task_fullflow_20261114.csv').open('w', encoding='utf-8-sig', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(table[0]))
    writer.writeheader(); writer.writerows(table)
print(json.dumps({k: summary[k] for k in ('completed_tasks', 'compiled_tasks', 'fixed_passed_cases', 'fixed_evaluated_cases', 'formal_status_counts', 'llm_calls', 'reported_tokens')}, ensure_ascii=False))
