import csv
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


class DatabentoOpraNormalizerError(ValueError):
    """Base error for Databento OPRA normalization failures."""


class MissingColumnError(DatabentoOpraNormalizerError):
    pass


class UnsafeInferenceError(DatabentoOpraNormalizerError):
    pass


_OPRA_SYMBOL_RE = re.compile(
    r"^(?P<underlying>[A-Z]+)\s*(?P<expiration>\d{6})(?P<side>[CP])(?P<strike>\d{8})$"
)

DEFINITION_COLUMNS = {
    "instrument_id",
    "symbol",
    "expiration",
    "instrument_class",
    "strike_price",
}

QUOTE_COLUMNS = {
    "instrument_id",
    "symbol",
    "ts_event",
    "ts_recv",
    "bid_px_00",
    "ask_px_00",
    "bid_sz_00",
    "ask_sz_00",
}

TRADE_COLUMNS = {
    "instrument_id",
    "symbol",
    "ts_event",
    "ts_recv",
    "price",
    "size",
}

STATISTICS_COLUMNS = {
    "instrument_id",
    "symbol",
    "ts_event",
    "ts_recv",
    "stat_type",
    "quantity",
}

STAT_TYPE_NAMES = {
    "6": "cleared_volume",
    6: "cleared_volume",
    "9": "open_interest",
    9: "open_interest",
}

FORBIDDEN_INFERENCES = {
    "fill",
    "fills",
    "trade",
    "trade_choice",
    "pnl",
    "p&l",
    "profitability",
    "proof",
    "readiness",
    "ready",
}


@dataclass(frozen=True)
class ParsedOpraSymbol:
    symbol: str
    underlying: str
    expiration: str
    side: str
    strike: Decimal


def parse_opra_symbol(symbol):
    compact = "".join(str(symbol).strip().split())
    match = _OPRA_SYMBOL_RE.match(compact)
    if not match:
        raise DatabentoOpraNormalizerError(
            f"Could not parse Databento OPRA option symbol: {symbol!r}"
        )

    expiration_raw = match.group("expiration")
    expiration = "20{}-{}-{}".format(
        expiration_raw[0:2],
        expiration_raw[2:4],
        expiration_raw[4:6],
    )
    strike = Decimal(match.group("strike")) / Decimal("1000")
    if strike == strike.to_integral_value():
        strike = strike.quantize(Decimal("1"))
    else:
        strike = strike.normalize()
    return ParsedOpraSymbol(
        symbol=str(symbol),
        underlying=match.group("underlying"),
        expiration=expiration,
        side=match.group("side"),
        strike=strike.normalize(),
    )


def normalize_timestamp(value):
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if not text:
            raise DatabentoOpraNormalizerError("Timestamp value is empty")
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        raise DatabentoOpraNormalizerError(
            f"Timestamp is missing timezone information: {value!r}"
        )
    return parsed.astimezone(timezone.utc)


def _decimal_or_none(value):
    text = str(value).strip()
    if text == "":
        return None
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise DatabentoOpraNormalizerError(
            f"Could not parse decimal value: {value!r}"
        ) from exc


def _require_columns(fieldnames, required_columns, source_name):
    present = set(fieldnames or ())
    missing = sorted(set(required_columns) - present)
    if missing:
        raise MissingColumnError(
            f"{source_name} missing required columns: {', '.join(missing)}"
        )


def _read_csv_rows(path, required_columns):
    csv_path = Path(path)
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames, required_columns, str(csv_path))
        return list(reader)


def load_definitions_csv(path):
    return [normalize_definition(row) for row in _read_csv_rows(path, DEFINITION_COLUMNS)]


def load_quotes_csv(path):
    return [normalize_quote(row) for row in _read_csv_rows(path, QUOTE_COLUMNS)]


def load_trades_csv(path):
    return [normalize_trade(row) for row in _read_csv_rows(path, TRADE_COLUMNS)]


def load_statistics_csv(path):
    return [
        normalize_statistic(row)
        for row in _read_csv_rows(path, STATISTICS_COLUMNS)
    ]


def normalize_definition(row):
    _require_columns(row.keys(), DEFINITION_COLUMNS, "definition row")
    parsed = parse_opra_symbol(row["symbol"])
    return {
        "instrument_id": str(row["instrument_id"]),
        "symbol": row["symbol"],
        "underlying": row.get("underlying") or parsed.underlying,
        "expiration": _date_only(row.get("expiration")) or parsed.expiration,
        "side": row.get("instrument_class") or parsed.side,
        "strike": _decimal_or_none(row.get("strike_price")) or parsed.strike,
        "contract_multiplier": _decimal_or_none(row.get("contract_multiplier", "")),
        "min_price_increment": _decimal_or_none(row.get("min_price_increment", "")),
    }


def normalize_quote(row):
    _require_columns(row.keys(), QUOTE_COLUMNS, "quote row")
    parsed = parse_opra_symbol(row["symbol"])
    bid = _decimal_or_none(row["bid_px_00"])
    ask = _decimal_or_none(row["ask_px_00"])
    quote = {
        "instrument_id": str(row["instrument_id"]),
        "symbol": row["symbol"],
        "ts_event": normalize_timestamp(row["ts_event"]),
        "ts_recv": normalize_timestamp(row["ts_recv"]),
        "bid": bid,
        "ask": ask,
        "bid_size": _decimal_or_none(row["bid_sz_00"]),
        "ask_size": _decimal_or_none(row["ask_sz_00"]),
        "underlying": parsed.underlying,
        "expiration": parsed.expiration,
        "side": parsed.side,
        "strike": parsed.strike,
    }
    quote.update(calculate_quote_spread_fields(quote))
    return quote


def normalize_trade(row):
    _require_columns(row.keys(), TRADE_COLUMNS, "trade row")
    parsed = parse_opra_symbol(row["symbol"])
    return {
        "instrument_id": str(row["instrument_id"]),
        "symbol": row["symbol"],
        "ts_event": normalize_timestamp(row["ts_event"]),
        "ts_recv": normalize_timestamp(row["ts_recv"]),
        "trade_price": _decimal_or_none(row["price"]),
        "trade_size": _decimal_or_none(row["size"]),
        "underlying": parsed.underlying,
        "expiration": parsed.expiration,
        "side": parsed.side,
        "strike": parsed.strike,
    }


def normalize_statistic(row):
    _require_columns(row.keys(), STATISTICS_COLUMNS, "statistics row")
    parsed = parse_opra_symbol(row["symbol"])
    stat_type = row["stat_type"]
    return {
        "instrument_id": str(row["instrument_id"]),
        "symbol": row["symbol"],
        "ts_event": normalize_timestamp(row["ts_event"]),
        "ts_recv": normalize_timestamp(row["ts_recv"]),
        "stat_type": stat_type,
        "stat_name": interpret_stat_type(stat_type),
        "quantity": _decimal_or_none(row["quantity"]),
        "underlying": parsed.underlying,
        "expiration": parsed.expiration,
        "side": parsed.side,
        "strike": parsed.strike,
    }


def _date_only(value):
    text = str(value or "").strip()
    if not text:
        return None
    return text[:10]


def calculate_quote_spread_fields(quote):
    bid = quote.get("bid")
    ask = quote.get("ask")
    if bid is None or ask is None:
        return {"midpoint": None, "spread": None, "spread_pct": None}

    midpoint = (bid + ask) / Decimal("2")
    spread = ask - bid
    spread_pct = None
    if midpoint > 0:
        spread_pct = spread / midpoint
    return {
        "midpoint": midpoint,
        "spread": spread,
        "spread_pct": spread_pct,
    }


def build_definition_index(definitions):
    index = {}
    for definition in definitions:
        index[("instrument_id", definition["instrument_id"])] = definition
        index[("symbol", definition["symbol"])] = definition
    return index


def join_rows_to_definitions(rows, definitions):
    index = build_definition_index(definitions)
    joined = []
    for row in rows:
        definition = index.get(("instrument_id", str(row.get("instrument_id"))))
        if definition is None:
            definition = index.get(("symbol", row.get("symbol")))
        if definition is None:
            raise DatabentoOpraNormalizerError(
                "No definition found for row instrument_id={} symbol={!r}".format(
                    row.get("instrument_id"),
                    row.get("symbol"),
                )
            )
        joined.append({**row, "definition": definition})
    return joined


def select_quote_at_or_before(quotes, signal_time, symbol=None, instrument_id=None):
    signal_at = normalize_timestamp(signal_time)
    selected = []
    for quote in quotes:
        if symbol is not None and quote.get("symbol") != symbol:
            continue
        if instrument_id is not None and str(quote.get("instrument_id")) != str(instrument_id):
            continue
        if quote["ts_event"] <= signal_at:
            selected.append(quote)

    if not selected:
        return None
    return max(selected, key=lambda row: row["ts_event"])


def interpret_stat_type(stat_type):
    return STAT_TYPE_NAMES.get(stat_type, STAT_TYPE_NAMES.get(str(stat_type), "unknown"))


def latest_statistics_by_symbol(statistics, at_or_before=None):
    cutoff = normalize_timestamp(at_or_before) if at_or_before is not None else None
    latest = {}
    for row in statistics:
        if cutoff is not None and row["ts_event"] > cutoff:
            continue
        stat_name = row.get("stat_name")
        if stat_name == "unknown":
            continue
        key = (row["symbol"], stat_name)
        existing = latest.get(key)
        if existing is None or row["ts_event"] > existing["ts_event"]:
            latest[key] = row
    return latest


def refuse_unsafe_inference(inference_name):
    normalized = str(inference_name).strip().lower()
    if normalized in FORBIDDEN_INFERENCES:
        raise UnsafeInferenceError(
            "Databento OPRA normalizer is read-only raw-data normalization; "
            f"it must not infer {inference_name}."
        )
    raise UnsafeInferenceError(
        "Databento OPRA normalizer does not perform SAFE-FAST evidence, "
        f"trade, execution, or readiness inference: {inference_name}."
    )


def infer_fill(*_args, **_kwargs):
    refuse_unsafe_inference("fill")


def choose_trade(*_args, **_kwargs):
    refuse_unsafe_inference("trade_choice")


def calculate_pnl(*_args, **_kwargs):
    refuse_unsafe_inference("P&L")


def mark_ready(*_args, **_kwargs):
    refuse_unsafe_inference("readiness")


def accept_proof(*_args, **_kwargs):
    refuse_unsafe_inference("proof")
