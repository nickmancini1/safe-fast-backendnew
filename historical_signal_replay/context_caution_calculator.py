from datetime import datetime


class ContextCautionCalculatorError(ValueError):
    """Base error for QQQ CFB context/caution calculation failures."""


class UnsafeInferenceError(ContextCautionCalculatorError):
    pass


EXPECTED_CANDIDATE_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
EXPECTED_SYMBOL = "QQQ"
EXPECTED_SETUP_TYPE = "Clean Fast Break"
ALLOWED_STATUSES = {"clean", "caution", "fail", "unknown"}
COMPLETE_PRECEDENCE = ("fail", "unknown", "caution", "clean")

COMPONENT_FIELDS = {
    "option_context_status",
    "headline_context_status",
    "execution_context_status",
}

COMPLETE_REQUIRED_COMPONENTS = (
    "gap_context_status",
    "lifecycle_status",
    "option_context_status",
    "headline_context_status",
    "execution_context_status",
)

MISSING_INPUT_REASONS = {
    "selected_contract_policy": "missing_selected_contract_policy",
    "historical_headline_source_policy": "missing_historical_headline_source_policy",
    "entry_timing_and_fill_assumption": "missing_entry_timing_and_fill_assumption",
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


def calculate_context_caution(
    *,
    component,
    candidate_id,
    symbol,
    setup_type,
    setup_time,
    component_inputs,
    expected_candidate_id=EXPECTED_CANDIDATE_ID,
    expected_symbol=EXPECTED_SYMBOL,
    expected_setup_type=EXPECTED_SETUP_TYPE,
):
    errors = []
    setup_at = _parse_timestamp_or_error(setup_time, "setup_time", errors)
    as_of = _isoformat_original_tz(setup_at) if setup_at is not None else None
    inputs = component_inputs or {}

    identity_reason = _identity_rejection_reason(
        candidate_id=candidate_id,
        symbol=symbol,
        setup_type=setup_type,
        expected_candidate_id=expected_candidate_id,
        expected_symbol=expected_symbol,
        expected_setup_type=expected_setup_type,
        errors=errors,
    )
    if identity_reason is not None:
        return _result(
            component=component,
            status="unknown",
            as_of=as_of,
            reviewed_before_signal=False,
            rejection_reason=identity_reason,
            errors=errors,
            ignored_forbidden_inputs=[],
        )

    if setup_at is None:
        return _result(
            component=component,
            status="unknown",
            as_of=None,
            reviewed_before_signal=False,
            rejection_reason="missing_or_invalid_setup_time",
            errors=errors,
            ignored_forbidden_inputs=[],
        )

    if component in COMPONENT_FIELDS:
        return _calculate_component_status(component, as_of, inputs)

    if component == "complete_caution_review_status":
        return _calculate_complete_caution(as_of, inputs)

    errors.append(f"component is unsupported: {component!r}")
    return _result(
        component=component,
        status="unknown",
        as_of=as_of,
        reviewed_before_signal=False,
        rejection_reason="unsupported_component",
        errors=errors,
        ignored_forbidden_inputs=[],
    )


def calculate_context_caution_from_fixture(fixture):
    return calculate_context_caution(
        component=fixture.get("component"),
        candidate_id=fixture.get("candidate_id"),
        symbol=fixture.get("symbol"),
        setup_type=fixture.get("setup_type"),
        setup_time=fixture.get("setup_time"),
        component_inputs=fixture.get("component_inputs"),
    )


def aggregate_complete_caution_status(component_statuses):
    normalized = [
        _normalize_complete_component_status(field_name, status)
        for field_name, status in component_statuses.items()
    ]
    if any(status is None for status in normalized):
        return "unknown"
    for status in COMPLETE_PRECEDENCE:
        if status in normalized:
            return status
    return "unknown"


def refuse_unsafe_inference(inference_name):
    raise UnsafeInferenceError(
        "QQQ CFB context/caution calculator only classifies setup-time "
        f"context/caution status; it must not infer {inference_name}."
    )


def choose_trade(*_args, **_kwargs):
    refuse_unsafe_inference("trade_choice")


def calculate_pnl(*_args, **_kwargs):
    refuse_unsafe_inference("P&L")


def accept_proof(*_args, **_kwargs):
    refuse_unsafe_inference("proof")


def mark_ready(*_args, **_kwargs):
    refuse_unsafe_inference("readiness")


def _calculate_component_status(component, as_of, inputs):
    future_reason = _component_future_rejection_reason(component, inputs)
    if future_reason is not None:
        return _result(
            component=component,
            status="unknown",
            as_of=as_of,
            reviewed_before_signal=False,
            rejection_reason=future_reason,
            errors=[],
            ignored_forbidden_inputs=_ignored_forbidden_inputs(inputs),
        )

    if inputs.get("missing_required_input") is True:
        missing_name = inputs.get("missing_input_name")
        return _result(
            component=component,
            status="unknown",
            as_of=as_of,
            reviewed_before_signal=False,
            rejection_reason=MISSING_INPUT_REASONS.get(
                missing_name,
                f"missing_required_input_{missing_name or 'unknown'}",
            ),
            errors=[],
            ignored_forbidden_inputs=[],
        )

    source_backed = inputs.get("source_backed_setup_time_inputs_present") is True
    accepted_rule = inputs.get("accepted_component_rule_present") is True
    status = inputs.get("accepted_fixture_component_status")
    if status is None:
        status = inputs.get("accepted_fixture_component_status_from_allowed_inputs")

    if not source_backed or not accepted_rule or status not in ALLOWED_STATUSES:
        return _result(
            component=component,
            status="unknown",
            as_of=as_of,
            reviewed_before_signal=False,
            rejection_reason="missing_source_backed_inputs_or_component_rule",
            errors=[],
            ignored_forbidden_inputs=[],
        )

    return _result(
        component=component,
        status=status,
        as_of=as_of,
        reviewed_before_signal=status != "unknown",
        rejection_reason=None if status != "unknown" else "component_status_unknown",
        errors=[],
        ignored_forbidden_inputs=[],
    )


def _calculate_complete_caution(as_of, inputs):
    forbidden_reason = _complete_forbidden_rejection_reason(inputs)
    missing_component = _missing_complete_component(inputs)
    if missing_component is not None:
        return _result(
            component="complete_caution_review_status",
            status="unknown",
            as_of=as_of,
            reviewed_before_signal=False,
            rejection_reason=f"missing_required_component_{missing_component}",
            errors=[],
            ignored_forbidden_inputs=_ignored_forbidden_inputs(inputs),
        )

    statuses = {
        field_name: inputs.get(field_name)
        for field_name in COMPLETE_REQUIRED_COMPONENTS
    }
    status = aggregate_complete_caution_status(statuses)

    if forbidden_reason is not None:
        return _result(
            component="complete_caution_review_status",
            status=status,
            as_of=as_of,
            reviewed_before_signal=False,
            rejection_reason=forbidden_reason,
            errors=[],
            ignored_forbidden_inputs=_ignored_forbidden_inputs(inputs),
        )

    rejection_reason = None
    reviewed_before_signal = status != "unknown"
    if status == "unknown":
        rejection_reason = "required_component_unknown"
        reviewed_before_signal = False

    return _result(
        component="complete_caution_review_status",
        status=status,
        as_of=as_of,
        reviewed_before_signal=reviewed_before_signal,
        rejection_reason=rejection_reason,
        errors=[],
        ignored_forbidden_inputs=[],
    )


def _identity_rejection_reason(
    *,
    candidate_id,
    symbol,
    setup_type,
    expected_candidate_id,
    expected_symbol,
    expected_setup_type,
    errors,
):
    if candidate_id != expected_candidate_id:
        errors.append(f"candidate_id is not {expected_candidate_id}")
        return "wrong_candidate_id"
    if symbol is None or str(symbol).strip().upper() != expected_symbol:
        errors.append(f"symbol is not {expected_symbol}")
        return "wrong_symbol"
    if setup_type != expected_setup_type:
        errors.append(f"setup_type is not {expected_setup_type}")
        return "wrong_setup_type"
    return None


def _component_future_rejection_reason(component, inputs):
    if component == "option_context_status" and (
        "forbidden_future_option_quote_time" in inputs
        or inputs.get("forbidden_future_inputs_present") is True
        and "forbidden_future_option_quote_claimed_status" in inputs
    ):
        return "ignored_future_option_quote"
    if component == "headline_context_status" and (
        "forbidden_future_headline_time" in inputs
        or inputs.get("forbidden_future_inputs_present") is True
        and "forbidden_future_headline_claimed_status" in inputs
    ):
        return "ignored_future_headline"
    return None


def _complete_forbidden_rejection_reason(inputs):
    forbidden_keys = {
        "actual_fill_data",
        "broker_order_account_data",
        "outcome_data",
        "pnl",
        "profitability_label",
        "readiness_label",
    }
    if any(key in inputs for key in forbidden_keys):
        return "ignored_fill_broker_order_account_outcome_pnl_profitability_readiness"
    return None


def _missing_complete_component(inputs):
    for field_name in COMPLETE_REQUIRED_COMPONENTS:
        if inputs.get(field_name) is None:
            return field_name
    return None


def _normalize_complete_component_status(field_name, status):
    if status is None:
        return None
    if field_name == "lifecycle_status":
        if status == "fresh":
            return "clean"
        if status in {"stale", "spent", "expired"}:
            return "fail"
        if status == "unknown":
            return "unknown"
        return None
    if status in ALLOWED_STATUSES:
        return status
    return None


def _ignored_forbidden_inputs(inputs):
    ignored = []
    for key in (
        "forbidden_future_option_quote_time",
        "forbidden_future_option_quote_claimed_status",
        "forbidden_future_headline_time",
        "forbidden_future_headline_claimed_status",
        "actual_fill_data",
        "broker_order_account_data",
        "outcome_data",
        "pnl",
        "profitability_label",
        "readiness_label",
    ):
        if key in inputs:
            ignored.append(key)
    return ignored


def _result(
    *,
    component,
    status,
    as_of,
    reviewed_before_signal,
    rejection_reason,
    errors,
    ignored_forbidden_inputs,
):
    return {
        component: status,
        "context_caution_status": status,
        "context_caution_as_of": as_of,
        "reviewed_before_signal": reviewed_before_signal,
        "rejection_reason": rejection_reason,
        "errors": errors,
        "ignored_forbidden_inputs": ignored_forbidden_inputs,
    }


def _parse_timestamp_or_error(value, field_name, errors):
    if value is None:
        errors.append(f"{field_name} is missing")
        return None
    try:
        return normalize_timestamp(value)
    except ContextCautionCalculatorError as exc:
        errors.append(f"{field_name} is invalid: {exc}")
        return None


def normalize_timestamp(value):
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if not text:
            raise ContextCautionCalculatorError("timestamp is empty")
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        raise ContextCautionCalculatorError(f"timestamp is missing timezone: {value!r}")
    return parsed


def _isoformat_original_tz(value):
    if value is None:
        return None
    return value.isoformat()
