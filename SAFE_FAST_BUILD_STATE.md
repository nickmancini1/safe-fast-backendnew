# SAFE-FAST Build State

- **Current frozen baseline:** `patch8`
- **Active repo:** `safe-fast-backendnew`
- **Latest confirmed live baseline:** `macro_surface_v26_2026_04_21_preserve_locked_trigger_patch8`
- **Current objective:** fix on-demand setup recognition and stage correctness
- **Continuation anchor-lock patch:** applied to `main.py`, locally tested, committed
- **On-demand classifier fix:** applied to `main.py`, locally tested, committed
- **Classifier bug fixed:** Ideal setup identity now survives blockers instead of being mislabeled as Clean Fast Break
- **Classifier contract test:** `replay/test_on_demand_classifier_contract.py`
- **Replay validation:** passed locally
- **Replay result:** `16/16 passed | local_fixture_engine=16 | placeholder_scaffold=0`
- **Replay protection status:** all 16 cases now use local fixture outputs, no placeholder scaffold
- **Do not touch:** Railway, production deploy, old repo
- **Next exact task:** find the next on-demand setup recognition/stage failure and add targeted replay coverage before further engine logic changes
