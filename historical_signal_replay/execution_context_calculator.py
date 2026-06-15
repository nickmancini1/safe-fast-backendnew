from datetime import datetime
from decimal import Decimal, InvalidOperation


class ExecutionContextCalculatorError(ValueError):
    """Base error for QQQ CFB execution-context calculation failures."""


class UnsafeInferenceError(ExecutionContextCalculatorError):
    pass


CLEAN_QUOTE_AGE_SECONDS_MAX = Decimal("60")
CAUTION_QUOTE_AGE_SECONDS_MAX = Decimal("300")
SPREAD_CAP = Decimal("0.15")
SPREAD_PCT_CAP = Decimal("0.02")
MIN_BID_SIZE = Decimal("1")
MIN_ASK_SIZE = Decimal("1")
MIN_TRADE_VOLUME = Decimal("1")

FORBIDDEN_OUTPUT_FIELDS = {
    "trade_choice",
    "chosen_trade",
    "fill",
    "actual_fill_data",
    "broker_order_account_data",
    "outcome_data",
    "pnl",
    "p&l",
    "proof",
    "proof_label",
    "profitability",
    "profitability_label",
    "readiness",
    "readiness_label",
    "ready",
    "candidate_ready",
}


def calculate_execution_context_from_fixture(fixture):
    return calculate_execution_context(
        signal_time=fixture.get("signal_time"),
        quote_time=fixture.get("quote_time"),
        bid=fixture.get("bid"),
        ask=fixture.get("ask"),
        spread=fixture.get("spread"),
        bid_size=fixture.get("bid_size"),
        ask_size=fixture.get("ask_size"),
        setup_time_trade_volume=fixture.get("setup_time_trade_volume"),
        fallback_candidate_present=fixture.get("fallback_candidate_present") is True,
        forbidden_fields_present=fixture.get("forbidden_fields_present") or [],
    )


def calculate_execution_context(
    *,
    signal_time,
    quote_time,
    bid,
    ask,
    spread,
    bid_size,
    ask_size,
    setup_time_trade_volume,
    fallback_candidate_present=False,
    forbidden_fields_present=None,
):
    errors = []
    ignored_forbidden_inputs = _known_forbidden_inputs(forbidden_fields_present or [])

    if _source_data_missing(
        quote_time=quote_time,
        bid=bid,
        ask=ask,
        spread=spread,
        bid_size=bid_size,
        ask_size=ask_size,
        setup_time_trade_volume=setup_time_trade_volume,
    ):
        return _result(
            status="unknown",
            quote_age_seconds=None,
            rejection_reason="missing_source_data",
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    signal_at = _parse_timestamp_or_error(signal_time, "signal_time", errors)
    quote_at = _parse_timestamp_or_error(quote_time, "quote_time", errors)
    if signal_at is None or quote_at is None:
        return _result(
            status="unknown",
            quote_age_seconds=None,
            rejection_reason="missing_or_invalid_timestamp",
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    quote_age_seconds = Decimal(str((signal_at - quote_at).total_seconds()))
    if quote_at > signal_at:
        return _result(
            status="fail",
            quote_age_seconds=quote_age_seconds,
            rejection_reason="quote_after_signal",
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    gate_reason = _gate_rejection_reason(
        bid=bid,
        ask=ask,
        spread=spread,
        bid_size=bid_size,
        ask_size=ask_size,
        setup_time_trade_volume=setup_time_trade_volume,
    )
    if gate_reason is not None:
        if fallback_candidate_present:
            gate_reason = "top_ranked_contract_failed_no_fallback"
        return _result(
            status="fail",
            quote_age_seconds=quote_age_seconds,
            rejection_reason=gate_reason,
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    if quote_age_seconds <= CLEAN_QUOTE_AGE_SECONDS_MAX:
        return _result(
            status="clean",
            quote_age_seconds=quote_age_seconds,
            rejection_reason=None,
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )
    if quote_age_seconds <= CAUTION_QUOTE_AGE_SECONDS_MAX:
        return _result(
            status="caution",
            quote_age_seconds=quote_age_seconds,
            rejection_reason=None,
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    return _result(
        status="fail",
        quote_age_seconds=quote_age_seconds,
        rejection_reason="quote_age_above_5_minutes",
        errors=errors,
        ignored_forbidden_inputs=ignored_forbidden_inputs,
    )


def refuse_unsafe_inference(inference_name):
    raise UnsafeInferenceError(
        "QQQ CFB execution-context calculator only classifies setup-time "
        f"execution context; it must not infer {inference_name}."
    )


def choose_trade(*_args, **_kwargs):
    refuse_unsafe_inference("trade_choice")


def calculate_pnl(*_args, **_kwargs):
    refuse_unsafe_inference("P&L")


def accept_proof(*_args, **_kwargs):
    refuse_unsafe_inference("proof")


def mark_ready(*_args, **_kwargs):
    refuse_unsafe_inference("readiness")


def _gate_rejection_reason(
    *,
    bid,
    ask,
    spread,
    bid_size,
    ask_size,
    setup_time_trade_volume,
):
    bid_value = _decimal_or_none(bid)
    if bid_value is None:
        return "missing_bid"
    if bid_value < 0:
        return "bid_below_0"

    ask_value = _decimal_or_none(ask)
    if ask_value is None:
        return "missing_ask"
    if ask_value <= bid_value:
        return "ask_not_greater_than_bid"

    midpoint = (bid_value + ask_value) / Decimal("2")
    if midpoint <= 0:
        return "missing_or_non_positive_midpoint"

    spread_value = _decimal_or_none(spread)
    if spread_value is None:
        spread_value = ask_value - bid_value
    if spread_value > SPREAD_CAP:
        return "spread_above_0_15"

    spread_pct = spread_value / midpoint
    if spread_pct > SPREAD_PCT_CAP:
        return "spread_percent_above_2_percent"

    bid_size_value = _decimal_or_none(bid_size)
    if bid_size_value is None:
        return "missing_bid_size"
    if bid_size_value < MIN_BID_SIZE:
        return "bid_size_below_1"

    ask_size_value = _decimal_or_none(ask_size)
    if ask_size_value is None:
        return "missing_ask_size"
    if ask_size_value < MIN_ASK_SIZE:
        return "ask_size_below_1"

    volume_value = _decimal_or_none(setup_time_trade_volume)
    if volume_value is None:
        return "missing_trade_volume"
    if volume_value < MIN_TRADE_VOLUME:
        return "trade_volume_below_1"

    return None


def _result(
    *,
    status,
    quote_age_seconds,
    rejection_reason,
    errors,
    ignored_forbidden_inputs,
):
    return {
        "execution_context_status": status,
        "quote_age_seconds": _decimal_to_float(quote_age_seconds),
        "rejection_reason": rejection_reason,
        "errors": errors,
        "ignored_forbidden_inputs": ignored_forbidden_inputs,
    }


def _source_data_missing(
    *,
    quote_time,
    bid,
    ask,
    spread,
    bid_size,
    ask_size,
    setup_time_trade_volume,
):
    return all(
        value is None
        for value in (
            quote_time,
            bid,
            ask,
            spread,
            bid_size,
            ask_size,
            setup_time_trade_volume,
        )
    )


def _known_forbidden_inputs(field_names):
    return [
        field_name
        for field_name in field_names
        if field_name in FORBIDDEN_OUTPUT_FIELDS
    ]


def _parse_timestamp_or_error(value, field_name, errors):
    if value is None:
        errors.append(f"{field_name} is missing")
        return None
    try:
        return normalize_timestamp(value)
    except (ExecutionContextCalculatorError, ValueError) as exc:
        errors.append(f"{field_name} is invalid: {exc}")
        return None


def normalize_timestamp(value):
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if not text:
            raise ExecutionContextCalculatorError("timestamp is empty")
        parsed = datetime.fromisoformat(_trim_nanoseconds(text).replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        raise ExecutionContextCalculatorError(f"timestamp is missing timezone: {value!r}")
    return parsed


def _trim_nanoseconds(text):
    timezone_suffix = ""
    timestamp = text
    if text.endswith("Z"):
        timestamp = text[:-1]
        timezone_suffix = "Z"
    else:
        for separator_index in range(len(text) - 1, 9, -1):
            if text[separator_index] in "+-":
                timestamp = text[:separator_index]
                timezone_suffix = text[separator_index:]
                break

    if "." not in timestamp:
        return text

    prefix, fraction = timestamp.split(".", 1)
    return f"{prefix}.{fraction[:6]}{timezone_suffix}"


def _decimal_or_none(value):
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _decimal_to_float(value):
    if value is None:
        return None
    return float(value)
