from datetime import datetime
from decimal import Decimal, InvalidOperation


class CfbTradeRuleCheckerError(ValueError):
    """Base error for CFB trade-rule checker failures."""


class UnsafeInferenceError(CfbTradeRuleCheckerError):
    pass


STALE_QUOTE_AGE_SECONDS_MAX = Decimal("300")

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


def check_cfb_trade_rules_from_fixture(fixture):
    return check_cfb_trade_rules(
        candidate_id=fixture.get("candidate_id"),
        signal_time=fixture.get("signal_time"),
        selected_contract=fixture.get("selected_contract"),
        top_ranked_contract=fixture.get("top_ranked_contract"),
        quote_time=fixture.get("quote_time"),
        ask=fixture.get("ask"),
        execution_context_status=fixture.get("execution_context_status"),
        underlying_invalidation=fixture["underlying_invalidation"]
        if "underlying_invalidation" in fixture
        else "not_provided",
        entry_fill_basis=fixture.get("entry_fill_basis"),
        exit_rule_defined=fixture.get("exit_rule_defined"),
        time_exit_rule_defined=fixture.get("time_exit_rule_defined"),
        cost_slippage_defined=fixture.get("cost_slippage_defined"),
        sample_size_gate_defined=fixture.get("sample_size_gate_defined"),
        promotion_gate_defined=fixture.get("promotion_gate_defined"),
        attempted_promotion_stage=fixture.get("attempted_promotion_stage"),
        provided_rejection_reason=fixture["provided_rejection_reason"]
        if "provided_rejection_reason" in fixture
        else "not_provided",
        fallback_candidate_present=fixture.get("fallback_candidate_present") is True,
        forbidden_fields_present=fixture.get("forbidden_fields_present") or [],
    )


def check_cfb_trade_rules(
    *,
    candidate_id,
    signal_time=None,
    selected_contract=None,
    top_ranked_contract=None,
    quote_time=None,
    ask=None,
    execution_context_status=None,
    underlying_invalidation="not_provided",
    entry_fill_basis=None,
    exit_rule_defined=None,
    time_exit_rule_defined=None,
    cost_slippage_defined=None,
    sample_size_gate_defined=None,
    promotion_gate_defined=None,
    attempted_promotion_stage=None,
    provided_rejection_reason="not_provided",
    fallback_candidate_present=False,
    forbidden_fields_present=None,
):
    errors = []
    ignored_forbidden_inputs = _known_forbidden_inputs(forbidden_fields_present or [])

    if provided_rejection_reason is None:
        return _result(
            status="blocked",
            rejection_reason="failure_diagnosis_required",
            entry_price=None,
            quote_age_seconds=None,
            blocking_reasons=["failure_diagnosis_required"],
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    quote_age_seconds = _quote_age_seconds(signal_time, quote_time, errors)
    if quote_age_seconds is not None and quote_age_seconds < 0:
        return _result(
            status="no_trade",
            rejection_reason="quote_after_signal",
            entry_price=None,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=["quote_after_signal"],
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    if quote_age_seconds is not None and quote_age_seconds > STALE_QUOTE_AGE_SECONDS_MAX:
        return _result(
            status="no_trade",
            rejection_reason="quote_age_above_5_minutes",
            entry_price=None,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=["quote_age_above_5_minutes"],
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    if attempted_promotion_stage is not None:
        return _check_promotion_gates(
            sample_size_gate_defined=sample_size_gate_defined,
            promotion_gate_defined=promotion_gate_defined,
            quote_age_seconds=quote_age_seconds,
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    entry_blocker = _entry_blocker(
        selected_contract=selected_contract,
        top_ranked_contract=top_ranked_contract,
        quote_time=quote_time,
        ask=ask,
        execution_context_status=execution_context_status,
        underlying_invalidation=underlying_invalidation,
        entry_fill_basis=entry_fill_basis,
        fallback_candidate_present=fallback_candidate_present,
    )
    if entry_blocker is not None:
        return _result(
            status="blocked",
            rejection_reason=entry_blocker,
            entry_price=None,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=[entry_blocker],
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    entry_price = _decimal_to_float(_decimal_or_none(ask))
    countable_blockers = _countable_result_blockers(
        exit_rule_defined=exit_rule_defined,
        time_exit_rule_defined=time_exit_rule_defined,
        cost_slippage_defined=cost_slippage_defined,
        sample_size_gate_defined=sample_size_gate_defined,
        promotion_gate_defined=promotion_gate_defined,
    )
    if countable_blockers:
        return _result(
            status="blocked_pre_backtest",
            rejection_reason=countable_blockers[0],
            entry_price=entry_price,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=countable_blockers,
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    return _result(
        status="entry_eligible",
        rejection_reason=None,
        entry_price=entry_price,
        quote_age_seconds=quote_age_seconds,
        blocking_reasons=[],
        errors=errors,
        ignored_forbidden_inputs=ignored_forbidden_inputs,
    )


def refuse_unsafe_inference(inference_name):
    raise UnsafeInferenceError(
        "CFB trade-rule checker only classifies accepted gate status; "
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


def _check_promotion_gates(
    *,
    sample_size_gate_defined,
    promotion_gate_defined,
    quote_age_seconds,
    errors,
    ignored_forbidden_inputs,
):
    if sample_size_gate_defined is False:
        reason = "sample_size_gate_missing"
    elif promotion_gate_defined is False:
        reason = "promotion_gate_missing"
    else:
        reason = None

    if reason is not None:
        return _result(
            status="blocked_promotion",
            rejection_reason=reason,
            entry_price=None,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=[reason],
            errors=errors,
            ignored_forbidden_inputs=ignored_forbidden_inputs,
        )

    return _result(
        status="promotion_gate_present",
        rejection_reason=None,
        entry_price=None,
        quote_age_seconds=quote_age_seconds,
        blocking_reasons=[],
        errors=errors,
        ignored_forbidden_inputs=ignored_forbidden_inputs,
    )


def _entry_blocker(
    *,
    selected_contract,
    top_ranked_contract,
    quote_time,
    ask,
    execution_context_status,
    underlying_invalidation,
    entry_fill_basis,
    fallback_candidate_present,
):
    if selected_contract is None:
        if top_ranked_contract is not None and fallback_candidate_present:
            return "top_ranked_contract_failed_no_fallback"
        return "missing_selected_contract"
    if quote_time is None or ask is None:
        return "missing_entry_quote"
    if _decimal_or_none(ask) is None:
        return "missing_entry_quote"
    if underlying_invalidation is None:
        return "missing_invalidation"
    if entry_fill_basis not in (None, "ask"):
        return "unsupported_entry_fill_basis"
    if execution_context_status == "fail":
        return "execution_context_failed"
    return None


def _countable_result_blockers(
    *,
    exit_rule_defined,
    time_exit_rule_defined,
    cost_slippage_defined,
    sample_size_gate_defined,
    promotion_gate_defined,
):
    blockers = []
    if exit_rule_defined is False:
        blockers.append("missing_exit_rule")
    if time_exit_rule_defined is False:
        blockers.append("missing_time_exit_rule")
    if cost_slippage_defined is False:
        blockers.append("missing_cost_slippage")
    if sample_size_gate_defined is False:
        blockers.append("sample_size_gate_missing")
    if promotion_gate_defined is False:
        blockers.append("promotion_gate_missing")
    return blockers


def _quote_age_seconds(signal_time, quote_time, errors):
    if signal_time is None or quote_time is None:
        return None
    signal_at = _parse_timestamp_or_error(signal_time, "signal_time", errors)
    quote_at = _parse_timestamp_or_error(quote_time, "quote_time", errors)
    if signal_at is None or quote_at is None:
        return None
    return Decimal(str((signal_at - quote_at).total_seconds()))


def _parse_timestamp_or_error(value, field_name, errors):
    try:
        return normalize_timestamp(value)
    except (CfbTradeRuleCheckerError, ValueError) as exc:
        errors.append(f"{field_name} is invalid: {exc}")
        return None


def normalize_timestamp(value):
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if not text:
            raise CfbTradeRuleCheckerError("timestamp is empty")
        parsed = datetime.fromisoformat(_trim_nanoseconds(text).replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        raise CfbTradeRuleCheckerError(f"timestamp is missing timezone: {value!r}")
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


def _known_forbidden_inputs(field_names):
    return [
        field_name
        for field_name in field_names
        if field_name in FORBIDDEN_OUTPUT_FIELDS
    ]


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


def _result(
    *,
    status,
    rejection_reason,
    entry_price,
    quote_age_seconds,
    blocking_reasons,
    errors,
    ignored_forbidden_inputs,
):
    return {
        "trade_rule_status": status,
        "rejection_reason": rejection_reason,
        "entry_fill_basis": "ask" if entry_price is not None else None,
        "entry_price": entry_price,
        "quote_age_seconds": _decimal_to_float(quote_age_seconds),
        "blocking_reasons": blocking_reasons,
        "errors": errors,
        "ignored_forbidden_inputs": ignored_forbidden_inputs,
    }
