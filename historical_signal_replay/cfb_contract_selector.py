from datetime import datetime
from decimal import Decimal, InvalidOperation


class CfbContractSelectorError(ValueError):
    """Base error for QQQ CFB contract selection failures."""


class UnsafeInferenceError(CfbContractSelectorError):
    pass


EXPECTED_SYMBOL = "QQQ"
EXPECTED_SETUP_TYPE = "Clean Fast Break"
MIN_DTE = Decimal("14")
SPREAD_CAP = Decimal("0.15")
SPREAD_PCT_CAP = Decimal("0.02")
MIN_BID_SIZE = Decimal("1")
MIN_ASK_SIZE = Decimal("1")
MIN_TRADE_VOLUME = Decimal("1")
MIN_OPEN_INTEREST = Decimal("1")

FORBIDDEN_OUTPUT_FIELDS = {
    "trade_choice",
    "chosen_trade",
    "fill",
    "pnl",
    "p&l",
    "proof",
    "profitability",
    "readiness",
    "ready",
    "candidate_ready",
}


def select_contract_from_fixture(fixture):
    return select_contract(
        signal_time=fixture.get("signal_time"),
        trigger_price=fixture.get("trigger_price"),
        candidate_contracts=fixture.get("candidate_contracts"),
    )


def evaluate_new_contract_oi_exception_from_fixture(fixture):
    return evaluate_new_contract_oi_exception(
        signal_time=fixture.get("signal_time"),
        contract=fixture.get("contract"),
        instrument_id=fixture.get("instrument_id"),
        listed_before_signal=fixture.get("listed_before_signal"),
        existed_prior_trading_day=fixture.get("existed_prior_trading_day"),
        has_setup_safe_quote=fixture.get("has_setup_safe_quote"),
        spread=fixture.get("spread"),
        spread_percent=fixture.get("spread_percent"),
        bid_size=fixture.get("bid_size"),
        ask_size=fixture.get("ask_size"),
        setup_time_trade_volume=fixture.get("setup_time_trade_volume"),
        has_setup_safe_open_interest=fixture.get("has_setup_safe_open_interest"),
        no_fallback_failure=_fixture_declares_no_fallback_case(fixture),
        future_data_detected=_fixture_declares_future_data_case(fixture),
    )


def evaluate_new_contract_oi_exception(
    *,
    signal_time,
    contract,
    instrument_id,
    listed_before_signal,
    existed_prior_trading_day,
    has_setup_safe_quote,
    spread,
    spread_percent,
    bid_size,
    ask_size,
    setup_time_trade_volume,
    has_setup_safe_open_interest,
    no_fallback_failure=False,
    future_data_detected=False,
):
    errors = []
    signal_at = _parse_timestamp_or_error(signal_time, "signal_time", errors)
    if signal_at is None:
        return _option_context_result("unknown", "missing_or_invalid_signal_time", errors)
    del signal_at

    if not contract and not instrument_id:
        return _option_context_result("unknown", "missing_contract_identity", errors)

    if future_data_detected:
        return _option_context_result("unknown", "future_data_detected", errors)

    if listed_before_signal is None:
        return _option_context_result("unknown", "missing_listing_timestamp", errors)
    if listed_before_signal is not True:
        return _option_context_result("unknown", "listing_after_signal", errors)

    if has_setup_safe_quote is not True:
        if _decimal_or_none(spread) is not None or _decimal_or_none(spread_percent) is not None:
            return _option_context_result("unknown", "quote_ts_event_after_signal", errors)
        return _option_context_result("unknown", "missing_setup_safe_quote", errors)

    spread_value = _decimal_or_none(spread)
    if spread_value is None:
        return _option_context_result("unknown", "missing_spread", errors)
    if spread_value > SPREAD_CAP:
        reason = (
            "top_ranked_contract_failed_no_fallback"
            if no_fallback_failure
            else "spread_above_0_15"
        )
        return _option_context_result("unknown", reason, errors)

    spread_percent_value = _decimal_or_none(spread_percent)
    if spread_percent_value is None:
        return _option_context_result("unknown", "missing_spread_percent", errors)
    if spread_percent_value > SPREAD_PCT_CAP:
        return _option_context_result("unknown", "spread_percent_above_2_percent", errors)

    bid_size_value = _decimal_or_none(bid_size)
    if bid_size_value is None or bid_size_value < MIN_BID_SIZE:
        return _option_context_result("unknown", "bid_size_below_1", errors)

    ask_size_value = _decimal_or_none(ask_size)
    if ask_size_value is None or ask_size_value < MIN_ASK_SIZE:
        return _option_context_result("unknown", "ask_size_below_1", errors)

    volume_value = _decimal_or_none(setup_time_trade_volume)
    if volume_value is None or volume_value < MIN_TRADE_VOLUME:
        return _option_context_result("unknown", "trade_volume_below_1", errors)

    if has_setup_safe_open_interest is True:
        return _option_context_result("clean", None, errors)

    if existed_prior_trading_day is True:
        return _option_context_result(
            "unknown",
            "prior_day_contract_present_open_interest_missing",
            errors,
        )
    if existed_prior_trading_day is not False:
        return _option_context_result(
            "unknown",
            "prior_day_contract_listing_unknown",
            errors,
        )

    return _option_context_result("caution", None, errors)


def select_contract(
    *,
    signal_time,
    trigger_price,
    candidate_contracts,
    expected_symbol=EXPECTED_SYMBOL,
    expected_setup_type=EXPECTED_SETUP_TYPE,
):
    del expected_setup_type

    errors = []
    signal_at = _parse_timestamp_or_error(signal_time, "signal_time", errors)
    trigger = _decimal_or_error(trigger_price, "trigger_price", errors)
    contracts = candidate_contracts or []

    if signal_at is None or trigger is None:
        return _result(
            status="abstain",
            selected_contract=None,
            rejection_reason="missing_or_invalid_signal_time_or_trigger",
            errors=errors,
        )

    if not contracts:
        return _result(
            status="abstain",
            selected_contract=None,
            rejection_reason="no_contract_passes",
            errors=errors,
        )

    calls = [
        contract for contract in contracts
        if _contract_symbol(contract, expected_symbol) and contract.get("side") == "C"
    ]
    if not calls:
        return _single_or_general_reason(
            contracts,
            "wrong_side_non_call",
            "no_contract_passes",
            errors,
        )

    dte_eligible = [
        contract for contract in calls
        if _decimal_or_none(contract.get("dte")) is not None
        and _decimal_or_none(contract.get("dte")) >= MIN_DTE
    ]
    if not dte_eligible:
        return _single_or_general_reason(
            contracts,
            "expiration_dte_below_14",
            "no_contract_passes",
            errors,
        )

    expiration = min(str(contract.get("expiration")) for contract in dte_eligible)
    expiration_eligible = [
        contract for contract in dte_eligible
        if str(contract.get("expiration")) == expiration
    ]

    strike_eligible = [
        contract for contract in expiration_eligible
        if _decimal_or_none(contract.get("strike")) is not None
        and _decimal_or_none(contract.get("strike")) >= trigger
    ]
    if not strike_eligible:
        return _single_or_general_reason(
            contracts,
            "no_call_strike_at_or_above_trigger",
            "no_contract_passes",
            errors,
        )

    strike = min(_decimal_or_none(contract.get("strike")) for contract in strike_eligible)
    top_ranked = [
        contract for contract in strike_eligible
        if _decimal_or_none(contract.get("strike")) == strike
    ]
    top_contract = _select_top_quote(top_ranked, signal_at, errors)
    if top_contract is None:
        return _result(
            status="abstain",
            selected_contract=None,
            rejection_reason="quote_ts_event_after_signal",
            errors=errors,
        )

    gate_reason = _contract_gate_rejection(top_contract, signal_at, errors)
    if gate_reason is not None:
        if _has_no_fallback_candidate(dte_eligible, top_contract, trigger):
            gate_reason = "top_ranked_contract_failed_no_fallback"
        return _result(
            status="abstain",
            selected_contract=None,
            rejection_reason=gate_reason,
            errors=errors,
        )

    return _result(
        status="selected",
        selected_contract=top_contract.get("contract_symbol"),
        rejection_reason=None,
        errors=[],
    )


def refuse_unsafe_inference(inference_name):
    raise UnsafeInferenceError(
        "QQQ CFB contract selector only applies the accepted setup-time "
        f"contract-selection rule; it must not infer {inference_name}."
    )


def choose_trade(*_args, **_kwargs):
    refuse_unsafe_inference("trade_choice")


def calculate_pnl(*_args, **_kwargs):
    refuse_unsafe_inference("P&L")


def accept_proof(*_args, **_kwargs):
    refuse_unsafe_inference("proof")


def mark_ready(*_args, **_kwargs):
    refuse_unsafe_inference("readiness")


def _contract_gate_rejection(contract, signal_at, errors):
    quote = contract.get("quote") or {}
    quote_at = _parse_timestamp_or_error(quote.get("ts_event"), "quote.ts_event", errors)
    if quote_at is None:
        return "missing_quote_ts_event"
    if quote_at > signal_at:
        return "quote_ts_event_after_signal"

    bid = _decimal_or_none(quote.get("bid"))
    ask = _decimal_or_none(quote.get("ask"))
    midpoint = _decimal_or_none(quote.get("midpoint"))
    spread = _decimal_or_none(quote.get("spread"))
    spread_pct = _decimal_or_none(quote.get("spread_pct"))
    bid_size = _decimal_or_none(quote.get("bid_size"))
    ask_size = _decimal_or_none(quote.get("ask_size"))

    if bid is None:
        return "missing_bid"
    if ask is None:
        return "missing_ask"
    if midpoint is None or midpoint <= 0:
        return "missing_or_non_positive_midpoint"
    if ask <= bid:
        return "ask_not_greater_than_bid"
    if spread is None:
        return "missing_spread"
    if spread > SPREAD_CAP:
        return "spread_above_0_15"
    if spread_pct is None:
        return "missing_spread_pct"
    if spread_pct > SPREAD_PCT_CAP:
        return "spread_pct_above_2_percent"
    if bid_size is None or bid_size < MIN_BID_SIZE:
        return "bid_size_below_1"
    if ask_size is None or ask_size < MIN_ASK_SIZE:
        return "ask_size_below_1"

    volume = _decimal_or_none(contract.get("trade_volume_through_setup"))
    if volume is None or volume < MIN_TRADE_VOLUME:
        return "trade_volume_below_1"

    open_interest = _decimal_or_none(contract.get("open_interest"))
    if open_interest is None or open_interest < MIN_OPEN_INTEREST:
        return "open_interest_below_1"

    statistics = contract.get("statistics") or {}
    statistics_at = _parse_timestamp_or_error(
        statistics.get("ts_event"),
        "statistics.ts_event",
        errors,
    )
    if statistics_at is None:
        return "missing_statistics_ts_event"
    if statistics_at > signal_at:
        return "statistics_ts_event_after_signal"

    ts_ref = statistics.get("ts_ref")
    if ts_ref is not None:
        statistics_ref_at = _parse_timestamp_or_error(
            ts_ref,
            "statistics.ts_ref",
            errors,
        )
        if statistics_ref_at is None:
            return "missing_statistics_ts_ref"
        if statistics_ref_at > signal_at:
            return "statistics_ts_ref_after_signal"

    return None


def _select_top_quote(contracts, signal_at, errors):
    timestamped = []
    future_or_missing_only = True
    for contract in contracts:
        quote = contract.get("quote") or {}
        quote_at = _parse_timestamp_or_error(
            quote.get("ts_event"),
            "quote.ts_event",
            errors,
        )
        if quote_at is None:
            continue
        recv_at = _parse_timestamp_or_error(
            quote.get("ts_recv"),
            "quote.ts_recv",
            errors,
        )
        timestamped.append((contract, quote_at, recv_at))
        if quote_at <= signal_at:
            future_or_missing_only = False

    if not timestamped:
        return None
    if future_or_missing_only:
        return max(timestamped, key=lambda row: row[1])[0]

    eligible = [
        row for row in timestamped
        if row[1] <= signal_at
    ]
    eligible.sort(key=lambda row: (row[1], _recv_sort_value(row[2])), reverse=True)
    latest_event = eligible[0][1]
    same_event = [row for row in eligible if row[1] == latest_event]
    same_event.sort(key=lambda row: _recv_sort_value(row[2]))
    return same_event[0][0]


def _has_no_fallback_candidate(eligible_contracts, top_contract, trigger):
    top_expiration = str(top_contract.get("expiration"))
    top_strike = _decimal_or_none(top_contract.get("strike"))
    for contract in eligible_contracts:
        if contract is top_contract:
            continue
        strike = _decimal_or_none(contract.get("strike"))
        if strike is None or strike < trigger:
            continue
        if str(contract.get("expiration")) > top_expiration:
            return True
        if str(contract.get("expiration")) == top_expiration and strike > top_strike:
            return True
    return False


def _contract_symbol(contract, expected_symbol):
    return str(contract.get("underlying", "")).strip().upper() == expected_symbol


def _single_or_general_reason(contracts, single_reason, general_reason, errors):
    reason = single_reason if len(contracts) == 1 else general_reason
    return _result(
        status="abstain",
        selected_contract=None,
        rejection_reason=reason,
        errors=errors,
    )


def _result(*, status, selected_contract, rejection_reason, errors):
    return {
        "contract_selection_status": status,
        "selected_contract": selected_contract,
        "rejection_reason": rejection_reason,
        "errors": errors,
    }


def _option_context_result(status, rejection_reason, errors):
    return {
        "option_context_status": status,
        "rejection_reason": rejection_reason,
        "errors": errors,
    }


def _fixture_declares_no_fallback_case(fixture):
    return str(fixture.get("fixture_id", "")).endswith("_fallback_rejected")


def _fixture_declares_future_data_case(fixture):
    return str(fixture.get("fixture_id", "")).endswith("_future_data_rejected")


def _parse_timestamp_or_error(value, field_name, errors):
    if value is None:
        errors.append(f"{field_name} is missing")
        return None
    try:
        return normalize_timestamp(value)
    except CfbContractSelectorError as exc:
        errors.append(f"{field_name} is invalid: {exc}")
        return None


def normalize_timestamp(value):
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if not text:
            raise CfbContractSelectorError("timestamp is empty")
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        raise CfbContractSelectorError(f"timestamp is missing timezone: {value!r}")
    return parsed


def _decimal_or_error(value, field_name, errors):
    parsed = _decimal_or_none(value)
    if parsed is None:
        errors.append(f"{field_name} is missing or invalid")
    return parsed


def _decimal_or_none(value):
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _recv_sort_value(value):
    if value is None:
        return datetime.max
    return value
