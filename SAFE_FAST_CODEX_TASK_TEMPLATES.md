# SAFE-FAST Codex Task Templates

Use these templates to keep future tasks bounded. Each task should name its baseline, allowed writes, forbidden writes, exact goal, and final response format.

## Common Guardrails

- Read `SAFE_FAST_BUILD_STATE.md` first.
- Then read `SAFE_FAST_PROJECT_DASHBOARD.md`.
- Then read `SAFE_FAST_PROJECT_RULE_INDEX.md`.
- Use `SAFE_FAST_CODEX_TASK_TEMPLATES.md` for task shape.
- Use `historical_signal_replay/candidate_packets/` before repeating old candidate discovery.
- Run `.\scripts\safe_fast_run_safe_checks.ps1` before and after code changes when the script exists.
- Do not modify `main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, raw vendor data, evidence fills, trade-selection code, backtest code, or P&L unless the task explicitly allows it.
- Do not claim proof, profitability, candidate readiness, intake readiness, or project death.
- Answer the user directly in plain English.

## Data Validation

```text
Baseline:
- Latest commit before this task:

First action:
- Read SAFE_FAST_BUILD_STATE.md, SAFE_FAST_PROJECT_DASHBOARD.md, and SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Validate the named local data artifact structurally.
- Record what fields exist, what fields are missing, and what cannot be inferred.
- Do not fill evidence or create labels unless explicitly allowed.

Allowed writes:
-

Do not write:
- raw vendor files
- evidence fills
- calculator code
- backtest code
- trade-selection code
- P&L
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Required checks:
- Presence, headers/schema, row counts where safe, timestamp shape, and no-hindsight boundary implications.
- State explicitly whether proof/readiness/profitability remain unproven.

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
```

## Rule Decision

```text
Baseline:
- Latest commit before this task:

First action:
- Read SAFE_FAST_BUILD_STATE.md, SAFE_FAST_PROJECT_DASHBOARD.md, SAFE_FAST_PROJECT_RULE_INDEX.md, and the relevant candidate packet.

Goal:
- Decide or document one narrowly scoped SAFE-FAST rule.
- Separate accepted/current wording from missing decisions and promotion-grade uncertainty.
- Do not write calculator code or fill evidence.

Allowed writes:
-

Do not write:
- evidence fills
- calculator code
- backtest code
- trade-selection code
- P&L
- main.py
- live/engine/broker/order/account/Railway files
- raw vendor data
- .env or secrets

Required output:
- Rule wording.
- Inputs required.
- Unknown/missing-data behavior.
- No-hindsight behavior.
- Regression cases needed before implementation.
- Explicit non-goals.

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
```

## Fixture Creation

```text
Baseline:
- Latest commit before this task:

First action:
- Read SAFE_FAST_BUILD_STATE.md, SAFE_FAST_PROJECT_DASHBOARD.md, SAFE_FAST_PROJECT_RULE_INDEX.md, and relevant rule decision docs.

Goal:
- Add data-only regression fixtures for the accepted rule wording.
- Include boundary, missing-input, wrong-symbol/session, future-data rejection, and known-target cases when relevant.
- Do not implement calculator logic.

Allowed writes:
-

Do not write:
- calculator code
- evidence fills
- backtest code
- trade-selection code
- P&L
- raw vendor data
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Required checks:
- JSON parse validation if fixtures are JSON.
- Confirm fixtures do not claim proof/readiness/profitability.

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
```

## Calculator + Tests

```text
Baseline:
- Latest commit before this task:

First action:
- Read SAFE_FAST_BUILD_STATE.md, SAFE_FAST_PROJECT_DASHBOARD.md, SAFE_FAST_PROJECT_RULE_INDEX.md, relevant fixtures, and candidate packet.
- Run .\scripts\safe_fast_run_safe_checks.ps1 before editing if present.

Goal:
- Implement the smallest calculator for the already accepted rule and fixtures.
- Add focused tests proving boundary, missing-data, and no-hindsight behavior.
- Do not fill evidence, choose trades, backtest, or calculate P&L unless explicitly allowed.

Allowed writes:
-

Do not write:
- evidence fills
- backtest code
- trade-selection code
- P&L
- raw vendor data
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Required checks:
- Focused unit tests.
- .\scripts\safe_fast_run_safe_checks.ps1 after editing if present.
- Compile check for changed Python modules.

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
```

## Evidence-Field Mapping

```text
Baseline:
- Latest commit before this task:

First action:
- Read SAFE_FAST_BUILD_STATE.md, SAFE_FAST_PROJECT_DASHBOARD.md, SAFE_FAST_PROJECT_RULE_INDEX.md, and relevant candidate packet.

Goal:
- Map available raw/source fields to required SAFE-FAST evidence fields.
- Classify fields as supported raw input, rule-calculable, missing, or blocked by missing decision.
- Do not fill evidence.

Allowed writes:
-

Do not write:
- evidence fills
- calculator code unless explicitly allowed
- backtest code
- trade-selection code
- P&L
- raw vendor data
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Required output:
- Field-by-field mapping.
- Source files reviewed.
- What cannot be inferred.
- Next smallest rule/test step.

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
```

## Regression

```text
Baseline:
- Latest commit before this task:

First action:
- Read SAFE_FAST_BUILD_STATE.md, SAFE_FAST_PROJECT_DASHBOARD.md, SAFE_FAST_PROJECT_RULE_INDEX.md, fixtures, tests, and candidate packet.
- Run .\scripts\safe_fast_run_safe_checks.ps1 before editing if present.

Goal:
- Add or run focused regression coverage for the named behavior.
- Keep scope to the accepted rule and existing artifacts.

Allowed writes:
-

Do not write:
- evidence fills
- backtest code
- trade-selection code
- P&L
- raw vendor data
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Required checks:
- Regression command and result.
- Safe-check runner after edits if present.
- Explicit statement of remaining risk.

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
```

## Dashboard Update

```text
Baseline:
- Latest commit before this task:

First action:
- Read SAFE_FAST_BUILD_STATE.md, SAFE_FAST_PROJECT_DASHBOARD.md, and SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Update the dashboard, next-chat intro, build state, rule index, or candidate packet to reflect completed work.
- Do not delete historical docs.
- Do not change implementation unless explicitly allowed.

Allowed writes:
-

Do not write:
- evidence fills
- calculator code
- backtest code
- trade-selection code
- P&L
- raw vendor data
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Required output:
- Current checkpoint.
- Active objective.
- Current blockers.
- Next single action.
- What remains unproven and must not be claimed.

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
```
