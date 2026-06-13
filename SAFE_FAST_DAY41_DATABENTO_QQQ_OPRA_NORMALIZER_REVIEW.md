# SAFE-FAST Day 41 Databento QQQ OPRA Normalizer Review

## Scope

Goal: create a read-only local normalizer for the already-downloaded QQQ Databento OPRA CSV files.

Baseline from task file: `7304497 Map QQQ Databento fields to evidence requirements`.

Allowed implementation:

- `historical_signal_replay/databento_opra_normalizer.py`
- `tests/test_databento_opra_normalizer.py`

No additional data was downloaded. No vendor API was called. No raw vendor file was edited. No evidence file was filled. No trade was chosen. No P&L was calculated. QQQ was not marked ready.

## Normalizer Added

Created `historical_signal_replay/databento_opra_normalizer.py`.

Supported read-only behaviors:

- load definitions, TCBBO quote rows, trade rows, and statistics rows from local CSV files
- validate required columns and fail with `MissingColumnError` when required Databento fields are absent
- parse OPRA/OCC-style option symbols such as `QQQ   260501C00610000`
- normalize timestamps to timezone-aware UTC datetimes
- normalize definitions into underlying, expiration, side, strike, multiplier, and tick metadata where present
- normalize quotes into bid, ask, sizes, expiration, strike, side, midpoint, spread, and spread percent
- normalize trades into trade price and trade size inspection rows
- normalize statistics and map Databento stat type `6` to `cleared_volume` and stat type `9` to `open_interest`
- join quote, trade, or statistics rows back to definitions by `instrument_id` first, with `symbol` fallback
- select the nearest quote at or before a signal timestamp without using post-signal rows

Explicit refusal guardrails:

- fill inference
- trade choice
- P&L calculation
- proof acceptance
- candidate readiness

These refusals are implemented with `UnsafeInferenceError`.

## Tests Added

Created `tests/test_databento_opra_normalizer.py`.

Covered cases:

- OPRA symbol parsing
- definition joins
- no-hindsight quote selection rejecting post-signal rows
- bid/ask midpoint, spread, and spread-percent calculation
- statistics interpretation for cleared volume and open interest
- timezone normalization and naive timestamp rejection
- missing-column failure with clear error text
- loader support for definitions, quotes, trades, and statistics CSVs
- refusal to infer fills, trade choice, P&L, proof, or readiness

## Verification

Focused test command:

`python -m unittest tests.test_databento_opra_normalizer`

Result: PASS, 9 tests.

Compile check:

`python -m py_compile .\historical_signal_replay\databento_opra_normalizer.py .\tests\test_databento_opra_normalizer.py`

Result: PASS.

## Limits Preserved

The normalizer only prepares raw Databento inspection fields. It does not create SAFE-FAST labels.

Still not proven:

- QQQ gap-context status
- QQQ Clean Fast Break stale/spent lifecycle status
- option-context status
- execution-context status
- complete caution review status
- exact contract selection
- entry or exit rule
- fill assumption
- slippage or cost rule
- P&L
- profitability
- proof
- QQQ readiness

## Result

Normalizer created: YES.

Tests created: YES.

Tests passed: YES.

Raw data files changed: NO.

Evidence filled: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
