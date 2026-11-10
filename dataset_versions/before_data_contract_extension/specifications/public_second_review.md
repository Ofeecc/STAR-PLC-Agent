# Public questions PUB011 to PUB020 review

The instructor JSON is the content authority. Every `requirements` value is copied verbatim from its `en` entry, and every FB parameter is copied from the official interface table. Task-specific interpretations are separate `assumptions`; they must accompany the prompts for both frameworks. Source statements are not rewritten to make the tasks easier. These test traces are expected values authored during dataset preparation. No trace is evidence of execution by CODESYS.

## Scan convention

Inputs are sampled at invocation and outputs are observed after that invocation. Retained state before scan k is q[k], and the call produces q[k+1]. Emergency/stop assertions therefore constrain the same observed scan. An automatic FSM accepts at most one phase transition per call. Newly entered phase outputs are decoded in that scan, but already-present completion of the new phase is not processed until another call. Single-step arm completion instead enters a wait with all commands off and requires a later fresh start edge.

Elapsed wall-clock timer age begins at zero on the first eligible invocation. `dt_ms` is the elapsed interval since the preceding call. The explicit `CycleTime` inputs in PUB012 represent the duration attributed to the current call, including a qualifying first call. These two timing mechanisms are deliberately distinguished. A human operating an online watch window cannot reproduce exact timer boundaries; use a controlled runtime clock or observations with recorded timing tolerances. Neither Python oracle checks nor compilation establish timer behavior.

## Review decisions and test scope

| Task | Main checks | Interpretation separated from source |
| --- | --- | --- |
| PUB011 three-station line | Manual forward/reverse conflict; ordered station waits; wrong buttons; completion removal | Both directions inhibited on manual conflict; mode change resets route; level confirmations accepted only in their station wait |
| PUB012 slab monitoring | Minimum 500 ms hold and invalid-signal override; six faults into five history entries; normal runtime gating | A valid fault after invalid input is a fresh occurrence; renewed faults restart holding; bounded tests do not specify UINT/LTIME overflow |
| PUB013 HVAC | Every mode/setback; energy-saving scope; 29.9/30 s boundary; interruption and full restart | Valid selectors 0..3 only, as required by the source; pre-call initialization and first normal calculation are separate |
| PUB014 IPv4 | Byte ordering; inclusive octet bounds; malformed fields, signs, whitespace, nondigits, overflow; stale-output clearing | Decimal leading zeros accepted; embedded NUL is constrained by PLC STRING representation |
| PUB015 proportioning | Edge toggles; held button; two/three-material branches; threshold equalities; emergency cancellation | Valve D remains open because no drain-complete input exists; a reset/new request is required after emergency; mode changes clear old sequence |
| PUB016 flexible route | Bidirectional [4,2,5]; one-entry [5]; repeated [2,2,5]; wrong completion | A repeated station requires a fresh completion edge; no movement between repeated same-station entries; input contract held fixed throughout a product |
| PUB017 recipes | Add/query/modify/delete/reuse; all five errors; ten-slot capacity; duplicate-before-full priority | Requests are edges; success flags are one-call pulses; invocation error clears on idle; query result retains last successful record |
| PUB018 generic FIFO | Wraparound, full/empty rejection, held requests, reset priority; DINT and BOOL bindings with different lower bounds | Reset updates edge memories; no simultaneous enqueue/dequeue is supplied; generic VARIANT portability remains unverified |
| PUB019 arm | Manual matching limits and conflicts; confirmed single steps; eight-action single cycle; continuous wrap; emergency recovery | Mode/no-mode resets; automatic sequence starts only from top-left; action completion has one transition per scan; emergency cancellation requires new verified starting pose |
| PUB020 five-station line | Manual conflict; weights 100, 150, 200; rejection at 99.9/200.1; full route; wrong feedback | Kick remains active until rejected material leaves weighing; setpoint retained unless a valid weight is accepted; mode change resets route |

The task source does not define every conflict, edge convention, restart rule or retained-output policy. The above choices make the benchmark executable, but they require disclosure and are not claimed as instructor-confirmed interpretations. Alternative legal interpretations should be reviewed before any scoring rule is changed; both frameworks must receive the same frozen convention.

## Composite values and persistent caller bindings

PUB017 supplies the official `ST_Recipe` DUT definition through `supporting_types`. The `recipe` array is initialized once before each test, then retained across steps. A step input object of the form `{"$binding":"recipe","binding_id":"default","retain_storage":true}` denotes the same caller reference, not a new zero array. Never assign the initial database before every call. The test procedure inspects record data through the query output and checks additional database mutations as specified in each test's notes. A deleted record's non-ID fields are unconstrained.

PUB018 retains the official VARIANT declaration. Binding A is `item:DINT`, `buffer:ARRAY[0..1] OF DINT`; binding B is `item:BOOL`, `buffer:ARRAY[1..3] OF BOOL`. `$binding` for `buffer` denotes fixed caller storage, retained across every test step. `item` is a writable scalar whose sampled value is supplied for the call, and a successful dequeue modifies it. Both bindings must run before genericity can be claimed. A DINT-only implementation or an interface adapter must be reported as a deviation, not silently counted as solving the unchanged public task. Availability of a suitable native VARIANT representation/reflection library in the installed CODESYS profile remains a concrete engineering question.

## LTL interpretation

Atomic propositions explicitly define observations, pre-state predicates, arithmetic relations and fairness assumptions. The formulas constrain these propositions using ordinary propositional logic and temporal operators. A predicate such as `ordered` names the stated transition relation; it is not an unexplained Boolean variable. Stateful predicates referencing pre-state or prior input require monitor memory. Timed predicates such as `mature` and `hold` need a clock in addition to the Boolean LTL monitor. Conditional liveness assumes advancing calls/time and eventual external feedback; it is not an unconditional promise that sensors will activate.

Finite traces cover selected safety and transition cases. They do not prove unbounded liveness, all numeric values, all active sequence lengths, all mode transitions, generic queue type support, or all possible combinations of mechanical feedback. No automated model checker has been run for these properties.

## Deterministic validation

`scripts/build_public_second.py` regenerates the ten files. The repository dataset validator checks nonempty LTL/tests, unique case-insensitive interface identifiers, complete sampled inputs/reference bindings and declared expected outputs. A separate source comparison verifies that all twenty public requirements remain verbatim. Logical review above is a documented engineering review, not formal verification and not PLC runtime evidence.
