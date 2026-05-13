from __future__ import annotations

import argparse
import asyncio
import csv
import math
import os
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


API_BASE = "https://api.tastyworks.com"
USER_AGENT = "safe-fast-backend/1.8.6"
ALLOWED_SYMBOLS = {"SPY", "QQQ", "IWM", "GLD"}
DEFAULT_SYMBOL = "SPY"
DEFAULT_DAYS_BACK = 14
DEFAULT_OUTPUT_PATH = Path(
    "historical_signal_replay/source_data/incoming/"
    "first_real_historical_replay_v1_SPY_source.csv"
)
TEMPLATE_PATH = Path(
    "historical_signal_replay/source_data/templates/"
    "first_real_historical_replay_v1_source_template.csv"
)


def _read_template_columns() -> List[str]:
    with TEMPLATE_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            return next(reader)
        except StopIteration as exc:
            raise RuntimeError(f"Template has no header: {TEMPLATE_PATH}") from exc


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


async def _get_access_token() -> str:
    import httpx

    client_id = _require_env("TT_CLIENT_ID")
    client_secret = _require_env("TT_CLIENT_SECRET")
    redirect_uri = _require_env("TT_REDIRECT_URI")
    refresh_token = _require_env("TT_REFRESH_TOKEN")

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{API_BASE}/oauth/token",
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "refresh_token": refresh_token,
            },
        )

    try:
        payload = resp.json()
    except Exception:
        payload = {"raw": resp.text}

    if resp.status_code >= 400:
        raise RuntimeError(f"Tastytrade OAuth token request failed: {payload}")

    access_token = payload.get("access_token")
    if not access_token:
        raise RuntimeError(f"Tastytrade OAuth token response missing access_token: {payload}")

    return str(access_token)


def _to_float(value: Any, field_name: str) -> float:
    try:
        out = float(value)
    except Exception as exc:
        raise ValueError(f"{field_name} is not numeric: {value!r}") from exc
    if not math.isfinite(out):
        raise ValueError(f"{field_name} is not finite: {value!r}")
    return out


def _validate_ohlcv(candle: Dict[str, Any]) -> Dict[str, float]:
    open_value = _to_float(candle.get("open"), "open")
    high_value = _to_float(candle.get("high"), "high")
    low_value = _to_float(candle.get("low"), "low")
    close_value = _to_float(candle.get("close"), "close")
    volume_value = _to_float(candle.get("volume"), "volume")

    if volume_value < 0:
        raise ValueError(f"volume is negative: {volume_value!r}")
    if high_value < low_value:
        raise ValueError(f"high is below low: high={high_value!r} low={low_value!r}")
    if not (low_value <= open_value <= high_value):
        raise ValueError(
            f"open is outside high/low: open={open_value!r} "
            f"high={high_value!r} low={low_value!r}"
        )
    if not (low_value <= close_value <= high_value):
        raise ValueError(
            f"close is outside high/low: close={close_value!r} "
            f"high={high_value!r} low={low_value!r}"
        )

    return {
        "open": open_value,
        "high": high_value,
        "low": low_value,
        "close": close_value,
        "volume": volume_value,
    }


def _nth_weekday_of_month(year: int, month: int, weekday: int, nth: int) -> int:
    first = datetime(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return 1 + offset + ((nth - 1) * 7)


def _eastern_timezone_for_utc(dt_utc: datetime) -> timezone:
    year = dt_utc.year
    dst_start_day = _nth_weekday_of_month(year, 3, 6, 2)
    dst_end_day = _nth_weekday_of_month(year, 11, 6, 1)
    dst_start_utc = datetime(year, 3, dst_start_day, 7, 0, tzinfo=timezone.utc)
    dst_end_utc = datetime(year, 11, dst_end_day, 6, 0, tzinfo=timezone.utc)

    if dst_start_utc <= dt_utc < dst_end_utc:
        return timezone(timedelta(hours=-4))
    return timezone(timedelta(hours=-5))


def _candle_datetime_et(candle: Dict[str, Any]) -> datetime:
    raw_time = candle.get("time_iso")
    if not raw_time:
        raise ValueError(f"candle missing time_iso: {candle!r}")

    normalized = str(raw_time).replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        raise ValueError(f"candle timestamp is naive: {raw_time!r}")
    dt_utc = dt.astimezone(timezone.utc)
    return dt_utc.astimezone(_eastern_timezone_for_utc(dt_utc))


def _source_as_of_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _is_rth_bar(dt_et: datetime) -> bool:
    if dt_et.weekday() >= 5:
        return False
    return time(9, 30) <= dt_et.time() < time(16, 0)


def _source_rows_from_candles(
    *,
    symbol: str,
    candles: Iterable[Dict[str, Any]],
    source_as_of: str,
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    for candle in candles:
        dt_et = _candle_datetime_et(candle)
        if not _is_rth_bar(dt_et):
            continue

        ohlcv = _validate_ohlcv(candle)
        rows.append(
            {
                "symbol": symbol,
                "timestamp": dt_et.isoformat(timespec="seconds"),
                "timezone": "America/New_York",
                "session_date": dt_et.date().isoformat(),
                "session_type": "regular",
                "regular_session": "true",
                "timeframe": "1h_rth",
                "open": str(ohlcv["open"]),
                "high": str(ohlcv["high"]),
                "low": str(ohlcv["low"]),
                "close": str(ohlcv["close"]),
                "volume": str(ohlcv["volume"]),
                "source": "dxlink_candles.get_1h_ema50_snapshot",
                "source_as_of": source_as_of,
                "data_vendor": "dxFeed via tastytrade dxLink",
                "context_24h_status": "CONTEXT_24H_DAILY_UNCONFIRMED",
                "context_24h_as_of": "",
                "macro_context_status": "MACRO_UNCONFIRMED",
                "macro_context_as_of": "",
                "iv_context_status": "IV_UNCONFIRMED",
                "iv_context_as_of": "",
                "event_context_status": "EVENT_UNCONFIRMED",
                "event_context_as_of": "",
                "notes": "OHLCV returned by dxLink; unavailable context fields UNCONFIRMED.",
            }
        )

    return rows


async def _export(args: argparse.Namespace) -> int:
    symbol = args.symbol.strip().upper()
    if symbol not in ALLOWED_SYMBOLS:
        raise RuntimeError(f"Unsupported symbol {symbol!r}; allowed: {sorted(ALLOWED_SYMBOLS)}")

    columns = _read_template_columns()
    output_path = Path(args.output)

    if args.dry_run:
        missing_env = [
            name
            for name in ("TT_CLIENT_ID", "TT_CLIENT_SECRET", "TT_REDIRECT_URI", "TT_REFRESH_TOKEN")
            if not os.getenv(name, "").strip()
        ]
        print("Dry run complete")
        print("No network request made")
        print("No file written")
        print(f"Symbol: {symbol}")
        print(f"Output path: {output_path}")
        print(f"Template columns: {len(columns)}")
        print(f"Output directory exists: {output_path.parent.exists()}")
        if missing_env:
            print(f"Missing environment variables: {', '.join(missing_env)}")
            return 1
        print("Required environment variables: present")
        return 0

    access_token = await _get_access_token()
    from dxlink_candles import get_1h_ema50_snapshot

    snapshot = await get_1h_ema50_snapshot(
        symbol=symbol,
        access_token=access_token,
        api_base=API_BASE,
        user_agent=USER_AGENT,
        days_back=args.days_back,
    )
    candles = snapshot.get("all_candles") or []
    source_as_of = _source_as_of_utc()
    rows = _source_rows_from_candles(
        symbol=symbol,
        candles=candles,
        source_as_of=source_as_of,
    )

    if not rows:
        raise RuntimeError("No valid RTH OHLCV candle rows returned; no CSV written")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Rows written: {len(rows)}")
    print(f"Output path: {output_path}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Export read-only tastytrade/dxLink RTH OHLCV candles to the "
            "Historical Signal Replay v1 source CSV format."
        )
    )
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL, help="Allowed symbol to export")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="CSV output path",
    )
    parser.add_argument(
        "--days-back",
        type=int,
        default=DEFAULT_DAYS_BACK,
        help="Requested candle lookback days; dxLink helper may enforce a larger warmup",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate local setup without making network requests or writing a file",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    return asyncio.run(_export(args))


if __name__ == "__main__":
    raise SystemExit(main())
