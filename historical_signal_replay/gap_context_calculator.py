from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation


class GapContextCalculatorError(ValueError):
    """Base error for QQQ gap-context calculation failures."""


class UnsafeInferenceError(GapContextCalculatorError):
    pass


CLEAN_ABS_GAP_PERCENT = Decimal("0.30")
CAUTION_ABS_GAP_PERCENT = Decimal("0.75")

FORBIDDEN_OUTPUT_FIELDS = {
    "trade_choice",
    "chosen_trade",
    "pnl",
    "p&l",
    "proof",
    "profitability",
    "readiness",
    "ready",
    "candidate_ready",
}


def calculate_gap_context(
    *,
    previous_close,
    signal_day_open,
    signal_time,
    latest_allowed_source_time,
    symbol=None,
    expected_symbol="QQQ",
    extra_source_times=None,
):
    errors = []
    rejected_future_source_times = []

    signal_at = _parse_timestamp_or_error(signal_time, "signal_time", errors)
    as_of_at = _parse_timestamp_or_error(
        latest_allowed_source_time,
        "latest_allowed_source_time",
        errors,
    )

    if signal_at is not None and as_of_at is not None and as_of_at > signal_at:
        errors.append("latest_allowed_source_time is after signal_time")

    for source_time in extra_source_times or ():
        parsed = _parse_timestamp_or_error(source_time, "extra_source_time", errors)
        if parsed is not None and signal_at is not None and parsed > signal_at:
            rejected_future_source_times.append(_isoformat_utc(parsed))

    if symbol is not None and str(symbol).strip().upper() != expected_symbol:
        errors.append(f"symbol is not {expected_symbol}")

    previous_close_decimal = _decimal_or_error(
        previous_close,
        "previous_close",
        errors,
    )
    signal_day_open_decimal = _decimal_or_error(
        signal_day_open,
        "signal_day_open",
        errors,
    )

    if previous_close_decimal is not None and previous_close_decimal <= 0:
        errors.append("previous_close must be greater than zero")

    if errors:
        return _result(
            gap_amount=None,
            gap_percent=None,
            direction="unknown",
            status="unknown",
            as_of=_isoformat_original_tz(as_of_at) if as_of_at is not None else None,
            reviewed_before_signal=False,
            errors=errors,
            rejected_future_source_times=rejected_future_source_times,
        )

    gap_amount = signal_day_open_decimal - previous_close_decimal
    gap_percent = (gap_amount / previous_close_decimal) * Decimal("100")
    direction = _direction(gap_amount)

    return _result(
        gap_amount=gap_amount,
        gap_percent=gap_percent,
        direction=direction,
        status=classify_gap_status(gap_percent),
        as_of=_isoformat_original_tz(as_of_at),
        reviewed_before_signal=True,
        errors=[],
        rejected_future_source_times=rejected_future_source_times,
    )


def calculate_gap_context_from_fixture(fixture):
    extra_source_times = []
    forbidden_future_source_time = fixture.get("forbidden_future_source_time")
    if forbidden_future_source_time:
        extra_source_times.append(forbidden_future_source_time)

    return calculate_gap_context(
        previous_close=fixture.get("previous_close"),
        signal_day_open=fixture.get("signal_day_open"),
        signal_time=fixture.get("signal_time"),
        latest_allowed_source_time=fixture.get("latest_allowed_source_time"),
        symbol=fixture.get("symbol"),
        extra_source_times=extra_source_times,
    )


def classify_gap_status(gap_percent):
    if gap_percent is None:
        return "unknown"

    abs_gap_percent = abs(_to_decimal(gap_percent))
    if abs_gap_percent <= CLEAN_ABS_GAP_PERCENT:
        return "clean"
    if abs_gap_percent <= CAUTION_ABS_GAP_PERCENT:
        return "caution"
    return "fail"


def refuse_unsafe_inference(inference_name):
    raise UnsafeInferenceError(
        "QQQ gap-context calculator only calculates setup-time gap context; "
        f"it must not infer {inference_name}."
    )


def choose_trade(*_args, **_kwargs):
    refuse_unsafe_inference("trade_choice")


def calculate_pnl(*_args, **_kwargs):
    refuse_unsafe_inference("P&L")


def accept_proof(*_args, **_kwargs):
    refuse_unsafe_inference("proof")


def mark_ready(*_args, **_kwargs):
    refuse_unsafe_inference("readiness")


def _result(
    *,
    gap_amount,
    gap_percent,
    direction,
    status,
    as_of,
    reviewed_before_signal,
    errors,
    rejected_future_source_times,
):
    return {
        "gap_amount": _decimal_to_float(gap_amount),
        "gap_percent": _decimal_to_float(gap_percent),
        "direction": direction,
        "gap_context_status": status,
        "gap_context_as_of": as_of,
        "gap_context_reviewed_before_signal": reviewed_before_signal,
        "errors": errors,
        "rejected_future_source_times": rejected_future_source_times,
    }


def _decimal_or_error(value, field_name, errors):
    if value is None:
        errors.append(f"{field_name} is missing")
        return None
    try:
        return _to_decimal(value)
    except GapContextCalculatorError as exc:
        errors.append(f"{field_name} is invalid: {exc}")
        return None


def _to_decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise GapContextCalculatorError(f"could not parse decimal value {value!r}") from exc


def _parse_timestamp_or_error(value, field_name, errors):
    if value is None:
        errors.append(f"{field_name} is missing")
        return None
    try:
        return normalize_timestamp(value)
    except GapContextCalculatorError as exc:
        errors.append(f"{field_name} is invalid: {exc}")
        return None


def normalize_timestamp(value):
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if not text:
            raise GapContextCalculatorError("timestamp is empty")
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        raise GapContextCalculatorError(f"timestamp is missing timezone: {value!r}")
    return parsed


def _isoformat_original_tz(value):
    if value is None:
        return None
    return value.isoformat()


def _isoformat_utc(value):
    return value.astimezone(timezone.utc).isoformat()


def _decimal_to_float(value):
    if value is None:
        return None
    return float(value)


def _direction(gap_amount):
    if gap_amount > 0:
        return "up"
    if gap_amount < 0:
        return "down"
    return "flat"
