# SAFE-FAST Day 48 Positive-Trade Capture and Miss Analysis — Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_RESULT.md`
2. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
3. `SAFE_FAST_DAY48_ACTUAL_GROUPED_THREE_FAMILY_REPLAY_TEST_RESULT.md`
4. `SAFE_FAST_DAY48_GROUPED_THREE_FAMILY_COVERAGE_EXPANSION_RESULT.md`
5. `SAFE_FAST_DAY48_CONTINUATION_STARTER_COVERAGE_RESULT.md`
6. `SAFE_FAST_DAY48_GROUPED_THREE_FAMILY_EXPANSION_AFTER_CONTINUATION_STARTER_RESULT.md`
7. `SAFE_FAST_DAY48_CONTINUATION_QQQ_SPY_OPTION_CONTEXT_EVIDENCE_PACKAGE_RESULT.md`
8. `SAFE_FAST_DAY48_CONTINUATION_QQQ_SPY_EXACT_SELECTED_REQUEST_COST_CHECK_RESULT.md`
9. `SAFE_FAST_PROJECT_DASHBOARD.md`
10. `SAFE_FAST_PROJECT_RULE_INDEX.md`
11. Existing Ideal, Clean Fast Break, and Continuation runners, calculators,
    fixtures, candidate packets, manifests, and regression tests
12. The canonical future-chat startup and handoff files identified by the rule
    index

Expected branch: `main`
Expected starting commit: `6b90016`
Expected status: clean except this task file

If local git, build state, dashboard, rule index, or current handoff disagree,
stop and identify the exact conflict.

This is actual SAFE-FAST build testing and measurement.

It is not live trade evaluation.

Do not replace this task with another governance-only document.

## Active build objective

Develop SAFE-FAST equally for:

1. strict rejection of unsafe or invalid trades; and
2. reliable capture of legitimate trades.

Correct no-trade behavior alone is not sufficient.

Do not weaken safety rules merely to create more trades.

Use existing local data and fixtures first.

Do not download data during this task.

## Required chronological trade funnel

Every runnable candidate must be traced through this exact sequence:

1. `SETUP_DEVELOPING`
2. `SETUP_QUALIFIED`
3. `TRADE_CANDIDATE`
4. `CONTRACT_SELECTED`
5. `PRICE_ACCEPTABLE`
6. `ENTRY_ELIGIBLE`
7. `ENTRY_RECORDED`
8. `EXIT_EVALUATED`
9. `FINAL_OUTCOME`

For every candidate, record:

- candidate identifier;
- setup family;
- underlying;
- direction;
- signal timestamp and timezone;
- evidence source;
- chronological stage path;
- highest stage reached;
- first stage not reached;
- exact blocker code;
- exact contemporaneous evidence supporting the blocker;
- whether the blocker is caused by:
  - a real frozen-rule failure;
  - missing data;
  - contradictory evidence;
  - replay or harness failure;
- contract-selection result;
- execution result;
- context and caution result;
- winner-selection result;
- entry result;
- exit result;
- final classification;
- first-run output;
- second-run output;
- deterministic or unstable result.

Use only information available at each decision timestamp.

Do not use future bars, later quotes, later classifications, exit results, or
profit outcomes to make an earlier decision.

An accepted-entry-stage row is not an executed trade.

A possible contract is not a selected contract.

A quote found somewhere in a file is not proof that it was usable at signal
time.

## Mandatory final classifications

Every candidate must finish in exactly one category:

### `VALID_TRADE_CAPTURED`

SAFE-FAST recognized the setup, selected a valid contract, passed the frozen
execution and safety rules, and recorded the entry using complete
contemporaneous evidence.

A captured trade may later win or lose.

A losing valid trade remains a valid captured trade.

### `TRUE_NO_TRADE`

Complete contemporaneous evidence proves that at least one frozen setup,
contract, execution, context, caution, portfolio, or risk rule failed.

### `MISSING_DATA`

The candidate may or may not have been tradable, but required historical
evidence is absent, incomplete, late, stale, or unavailable.

Never report missing evidence as a true no-trade.

### `MISSED_VALID_TRADE`

Complete contemporaneous evidence proves that the candidate should have passed
the frozen rules, but SAFE-FAST failed to recognize, select, approve, or record
it.

This is the primary false-negative category.

### `INVALID_TRADE_ALLOWED`

SAFE-FAST approved a trade that complete contemporaneous evidence proves should
have been rejected.

This is the primary false-positive category and must block promotion.

### `UNRESOLVED`

Evidence is contradictory, a frozen rule cannot be executed safely, or no
defensible classification is currently possible.

Do not hide unresolved cases inside no-trade totals.

## Grouped candidate inventory

Inventory every existing development candidate across:

- Ideal;
- Clean Fast Break;
- Continuation.

Include every candidate that reached at least `TRADE_CANDIDATE`, plus all
existing rejection and boundary controls needed to protect safety behavior.

The grouped development batch must include, where locally available:

- known valid entries;
- valid winning trades;
- valid losing trades;
- true no-trade controls;
- stale-quote controls;
- quote-after-signal controls;
- excessive-spread controls;
- missing-data cases;
- ambiguous and boundary cases;
- contract-selection blockers;
- price and execution blockers;
- context and caution blockers;
- developing-stage transition cases;
- session-boundary cases;
- winner-selection and tie-breaking cases.

Verify the existing committed Clean Fast Break winner and rejection controls
against the current canonical evidence rather than relying on stale prose.

Do not cherry-pick only profitable examples.

Do not remove losing or unfavorable cases after inspecting outcomes.

Do not use protected holdout evidence for development or repair.

Run all runnable cases in one grouped batch whenever their dependencies permit.

Run the complete grouped batch twice and require deterministic equality.

## Positive labels

A candidate may be labeled as a known valid entry only when complete
chronological evidence proves that it met the canonical frozen rules.

The label must be independent of whether the trade later won or lost.

Maintain separate evidence sets for:

- development and repair;
- regression controls;
- protected holdout evaluation.

Any rule change after protected holdout evidence is viewed invalidates the
affected holdout result.

## Required scorecards

Produce separate scorecards for:

1. Ideal;
2. Clean Fast Break;
3. Continuation;
4. the combined plan.

Each scorecard must report:

- candidates found;
- candidates runnable;
- setup-developing count;
- setup-qualified count;
- trade-candidate count;
- contracts selected;
- prices accepted;
- entries eligible;
- entries recorded;
- exits evaluated;
- valid trades captured;
- true no-trades;
- missing-data cases;
- missed valid trades;
- invalid trades allowed;
- unresolved cases;
- winners;
- losers;
- deterministic cases;
- unstable cases;
- first-blocker totals by funnel stage;
- conversion rate between every consecutive funnel stage.

Show progress against the canonical per-family evidence contract currently
defined in `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`, including the existing
minimums for accepted entries, no-trade controls, boundary cases, winners,
losers, and holdout evidence.

Do not use success at an earlier funnel stage to disguise failure at a later
stage.

## Owner-facing plain-English summary

Every result, dashboard update, and future-chat handoff must directly answer:

1. Did SAFE-FAST recognize the setup before the move?
2. Did it classify the setup as a possible trade?
3. Was a tradable option available at that exact time?
4. Was rejection caused by a real safety rule or by missing evidence?
5. How many valid trades were caught, missed, or incorrectly allowed?

Answer these in plain English.

Do not make the user reconstruct them from technical output.

## First-blocker analysis

Group candidates by the first funnel stage they failed to pass.

For each blocker group, report:

- affected setup families;
- affected candidate count;
- exact common cause;
- whether the cause is:
  - correct safety behavior;
  - missing evidence;
  - frozen-rule defect;
  - replay or test-harness defect;
- whether local evidence can resolve it;
- whether external data is required;
- the smallest safe next action.

This task must reveal whether SAFE-FAST is failing primarily at:

- setup recognition;
- candidate qualification;
- option-contract selection;
- price and spread validation;
- entry eligibility;
- entry recording;
- exit evaluation.

## Repair workflow

When a valid trade is missed:

1. identify the first failed funnel stage;
2. group every candidate sharing that failure;
3. diagnose the common cause;
4. make no trading-rule change inside this task unless the current task and
   frozen-baseline rules explicitly authorize it;
5. create one bounded evidence-backed grouped repair task;
6. require the repair task to rerun affected positive cases;
7. require it to rerun all related no-trade controls;
8. require it to rerun the full three-family regression suite;
9. require before-and-after funnel scorecards.

Do not loosen a threshold merely to create entries.

Do not patch one favorable example in isolation.

No repair may be accepted if it increases unsafe false positives without a
specific evidence-backed project decision.

Replay and scorecard harness changes are allowed when they only expose existing
frozen behavior.

## Missing-data workflow

Use existing local evidence first, including ignored raw-data directories.

For every candidate blocked by missing option or context evidence:

1. identify the exact missing setup-time field;
2. identify the exact rule decision that field would resolve;
3. create the smallest grouped request shape;
4. keep setup-time and conditional exit-path evidence separate;
5. do not request exit evidence until a valid entry exists;
6. perform an exact cost check in a later task;
7. explain the exact price and decision value;
8. obtain user approval before download.

Do not treat a missing Databento key as evidence that the market data does not
exist.

Do not create broad speculative data requests.

## Profit-and-loss handling

Do not calculate strategy performance for candidates without a valid recorded
entry.

For valid entries, use the canonical conservative execution rules covering:

- bid and ask;
- spread;
- quote age;
- signal-to-order delay;
- slippage;
- displayed size;
- partial fills;
- target and stop ordering;
- same-interval ambiguity;
- fees and costs.

Report valid winners and valid losers.

Do not hide losing valid trades.

Do not claim profitability from one example or from incomplete entry evidence.

## Required machine-readable output

Create:

`historical_signal_replay/results/day48_positive_trade_capture_funnel.json`

Create the directory when necessary.

The JSON must contain:

- frozen engine or rule version;
- source commit;
- run timestamp;
- candidate records;
- funnel stages;
- first blockers;
- final classifications;
- family scorecards;
- combined scorecard;
- first-run hash;
- second-run hash;
- deterministic comparison;
- unresolved evidence requirements.

Add a focused validator for this output.

## Required result document

Create:

`SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`

The result document must include:

- the four scorecards;
- the candidate-level funnel table;
- first-blocker analysis;
- caught, missed, invalidly allowed, missing-data, unresolved, winning, and
  losing totals;
- progress against the canonical sample contract;
- the five owner questions and answers;
- exact evidence-backed next action.

Do not claim proof, profitability, readiness, promotion, paper eligibility, or
live eligibility unless the existing canonical promotion gates are actually
met.

## Future-chat handoff implementation

Locate the canonical current startup and handoff files through
`SAFE_FAST_PROJECT_RULE_INDEX.md`.

At minimum, update:

- `SAFE_FAST_BUILD_STATE.md`;
- `SAFE_FAST_PROJECT_DASHBOARD.md`;
- `SAFE_FAST_PROJECT_RULE_INDEX.md`;
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`;
- the current canonical next-chat handoff and start file named by the rule
  index.

Do not duplicate the entire project plan across every file.

`SAFE_FAST_BUILD_STATE.md` remains the current-state authority.

The future-chat entry point must explicitly require the next chat to:

- read `SAFE_FAST_BUILD_STATE.md` first;
- verify local branch, commit, and status;
- continue the exact active task;
- treat positive-trade capture and no-trade safety as co-equal objectives;
- use grouped batches;
- require the funnel scorecard;
- distinguish true no-trades, missing data, missed valid trades, invalid trades
  allowed, and unresolved cases;
- avoid restarting completed discovery;
- avoid replacing runnable testing with governance-only documents;
- avoid making the user repeat project state;
- preserve cost checks and download approval requirements;
- explain current results and next action in plain English.

Add or update an automated consistency test that fails when:

- build state and handoff identify different active tasks;
- a stale commit is presented as current;
- positive-trade capture disappears from the completion plan;
- the current handoff does not point to build state;
- control files disagree about what is fixed, blocked, unproven, or next;
- the funnel scorecard is missing from future grouped test requirements.

Future-chat continuity is an acceptance gate.

## Required tests

Run:

1. direct `scripts/safe_fast_run_safe_checks.ps1`;
2. the existing execution-policy bypass when direct execution is blocked;
3. all Ideal replay tests;
4. all Clean Fast Break replay tests;
5. all Continuation replay tests;
6. Day 48 grouped three-family replay tests;
7. developing-stage transition tests;
8. session-boundary tests;
9. contract-selection tests;
10. execution-realism tests;
11. context and caution tests;
12. stable winner-selection tests;
13. positive-trade funnel validator tests;
14. true-no-trade versus missing-data classification tests;
15. missed-valid-trade detection tests;
16. invalid-trade-allowed detection tests;
17. family and combined scorecard tests;
18. repeated grouped batch twice;
19. handoff and control-file consistency tests;
20. evidence content validator;
21. package-to-intake bridge;
22. `git diff --check`.

Remove generated `__pycache__` directories before final status.

Do not commit or push.

## Exact next-task routing

Create or reuse exactly one next grouped task based on actual evidence:

- grouped repair task when valid trades are proven missed;
- grouped safety repair task when invalid trades are allowed;
- grouped positive-entry expansion when the funnel works but valid-entry
  coverage is thin;
- grouped exact missing-data cost check only when unavailable evidence is the
  proven blocker.

Do not create another general governance-only task.

## Final Codex summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Ideal funnel totals
- Clean Fast Break funnel totals
- Continuation funnel totals
- Combined funnel totals
- Valid trades captured
- True no-trades
- Missing-data cases
- Missed valid trades
- Invalid trades allowed
- Unresolved cases
- Winners
- Losers
- First blockers by stage
- Five owner questions and answers
- Future-chat handoff files updated
- Exact next grouped task filename