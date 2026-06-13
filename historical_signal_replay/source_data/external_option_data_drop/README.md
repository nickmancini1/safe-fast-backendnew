# External Option Data Drop

Put only user-downloaded historical option data files for the QQQ Day 41 request in this folder.

Target request:

- Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`
- Underlying: `QQQ`
- Signal time: `2026-04-13T12:30:00-04:00`
- Quote window: `2026-04-13T12:25:00-04:00` through `2026-04-13T12:35:00-04:00`
- Expirations: `2026-04-27` through `2026-05-13`, inclusive, or all QQQ expirations if vendor filtering is not available
- Strikes: `590` through `640`, inclusive, or full chain if vendor filtering is not available
- Option types: calls and puts

Accepted formats:

- `.csv`
- `.json`
- `.jsonl`
- `.zip` containing `.csv`, `.json`, or `.jsonl`

Preferred contents:

- historical QQQ option quote/NBBO rows with quote timestamp, bid, ask, bid size, ask size, expiration, strike, option type, and option identifier
- QQQ option chain/security definition metadata for the same date and expiration range

Do not put credentials, API keys, account data, broker statements, orders, fills, screenshots, `.env` files, executables, or unrelated market data here.

After files are placed here, Codex should validate structure and coverage only. It should not call paid APIs, use credentials, write ingestion code, fill evidence files, or promote the candidate unless a later task explicitly authorizes that work.
