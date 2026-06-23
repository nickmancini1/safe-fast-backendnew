# SAFE-FAST Day 52 Replay-Only Numeric Rule Candidates Result

## Scope

- Task executed: `SAFE_FAST_DAY52_REPLAY_ONLY_NUMERIC_RULE_CANDIDATES_CODEX_TASK.md`.
- Machine-readable result: `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates.json`.
- Provisional manifest: `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates_manifest.json`.
- Compact setup-time review: `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates_setup_time_review.json`.
- Implementation: `historical_signal_replay/day52_replay_only_numeric_rule_candidates.py`.
- Status: `PROVISIONAL_REPLAY_ONLY` research evidence only.

## Values

- Ideal: trigger `668.360000000` from `high`, invalidation `667.870000000` from `low`, rule `CANDIDATE_A_SETUP_BAR_RANGE`.
- Clean Fast Break: trigger `668.360000000` from `high`, invalidation `667.870000000` from `low`, rule `CANDIDATE_A_SETUP_BAR_RANGE`.
- Continuation: trigger `668.360000000` from `high`, invalidation `667.870000000` from `low`, rule `CANDIDATE_A_SETUP_BAR_RANGE`.

Candidate B and Candidate C were not produced because the accepted mapper packages do not contain setup-structure boundaries or explicit named breakout/reclaim/resistance/support/pivot/base levels. Candidate A was selected by fixed priority after those higher-priority fields were absent, not by later price movement.

## Counts

- Accepted mode remains unresolved: numeric values established `0`, numeric values unresolved `6`.
- Provisional mode: setup-qualified under provisional mode `3`, selected winners `1`, suppressed `2`, recognition-layer executable `1`.
- Trade candidates `0`; selected contracts `0`; eligible entries `0`; recorded entries `0`.

## Guardrails

Accepted numeric rules remain unresolved unless separately proven. These provisional replay-only numeric candidates are not profitability proof, not OPRA evidence, and not paper/live eligibility. No option P&L, paid data download, `main.py`, Railway/deploy, broker/account/order/fill/alert, credential, `.env`, sizing, or frozen `patch8` threshold change was made.

## Required Decision

Promote, revise, or reject the setup-bar range candidate for each family with an explicit accepted rule and regression cases before any accepted setup-qualified recognition claim.
