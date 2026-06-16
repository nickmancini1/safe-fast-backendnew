from datetime import datetime, timezone


class CfbLifecycleCalculatorError(ValueError):
    """Base error for CFB lifecycle calculation failures."""


class UnsafeInferenceError(CfbLifecycleCalculatorError):
    pass


EXPECTED_SYMBOL = "QQQ"
EXPECTED_SETUP_TYPE = "Clean Fast Break"
EXPECTED_RULE = "same_candle_initial_break_freshness"
SUPPORTED_RULES = {
    EXPECTED_RULE,
    "spy_cfb_exact_signal_candle_freshness",
    "spy_ideal_exact_signal_candle_freshness",
}

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


def calculate_lifecycle(
    *,
    setup_type,
    signal_time,
    source_time,
    candidate_state_inputs,
    expected_symbol=EXPECTED_SYMBOL,
    expected_setup_type=EXPECTED_SETUP_TYPE,
):
    errors = []
    ignored_future_inputs = []

    signal_at = _parse_timestamp_or_error(signal_time, "signal_time", errors)
    source_at = _parse_timestamp_or_error(source_time, "source_time", errors)
    inputs = candidate_state_inputs or {}
    as_of = _isoformat_original_tz(source_at) if source_at is not None else None

    if candidate_state_inputs is None:
        errors.append("candidate_state_inputs is missing")

    rejection_reason = _future_rejection_reason(inputs)
    if rejection_reason is not None:
        ignored_future_inputs = _ignored_future_inputs(inputs)

    unknown_reason = _unknown_rejection_reason(
        setup_type=setup_type,
        signal_at=signal_at,
        source_at=source_at,
        inputs=inputs,
        errors=errors,
        expected_symbol=expected_symbol,
        expected_setup_type=expected_setup_type,
    )
    if unknown_reason is not None:
        return _result(
            status="unknown",
            as_of=as_of,
            reviewed_before_signal=False,
            rejection_reason=unknown_reason,
            errors=errors,
            ignored_future_inputs=ignored_future_inputs,
        )

    if _is_spent(inputs):
        return _result(
            status="spent",
            as_of=as_of,
            reviewed_before_signal=True,
            rejection_reason=rejection_reason,
            errors=[],
            ignored_future_inputs=ignored_future_inputs,
        )

    higher_base_rejection = _higher_base_refresh_rejection(inputs)
    if higher_base_rejection is not None:
        return _result(
            status="stale",
            as_of=as_of,
            reviewed_before_signal=True,
            rejection_reason=higher_base_rejection,
            errors=[],
            ignored_future_inputs=ignored_future_inputs,
        )

    if _is_fresh(signal_at, source_at, inputs):
        return _result(
            status="fresh",
            as_of=as_of,
            reviewed_before_signal=True,
            rejection_reason=rejection_reason,
            errors=[],
            ignored_future_inputs=ignored_future_inputs,
        )

    if _is_expired(source_at, inputs):
        return _result(
            status="expired",
            as_of=as_of,
            reviewed_before_signal=True,
            rejection_reason=rejection_reason,
            errors=[],
            ignored_future_inputs=ignored_future_inputs,
        )

    return _result(
        status="stale",
        as_of=as_of,
        reviewed_before_signal=True,
        rejection_reason=rejection_reason,
        errors=[],
        ignored_future_inputs=ignored_future_inputs,
    )


def calculate_lifecycle_from_fixture(fixture):
    return calculate_lifecycle(
        setup_type=fixture.get("setup_type"),
        signal_time=fixture.get("signal_time"),
        source_time=fixture.get("source_time"),
        candidate_state_inputs=fixture.get("candidate_state_inputs"),
        expected_symbol=_expected_symbol_from_fixture(fixture),
        expected_setup_type=fixture.get("expected_setup_type", EXPECTED_SETUP_TYPE),
    )


def refuse_unsafe_inference(inference_name):
    raise UnsafeInferenceError(
        "QQQ CFB lifecycle calculator only classifies setup-time lifecycle state; "
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


def _expected_symbol_from_fixture(fixture):
    candidate_id = str(fixture.get("candidate_id", ""))
    if candidate_id.startswith("SPY-"):
        return "SPY"
    if candidate_id.startswith("QQQ-"):
        return "QQQ"
    return EXPECTED_SYMBOL


def _result(
    *,
    status,
    as_of,
    reviewed_before_signal,
    rejection_reason,
    errors,
    ignored_future_inputs,
):
    return {
        "lifecycle_status": status,
        "lifecycle_as_of": as_of,
        "reviewed_before_signal": reviewed_before_signal,
        "rejection_reason": rejection_reason,
        "errors": errors,
        "ignored_future_inputs": ignored_future_inputs,
    }


def _unknown_rejection_reason(
    *,
    setup_type,
    signal_at,
    source_at,
    inputs,
    errors,
    expected_symbol,
    expected_setup_type,
):
    if setup_type != expected_setup_type:
        errors.append(f"setup_type is not {expected_setup_type}")
        return "wrong_setup_type"

    symbol = inputs.get("symbol")
    if symbol is None or str(symbol).strip().upper() != expected_symbol:
        errors.append(f"symbol is not {expected_symbol}")
        return "wrong_symbol"

    if inputs.get("trigger") is None:
        errors.append("trigger is missing")
        return "missing_required_trigger"

    if inputs.get("invalidation") is None:
        errors.append("invalidation is missing")
        return "missing_required_invalidation"

    if inputs.get("trigger_state") is None:
        errors.append("trigger_state is missing")
        return "missing_required_trigger_state_precedence_unknown"

    missing_core = (
        signal_at is None
        or source_at is None
        or inputs.get("stage") is None
        or inputs.get("prior_completed_break") is None
        or inputs.get("source_backed_row_ordering") is not True
    )
    if missing_core:
        errors.append(
            "timestamp, stage, prior_completed_break, or "
            "source_backed_row_ordering is missing"
        )
        return "missing_required_timestamp_stage_prior_state_or_row_ordering"

    if inputs.get("accepted_lifecycle_rule") not in SUPPORTED_RULES:
        errors.append("accepted_lifecycle_rule is missing or unsupported")
        return "missing_required_lifecycle_rule_metadata"

    return None


def _is_spent(inputs):
    if (
        inputs.get("higher_base_stage") is True
        and inputs.get("completed_breakout") is not True
    ):
        return False

    return (
        inputs.get("prior_completed_break") is True
        or inputs.get("follow_through_context") is True
        or inputs.get("trigger_state") in {"spent", "follow_through"}
        or inputs.get("current_state") == "spent"
    )


def _higher_base_refresh_rejection(inputs):
    if inputs.get("higher_base_stage") is not True:
        return None
    if inputs.get("completed_breakout") is not True:
        return None
    if inputs.get("new_higher_base_trigger") is not True:
        return "higher_base_refresh_missing_new_trigger"
    if inputs.get("new_higher_base_invalidation") is not True:
        return "higher_base_refresh_missing_new_invalidation"
    return None


def _is_fresh(signal_at, source_at, inputs):
    if inputs.get("trigger_state") != "triggered":
        return False

    if inputs.get("higher_base_stage") is True:
        return (
            inputs.get("new_higher_base_trigger") is True
            and inputs.get("new_higher_base_invalidation") is True
            and inputs.get("completed_breakout") is True
            and source_at == signal_at
        )

    return source_at == signal_at


def _is_expired(source_at, inputs):
    previously_fresh = inputs.get("previously_fresh_signal_time")
    if not previously_fresh:
        return False
    previous_at = normalize_timestamp(previously_fresh)
    return source_at > previous_at


def _future_rejection_reason(inputs):
    if "option_quote_context" in inputs:
        return "ignored_option_fill_pnl_profitability_readiness"
    if "forbidden_future_replay_row_time" in inputs:
        return "ignored_future_replay_row"
    if "forbidden_future_candle_time" in inputs:
        return "ignored_future_candle"
    return None


def _ignored_future_inputs(inputs):
    ignored = []
    for key in (
        "forbidden_future_replay_row_time",
        "forbidden_future_replay_row_state",
        "forbidden_future_candle_time",
        "option_quote_context",
        "fill_assumption",
        "pnl",
        "profitability_label",
        "readiness_label",
    ):
        if key in inputs:
            ignored.append(key)
    return ignored


def _parse_timestamp_or_error(value, field_name, errors):
    if value is None:
        errors.append(f"{field_name} is missing")
        return None
    try:
        return normalize_timestamp(value)
    except CfbLifecycleCalculatorError as exc:
        errors.append(f"{field_name} is invalid: {exc}")
        return None


def normalize_timestamp(value):
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if not text:
            raise CfbLifecycleCalculatorError("timestamp is empty")
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        raise CfbLifecycleCalculatorError(f"timestamp is missing timezone: {value!r}")
    return parsed


def _isoformat_original_tz(value):
    if value is None:
        return None
    return value.isoformat()


def _isoformat_utc(value):
    return value.astimezone(timezone.utc).isoformat()
