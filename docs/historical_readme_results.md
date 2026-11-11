# 历史README结果（未复核）

以下为继承材料，不作为STAR v2或当前题库实测结论。

## Current Evidence & Campaign Outcomes

Use the timestamped records in `results/summary/` as the authority. Real CODESYS preflight produced 0, 2 and 0 compiler errors for valid, deliberately invalid and repaired programs. Both selected models have generated and compiled code across all conditions:

| Condition | Framework | Model ID | First compilation | Final compilation | Actual cases passed/evaluated | Case coverage |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| E1 | smolagents 1.26.0 ToolCallingAgent | deepseek-v4.1-flash | 27/32 | 29/32 | 42/45 | 45/81 |
| E2 | smolagents 1.26.0 ToolCallingAgent | kimi-k3.1-pro | 27/32 | 27/32 | 46/48 | 48/81 |
| E3 | STAR v2 harness | deepseek-v4.1-flash | 26/32 | 26/32 | 38/38 | 38/81 |
| E4 | STAR v2 harness | kimi-k3.1-pro | 30/32 | 31/32 | 50/52 | 52/81 |

Full analysis is available in [results/analysis/summary.md](results/analysis/summary.md). Final artifacts include the [English report](report/report.pdf), [editable slide deck](presentation/slides.pptx), [speaker notes](presentation/speaker_notes.md), [defense Q&A](presentation/defense_qa.md), and [explanation video](video/explanation.mp4).
