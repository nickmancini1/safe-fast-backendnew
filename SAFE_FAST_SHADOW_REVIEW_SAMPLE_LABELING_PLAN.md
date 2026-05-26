# SAFE-FAST Shadow Review Sample Labeling Plan

## Purpose

Define a local, after-the-fact human review workflow for replay outputs, trigger cards, diagnostics, and shadow-log-like records already produced by local tests.

This plan is for labeling and reviewing watch-only samples after local replay/regression execution. It does not approve trades, create live trade decisions, invent triggers, invent outcomes, calculate P&L, or produce generated reports.

## Allowed inputs

Reviewers may use only local artifacts already available from local replay/regression or local test execution:

- Local/in-memory replay outputs.
- Trigger cards emitted by local watcher foundation paths.
- Diagnostics emitted by local watcher foundation paths.
- Shadow-log-like records already produced by local tests.
- Duplicate suppression state and material-change flags already present in local outputs.
- Focus winner fields already present in local outputs.
- No-trade boundary fields already present in local outputs.

## Review labels

Allowed reviewer labels are:

- `valid_watch_candidate`
- `invalid_watch_candidate`
- `needs_more_evidence`
- `stale_or_spent`
- `duplicate_suppressed`
- `winner_correct`
- `winner_questionable`
- `no_trade_boundary_preserved`

## Required review fields

Each reviewed sample must include:

- `sample_id`
- `setup_type`
- `stage`
- `trigger_status`
- `headline_news_status`
- `duplicate_suppression_status`
- `focus_winner_status`
- `diagnostics_summary`
- `reviewer_label`
- `reviewer_notes`
- `no_trade_boundary_check`

## Review rules

- No live trade decisions.
- No trigger invention.
- No outcome invention.
- No P&L.
- No broker/order/account/option fields.
- No live data.
- No generated reports.
- Reviewers must label only what is supported by the local artifact under review.
- Missing or unavailable evidence must be labeled as `needs_more_evidence` instead of filled in from assumptions.
- Stale, spent, or no-fresh-trigger samples must not be upgraded into active watch candidates.
- Duplicate-suppressed samples must remain reviewable as suppressed local samples, not new alerts.
- Focus winner review must compare only candidates already present in the local replay output.
- No-trade boundary review must confirm the local output remains watch-only and emits no trade approval.

## Review workflow

1. Select one local sample from an in-memory replay output, trigger card, diagnostics object, or shadow-log-like record.
2. Copy only the supported fields into the required review fields.
3. Normalize missing local evidence to explicit unavailable wording in `diagnostics_summary` or `reviewer_notes`.
4. Choose one or more applicable review labels from the allowed label list.
5. Confirm `no_trade_boundary_check` is preserved before accepting the review entry.
6. Do not create a persistent generated report from the review.

## Recommended next implementation step

Create a local shadow review label schema/test fixture using in-memory sample dicts only.

The next step should validate the allowed labels, required fields, unavailable-field behavior, duplicate-suppressed handling, focus-winner labeling, and no-trade boundary preservation without touching live data, reports, broker/order/account/option/P&L fields, production files, Railway files, `main.py`, or trading logic.
