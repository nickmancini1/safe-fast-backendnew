# SAFE-FAST Existing-Setup Option Evidence and End-to-End Backtest

Read `SAFE_FAST_BUILD_STATE.md` first.

The local repository is the only source of truth.

Use bounded reads and targeted searches. Do not begin with a broad repository scan.

## Proven starting point

The accepted March 16, 2026 SPY replay now has:

- one 751-row session;
- three setup-qualified family labels;
- one selected economic winner;
- two duplicate/suppressed labels;
- accepted trigger: `668.360000000`;
- accepted invalidation: `667.870000000`;
- shared accepted setup timestamp: `2026-03-16T13:30:00Z`;
- profitability proof: `NO`;
- paper/live eligibility: `NO`.

Ideal, Clean Fast Break, and Continuation intentionally share the accepted setup-time row. Do not create three economic trades from one duplicate group.

## Immediate objective

Move the selected existing setup through:

1. deterministic option-contract selection;
2. complete allowed option-entry-price window;
3. valid entry;
4. exit replay;
5. spread, slippage, commissions, and fees;
6. net profit/loss.

Do not return to broad candidate hunting.

Do not create another provisional recognition layer.

Do not stop with another planning-only document.

## Required reads

Read these first:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
3. `SAFE_FAST_PROJECT_DASHBOARD.md`
4. `SAFE_FAST_PROJECT_RULE_INDEX.md`
5. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
6. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
7. `SAFE_FAST_DAY52_FAMILY_NUMERIC_BINDING_AND_PROMOTION_RESULT.md`
8. `historical_signal_replay/results/day52_family_numeric_binding_and_promotion.json`
9. existing option-selection, option-evidence, entry-timing, execution-cost, and exit-replay files directly referenced by those documents.

## First required decision

Confirm:

- selected winner ID;
- setup family used for the economic winner;
- direction;
- trigger timestamp;
- selected-contract rule;
- exact option-entry timing rule already present in the repo.

Record the existing timing rule exactly:

- earliest allowed option price;
- latest allowed option price;
- whether the rule uses quote, trade, midpoint, ask, or another field;
- maximum quote age;
- spread/liquidity requirements;
- exact rejection reasons.

Do not loosen or replace the existing rule to make a price fit.

## Contract selection

Use only existing frozen contract-selection rules.

Record:

- expiration;
- strike;
- call or put;
- vendor symbol;
- selection inputs available by the cutoff;
- liquidity checks;
- deterministic tie-break;
- exact rejection reason if no contract qualifies.

Do not select a contract using future price performance.

Do not substitute a different contract merely because its data is easier to obtain.

## Complete option-price window

The prior problem was incomplete or mistimed option-price evidence.

For the selected contract, inspect or request the entire interval required by the accepted timing rule.

Do not request another tiny slice.

Include enough pre-window context to establish quote state when technically required, but do not use a pre-trigger quote as an entry unless the accepted rule explicitly permits it.

Record every relevant update:

- event timestamp;
- receive timestamp where available;
- bid;
- ask;
- midpoint;
- trade price;
- quote age;
- spread;
- source;
- first valid price;
- rejection reason for every invalid price.

A missing update at the exact trigger second does not automatically mean no valid price exists. Apply the accepted freshness and as-of rules to the complete stream.

## Data-source order

Use this order:

### 1. Existing local evidence

Search local cached results, fixtures, downloaded evidence, and prior responses first.

### 2. tastytrade

Use the existing local tastytrade path next.

Use only fields actually returned by tastytrade.

Do not claim that tastytrade supplied historical bid/ask evidence unless the payload proves it.

If tastytrade returns candles only, record that limitation and decide whether the accepted entry-price rule permits those fields.

### 3. Databento

Use Databento as the fallback for exact historical OPRA evidence.

Use:

- exact selected symbol;
- exact dataset;
- exact schema;
- complete entry window;
- complete exit window;
- definition evidence when required;
- consolidated bid/ask evidence when required;
- trades or statistics only when the accepted rule requires them.

Run a cost estimate before downloading.

Do not purchase or download nonzero-cost data without explicit operator approval.

### 4. Schwab

Schwab is not required for this historical backtest.

Do not wait for Schwab.

Do not perform OAuth, account, position, order, fill, or broker work.

## Network and credentials

Do not edit `.env`, credentials, tokens, or secret files.

Do not print secret values.

Use existing environment variables when present.

If Codex cannot reach tastytrade or Databento because of its sandbox, proxy, or network:

- report `NETWORK_EXECUTION_BLOCKED`;
- do not report market data as `NOT_AVAILABLE`;
- create one exact operator-run script;
- make the script read credentials from environment variables;
- state the exact command to run;
- state the exact output file expected;
- continue all offline implementation and tests.

## Source separation

Do not confuse raw evidence with SAFE-FAST decisions.

Databento and tastytrade may provide raw market evidence such as:

- underlying bars;
- option definitions;
- quotes;
- trades;
- statistics.

Separate named sources provide macro events and headlines.

SAFE-FAST calculates:

- setup family;
- trigger;
- invalidation;
- freshness;
- caution/blocker state;
- stage transitions;
- duplicate suppression;
- winner selection;
- trade/no-trade decision.

Every calculated field must state:

- raw source;
- raw fields;
- calculation rule;
- information cutoff;
- missing-data behavior.

## Entry, exit, and P&L

For every executable economic winner, report:

- setup family;
- signal time;
- trigger time;
- contract;
- accepted entry window;
- entry timestamp;
- entry price;
- price basis;
- quote age;
- spread;
- invalidation;
- exit timestamp;
- exit price;
- exit reason;
- holding duration;
- gross P&L;
- spread cost;
- slippage;
- commissions;
- fees;
- net P&L.

Use existing frozen exit and cost rules.

Do not invent cost or exit assumptions.

If evidence is missing, stop at the exact stage and identify the smallest missing evidence.

## Required outcome

The result must be one of:

### Executable result

The selected winner reaches:

- selected contract;
- eligible entry;
- recorded entry;
- costed exit;
- net P&L.

### Exact evidence request

If raw evidence blocks completion, produce one grouped request with:

- selected contract;
- dataset;
- schemas;
- symbols;
- entry window;
- exit window;
- numerical cost;
- exact stages unlocked.

`NOT_AVAILABLE` is not acceptable when the vendor API was never successfully reached.

## Tests

Add focused tests for:

- deterministic contract selection;
- complete entry-window coverage;
- pre-trigger price rejection;
- first valid post-trigger price;
- late price rejection;
- stale quote rejection;
- spread/liquidity rejection;
- tastytrade field limitations;
- Databento fallback;
- network failure classification;
- no-hindsight behavior;
- stage-transition legality;
- duplicate suppression;
- stable winner selection;
- strict no-trade behavior;
- exit replay;
- costs;
- deterministic reruns.

Run affected Ideal, Clean Fast Break, Continuation, Day 50, Day 51, and Day 52 regressions.

Run affected validators.

Run:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Run:

`git diff --check`

Do not run unrelated broad suites.

## Mandatory handoff update

Audit existing canonical files and remove or correct stale current-objective text without duplicating history.

Update factual current state in:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
- `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`

The canonical handoff must explicitly require future chats to:

- continue this same option-evidence and end-to-end backtest objective;
- avoid broad candidate hunting;
- use local evidence first, tastytrade second, Databento fallback;
- apply the existing timing rule to the complete quote window;
- not wait for Schwab;
- finish the economic winner through net P&L or an exact priced request;
- avoid another provisional or documentation-only loop.

The handoff must state:

- latest verified commit;
- exact dirty/clean status;
- exact selected winner;
- exact contract-selection result;
- exact tastytrade result;
- exact Databento result;
- exact entry-window result;
- stage reached;
- tests passed;
- exact remaining blocker;
- profitability proof: `NO`;
- paper/live eligibility: `NO`.

## Guardrails

Do not modify:

- `main.py`;
- production/live backend;
- Railway/deploy;
- broker/account/order/alert code;
- credentials or `.env`;
- sizing;
- frozen `patch8` thresholds.

Do not push.

Do not claim profitability, paper eligibility, or live eligibility.

## Completion

Remove generated `__pycache__` directories.

Do not run `git add` or `git commit` inside the Codex sandbox.

Finish with:

- `READY_FOR_OPERATOR_COMMIT`;
- exact changed/untracked files;
- selected winner;
- contract-selection result;
- complete entry-window result;
- tastytrade result;
- Databento result;
- entry/exit/P&L result or exact priced request;
- tests and validators passed;
- remaining blockers;
- profitability proof: `NO`;
- paper/live eligibility: `NO`.