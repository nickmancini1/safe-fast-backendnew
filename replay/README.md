# Replay / Regression Foundation (SAFE-FAST)

Offline replay/regression scaffold for SAFE-FAST on-demand validation.

## Run validation

```bash
python replay/validate_fixtures.py
```

## Run replay

```bash
python replay/run_replay.py
```

## Structure

- `replay/schema_case.md` — fixture/expected format contract
- `replay/fixtures/cases/*.json` — frozen input cases
- `replay/fixtures/local_output/*.json` — deterministic local output fixtures for critical continuation states
- `replay/expected/*_expected.json` — expected labeled outcomes
- `replay/engine_adapter.py` — deterministic local fixture adapter
- `replay/validate_fixtures.py` — schema + case/expected consistency checks
- `replay/run_replay.py` — offline comparator runner

## Current coverage

Base setup cases:
- `ideal_001`
- `clean_fast_break_001`
- `continuation_001`

Continuation setup-state cases:
- `continuation_too_early_001`
- `continuation_needs_more_candles_001`
- `continuation_valid_001`
- `continuation_too_late_001`
- `continuation_shelf_reroll_001`

Ideal setup-state cases:
- `ideal_too_early_001`
- `ideal_needs_more_candles_001`
- `ideal_valid_001`
- `ideal_too_late_001`

Clean Fast Break setup-state cases:
- `clean_fast_break_too_early_001`
- `clean_fast_break_needs_more_candles_001`
- `clean_fast_break_valid_001`
- `clean_fast_break_too_late_001`

## Critical continuation local fixture engine cases

These cases must use `source: local_fixture_engine`:
- `continuation_too_early`
- `continuation_needs_more_candles`
- `continuation_valid`
- `continuation_too_late`
- `continuation_shelf_reroll`

The `continuation_shelf_reroll` case asserts that the original shelf/trigger anchor does not reroll or ratchet to a later worse candle level.
