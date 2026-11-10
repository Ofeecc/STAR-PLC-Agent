# Recalculated experiment results

Snapshot: 2026-10-27T11:52:38.761521+00:00. Campaign `campaign_2026-10-25T121252267365+0000`.

Agent-run coverage: all 128 planned runs were attempted.

All compilation rates use the fixed denominator of 32 tasks per condition, including transport failures. Functional rates use only actually evaluated CODESYS cases or tasks; their coverage is shown separately. Compilation is a syntax/type/build measurement, not proof of task correctness.

| Condition | Framework | Relay model ID | Agent attempted | First compile | Final compile | Compiler evaluated |
|---|---|---|---:|---:|---:|---:|
| E1 | smolagents | `deepseek-v4.1-flash` | 32/32 | 27/32 (84.38%) | 29/32 (90.62%) | 29/32 |
| E2 | smolagents | `kimi-k3.1-pro` | 32/32 | 27/32 (84.38%) | 27/32 (84.38%) | 28/32 |
| E3 | self_harness | `deepseek-v4.1-flash` | 32/32 | 26/32 (81.25%) | 26/32 (81.25%) | 26/32 |
| E4 | self_harness | `kimi-k3.1-pro` | 32/32 | 30/32 (93.75%) | 31/32 (96.88%) | 31/32 |

| Condition | Passed/evaluated cases | Case pass rate | Cases evaluated/planned | Passed/fully evaluated tasks | Task pass rate | Tasks evaluated/planned |
|---|---:|---:|---:|---:|---:|---:|
| E1 | 42/45 | 93.33% | 45/81 | 17/19 | 89.47% | 19/32 |
| E2 | 46/48 | 95.83% | 48/81 | 18/19 | 94.74% | 19/32 |
| E3 | 38/38 | 100.00% | 38/81 | 18/18 | 100.00% | 18/32 |
| E4 | 50/52 | 96.15% | 52/81 | 20/21 | 95.24% | 21/32 |

| Condition | Compiler calls | Repair successes/initial failures | Saved request attempts | Usage-reported calls | Observed input/output tokens | Mean/median agent time (s) |
|---|---:|---:|---:|---:|---:|---:|
| E1 | 31 | 2/2 | 65 | 62 | 369513/88844 | 41.6/34.4 |
| E2 | 28 | 0/1 | 77 | 73 | 458347/26742 | 50.0/50.9 |
| E3 | 26 | 0/0 | 32 | 26 | 89846/85898 | 47.9/41.8 |
| E4 | 32 | 1/1 | 33 | 32 | 127912/47125 | 70.0/49.3 |

## Interpretation and limits

- `agent_campaign_complete` means every planned task was attempted. It differs from `metrics.json`'s conservative `campaign_complete`, which requires a real compiler observation for every task; provider failures lower compiler coverage.
- Attempt counts come from each active run's `llm_*/request.json`. The self harness's stored `llm_calls` increments after a successful response, whereas the baseline counts attempts. The request-file derivation makes the count comparable without editing historical rows.
- Token totals are sums of observed provider usage records only. Every missing input/output/total usage field has a separate missing-call count. Unknown calls are not assigned zero. Complete token totals and API costs remain null when unreported; prices and upstream model identity are unverified.
- Mean/median times describe the original end-to-end agent runs, including compiler calls and failures. Later functional-test acquisition time is excluded. There is one repetition per task and condition; no statistical significance or causal superiority is claimed.
- The automatic simulator adapter supports 21/32 tasks, 52/81 cases and 359/576 scan observations. Remaining tasks require elapsed-time, composite or IN_OUT adapters. Eligibility alone is not execution evidence.
- A custom `VARIANT` DUT allowed E1/PUB018 to compile, but its caller interface differs from native generic storage. This remains a task-fidelity limitation, not a verified generic FIFO implementation.

E1 agent errors: `{"relay_incomplete_stream": 2, "tls_transport": 1}`. Functional outcomes: `{"NOT_RUN": 3, "PASS": 17, "TEST_FAIL": 2, "UNVERIFIED": 10}`.

E2 agent errors: `{"tls_transport": 4}`. Functional outcomes: `{"NOT_RUN": 5, "PASS": 18, "TEST_FAIL": 1, "UNVERIFIED": 8}`.

E3 agent errors: `{"relay_incomplete_stream": 6}`. Functional outcomes: `{"NOT_RUN": 6, "PASS": 18, "UNVERIFIED": 8}`.

E4 agent errors: `{"proxy_or_disconnected_transport": 1}`. Functional outcomes: `{"NOT_RUN": 1, "PASS": 20, "TEST_FAIL": 1, "UNVERIFIED": 10}`.
