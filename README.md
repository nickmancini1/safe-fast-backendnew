# SAFE-FAST Backend

GitHub-ready packaging of the PATCH8 frozen SAFE-FAST backend.

## Source files

- `main.py` — FastAPI SAFE-FAST backend, copied from `main_preserve_locked_trigger_patch8_full.py`.
- `dxlink_candles.py` — DXLink 1H candle / EMA50 helper required by `main.py`.
- `docs/` — PATCH8 handoff notes.
- `replay/fixtures/` — preserved sample output fixture.

## Required environment variables

Copy `.env.example` to `.env` locally, or set these variables in Railway/hosting:

```text
TT_CLIENT_ID=
TT_CLIENT_SECRET=
TT_REDIRECT_URI=
TT_REFRESH_TOKEN=
SAFE_FAST_CONTINUOUS_STATE_DIR=
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Health check

```text
GET /health
```

## Canonical SAFE-FAST route

```text
POST /safe-fast/on-demand
```

## Deployment notes

For Railway, use either:

```text
uvicorn main:app --host 0.0.0.0 --port $PORT
```

or the included `Procfile` / `Dockerfile`.

## Next build objective

Per the PATCH8 handoff docs, do not blindly patch the engine. The next safest build step is replay / regression validation around the frozen PATCH8 baseline.
