# Replay Case Contract

## Fixture input (`replay/fixtures/cases/*.json`)

```json
{
  "case_id": "ideal_001",
  "setup_type_target": "IDEAL",
  "symbol": "SPY",
  "timeframe": "5m",
  "timestamp_utc": "2026-05-03T14:35:00Z",
  "payload": {
    "option_type": "C",
    "open_positions": 0,
    "weekly_trade_count": 0
  }
}
```

## Expected output (`replay/expected/*_expected.json`)

```json
{
  "case_id": "ideal_001",
  "expected": {
    "setup_type": "IDEAL",
    "recognized": true,
    "min_confidence": 0.7
  },
  "assertions": [
    "setup_type == IDEAL",
    "recognized == true",
    "confidence >= 0.7"
  ]
}
```

## Allowed setup labels
- `IDEAL`
- `CLEAN_FAST_BREAK`
- `CONTINUATION`
