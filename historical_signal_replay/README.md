# SAFE-FAST Historical Signal Replay v1

This folder contains the minimal local Historical Signal Replay v1 scaffold and runner.

Historical Signal Replay v1 proves signal and stage behavior over historical bars. It does not prove profitability.

## Explicit Boundaries

- No trade outcome backtesting
- No option P&L
- No option contract economics
- No account sizing
- No live trade decisions
- No auto-trading

The final target remains full SAFE-FAST automation with manual trade execution only. The system may eventually automate scanning, setup recognition, lifecycle tracking, state-change alerts, context checks, and trade-plan preparation, but the human remains responsible for entering and managing trades manually.

## Scaffold Contents

- `schemas/signal_replay_input_v1.schema.json`
- `schemas/signal_replay_output_v1.schema.json`
- `fixtures/no_hindsight_sample_signal_replay_fixture.json`
- `reports/.gitkeep`

The fixture is a no-hindsight example shape only. Unavailable macro, IV, event, and context fields are marked unconfirmed instead of inferred.

## Minimal implementation v1

Run command:

```powershell
python -B historical_signal_replay/run_signal_replay.py
```

Output files:

- `reports/no_hindsight_sample_signal_log.jsonl`
- `reports/no_hindsight_sample_summary.json`
- `reports/no_hindsight_regression_candidates.json`

Boundaries:

- Local, non-production signal/stage replay only
- No trade outcome backtesting
- No option P&L
- No account sizing
- No live trade decisions
- No broker or live market API calls
- No auto-trading
