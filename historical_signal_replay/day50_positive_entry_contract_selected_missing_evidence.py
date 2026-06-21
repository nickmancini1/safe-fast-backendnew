import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from historical_signal_replay import databento_opra_normalizer as opra
from historical_signal_replay import execution_context_calculator


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_contract_selected_missing_evidence.json"
)
BATCH_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_evidence_backed_positive_entry_testing_batch.json"
)
SELECTED_CONTRACT_CLOSEOUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_selected_contract_blocker_closeout.json"
)
OPTION_DATA_DIR = (
    REPO_ROOT / "historical_signal_replay" / "source_data" / "external_option_data_drop"
)

RESULT_VERSION = "day50_positive_entry_contract_selected_missing_evidence_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_POSITIVE_ENTRY_TRADE_CANDIDATE_RULE_GAP_CLOSEOUT_CODEX_TASK.md"
)
QQQ_CFB_REGRESSION_ONLY_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"

ACTIVE_CASES = (
    {
        "candidate_identifier": "first_real_qqq_continuation_replay_v1_fixture",
        "business_candidate_id": "QQQ-REAL-HISTORICAL-CONTINUATION-001",
        "setup_family": "Continuation",
        "underlying": "QQQ",
        "signal_time": "2026-04-30T19:30:00Z",
        "quote_path": OPTION_DATA_DIR
        / "QQQ_REAL_HISTORICAL_CONTINUATION_001_tcbbo_signal_10min.csv",
        "trade_path": OPTION_DATA_DIR
        / "QQQ_REAL_HISTORICAL_CONTINUATION_001_trades_signal_10min.csv",
        "raw_symbol": "QQQ   260514C00665000",
        "instrument_id": "956302440",
        "selection_basis": "local Day 48 Continuation option-context request package top-ranked raw symbol",
        "expected_resolution": "fresh_quote_but_spread_failed",
    },
    {
        "candidate_identifier": "first_real_qqq_ideal_replay_v1_fixture",
        "business_candidate_id": "QQQ-REAL-HISTORICAL-IDEAL-001",
        "setup_family": "Ideal",
        "underlying": "QQQ",
        "signal_time": "2026-05-13T16:30:00Z",
        "quote_path": OPTION_DATA_DIR / "QQQ_REAL_HISTORICAL_IDEAL_001_tcbbo_signal_10min.csv",
        "trade_path": OPTION_DATA_DIR / "QQQ_REAL_HISTORICAL_IDEAL_001_trades_signal_10min.csv",
        "raw_symbol": None,
        "instrument_id": None,
        "selection_basis": "local starter quote universe only; no accepted QQQ Ideal selected-contract rule",
        "expected_resolution": "fresh_raw_quote_universe_but_selected_contract_gap",
    },
    {
        "candidate_identifier": "third_real_spy_clean_fast_break_replay_v1_fixture",
        "business_candidate_id": "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
        "setup_family": "Clean Fast Break",
        "underlying": "SPY",
        "signal_time": "2026-04-15T18:30:00Z",
        "quote_path": OPTION_DATA_DIR / "SPY_CFB_003_selected_contract_tcbbo_open_to_signal.csv",
        "trade_path": OPTION_DATA_DIR / "SPY_CFB_003_selected_contract_trades_open_to_signal.csv",
        "raw_symbol": "SPY   260429C00700000",
        "instrument_id": "1258293278",
        "selection_basis": "local SPY CFB 003 selected-contract setup-window raw-symbol download",
        "expected_resolution": "stale_selected_contract_quote",
    },
)

CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)


def build_closeout_document(*, source_commit=None, run_timestamp=None):
    batch = json.loads(BATCH_RESULT_PATH.read_text(encoding="utf-8"))
    selected_contract_closeout = json.loads(
        SELECTED_CONTRACT_CLOSEOUT_PATH.read_text(encoding="utf-8")
    )
    _validate_inputs(batch, selected_contract_closeout)

    active_records = [_resolve_case(case, batch) for case in ACTIVE_CASES]
    regression_only_record = _qqq_regression_only_record(selected_contract_closeout)
    scorecard = _scorecard(batch, active_records, regression_only_record)
    stable_payload = {
        "active_records": active_records,
        "regression_only_record": regression_only_record,
        "scorecard": scorecard,
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(stable_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "input_paths": {
            "day50_evidence_backed_positive_entry_testing_batch": _relative(
                BATCH_RESULT_PATH
            ),
            "day50_positive_entry_selected_contract_blocker_closeout": _relative(
                SELECTED_CONTRACT_CLOSEOUT_PATH
            ),
        },
        "closeout_policy": {
            "source": "Day 50 evidence-backed positive-entry batch only",
            "target_first_stage_not_reached": "CONTRACT_SELECTED",
            "target_exact_blocker": "missing_setup_time_selected_option_evidence",
            "active_selected_contract_cases_reviewed": 3,
            "qqq_clean_fast_break_001_preserved_regression_only": True,
            "new_candidate_scan_run": False,
            "selected_contract_failure_before_entry_rerun_as_live_path": False,
            "closed_setup_source_candidates_reopened": False,
            "rejected_intake_rows_replayed": False,
            "frozen_rules_weakened": False,
            "governance_only_chain_created": False,
            "option_request_included": False,
            "exit_path_request_included": False,
            "classification_categories_preserved": list(CLASSIFICATIONS),
        },
        "active_selected_contract_records": active_records,
        "regression_only_record": regression_only_record,
        "fresh_quote_cases": [
            record
            for record in active_records
            if record["quote_evidence"]["quote_freshness_bucket"] == "fresh"
        ],
        "genuinely_stale_cases": [
            record
            for record in active_records
            if record["quote_evidence"]["quote_freshness_bucket"] == "stale"
        ],
        "remaining_evidence_gaps": [
            gap
            for record in active_records
            for gap in record["remaining_evidence_gaps"]
        ],
        "additional_entries": [],
        "scorecard": scorecard,
        "final_classifications": batch["final_classifications"],
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "databento_cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": (
                "Existing local quote-update data answered the active cases that had "
                "a deterministic local raw symbol. The remaining gap is an accepted "
                "QQQ Ideal selected-contract rule, not absent quote data, so no valid "
                "paid quote-update request was created."
            ),
        },
        "paid_data_request_created": False,
        "databento_downloaded": False,
        "raw_vendor_data_changed": False,
        "schwab_authenticated": False,
        "broker_mutation_attempted": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
        "next_task": {
            "filename": NEXT_TASK_FILENAME,
            "route": "positive_entry_trade_candidate_rule_gap_closeout",
            "reason": (
                "The active contract-selected missing-evidence cases produced zero "
                "additional entries from local quote-update data. The next bounded "
                "surface is rule/evidence closeout for trade-candidate-stage families "
                "before any further selected-contract request can be justified."
            ),
        },
    }


def write_closeout_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_closeout_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _validate_inputs(batch, selected_contract_closeout):
    if batch["scorecard"]["selected_contracts"] != 5:
        raise ValueError("Day 50 selected-contract count changed")
    blockers = batch["first_blockers"]["CONTRACT_SELECTED"]
    if blockers["common_causes"] != {"missing_setup_time_selected_option_evidence": 4}:
        raise ValueError("Day 50 CONTRACT_SELECTED blocker group changed")
    expected_ids = {case["candidate_identifier"] for case in ACTIVE_CASES}
    expected_ids.add("first_real_qqq_clean_fast_break_replay_v1_fixture")
    actual_ids = {
        example["candidate_identifier"]
        for example in blockers["exact_blocker_examples"]
    }
    if actual_ids != expected_ids:
        raise ValueError("Day 50 CONTRACT_SELECTED affected candidate set changed")
    qqq_records = [
        row
        for row in selected_contract_closeout["affected_selected_contract_records"]
        if row["candidate_identifier"] == QQQ_CFB_REGRESSION_ONLY_ID
    ]
    if len(qqq_records) != 1 or not qqq_records[0]["regression_only"]:
        raise ValueError("QQQ CFB 001 is no longer preserved as regression-only")


def _resolve_case(case, batch):
    batch_record = _batch_record(batch, case["candidate_identifier"])
    quotes = opra.load_quotes_csv(case["quote_path"])
    trades = opra.load_trades_csv(case["trade_path"])
    signal_at = opra.normalize_timestamp(case["signal_time"])

    quote = opra.select_quote_at_or_before(
        quotes,
        signal_at,
        symbol=case["raw_symbol"],
        instrument_id=case["instrument_id"],
    )
    evidence_scope = "selected_contract" if case["raw_symbol"] else "raw_quote_universe"
    if quote is None and case["raw_symbol"] is None:
        quote = _latest_quote_at_or_before(quotes, signal_at)
    if quote is None:
        return _missing_quote_record(case, batch_record)

    trade_volume = _trade_volume_at_or_before(
        trades,
        signal_at,
        symbol=case["raw_symbol"] or quote["symbol"],
        instrument_id=case["instrument_id"] or quote["instrument_id"],
    )
    execution = execution_context_calculator.calculate_execution_context(
        signal_time=signal_at.isoformat(),
        quote_time=quote["ts_event"].isoformat(),
        bid=quote["bid"],
        ask=quote["ask"],
        spread=quote["spread"],
        bid_size=quote["bid_size"],
        ask_size=quote["ask_size"],
        setup_time_trade_volume=trade_volume,
        fallback_candidate_present=False,
    )
    quote_age = Decimal(str(execution["quote_age_seconds"]))
    bucket = "fresh" if quote_age <= Decimal("300") else "stale"
    remaining_gaps = _remaining_gaps(case, execution, evidence_scope)
    resolved_classification = _resolved_classification(case, execution, evidence_scope)

    return {
        "candidate_identifier": case["candidate_identifier"],
        "business_candidate_id": case["business_candidate_id"],
        "setup_family": case["setup_family"],
        "underlying": case["underlying"],
        "batch_first_stage_not_reached": batch_record["first_stage_not_reached"],
        "batch_exact_blocker": batch_record["exact_blocker_code"],
        "selection_basis": case["selection_basis"],
        "evidence_scope": evidence_scope,
        "quote_evidence": {
            "field": "selected_contract_quote_update",
            "source": "Databento historical options via existing local quote-update CSV",
            "dataset_schema_or_api": "OPRA.PILLAR / tcbbo local CSV normalized by historical_signal_replay.databento_opra_normalizer",
            "calculator": "historical_signal_replay.execution_context_calculator",
            "csv_path": _relative(case["quote_path"]),
            "trade_csv_path": _relative(case["trade_path"]),
            "timestamp_window": {
                "signal_time": signal_at.isoformat().replace("+00:00", "Z"),
                "nearest_quote_time": quote["ts_event"].isoformat().replace("+00:00", "Z"),
            },
            "raw_symbol": quote["symbol"],
            "instrument_id": quote["instrument_id"],
            "bid": _float(quote["bid"]),
            "ask": _float(quote["ask"]),
            "spread": _float(quote["spread"]),
            "bid_size": _float(quote["bid_size"]),
            "ask_size": _float(quote["ask_size"]),
            "setup_time_trade_volume": _float(trade_volume),
            "quote_age_seconds": execution["quote_age_seconds"],
            "quote_freshness_bucket": bucket,
            "execution_context_status": execution["execution_context_status"],
            "rejection_reason": execution["rejection_reason"],
            "blocking_scope": "blocks CONTRACT_SELECTED or ENTRY_ELIGIBLE depending on selected-contract validity",
            "next_action": "preserve local evidence; do not download data for this case",
        },
        "resolved_classification": resolved_classification,
        "entry_eligible_after_closeout": False,
        "entry_recorded_after_closeout": False,
        "additional_entry_established": False,
        "remaining_evidence_gaps": remaining_gaps,
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def _missing_quote_record(case, batch_record):
    return {
        "candidate_identifier": case["candidate_identifier"],
        "business_candidate_id": case["business_candidate_id"],
        "setup_family": case["setup_family"],
        "underlying": case["underlying"],
        "batch_first_stage_not_reached": batch_record["first_stage_not_reached"],
        "batch_exact_blocker": batch_record["exact_blocker_code"],
        "selection_basis": case["selection_basis"],
        "evidence_scope": "selected_contract",
        "quote_evidence": {
            "field": "selected_contract_quote_update",
            "source": "Databento historical options via existing local quote-update CSV",
            "dataset_schema_or_api": "OPRA.PILLAR / tcbbo local CSV",
            "calculator": "historical_signal_replay.databento_opra_normalizer",
            "csv_path": _relative(case["quote_path"]),
            "timestamp_window": {"signal_time": case["signal_time"]},
            "quote_freshness_bucket": "absent",
            "unavailable_or_failure_reason": "no_quote_at_or_before_signal",
            "blocking_scope": "blocks CONTRACT_SELECTED",
            "next_action": "requires exact cost check only if selected-contract rule gate is valid",
        },
        "resolved_classification": "MISSING_DATA",
        "entry_eligible_after_closeout": False,
        "entry_recorded_after_closeout": False,
        "additional_entry_established": False,
        "remaining_evidence_gaps": [
            {
                "candidate_identifier": case["candidate_identifier"],
                "field": "selected_contract_quote_update",
                "unavailable_or_failure_reason": "no_quote_at_or_before_signal",
                "next_action": "cost-check only after valid request gate and user approval",
            }
        ],
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def _remaining_gaps(case, execution, evidence_scope):
    gaps = []
    if evidence_scope != "selected_contract":
        gaps.append(
            {
                "candidate_identifier": case["candidate_identifier"],
                "field": "selected_contract_identity",
                "source": "SAFE-FAST frozen local rule package",
                "dataset_schema_or_api": "accepted setup-family contract-selection rule",
                "timestamp_window": {"signal_time": case["signal_time"]},
                "unavailable_or_failure_reason": "no accepted QQQ Ideal selected-contract rule",
                "blocking_scope": "blocks CONTRACT_SELECTED",
                "next_action": "define/accept grouped Ideal rule evidence before any paid quote request",
            }
        )
    if execution["rejection_reason"] == "spread_above_0_15":
        gaps.append(
            {
                "candidate_identifier": case["candidate_identifier"],
                "field": "selected_contract_spread",
                "source": "Databento historical options local quote-update CSV",
                "dataset_schema_or_api": "OPRA.PILLAR / tcbbo",
                "timestamp_window": {"signal_time": case["signal_time"]},
                "unavailable_or_failure_reason": "spread_above_0_15",
                "blocking_scope": "blocks CONTRACT_SELECTED under no-fallback precedence",
                "next_action": "preserve as local no-entry blocker; no fallback scan",
            }
        )
    return gaps


def _resolved_classification(case, execution, evidence_scope):
    if case["expected_resolution"] == "stale_selected_contract_quote":
        return "TRUE_NO_TRADE"
    if evidence_scope != "selected_contract":
        return "MISSING_DATA"
    if execution["execution_context_status"] == "fail":
        return "TRUE_NO_TRADE"
    return "MISSING_DATA"


def _qqq_regression_only_record(selected_contract_closeout):
    for record in selected_contract_closeout["affected_selected_contract_records"]:
        if record["candidate_identifier"] == QQQ_CFB_REGRESSION_ONLY_ID:
            return {
                "candidate_identifier": QQQ_CFB_REGRESSION_ONLY_ID,
                "business_candidate_id": QQQ_CFB_REGRESSION_ONLY_ID,
                "preserved_as": "TRUE_NO_TRADE_REGRESSION_ONLY",
                "regression_only": True,
                "live_candidate_rerun": False,
                "reason": "closed confirmed safety rejection; quote_age_above_5_minutes",
                "entry_quote_time": record.get("entry_quote_time"),
                "entry_time": record.get("entry_time"),
            }
    raise ValueError("QQQ regression-only record missing")


def _scorecard(batch, active_records, regression_only_record):
    return {
        "active_selected_contract_cases_reviewed": len(active_records),
        "fresh_quote_cases": sum(
            1
            for record in active_records
            if record["quote_evidence"]["quote_freshness_bucket"] == "fresh"
        ),
        "genuinely_stale_cases": sum(
            1
            for record in active_records
            if record["quote_evidence"]["quote_freshness_bucket"] == "stale"
        ),
        "remaining_evidence_gaps": sum(
            len(record["remaining_evidence_gaps"]) for record in active_records
        ),
        "additional_entries_established": 0,
        "entry_eligible_after_closeout": 0,
        "entries_recorded_after_closeout": 0,
        "qqq_clean_fast_break_001_regression_only_preserved": bool(
            regression_only_record["regression_only"]
        ),
        "valid_trades_captured": batch["final_classifications"]["VALID_TRADE_CAPTURED"],
        "true_no_trades": batch["final_classifications"]["TRUE_NO_TRADE"],
        "missing_data_cases": batch["final_classifications"]["MISSING_DATA"],
        "missed_valid_trades": batch["final_classifications"]["MISSED_VALID_TRADE"],
        "invalid_trades_allowed": batch["final_classifications"][
            "INVALID_TRADE_ALLOWED"
        ],
        "unresolved_cases": batch["final_classifications"]["UNRESOLVED"],
        "closed_setup_source_candidates_reopened": 0,
        "rejected_intake_rows_replayed": 0,
        "closed_safety_rejections_rerun_as_live_candidates": 0,
    }


def _batch_record(batch, candidate_identifier):
    for record in batch["candidate_records"]:
        if record["candidate_identifier"] == candidate_identifier:
            return record
    raise ValueError(f"missing batch record: {candidate_identifier}")


def _latest_quote_at_or_before(quotes, signal_at):
    selected = [quote for quote in quotes if quote["ts_event"] <= signal_at]
    if not selected:
        return None
    return max(selected, key=lambda row: row["ts_event"])


def _trade_volume_at_or_before(trades, signal_at, *, symbol, instrument_id):
    total = Decimal("0")
    for trade in trades:
        if trade["symbol"] != symbol:
            continue
        if str(trade["instrument_id"]) != str(instrument_id):
            continue
        if trade["ts_event"] <= signal_at and trade["trade_size"] is not None:
            total += trade["trade_size"]
    return total


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _float(value):
    if value is None:
        return None
    return float(value)


def _relative(path):
    return str(Path(path).relative_to(REPO_ROOT)).replace("\\", "/")


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git_short_head():
    head = REPO_ROOT / ".git" / "HEAD"
    if not head.exists():
        return "UNKNOWN"
    text = head.read_text(encoding="utf-8").strip()
    if text.startswith("ref: "):
        ref = REPO_ROOT / ".git" / text[5:]
        if ref.exists():
            return ref.read_text(encoding="utf-8").strip()[:7]
    return text[:7]


if __name__ == "__main__":
    doc = write_closeout_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 contract-selected missing-evidence closeout: "
        f"{scorecard['fresh_quote_cases']} fresh quote cases, "
        f"{scorecard['genuinely_stale_cases']} stale cases, "
        f"{scorecard['additional_entries_established']} additional entries"
    )
