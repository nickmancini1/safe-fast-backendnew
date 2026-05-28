# SAFE-FAST Shadow Review Export Bundle Review Package Plan

## Purpose

- Define the intended shape of a local review package for later human or ChatGPT review.
- Package only already-validated local shadow review/export artifacts.
- Keep all package inputs and proposed output local and in memory at this stage.
- Avoid implementation, generated files, generated reports, persistent logs, live data, network calls, alerts, loops, schedulers, or trade-decision behavior.

## Allowed Local Artifacts

A later review package may include only caller-provided, already-local artifacts from the shadow review/export bundle foundation:

- Validated shadow review samples.
- Label workflow summaries.
- Export-shape dicts.
- Export bundle dicts.
- Rejected sample/export reasons.
- Label/setup/export counts.
- No-trade boundary summary.

## Proposed Package Shape

A later in-memory review package should be a plain dict with these top-level fields:

- `package_id`: deterministic local identifier for the package.
- `schema_version`: review-package schema version.
- `created_from`: local provenance describing the validated source artifacts and baseline.
- `source_exports`: included validated export-shape dicts.
- `source_bundles`: included validated export bundle dicts.
- `review_summary`: local summary of accepted samples, workflow status, export status, counts, and no-trade posture.
- `rejected_items`: rejected sample/export entries with preserved rejection reasons.
- `no_trade_boundary_summary`: explicit watch-only/no-trade boundary statement carried forward from source artifacts.
- `unavailable_fields`: fields intentionally unavailable and not fabricated.
- `reviewer_notes`: empty or caller-provided local review notes for later human/ChatGPT review.

## Boundaries

- No files are written by implementation yet.
- No generated reports.
- No persistent logs.
- No live data.
- No network calls.
- No alerts.
- No loops or schedulers.
- No broker, order, account, option, or P&L fields.
- No live trade decisions.
- No production, Railway, deployment, `main.py`, engine-logic, live-backend, secret, `.env`, credential, or deployment-setting changes.

## Validation Rules For Later Implementation

A later validator should:

- Accept dict input only.
- Require all required top-level fields.
- Validate included export-shape dicts.
- Validate included export bundle dicts.
- Preserve rejected sample/export reasons without rewriting or dropping them.
- Preserve the no-trade boundary summary.
- Reject forbidden execution/trade fields, including nested fields.
- Reject broker, order, account, option, P&L, live-trade, approval, execution, and trade-decision fields anywhere in the package.
- Produce deterministic output for the same input.

## Recommended Next Build Step

- Implement a local shadow review/export bundle review-package validator using in-memory dicts only.
- Keep the next build local and docs/test bounded until explicitly approved.
