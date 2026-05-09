# SAFE-FAST Build State

## Current baseline

- **Current frozen baseline:** `patch8`
- **Active repo:** `safe-fast-backendnew`
- **Branch:** `main`
- **Latest confirmed live baseline:** `macro_surface_v26_2026_04_21_preserve_locked_trigger_patch8`
- **main.py source state:** repaired patch8 source confirmed; `import copy` restored
- **Current objective:** on-demand setup recognition and stage correctness
- **Current build direction:** finish recognition/stage correctness, then build continuous watch-only automation
- **Work mode:** build work only, no live trade decisions

## Do not touch

- Do not touch Railway
- Do not touch production deploy files
- Do not touch the old repo
- Do not add auto-trading
- Do not invent live reads
- If `getSafeFastOnDemand` is unavailable, mark live fields unconfirmed

## Fixed and protected in patch8

- **Continuation anchor-lock patch:** applied to `main.py`, locally tested, committed
- **On-demand classifier fix:** applied to `main.py`, locally tested, committed
- **Classifier bug fixed:** Ideal setup identity now survives blockers instead of being mislabeled as Clean Fast Break
- **Classifier contract test:** `replay/test_on_demand_classifier_contract.py`
- **Winner-selection contract test:** `replay/test_on_demand_winner_selection_contract.py`
- **Winner-selection rule protected:** Ideal, Clean Fast Break, and Continuation selection remains deterministic; Continuation shelf context is not overwritten by a fast-break profile
- **Mixed setup stage contract test:** `replay/test_on_demand_mixed_setup_stage_contract.py`
- **Mixed setup stage rule protected:** spent/blocked Continuation does not beat a valid fresh Ideal or Clean Fast Break candidate; trade-ready Clean Fast Break beats pending fresh Continuation in mixed setup pools
- **Mixed setup stage proof status:** committed on `main`; GitHub Actions passed for commit `ae6236b`; no `main.py` engine behavior was changed by this contract-only commit
- **Spent pending Continuation winner contract test:** `replay/test_on_demand_spent_pending_continuation_winner_contract.py`
- **Spent pending Continuation winner rule protected:** a stale/spent Continuation that reaches screened selection as `PENDING` does not beat a fresh pending Ideal candidate on risk rank or raw engine winner carry-forward
- **Spent pending Continuation winner proof status:** contract failed before patch; minimal `main.py` winner-selection sort patch demotes prior/spent Continuation candidates; no trigger math, setup classification, or trade approval logic changed

- **Stage-message fix:** applied to `main.py`, locally tested, committed
- **Stage-message bug fixed:** spent/prior-break Continuation no longer says it is waiting for the first completed break
- **Stage-message contract test:** `replay/test_on_demand_stage_messages.py`
- **Trigger-stage contract test:** `replay/test_on_demand_trigger_stage_contract.py`
- **Trigger-stage rule protected:** intrabar raw Continuation breaks do not become completed-candle approval; completed triggers while market is closed do not become live trades; too-early holds do not become trigger-ready
- **Trigger-stage proof status:** committed on `main` as contract-only coverage; no `main.py` engine behavior was changed by this contract-only commit
- **User-facing stage surface contract test:** `replay/test_on_demand_user_facing_stage_surface_contract.py`
- **User-facing stage surface rule protected:** raw trigger keys are humanized; prior spent breaks explain already-happened/no-fresh-trigger; pending shelf breaks and market-closed pending triggers show clear next steps; watchouts/cautions appear in `response_text`
- **User-facing stage surface proof status:** committed on `main` as contract-only coverage; no `main.py` engine behavior was changed by this contract-only commit

- **Session-boundary Continuation fix:** applied to `main.py`, locally tested, committed
- **Session-boundary Continuation contract test:** `replay/test_on_demand_session_boundary_contract.py`
- **Session-boundary rule protected:** prior-session completed shelf breaks are carried only as spent/blocked context unless a fresh current-session break is selected; prior-session breaks do not become fresh current-session Continuation triggers
- **Session-boundary trigger-state reason fix:** applied to `main.py`, locally tested, committed
- **Session-boundary trigger-state rule protected:** prior-session completed shelf breaks surface `prior_completed_shelf_break_spent` in trigger state instead of generic too-early/structure-not-ready reasons
- **Session-boundary user-facing surface fix:** applied to `main.py`, locally tested, committed
- **Session-boundary user-facing surface contract test:** `replay/test_on_demand_session_boundary_surface_contract.py`
- **Session-boundary user-facing rule protected:** prior-session completed shelf breaks are humanized as already spent/no fresh trigger now instead of surfacing only the raw reason key
- **Session-boundary fresh-break fix:** applied to `main.py`, locally tested, committed
- **Session-boundary fresh-break contract test:** `replay/test_on_demand_session_boundary_fresh_break_contract.py`
- **Session-boundary fresh-break rule protected:** a fresh current-session Continuation break is not suppressed by an older prior-session spent break
- **Continuation shelf trigger-basis bug fixed:** `shelf_trigger_basis` is defined before preserve-pending-window logic
- **Session-boundary weekend carry contract test:** `replay/test_on_demand_session_boundary_weekend_carry_contract.py`
- **Session-boundary weekend carry rule protected:** a Friday completed Continuation shelf break is treated as the immediately prior regular-session break on Monday, surfaces as spent/no-fresh-trigger context, and does not become a generic early hold or fresh current-session trigger
- **Session-boundary weekend carry proof status:** contract failed before patch; minimal `main.py` session carry-forward date patch now skips weekend calendar days when finding the prior regular session; `main.py` changed; this was engine stage/carry-forward logic only, not trigger math, setup classification, trade approval, or winner selection

- **24H caution fix:** applied to `main.py`, locally tested, committed
- **24H rule fixed:** 24H countertrend is a caution, not a hard blocker
- **24H caution contract test:** `replay/test_on_demand_24h_caution_contract.py`
- **24H support classifier contract test:** `replay/test_on_demand_24h_support_contract.py`
- **24H support classifier rule protected:** mixed/not-bearish 24H context does not block Continuation; 24H countertrend alone does not disallow Clean Fast Break

- **24H caution surface fix:** applied to `main.py`, locally tested, committed
- **24H surface bug fixed:** 24H countertrend caution now appears in user-facing watchouts/cautions
- **24H surface contract test:** `replay/test_on_demand_24h_surface_contract.py`
- **24H response-surface contract test:** `replay/test_on_demand_24h_response_surface_contract.py`

- **Macro-event surface contract test:** `replay/test_on_demand_macro_event_surface_contract.py`
- **Macro-event surface rule protected:** macro event risk is surfaced as caution/context in user-facing response surfaces without destroying setup identity
- **IV/event-day surface contract test:** `replay/test_on_demand_iv_event_surface_contract.py`
- **IV/event-day surface rule protected:** high IV / event-day risk is surfaced as caution/context in user-facing response surfaces

- **Extension caution fix:** applied to `main.py`, locally tested, committed
- **Extension rule fixed:** elevated/soft extension is surfaced as a caution, not an automatic hard blocker
- **Extension caution contract test:** `replay/test_on_demand_extension_caution_contract.py`
- **Soft-extension pending-trigger contract test:** `replay/test_on_demand_soft_extension_pending_trigger_contract.py`
- **Soft-extension pending-trigger rule protected:** soft-extension Continuation intrabar shelf breaks become pending completed-candle approval, not live trade and not generic waiting
- **Soft-extension pending-trigger proof status:** no `main.py` engine behavior changed by this contract-only commit
- **Pending completed approval surface contract test:** `replay/test_on_demand_pending_completed_approval_surface_contract.py`
- **Pending completed approval surface rule protected:** pending_completed_candle_approval shows a specific completed-candle approval next step instead of generic live-trigger language
- **Pending completed approval surface proof status:** contract failed before patch; minimal `main.py` surface-only patch added in `_derive_trade_day_acceptability_condition`; no trigger-state math, setup classification, or trade approval logic changed
- **Next-bar hold failure surface contract test:** `replay/test_on_demand_next_bar_hold_failure_surface_contract.py`
- **Next-bar hold failure surface rule protected:** failed or unconfirmed next-bar breakout hold surfaces as rebuild/confirm hold language instead of generic live-trigger language
- **Next-bar hold failure surface proof status:** contract failed before patch; minimal `main.py` surface-only patch added in `_derive_trade_day_acceptability_condition`; no trigger-state math, setup classification, or trade approval logic changed
- **ATH/open-air stage contract test:** `replay/test_on_demand_ath_open_air_stage_contract.py`
- **ATH/open-air stage rule protected:** open-air price discovery near all-time highs that lacks rebuilt 1H structure surfaces `ath_open_air` / rebuilt-structure as the first decision blocker, effective blocker, approval next flip, and user-facing failed reason instead of generic room or extension language
- **ATH/open-air stage proof status:** contract failed before patch; minimal `main.py` surface-only patch added in checklist blocker priority, approval next-flip derivation, and failed-reason messaging; no trigger math, setup classification, or trade approval logic changed

- **Room caution fix:** applied to `main.py`, locally tested, committed
- **Room rule fixed:** workable/tight room is surfaced as a caution, while cramped room remains a hard blocker
- **Room caution / cramped first-wall contract test:** `replay/test_on_demand_room_caution_contract.py`

- **Cramped first-wall rule protected:** cramped room / first wall too close hard-fails as `clear_room` and appears first in decision/effective blocker priority

- **Wall-thesis fit contract test:** `replay/test_on_demand_wall_thesis_fit_contract.py`
- **Wall-thesis fit rule protected:** failed wall-thesis/hidden-level fit blocks live entry as `wall_thesis_fit` global/effective blocker without becoming a base failed checklist item

- **No-trade gate priority fix:** applied to `main.py`, locally targeted-tested, committed
- **No-trade gate priority contract test:** `replay/test_on_demand_no_trade_gate_priority_contract.py`
- **No-trade gate priority rule protected:** bad liquidity, missing invalidation, risk mismatch, and existing open position surface as first decision/effective no-trade blockers

- **Valid-shelf-not-chop fix:** applied to `main.py`, locally tested, committed
- **Valid shelf rule fixed:** valid post-impulse Continuation shelf/base is not treated as noisy chop
- **Valid-shelf-not-chop contract test:** `replay/test_on_demand_valid_shelf_not_chop_contract.py`

- **Continuation reason-priority contract test:** `replay/test_on_demand_continuation_reason_priority_contract.py`
- **Continuation reason-priority rule protected:** developing Continuations surface `no_proven_hold`, `no_valid_trigger`, or `move_too_extended` ahead of generic blockers

- **Duplicate nested replay cleanup:** accidental `replay/replay/` duplicate continuation reason-priority test removed

## Replay / regression status

- **Replay validation:** passed locally
- **Latest local replay result:** `16/16 passed | local_fixture_engine=16 | placeholder_scaffold=0`
- **Replay protection status:** all 16 cases use local fixture outputs, no placeholder scaffold
- **GitHub Actions regression workflow:** `.github/workflows/safe-fast-regression.yml`
- **GitHub Actions contract sweep:** workflow runs all `replay/test_on_demand_*contract.py` files, then stage-message contract, fixture validation, and replay regression
- **Latest GitHub Actions run number:** unconfirmed / needs UI verification
- **Latest observed Actions status:** passed on `main` for commit `ae6236b` adding `replay/test_on_demand_mixed_setup_stage_contract.py`
- **Reason:** repo and handoff previously disagreed on the latest Actions run number
- **Do not promote from Actions run number alone:** require local replay/regression evidence plus build-state update

## Current unproven items

- Remaining on-demand setup recognition edge cases
- Remaining stage correctness edge cases beyond currently protected trigger-stage and user-facing surface cases
- Remaining session-boundary carry-forward edge cases
- Remaining stable winner-selection edge cases beyond currently protected mixed setup stage cases
- Continuous lifecycle memory
- Alert suppression / no duplicate alert spam
- Shadow accuracy review
- Production readiness

## Continuous automation target

Final target is **SAFE-FAST Continuous Watcher v1**:

- Watch-only
- No auto-trade
- Tracks Ideal / Clean Fast Break / Continuation
- Tracks setup lifecycle over time
- Preserves no-trade discipline
- Sends alerts only on meaningful state changes
- Marks unavailable live fields as unconfirmed
- Requires replay/regression and shadow accuracy checks before promotion

## Work mode

### Laptop mode

- Move fast
- Use PowerShell command blocks when useful
- Use full replacement files when changing repo files
- Do not ask user to hunt through code

### Phone mode

- Move slower
- Short instructions only
- Provide linked replacement files when needed
- No long code blocks unless user asks

## Current account-mode / trade-style status

- **Account-mode/trade-style plan:** `SAFE_FAST_ACCOUNT_MODE_AND_TRADE_STYLE_PLAN.md`
- **Current account size for plan:** `$1,500`
- **Plan rule:** do not add account-mode/trade-style engine logic until on-demand setup recognition and stage correctness are stable and protected

## Levels / context plan status

- **Levels/context indicators plan:** `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md`
- **Status:** planned later
- **Rule:** do not add level-ranking or optional indicator engine logic until recognition/stage correctness and continuous watcher foundation are stable
- **Indicator rule:** optional indicators should usually create cautions, not hard blockers

## News / headline risk plan status

- **News/headline risk plan:** `SAFE_FAST_NEWS_AND_HEADLINE_RISK_PLAN.md`
- **Status:** planned later
- **Rule:** do not add news/headline engine behavior until on-demand setup recognition and stage correctness are stable and protected
- **Principle:** setup first, stage second, structure/risk/news context third, trade style last
- **News rule:** most news should be caution, not hard blocker; hard block only when immediate and material to setup/trade window/hold risk
- **Unconfirmed rule:** do not invent macro, earnings, filings, or headline data; mark unavailable data as `NEWS_UNCONFIRMED`

## On-demand closeout plan status

- **On-demand closeout plan:** `SAFE_FAST_ON_DEMAND_CLOSEOUT_PLAN.md`
- **Status:** planned closeout gates before Continuous Watcher foundation
- **Rule:** close on-demand by proven failure classes, not percentage estimates
- **Closeout gates:** mixed setup recognition, stage correctness, session-boundary carry-forward, macro/IV/event-day integration boundary, user-facing output cleanup, and closeout regression proof
- **Continuous handoff rule:** start Continuous Watcher foundation only after on-demand closeout proof is clean
- **Phone/laptop rule:** phone-safe work is docs/build-state/Actions review; laptop-only work is `main.py`, local replay/regression, and engine behavior changes

## Next exact task

Continue from patch8.

Next task is to find the next small on-demand setup recognition or stage correctness failure, add/confirm targeted contract or replay coverage first, then make the smallest engine change needed.

No new engine work should happen without coverage first.
