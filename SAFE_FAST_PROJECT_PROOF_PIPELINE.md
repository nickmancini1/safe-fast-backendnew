# SAFE-FAST Project Proof Pipeline

## Purpose

SAFE-FAST is still being turned from a setup-recognition system into a complete trade plan. Recognition success is required, but it is not proof of profitability.

This pipeline is project-wide. It applies to QQQ, SPY, IWM, GLD, and any setup type unless a later accepted rule narrows the project.

This document is the canonical rule document for promotion gates, falsifiable Day 90 outcomes, sample-size and coverage requirements, protected holdout rules, and candidate/option-contract freeze rules. Supporting result and task files may cite this document, but they do not replace it.

## Day 45 Bounded Sprint Rule

Day 60 is a progress checkpoint, not the finish line. The build target is a profitable trading plan, and the project will not cut corners to hit a date. The project also cannot run indefinitely. The next $200 month is the final high-intensity build sprint before moving toward the $20 tier.

The final sprint must stay batched, evidence-backed, cost-controlled, and focused on tested examples, comparison, trade-plan rules, and a clear decision package. Weak, failed, unclear, missing, or unprofitable results trigger diagnosis and repair; they are not forced into passing results.

## Promotion Ladder

No setup family, candidate, combined plan, paper path, or live path advances because a date was reached. No result may skip a gate. Advancement approval must be recorded in repo documentation before the next gate starts.

| Gate | Required evidence | Required tests | Minimum sample or coverage | Execution-cost assumptions | Risk requirements | Automatic failure conditions | Permitted next action | Advancement approval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Development evidence | Source-backed setup, context, option, timestamp, and blocker fields for the candidate or family. Missing evidence is recorded as blocker, not confidence. | Content validator, package-to-intake bridge, and focused calculators/selectors for affected fields. | At least one accepted development fixture plus one missing-data and one future-data rejection fixture for each changed rule. | No full-window data purchase unless a cost check and user approval exist; starter/local data may be used only within its documented scope. | No risk claim is accepted; risk gaps must be listed before replay. | Future data in setup decisions; unsupported label; raw vendor field treated as SAFE-FAST label; proof/profitability/readiness wording. | Build or repair rule/evidence package. | Repository rule owner plus explicit human task approval. |
| 2. Grouped replay eligibility | Complete trade-plan fields for the replayed setup family and candidate freeze records for every included candidate. | Trade-rule, contract-selection, stage-transition, no-hindsight, missing-data, and failure-label regression tests. | Setup family must meet the pre-holdout development sample minimum in the sample contract table before grouped replay can be treated as countable. | Entry, exit, spread, quote-age, slippage, data-cost, and missing-data assumptions must be fixed before replay. | Max loss, stop/invalidation, time exit, and no-entry conditions must be documented for the replay path. | Missing trade-plan field; post-outcome candidate inclusion; unapproved data download; untested rule change. | Run bounded grouped replay only for frozen candidates and frozen rules. | Canonical rule doc update plus task/result doc approval. |
| 3. Regression acceptance | Replay outputs, accepted/rejected/ambiguous classifications, and all rule versions used. | Safe checks, focused rule-package tests, audit/control-file consistency tests, and `git diff --check`. | All coverage categories in the sample contract must be either satisfied or explicitly blocked before promotion-grade use. | Cost/slippage rules must be included in every counted result; zero-cost or missing-cost fills fail. | Risk plan must block any result missing stop, invalidation, sizing placeholder, or exit boundary. | Test failure; unclassified case; selective result removal; missing loser/no-trade control; inconsistent control files. | Package accepted regression set for protected-holdout selection. | Repo result doc accepted by user, with no promotion claim unless later gates pass. |
| 4. Protected-holdout evaluation | Pre-committed holdout manifest with candidate ids, timestamps, setup family, data references, hashes where available, rule/config versions, and reveal time. | Holdout-manifest consistency test and replay/regression tests pinned to frozen versions. | Holdout slice must meet the protected holdout minimum in the sample contract table before any paper-validation claim. | Data-cost and execution-cost assumptions must be frozen before reveal; holdout data cannot tune costs. | Risk plan must be frozen before reveal and applied to every pass, fail, reject, and missing-data case. | Holdout selected after outcome inspection; post-reveal rule/config change; omitted unfavorable case; missing manifest field. | Report all pass, fail, rejected, ambiguous, and missing-data holdout cases. | Human approval after manifest and tests; no self-approval by replay output. |
| 5. Controlled paper-validation eligibility | Accepted development, grouped replay, regression, holdout report, risk plan, and candidate/contract freeze evidence. | End-to-end dry-run/paper harness tests, risk-limit tests, no-order/live-blocker checks, and control-file agreement tests. | Every family included in paper validation must satisfy sample contract and holdout minima; excluded families must be marked narrowed, repair, or redesign. | Paper assumptions must match the accepted execution model; any broker/platform fee, spread, latency, size, or partial-fill assumption must be recorded. | Max loss per trade, daily/weekly loss, drawdown shutdown, consecutive-loss stop, concurrent-position limit, and de-risking rules must exist before paper. | Missing risk rule; failed holdout; unbounded repair; untracked config drift; live order path touched without explicit authorization. | Start controlled paper-validation planning only. | Human approval in a dedicated result/task; repo must still state no live readiness. |
| 6. Paper-to-live review eligibility | Completed paper-validation logs, frozen paper rules, risk adherence evidence, rejected/missing-data cases, and variance analysis against replay/holdout. | Paper-log integrity tests, risk-limit replay tests, config-freeze tests, and final decision-package consistency tests. | Paper sample must be at least the protected holdout minimum again under live-like timing; no family advances with fewer cases. | Actual observed paper slippage, latency, fees, spreads, and missed-fill behavior must be compared with frozen assumptions. | Live-readiness review must include max loss, capital allocation, shutdown, broker/order, and rollback plan. | Paper rule drift; hidden manual overrides; missing losing examples; breached risk limit; incomplete logs; unresolved broker/order risk. | Prepare live-review decision package only; live trading still requires explicit later authorization. | Human approval in a later live-review task. |

## Falsifiable Day 90 Outcomes

Day 90 must end in exactly one of these outcomes. Undefined outcomes such as "continue developing" are not allowed.

| Outcome | Deterministic entry criteria | Disqualifiers | Required evidence | Exact permitted next work |
| --- | --- | --- | --- | --- |
| `PAPER_VALIDATION_ELIGIBLE` | At least one setup family passes all six promotion ladder gates through controlled paper-validation eligibility, meets the sample contract, passes protected holdout without invalidation, has complete risk rules, and has no unresolved proof/pipeline contradiction. | Missing holdout manifest; missing risk rule; failed regression; unresolved future-data or hindsight issue; incomplete sample contract; no accepted losing examples. | Canonical rule doc, sample matrix, frozen candidate/contract records, regression results, holdout report, risk plan, control-file agreement. | Create controlled paper-validation task; do not touch live order paths without explicit later task. |
| `BOUNDED_REPAIR_REQUIRED` | At least one setup family has credible development/replay evidence but fails a specific gate with a bounded, named repair that can be regression-tested without reopening protected holdout evidence. | Repair would require changing post-reveal holdout rules without invalidation; repair scope is undefined; no family has enough evidence to isolate a fix. | Failure diagnosis, affected gate, affected cases, smallest proposed rule/evidence fix, required tests, whether current holdout is invalidated. | Create one bounded repair task with max scope and retest requirements. |
| `NARROWED_PLAN` | One or more families/symbols/expirations are excluded by deterministic blockers while a narrower path remains evidence-backed and testable. | Narrowing removes unfavorable examples selectively; no frozen exclusion rule; narrowed path lacks sample/holdout path. | Rule-backed exclusion table, before/after coverage table, candidate-freeze records, reason for every removed family or condition. | Create next task only for the narrowed eligible path and mark excluded paths historical/blocked. |
| `REDESIGN_REQUIRED` | No setup family can satisfy development, replay, regression, holdout, risk, and sample gates without broad rule redesign or materially new data spend. | Any family already meets `PAPER_VALIDATION_ELIGIBLE`; a bounded repair has a clear limited path. | Failed gate map, missing rule/evidence list, data-cost ledger, invalidated holdout notes, strongest/weakest family summary. | Stop promotion work and create redesign or shutdown decision package. |

## Sample-Size And Coverage Contract

These numbers are the current exact governance contract. Clean Fast Break uses the already accepted blocker below `20` valid completed CFB examples as its accepted completed-entry floor. Other numeric values are conservative governance assumptions because the repo has no evidence-backed numerical value yet. Every governance assumption must be frozen in a manifest before protected holdout evidence is opened.

| Setup family | Accepted entries | Rejection/no-trade controls | Ambiguous or boundary cases | Winners | Losers | Protected holdout accepted entries | Protected holdout rejection/no-trade controls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | 20 | 10 | 5 | 5 | 5 | 8 | 4 |
| Clean Fast Break | 20 | 10 | 5 | 5 | 5 | 8 | 4 |
| Continuation | 20 | 10 | 5 | 5 | 5 | 8 | 4 |

Each setup family must also satisfy this coverage matrix before controlled paper-validation eligibility:

| Coverage dimension | Exact minimum per setup family | Status of value |
| --- | ---: | --- |
| Major market regimes | 3 regimes: uptrend, downtrend, range/chop | Governance assumption |
| Volatility conditions | 3 conditions: low, normal, high | Governance assumption |
| Trend and chop | 2 trend examples and 2 chop examples beyond the major-regime count where separately labeled | Governance assumption |
| Time-of-day periods | 3 periods: first 60 minutes, middle session, final 90 minutes | Governance assumption |
| Weekdays | 5 weekdays, at least 2 examples each | Governance assumption |
| Liquidity and spread conditions | 3 buckets: clean, caution, fail/reject | Governance assumption |
| Symbols approved by plan | At least 2 approved symbols per active family unless a narrowed plan explicitly limits to 1 symbol with a rule-backed reason | Governance assumption |
| Expirations approved by plan | At least 2 expiration buckets per active family: 14-21 DTE and 22-45 DTE, unless narrowed by accepted contract-selection rule | Governance assumption |
| Developing-stage transitions | 5 examples covering watch, candidate, signal, spent/stale, and invalidated or blocked | Governance assumption |
| Session-boundary cases | 3 cases: prior-session carry-forward, same-session reset, and next-session invalidation or block | Governance assumption |

Cases may count toward multiple coverage dimensions only when the frozen record names each dimension before outcome inspection. A missing-data case is countable only as a missing-data or rejection/control example, not as a winner or loser.

## Protected Holdout Rules

Protected holdout candidates and dates must be selected before outcome inspection. The holdout manifest must be committed before reveal and must include exact candidate identifiers, signal timestamps and timezone, setup families, underlying symbols, data references, available file hashes, rule versions, configuration versions, and the reveal boundary.

Holdout data must remain excluded from tuning, repair, threshold selection, candidate ranking, stable-winner selection, execution-cost calibration, and family selection. Rule and configuration versions must be frozen before reveal. Any post-reveal rule or configuration change invalidates the affected holdout result unless the change is purely clerical and does not alter selection, classification, replay, risk, entry, exit, cost, or reporting behavior.

Invalidated holdout evidence cannot be patched into passing status. Replacement holdout evidence must be newly selected, documented in a new manifest, and kept out of tuning before reveal. Holdout reports must include every passing, failing, rejected, ambiguous, and missing-data case. Selective removal of unfavorable examples is prohibited.

## Candidate And Option-Contract Freeze Rules

Candidate generation and option-contract selection must use only information available at the decision timestamp. The frozen record must include:

- candidate-generation rule version
- setup-family label and stage
- underlying
- direction
- signal timestamp and timezone
- expiration-selection rule
- strike-selection rule
- call or put
- liquidity and spread filters
- quote-age limit
- selected raw symbol and instrument identifier when available
- reason for every exclusion
- deterministic tie-break
- evidence that outcome data was unavailable during selection

Explicitly prohibited:

- selecting candidates because they later looked profitable
- replacing losing candidates after outcome inspection
- selecting the best-performing contract retrospectively
- using future bars, quotes, classifications, exit information, fills, P&L, or profitability
- excluding valid candidates without a recorded pre-outcome rule

## Operational Decision Tables

| Decision question | Required answer before action | If answer is missing |
| --- | --- | --- |
| Can a setup family enter grouped replay? | Complete trade-plan rules, frozen candidate/contract records, regression tests, and pre-holdout sample minimum. | Block replay or keep output review-only. |
| Can a result count toward sample size? | Candidate and contract were frozen before outcome inspection; trade plan and costs were fixed; tests passed. | Do not count it. |
| Can holdout be opened? | Manifest committed with frozen rule/config versions and sample contract values. | Do not inspect holdout outcome. |
| Can post-reveal repair use the same holdout? | Only if the repair is clerical and cannot affect selection, classification, replay, risk, entry, exit, cost, or reporting. | Invalidate affected holdout and select replacement. |
| Can paper validation start? | All included families pass development, replay, regression, protected holdout, sample, cost, and risk gates. | Choose bounded repair, narrowed plan, or redesign. |

## Existing Pipeline Stages

1. Raw data
   - Source-backed market, option, timestamp, context, and outcome inputs must exist.
   - Missing evidence is a blocker, not low confidence.
   - Raw vendor files do not by themselves prove a SAFE-FAST label or trade result.

2. Calculated labels
   - SAFE-FAST labels must be calculated from raw evidence or accepted rule artifacts.
   - Vendor data may provide fields such as bid, ask, timestamp, expiration, strike, volume, and open interest.
   - Vendor data must not be treated as providing SAFE-FAST labels unless the repo has a reviewed mapping rule.

3. Setup recognition
   - Setup type, symbol, setup candle, trigger, invalidation, freshness/final-signal state, blockers, and no-hindsight boundary must be explicit.
   - Favorable later price movement is not enough.

4. Stage transitions
   - The setup must have accepted rules for moving between watch, candidate, signal, spent, stale, invalidated, blocked, no-trade, and review states.
   - If stage-transition rules are missing or unclear, the candidate remains blocked.

5. Trade-plan completeness
   - A result cannot count unless the trade plan completeness gate is satisfied.
   - Contract, entry, exit, cost, slippage, liquidity, invalidation, stop, and failure rules must be fixed before counting the result.

6. Replay
   - Replay must use setup-time evidence only for setup-time decisions.
   - Future bars, future replay rows, outcome fields, fills, P&L, and profitability cannot backfill setup-time decisions.

7. Regression
   - Rules that affect labels, stage transitions, entries, exits, stale/spent status, or trade outcome must have regression cases before promotion.
   - Regression cases must include missing data, future-data rejection, boundary conditions, and wrong-symbol or wrong-setup contamination where relevant.

8. Evidence review
   - Evidence review must identify what is accepted, missing, partial, blocked, or invalid.
   - A passing structure check is not a passing content check.
   - A passing data-file validation is not a trade proof.

9. Failure diagnosis
   - Failed, weak, unclear, missing, or unprofitable results trigger diagnosis and repair.
   - Diagnosis must identify the affected setup type, symbol, layer, bad or missing evidence, smallest evidence-backed fix, and required regression protection.

10. Promotion decision
   - Promotion requires accepted evidence, passing regressions, complete trade-plan rules, no-hindsight review, protected holdout, sample contract satisfaction, and risk-rule satisfaction.
   - Promotion can also mean narrowing, replacing, or removing a setup or symbol from the profitable plan.
   - No candidate is intake-ready from raw data or recognition alone.

11. Final sprint decision package
   - Before moving toward the $20 tier, the project needs a clear package stating what works, what failed, what needs repair, what data costs remain, strongest and weakest candidate families, accepted and missing rules, what can continue on the $20 tier, and what would require another serious spend or redesign.
   - Full-window data spending requires exact cost check and user approval before download.

## Current Project Status

Promotion gates defined: YES.

Day 90 outcomes defined: YES.

Sample-size and coverage contract defined: YES, with non-CFB numeric values and most coverage dimensions labeled as governance assumptions that must be frozen before protected holdout reveal.

Protected holdout rules defined: YES.

Candidate and option-contract freeze rules defined: YES.

Proof accepted: NO.

Profitability claimed: NO.

Current known state: repo docs after the Day 47 grouped selected-contract replay and consolidated audit show work-package content validation at `9` passed requests and `0` failed requests. Intake-ready remains controlled by the separate readiness gate. SAFE-FAST still needs CFB execution realism, risk/capital rules, portfolio interaction rules, data-cost ledger, grouped replay/regression, repair/retirement/invalidation thresholds, and a Day 90 decision package before any paper-validation or live-readiness claim.
