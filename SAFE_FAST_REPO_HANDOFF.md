# GitHub / Codex Handoff

Use this repo as the clean source of truth.

## What changed from the raw handoff ZIP

1. `main_preserve_locked_trigger_patch8_full.py` was copied to `main.py`.
2. The missing `dxlink_candles.py` dependency was added.
3. Repo scaffolding was added:
   - `README.md`
   - `.gitignore`
   - `.env.example`
   - `requirements.txt`
   - `Procfile`
   - `Dockerfile`
4. PATCH8 text handoff files were moved into `docs/`.
5. The saved response fixture was moved into `replay/fixtures/`.

## Important

Do not commit real `.env` files or secrets.

## Codex instruction

Before changing production logic, read:
- `docs/SAFE_FAST_AUTOMATION_READ_FIRST_2026_04_23_PATCH8.txt`
- `docs/SAFE_FAST_NEXT_BUILD_OBJECTIVE_2026_04_23_PATCH8.txt`

The next build objective is replay / regression validation, not more blind production patching.
