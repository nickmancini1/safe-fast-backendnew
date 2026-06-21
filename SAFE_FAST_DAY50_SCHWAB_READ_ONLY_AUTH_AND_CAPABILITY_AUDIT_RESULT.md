# SAFE-FAST Day 50 Schwab Read-Only Auth and Capability Audit Result

## Baseline

- Branch: `main`.
- Scope: read-only Schwab broker/source capability work.
- Official Schwab source access: `api.schwabapi.com` official endpoints were reachable and returned unauthenticated `401` for protected account/market-data GET endpoints. The Schwab Developer Portal documentation pages returned `403 Access Denied` from this environment, so no non-official documentation was used.
- Schwab OAuth config present locally: `NO`.
- Missing config names: `SCHWAB_CLIENT_ID` or `SCHWAB_APP_KEY`, `SCHWAB_CLIENT_SECRET` or `SCHWAB_APP_SECRET`, and `SCHWAB_REDIRECT_URI`.

## Fixed

- Added isolated read-only Schwab helper: `watcher_foundation/schwab_read_only_audit.py`.
- Added focused tests: `tests/test_schwab_read_only_audit.py`.
- Updated registry Schwab live-fill entry to point at the implemented read-only audit helper and test.
- Updated registry documentation with the current blocked Schwab status.

## Verified

- Token storage rule is enforced: token paths inside the repository are rejected.
- OAuth authorization URL builder uses the official Schwab `https://api.schwabapi.com/v1/oauth/authorize` endpoint and requires a `state` value.
- Token exchange/refresh helpers target the official Schwab `https://api.schwabapi.com/v1/oauth/token` endpoint and redact token values from returned status.
- Read-only request builder allow-lists only GET endpoints for:
  - account-number lookup;
  - account detail/account positions;
  - transactions;
  - existing orders;
  - quotes;
  - option chains;
  - price history.
- Order-submission behavior remains absent. Submit, preview, replace, cancel, and saved-order mutation behavior is explicitly forbidden by the helper and tests.

## Blocked

- OAuth browser authorization was not requested because the client id/app key, client secret/app secret, and redirect URI are missing. Asking for browser authorization before those values exist would not be actionable.
- Account-list access was not verified.
- Balances, buying power, positions, transaction history, existing orders/fills, quotes, option chains, and price history were not verified.
- Historical range, granularity, timestamp semantics, adjustments, option-history availability, rate limits, and entitlement limits remain unverified.
- Bounded timestamp comparisons against Databento and option-chain comparisons against tastytrade were not attempted because Schwab authentication was unavailable.
- No Schwab capability is promoted as a Databento replacement. Schwab remains the live broker/account/order/fill authority only.

## Source-Registry Impact

- Proven repo capability: isolated read-only Schwab OAuth/capability audit helper exists and is covered by focused tests.
- Proven Schwab data capability: none, because OAuth was not configured and no authenticated endpoint was called.
- Registry status: only the `schwab_live_fill` consumer/test routing was updated. Historical underlying and historical options authorities remain Databento. SAFE-FAST setup labels remain local-only.

## Future Local Schwab Archive

Future read-only snapshots should be written only after explicit authorization to an ignored local archive. Token values, client secrets, raw account numbers, and account hashes must not be committed, printed, or documented. Archive rows should record endpoint name, request parameter shape, response timestamp, redaction status, and capability conclusion without creating trade approval, proof, profitability, paper eligibility, or live eligibility.

## Tests

- `python -B -m unittest discover -s tests -p "test_schwab_read_only_audit.py"`: PASS, `7` tests.
- `python -B -m watcher_foundation.schwab_read_only_audit`: PASS, blocked status emitted with `live_schwab_verification_attempted=false`, `oauth_browser_action_required_now=false`, `broker_mutation_attempted=false`, and `orders_submitted_or_previewed=false`.
