from datetime import datetime
from decimal import Decimal, InvalidOperation


class CfbTradeRuleCheckerError(ValueError):
    """Base error for CFB trade-rule checker failures."""


class UnsafeInferenceError(CfbTradeRuleCheckerError):
    pass


STALE_QUOTE_AGE_SECONDS_MAX = Decimal("300")
ENTRY_SLIPPAGE_BUFFER = Decimal("0.02")
EXIT_SLIPPAGE_BUFFER = Decimal("0.02")
PROFIT_TARGET_PERCENT = Decimal("0.25")
OPTION_STOP_PERCENT = Decimal("-0.15")
MINIMUM_VALID_COMPLETED_CFB_EXAMPLES = 20

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
    if "expected_rule_status" in fixture:
        return check_cfb_exact_trade_values_from_fixture(fixture)

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


def check_cfb_exact_trade_values_from_fixture(fixture):
    return check_cfb_exact_trade_values(
        candidate_id=fixture.get("candidate_id"),
        setup_type=fixture.get("setup_type"),
        signal_time=fixture.get("signal_time"),
        signal_session=fixture.get("signal_session"),
        selected_contract=fixture.get("selected_contract"),
        top_ranked_contract=fixture.get("top_ranked_contract"),
        quote_time=fixture.get("quote_time"),
        bid=fixture.get("bid"),
        ask=fixture.get("ask"),
        option_context_status=fixture.get("option_context_status"),
        execution_context_status=fixture.get("execution_context_status"),
        underlying_invalidation=fixture.get("underlying_invalidation"),
        entry_side=fixture.get("entry_side"),
        entry_fill_basis=fixture.get("entry_fill_basis"),
        entry_ask=fixture.get("entry_ask"),
        exit_bid=fixture.get("exit_bid"),
        underlying_price_at_review=fixture.get("underlying_price_at_review"),
        review_time=fixture.get("review_time"),
        latest_exit_time_et=fixture.get("latest_exit_time_et"),
        provided_rejection_reason=fixture["provided_rejection_reason"]
        if "provided_rejection_reason" in fixture
        else "not_provided",
        known_blocker=fixture.get("known_blocker"),
        valid_completed_cfb_examples=fixture.get("valid_completed_cfb_examples"),
        accepted_rules=fixture.get("accepted_rules"),
        passing_replay_regression=fixture.get("passing_replay_regression"),
        positive_expectancy_review_after_costs=fixture.get(
            "positive_expectancy_review_after_costs"
        ),
        attempted_promotion_stage=fixture.get("attempted_promotion_stage"),
    )


def check_cfb_exact_trade_values(
    *,
    candidate_id,
    setup_type=None,
    signal_time=None,
    signal_session=None,
    selected_contract=None,
    top_ranked_contract=None,
    quote_time=None,
    bid=None,
    ask=None,
    option_context_status=None,
    execution_context_status=None,
    underlying_invalidation=None,
    entry_side=None,
    entry_fill_basis=None,
    entry_ask=None,
    exit_bid=None,
    underlying_price_at_review=None,
    review_time=None,
    latest_exit_time_et=None,
    provided_rejection_reason="not_provided",
    known_blocker=None,
    valid_completed_cfb_examples=None,
    accepted_rules=None,
    passing_replay_regression=None,
    positive_expectancy_review_after_costs=None,
    attempted_promotion_stage=None,
):
    errors = []
    quote_age_seconds = _quote_age_seconds(signal_time, quote_time, errors)

    if provided_rejection_reason is None:
        return _exact_result(
            status="blocked",
            rejection_reason="failure_diagnosis_required",
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=["failure_diagnosis_required"],
            errors=errors,
        )

    if known_blocker is not None and provided_rejection_reason is None:
        return _exact_result(
            status="blocked",
            rejection_reason="failure_diagnosis_required",
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=["failure_diagnosis_required"],
            errors=errors,
        )

    if quote_age_seconds is not None and quote_age_seconds < 0:
        return _exact_result(
            status="no_trade",
            rejection_reason="quote_after_signal",
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=["quote_after_signal"],
            errors=errors,
        )

    if quote_age_seconds is not None and quote_age_seconds > STALE_QUOTE_AGE_SECONDS_MAX:
        return _exact_result(
            status="no_trade",
            rejection_reason="quote_age_above_5_minutes",
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=["quote_age_above_5_minutes"],
            errors=errors,
        )

    if attempted_promotion_stage is not None:
        return _check_exact_promotion_gates(
            valid_completed_cfb_examples=valid_completed_cfb_examples,
            accepted_rules=accepted_rules,
            passing_replay_regression=passing_replay_regression,
            positive_expectancy_review_after_costs=positive_expectancy_review_after_costs,
            quote_age_seconds=quote_age_seconds,
            errors=errors,
        )

    zero_cost_blocker = _zero_cost_blocker(ask=ask, entry_ask=entry_ask, exit_bid=exit_bid)
    if zero_cost_blocker is not None:
        return _exact_result(
            status="blocked",
            rejection_reason=zero_cost_blocker,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=[zero_cost_blocker],
            errors=errors,
        )

    entry_basis = _adjusted_entry_basis(entry_ask if entry_ask is not None else ask)
    exit_basis = _adjusted_exit_basis(exit_bid)
    exit_reason = _accepted_exit_reason(
        cost_adjusted_entry_basis=entry_basis,
        cost_adjusted_exit_basis=exit_basis,
        underlying_invalidation=underlying_invalidation,
        underlying_price_at_review=underlying_price_at_review,
        review_time=review_time,
        latest_exit_time_et=latest_exit_time_et,
        signal_session=signal_session,
    )

    if exit_reason is not None:
        return _exact_result(
            status="exit_rule_value_fixture",
            rejection_reason=None,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=[],
            errors=errors,
            cost_adjusted_entry_basis=entry_basis,
            cost_adjusted_exit_basis=exit_basis,
            exit_reason=exit_reason,
        )

    if entry_ask is not None or entry_fill_basis == "ask_plus_slippage":
        return _exact_result(
            status="cost_rule_value_fixture",
            rejection_reason=None,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=[],
            errors=errors,
            cost_adjusted_entry_basis=entry_basis,
            cost_adjusted_exit_basis=exit_basis,
        )

    if exit_bid is not None:
        return _exact_result(
            status="cost_rule_value_fixture",
            rejection_reason=None,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=[],
            errors=errors,
            cost_adjusted_entry_basis=entry_basis,
            cost_adjusted_exit_basis=exit_basis,
        )

    entry_blocker = _exact_entry_blocker(
        setup_type=setup_type,
        selected_contract=selected_contract,
        top_ranked_contract=top_ranked_contract,
        quote_time=quote_time,
        ask=ask,
        option_context_status=option_context_status,
        execution_context_status=execution_context_status,
        underlying_invalidation=underlying_invalidation,
        entry_side=entry_side,
    )
    if entry_blocker is not None:
        return _exact_result(
            status="blocked",
            rejection_reason=entry_blocker,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=[entry_blocker],
            errors=errors,
        )

    return _exact_result(
        status="entry_rule_ready_awaiting_backtest_harness",
        rejection_reason=None,
        quote_age_seconds=quote_age_seconds,
        blocking_reasons=[],
        errors=errors,
        cost_adjusted_entry_basis=entry_basis,
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


def _check_exact_promotion_gates(
    *,
    valid_completed_cfb_examples,
    accepted_rules,
    passing_replay_regression,
    positive_expectancy_review_after_costs,
    quote_age_seconds,
    errors,
):
    example_count = valid_completed_cfb_examples or 0
    if example_count < MINIMUM_VALID_COMPLETED_CFB_EXAMPLES:
        reason = "sample_size_below_20"
    elif accepted_rules is not True:
        reason = "accepted_rules_missing"
    elif passing_replay_regression is not True:
        reason = "passing_replay_regression_missing"
    elif positive_expectancy_review_after_costs is not True:
        reason = "positive_expectancy_review_missing"
    else:
        reason = None

    if reason is not None:
        return _exact_result(
            status="blocked_promotion",
            rejection_reason=reason,
            quote_age_seconds=quote_age_seconds,
            blocking_reasons=[reason],
            errors=errors,
        )

    return _exact_result(
        status="promotion_gate_present",
        rejection_reason=None,
        quote_age_seconds=quote_age_seconds,
        blocking_reasons=[],
        errors=errors,
    )


def _exact_entry_blocker(
    *,
    setup_type,
    selected_contract,
    top_ranked_contract,
    quote_time,
    ask,
    option_context_status,
    execution_context_status,
    underlying_invalidation,
    entry_side,
):
    if setup_type not in (None, "Clean Fast Break"):
        return "unsupported_setup_type"
    if entry_side not in (None, "long_call"):
        return "unsupported_entry_side"
    if selected_contract is None:
        if top_ranked_contract is not None:
            return "top_ranked_contract_failed_no_fallback"
        return "missing_selected_contract"
    if quote_time is None or _decimal_or_none(ask) is None:
        return "missing_entry_quote"
    if option_context_status != "clean":
        return "option_context_not_passed"
    if execution_context_status != "clean":
        return "execution_context_not_passed"
    if underlying_invalidation is None:
        return "missing_invalidation"
    return None


def _zero_cost_blocker(*, ask, entry_ask, exit_bid):
    entry_value = _decimal_or_none(entry_ask if entry_ask is not None else ask)
    exit_value = _decimal_or_none(exit_bid)
    if entry_value is not None and entry_value <= 0:
        return "zero_cost_fill_forbidden"
    if exit_value is not None and exit_value <= 0:
        return "zero_cost_fill_forbidden"
    return None


def _adjusted_entry_basis(value):
    decimal_value = _decimal_or_none(value)
    if decimal_value is None:
        return None
    return decimal_value + ENTRY_SLIPPAGE_BUFFER


def _adjusted_exit_basis(value):
    decimal_value = _decimal_or_none(value)
    if decimal_value is None:
        return None
    return decimal_value - EXIT_SLIPPAGE_BUFFER


def _accepted_exit_reason(
    *,
    cost_adjusted_entry_basis,
    cost_adjusted_exit_basis,
    underlying_invalidation,
    underlying_price_at_review,
    review_time,
    latest_exit_time_et,
    signal_session,
):
    if (
        cost_adjusted_entry_basis is not None
        and cost_adjusted_exit_basis is not None
        and cost_adjusted_exit_basis
        >= cost_adjusted_entry_basis * (Decimal("1") + PROFIT_TARGET_PERCENT)
    ):
        return "profit_target"

    if (
        cost_adjusted_entry_basis is not None
        and cost_adjusted_exit_basis is not None
        and cost_adjusted_exit_basis
        <= cost_adjusted_entry_basis * (Decimal("1") + OPTION_STOP_PERCENT)
    ):
        return "option_premium_stop"

    invalidation = _decimal_or_none(underlying_invalidation)
    review_price = _decimal_or_none(underlying_price_at_review)
    if invalidation is not None and review_price is not None and review_price < invalidation:
        return "setup_invalidation_stop"

    if _is_time_exit(review_time, latest_exit_time_et, signal_session):
        return "time_exit_1545_et"

    return None


def _is_time_exit(review_time, latest_exit_time_et, signal_session):
    if review_time is None or latest_exit_time_et is None:
        return False
    try:
        review_at = normalize_timestamp(review_time)
    except (CfbTradeRuleCheckerError, ValueError):
        return False
    if signal_session is not None and review_at.date().isoformat() != str(signal_session):
        return False
    return review_at.strftime("%H:%M:%S") >= latest_exit_time_et


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


def _exact_result(
    *,
    status,
    rejection_reason,
    quote_age_seconds,
    blocking_reasons,
    errors,
    cost_adjusted_entry_basis=None,
    cost_adjusted_exit_basis=None,
    exit_reason=None,
):
    return {
        "trade_rule_status": status,
        "rejection_reason": rejection_reason,
        "entry_fill_basis": "ask_plus_slippage"
        if cost_adjusted_entry_basis is not None
        else None,
        "exit_fill_basis": "bid_minus_slippage"
        if cost_adjusted_exit_basis is not None
        else None,
        "cost_adjusted_entry_basis": _decimal_to_float(cost_adjusted_entry_basis),
        "cost_adjusted_exit_basis": _decimal_to_float(cost_adjusted_exit_basis),
        "exit_reason": exit_reason,
        "quote_age_seconds": _decimal_to_float(quote_age_seconds),
        "blocking_reasons": blocking_reasons,
        "errors": errors,
        "ignored_forbidden_inputs": [],
    }
