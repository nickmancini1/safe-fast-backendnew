import csv
import json
import sys
import unittest
from copy import deepcopy
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_REPLAY_DIR = ROOT / "historical_signal_replay"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(HISTORICAL_REPLAY_DIR) not in sys.path:
    sys.path.insert(0, str(HISTORICAL_REPLAY_DIR))

from historical_signal_replay import cfb_contract_selector
from historical_signal_replay import context_caution_calculator
from historical_signal_replay import execution_context_calculator
from metrics import build_lifecycle_summary
from signal_replay import validate_lifecycle_fixture


EXPANSION_FIXTURE = (
    HISTORICAL_REPLAY_DIR
    / "fixtures"
    / "day48_grouped_three_family_after_continuation_expansion_fixtures.json"
)

GROUPED_FIXTURE_NAMES = (
    "first_real_gld_clean_fast_break_replay_v1_fixture.json",
    "first_real_gld_continuation_replay_v1_fixture.json",
    "first_real_gld_ideal_replay_v1_fixture.json",
    "first_real_iwm_clean_fast_break_replay_v1_fixture.json",
    "first_real_iwm_continuation_replay_v1_fixture.json",
    "first_real_iwm_ideal_replay_v1_fixture.json",
    "first_real_qqq_clean_fast_break_replay_v1_fixture.json",
    "first_real_qqq_continuation_replay_v1_fixture.json",
    "first_real_qqq_ideal_replay_v1_fixture.json",
    "first_real_spy_continuation_replay_v1_fixture.json",
    "second_real_spy_ideal_replay_v1_fixture.json",
    "third_real_spy_clean_fast_break_replay_v1_fixture.json",
)

FORBIDDEN_EXECUTION_FIELDS = {
    "account_id",
    "account_size",
    "broker_order_id",
    "buying_power",
    "live_trade_approval",
    "live_trade_decision",
    "live_trade_decisions",
    "order_id",
    "order_qty",
    "order_quantity",
    "order_status",
    "position_size",
    "qty",
    "quantity",
    "trade_approval",
    "trade_decision",
    "trade_decision_status",
    "trade_decisions",
}


def _load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _load_grouped_fixture(name):
    path = HISTORICAL_REPLAY_DIR / "fixtures" / name
    fixture = _load_json(path)
    validate_lifecycle_fixture(fixture)
    return fixture


def _expansion_cases():
    return _load_json(EXPANSION_FIXTURE)["continuation_option_cases"]


def _grouped_candidates():
    candidates = []
    for name in GROUPED_FIXTURE_NAMES:
        fixture = _load_grouped_fixture(name)
        rows = [
            deepcopy(row["expected_output_shape"])
            for row in fixture["lifecycle_rows"]
        ]
        final_row = rows[-1]
        source_data = fixture.get("source_data", {})
        candidates.append(
            {
                "candidate_identifier": fixture["fixture_name"],
                "setup_family": final_row["setup_type"],
                "symbol": source_data.get("symbol", final_row["symbol"]),
                "final_result": final_row["final_verdict"],
                "final_reason": final_row["primary_blocker"],
                "accepted_entry_rows": [
                    row for row in rows if row["final_verdict"] == "TRADE"
                ],
                "pending_rows": sum(
                    1 for row in rows if row["final_verdict"] == "PENDING"
                ),
                "summary": build_lifecycle_summary(rows),
            }
        )
    return candidates


def _run_expansion_package():
    results = []
    for case in _expansion_cases():
        contract_result = cfb_contract_selector.select_contract_from_fixture(case)
        execution_result = (
            execution_context_calculator.calculate_execution_context_from_fixture(
                {
                    "signal_time": case["signal_time"],
                    "quote_time": None,
                    "bid": None,
                    "ask": None,
                    "spread": None,
                    "bid_size": None,
                    "ask_size": None,
                    "setup_time_trade_volume": None,
                }
            )
        )
        complete_caution = (
            context_caution_calculator.calculate_context_caution_from_fixture(
                {
                    "component": "complete_caution_review_status",
                    "expected_candidate_id": case["candidate_id"],
                    "expected_symbol": case["expected_symbol"],
                    "expected_setup_type": "Continuation",
                    "candidate_id": case["candidate_id"],
                    "symbol": case["expected_symbol"],
                    "setup_type": "Continuation",
                    "setup_time": case["signal_time"],
                    "component_inputs": {
                        "gap_context_status": "unknown",
                        "lifecycle_status": (
                            "fresh"
                            if case["candidate_id"]
                            in {
                                "QQQ-REAL-HISTORICAL-CONTINUATION-001",
                                "SPY-REAL-HISTORICAL-CONTINUATION-001",
                            }
                            else "unknown"
                        ),
                        "option_context_status": "unknown",
                        "headline_context_status": "unknown",
                        "execution_context_status": execution_result[
                            "execution_context_status"
                        ],
                    },
                }
            )
        )
        results.append(
            {
                "candidate_id": case["candidate_id"],
                "symbol": case["expected_symbol"],
                "local_option_files_present": case["local_option_files_present"],
                "contract_result": contract_result,
                "execution_result": execution_result,
                "complete_caution": complete_caution,
            }
        )
    return {
        "continuation_option_cases": results,
        "totals": {
            "cases": len(results),
            "local_option_supported_cases": sum(
                1 for result in results if result["local_option_files_present"]
            ),
            "contract_abstentions": sum(
                1
                for result in results
                if result["contract_result"]["contract_selection_status"]
                == "abstain"
            ),
            "selected_contracts": sum(
                1
                for result in results
                if result["contract_result"]["contract_selection_status"]
                == "selected"
            ),
            "unknown_execution_cases": sum(
                1
                for result in results
                if result["execution_result"]["execution_context_status"]
                == "unknown"
            ),
            "unknown_complete_caution_cases": sum(
                1
                for result in results
                if result["complete_caution"]["complete_caution_review_status"]
                == "unknown"
            ),
        },
    }


def _derive_top_contract_from_local_rows(case):
    source_files = case.get("source_files")
    if not source_files:
        return None

    signal_at = _parse_timestamp(case["signal_time"])
    trigger = Decimal(str(case["trigger_price"]))
    definitions = []
    with (ROOT / source_files["definitions"]).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["underlying"] != case["expected_symbol"]:
                continue
            if row["instrument_class"] != "C":
                continue
            expiration = _parse_timestamp(row["expiration"]).date()
            dte = (expiration - signal_at.date()).days
            strike = _decimal_or_none(row["strike_price"])
            if dte >= 14 and strike is not None and strike >= trigger:
                definitions.append(
                    {
                        "instrument_id": row["instrument_id"],
                        "contract_symbol": row["raw_symbol"],
                        "expiration": expiration.isoformat(),
                        "dte": dte,
                        "strike": strike,
                    }
                )

    expiration = min(row["expiration"] for row in definitions)
    expiration_rows = [
        row for row in definitions if row["expiration"] == expiration
    ]
    strike = min(row["strike"] for row in expiration_rows)
    top = [row for row in expiration_rows if row["strike"] == strike][0]
    quote = _nearest_quote(ROOT / source_files["tcbbo"], top["instrument_id"], signal_at)
    volume = _trade_volume(ROOT / source_files["trades"], top["instrument_id"], signal_at)
    return {
        "contract_symbol": top["contract_symbol"],
        "instrument_id": top["instrument_id"],
        "expiration": top["expiration"],
        "dte": top["dte"],
        "strike": float(top["strike"]),
        "quote_ts_event": None if quote is None else quote["ts_event"],
        "trade_volume_through_setup": float(volume),
    }


def _nearest_quote(path, instrument_id, signal_at):
    timestamped = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["instrument_id"] == str(instrument_id):
                timestamped.append(row)
    if not timestamped:
        return None

    setup_safe = [
        row for row in timestamped if _parse_timestamp(row["ts_event"]) <= signal_at
    ]
    rows = setup_safe or timestamped
    return max(rows, key=lambda row: _parse_timestamp(row["ts_event"]))


def _trade_volume(path, instrument_id, signal_at):
    total = Decimal("0")
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["instrument_id"] != str(instrument_id):
                continue
            if _parse_timestamp(row["ts_event"]) <= signal_at:
                total += _decimal_or_none(row["size"]) or Decimal("0")
    return total


def _parse_timestamp(value):
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def _decimal_or_none(value):
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _find_key_paths(value, forbidden_fields, path=()):
    matches = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            nested_path = (*path, str(key))
            if str(key).lower() in forbidden_fields:
                matches.append(".".join(nested_path))
            matches.extend(_find_key_paths(nested_value, forbidden_fields, nested_path))
    elif isinstance(value, list):
        for index, nested_value in enumerate(value):
            matches.extend(
                _find_key_paths(nested_value, forbidden_fields, (*path, str(index)))
            )
    return matches


class Day48GroupedThreeFamilyExpansionAfterContinuationTests(unittest.TestCase):
    def test_continuation_option_contract_fixtures_match_local_rows_and_abstain(self):
        by_id = {case["candidate_id"]: case for case in _expansion_cases()}

        qqq_derived = _derive_top_contract_from_local_rows(
            by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"]
        )
        spy_derived = _derive_top_contract_from_local_rows(
            by_id["SPY-REAL-HISTORICAL-CONTINUATION-001"]
        )

        self.assertEqual(qqq_derived["contract_symbol"], "QQQ   260514C00665000")
        self.assertEqual(qqq_derived["trade_volume_through_setup"], 8.0)
        self.assertEqual(
            qqq_derived["quote_ts_event"],
            "2026-04-30T19:29:52.881394545Z",
        )
        self.assertEqual(spy_derived["contract_symbol"], "SPY   260514C00720000")
        self.assertEqual(
            spy_derived["quote_ts_event"],
            "2026-04-30T16:30:14.612354668Z",
        )

        package = _run_expansion_package()
        results = {
            result["candidate_id"]: result
            for result in package["continuation_option_cases"]
        }
        self.assertEqual(
            "top_ranked_contract_failed_no_fallback",
            results["QQQ-REAL-HISTORICAL-CONTINUATION-001"]["contract_result"][
                "rejection_reason"
            ],
        )
        self.assertEqual(
            "top_ranked_contract_failed_no_fallback",
            results["SPY-REAL-HISTORICAL-CONTINUATION-001"]["contract_result"][
                "rejection_reason"
            ],
        )
        self.assertEqual(
            "missing_or_invalid_signal_time_or_trigger",
            results["GLD-REAL-HISTORICAL-CONTINUATION-001"]["contract_result"][
                "rejection_reason"
            ],
        )
        self.assertEqual(
            {
                "cases": 4,
                "local_option_supported_cases": 2,
                "contract_abstentions": 4,
                "selected_contracts": 0,
                "unknown_execution_cases": 4,
                "unknown_complete_caution_cases": 4,
            },
            package["totals"],
        )

    def test_grouped_three_family_no_trade_and_ambiguous_controls_remain_unchanged(self):
        candidates = _grouped_candidates()
        package_first = _run_expansion_package()
        package_second = _run_expansion_package()

        self.assertEqual(package_first, package_second)
        self.assertEqual(len(candidates), 12)
        self.assertEqual(
            12,
            sum(1 for candidate in candidates if candidate["final_result"] == "NO_TRADE"),
        )
        self.assertEqual(
            7,
            sum(len(candidate["accepted_entry_rows"]) for candidate in candidates),
        )
        self.assertEqual(
            {"Clean Fast Break": 4, "Continuation": 4, "Ideal": 4},
            {
                family: sum(
                    1 for candidate in candidates if candidate["setup_family"] == family
                )
                for family in {"Clean Fast Break", "Continuation", "Ideal"}
            },
        )
        self.assertEqual(
            8,
            sum(1 for candidate in candidates if candidate["pending_rows"]),
        )

    def test_expansion_package_keeps_no_execution_scope(self):
        package = _run_expansion_package()

        self.assertEqual(
            [],
            _find_key_paths(
                package,
                {field.lower() for field in FORBIDDEN_EXECUTION_FIELDS},
            ),
        )


if __name__ == "__main__":
    unittest.main()
