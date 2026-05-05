# SAFE-FAST Build State

- **Current frozen baseline:** `patch8`
- **Active repo:** `safe-fast-backendnew`
- **Latest confirmed live baseline:** `macro_surface_v26_2026_04_21_preserve_locked_trigger_patch8`
- **Current objective:** fix on-demand setup recognition and stage correctness
- **Continuation anchor-lock patch:** applied to `main.py`, locally tested, committed
- **Replay validation:** passed locally
- **Replay result:** `16/16 passed | local_fixture_engine=16 | placeholder_scaffold=0`
- **Replay protection status:** all 16 cases now use local fixture outputs, no placeholder scaffold
- **Do not touch:** Railway, production deploy, old repo
- **Next exact task:** inspect on-demand setup classification failures and add targeted replay cases before further engine logic changes
