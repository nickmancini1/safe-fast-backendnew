# SAFE-FAST Shadow Review Export-Shape Plan

## Purpose

Define the local in-memory shape for shadow review exports so later ChatGPT or human review can inspect watch-only shadow review results without live trading.

This plan is documentation only. It does not implement an exporter, write files, generate reports, persist logs, fetch live data, emit alerts, run loops, or make live trade decisions.

## Allowed input

Later implementation may accept only caller-provided local in-memory dictionaries from the shadow review workflow:

- Local shadow review workflow summary dicts.
- Local validated sample dicts.
- Local label counts.
- Local setup type counts.

The export shape must not read from disk, write to disk, call live services, use network access, or derive trade execution data.

## Proposed in-memory export shape

The proposed export object is a plain dictionary with these top-level fields:

- `export_id`: deterministic local identifier supplied by the caller or derived from stable local input values.
- `created_from`: short local source summary, such as `local_shadow_review_workflow_summary`.
- `schema_version`: explicit export schema version, starting with `1`.
- `samples`: list of validated local shadow review sample dicts.
- `label_counts`: dict keyed by approved reviewer label.
- `setup_type_counts`: dict keyed by local setup type.
- `rejected_samples`: list of rejected sample summaries preserving `sample_id` and rejection reason.
- `no_trade_boundary_summary`: dict summarizing watch-only/no-trade preservation counts and status.
- `reviewer_notes`: local reviewer/export notes, with unavailable evidence stated explicitly.
- `unavailable_fields`: list or dict naming fields intentionally unavailable for review.

## Required boundaries

- No files written.
- No generated reports.
- No persistent logs.
- No live data.
- No network.
- No alerts.
- No loops or schedulers.
- No broker, order, account, option, or P&L fields.
- No live trade decisions.

## Validation rules for later implementation

- Accept dict input only.
- Require all required export fields.
- Require `samples`, `label_counts`, `setup_type_counts`, `rejected_samples`, `no_trade_boundary_summary`, `reviewer_notes`, and `unavailable_fields` to be present.
- Reject forbidden execution/trade fields at any depth, including nested dictionaries, lists, and tuples.
- Preserve the local watch-only/no-trade boundary.
- Preserve rejected sample reasons exactly enough for later review.
- Preserve unavailable-field semantics rather than filling missing evidence from assumptions.
- Keep output deterministic for the same input.
- Return an in-memory dict only.

## Recommended next build step

Create a local shadow review export-shape validator using in-memory dicts only.

The validator should prove the proposed export shape, required fields, nested forbidden-field rejection, rejected-sample reason preservation, unavailable-field preservation, deterministic output, and watch-only/no-trade boundary without writing files, creating generated reports, touching live data, adding network access, adding alerts, adding loops/schedulers, or adding broker/order/account/option/P&L behavior.
