# SAFE-FAST Build State

- **Current frozen baseline:** `patch8`
- **Current repo baseline commit:** current GitHub `main` from uploaded ZIP
- **Latest confirmed live baseline:** `macro_surface_v26_2026_04_21_preserve_locked_trigger_patch8`
- **Current objective:** build replay/regression validation before engine patches
- **Replay foundation status:** expanded to setup-state coverage with deterministic local fixture adapter
- **Replay expected count after this package:** `16/16`
- **Continuation local fixture engine count after this package:** `5`
- **Known issue:** on-demand setup-state classification
- **Specific states covered:** too early, needs more candles, valid/actionable, too late
- **Specific suspect area:** continuation shelf/reclaim/trigger may reroll or ratchet as live candles update
- **Rule:** do not patch setup logic until replay cases exist for the exact failure state
- **Next exact task:** after this package is committed to GitHub, inspect and patch continuation context selection/finalization in `main.py` only if replay protection remains passing
