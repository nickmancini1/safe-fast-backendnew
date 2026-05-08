# SAFE-FAST On-Demand Closeout Plan

## Status

Planning document only.

No engine behavior is added by this document.

## Purpose

This document defines what must be true before SAFE-FAST on-demand recognition/stage correctness can be considered stable enough to begin Continuous Watcher foundation work.

Current build priority remains on-demand setup recognition and stage correctness.

Continuous Watcher v1 remains the final target, but it should not replace or bypass the on-demand closeout gates.

## Closeout principle

SAFE-FAST must close on-demand by proven failure classes, not by percentage estimates.

On-demand is considered ready for Continuous Watcher foundation only when:

- no known unprotected setup-recognition failure class remains
- no known unprotected stage-correctness failure class remains
- all targeted on-demand contracts pass
- full replay passes
- fixture validation passes
- no placeholder scaffold is used
- build state is updated with local regression proof
- GitHub Actions is checked as remote verification, not as the only proof

## Current protected areas

Already protected areas include:

- Ideal / Clean Fast Break / Continuation classifier identity
- deterministic winner selection
- 24H countertrend as caution, not automatic hard blocker
- 24H caution user-facing surfacing
- macro-event surface caution/context surfacing
- IV/event-day surface caution/context surfacing
- extension caution behavior
- room caution vs cramped-room hard fail
- wall-thesis fit blocker priority
- no-trade gate priority
- valid Continuation shelf not treated as chop
- Continuation reason priority
- session-boundary prior-break carry-forward
- session-boundary trigger-state reason
- session-boundary user-facing no-fresh-trigger surface
- fresh current-session Continuation break after older prior-session break
- replay workflow running on-demand contracts

## Remaining on-demand gates

### Gate 1 — Mixed setup recognition

Protect edge cases where more than one setup shape is visible.

Examples:

- Ideal is present but blocked; it must not be mislabeled as Clean Fast Break.
- Clean Fast Break is visible while Continuation shelf context is forming.
- Continuation shelf exists but is spent; it must not steal the winner from a valid fresh setup.
- A valid fresh setup must not be suppressed by an older spent Continuation.
- Winner selection must remain deterministic across SPY / QQQ / IWM / GLD.

Required proof:

- targeted contract first
- no `main.py` patch unless the contract fails or protects a real edge case
- full contract sweep and replay after any change

### Gate 2 — Stage correctness

Protect exact stage language and state transitions.

Stages to protect:

- too early
- developing
- pending hold
- pending trigger
- pending completed candle
- valid / trade-ready
- too late
- spent
- no trade
- context only

Examples:

- A spent Continuation must not say it is waiting for the first break.
- A fresh break must not be marked spent.
- A raw intrabar move must not be treated as completed-candle approval unless the completed candle qualifies.
- Market-closed context must not become a live entry.

Required proof:

- stage-message contract coverage
- trigger-context and user-facing output coverage
- replay after changes

### Gate 3 — Session-boundary carry-forward

Continue protecting session-boundary behavior.

Examples:

- prior-session completed break is spent unless a fresh current-session break forms
- fresh current-session break is not blocked by older prior-session break
- current session shelf reroll does not erase a protected spent/locked state
- next-session context is clear and not confused with live entry permission

Required proof:

- targeted contract coverage before engine changes
- local replay after changes

### Gate 4 — Macro / IV / event-day integration boundary

Current macro/IV surface contracts protect caution surfacing. Future engine behavior must stay limited until on-demand setup/stage is stable.

Rules:

- macro/event risk is context first
- IV/event-day risk is caution first unless immediate/material
- risk context must not erase setup identity
- risk context must not create trades
- unavailable data must be unconfirmed

Required proof before any future behavior change:

- `NEWS_CLEAR`
- `NEWS_CAUTION`
- `NEWS_BLOCK`
- `NEWS_UNCONFIRMED`
- caution-vs-block rules
- setup identity preservation

### Gate 5 — User-facing output cleanup

The user-facing output must be plain and useful.

Required output concepts:

- setup type
- stage
- action
- reason
- primary blocker
- next flip needed
- trigger level if available
- invalidation
- watchouts / cautions
- unconfirmed fields clearly marked

Examples:

- Do not show raw reason keys without human text.
- Do not say “waiting for first break” after the first break already happened.
- Do not hide the real blocker behind generic `structure_not_ready` when a better reason is known.

### Gate 6 — Closeout regression proof

Final on-demand closeout must include:

- all `replay/test_on_demand_*contract.py` tests pass
- `replay/test_on_demand_stage_messages.py` passes
- `replay/validate_fixtures.py` passes
- `replay/run_replay.py` passes
- latest local result recorded in build state
- no unexpected working-tree files
- GitHub Actions checked afterward

## Do not do during on-demand closeout

Do not add:

- auto-trading
- Railway/deploy changes
- production backend changes
- account-mode engine behavior
- optional indicator engine behavior
- news/headline engine behavior
- Continuous Watcher alert dispatch

## Continuous Watcher handoff condition

Start Continuous Watcher foundation only after on-demand closeout proof is clean.

The first Continuous Watcher work should be watch-only lifecycle tracking, not alerts first.

Continuous Watcher foundation order:

1. state/lifecycle memory
2. transition detection
3. duplicate suppression
4. shadow-mode logs
5. pending/actual setup alert candidate rules
6. alert dispatch only after replay/shadow proof

## Phone vs laptop rule

Phone-safe:

- docs
- build-state replacement files
- GitHub Actions verification
- reviewing commits and diffs

Laptop-only:

- `main.py` edits
- local replay/regression
- engine behavior changes
- large code changes

## SAFE-FAST closeout rule

Setup first.

Stage second.

Structure/risk/news context third.

Trade style last.

No trade automation.
