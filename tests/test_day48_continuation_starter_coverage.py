import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_REPLAY_DIR = ROOT / "historical_signal_replay"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(HISTORICAL_REPLAY_DIR) not in sys.path:
    sys.path.insert(0, str(HISTORICAL_REPLAY_DIR))

from historical_signal_replay import cfb_contract_selector
from historical_signal_replay import cfb_lifecycle_calculator
from historical_signal_replay import context_caution_calculator
from historical_signal_replay import execution_context_calculator
from metrics import build_lifecycle_summary
from signal_replay import validate_lifecycle_fixture


STARTER_FIXTURE = (
    HISTORICAL_REPLAY_DIR / "fixtures" / "continuation_starter_coverage_fixtures.json"
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


def _starter_cases():
    fixture = _load_json(STARTER_FIXTURE)
    return fixture["cases"], fixture["lifecycle_rule"]


def _row_at(rows, one_based_index):
    return deepcopy(rows[one_based_index - 1]["expected_output_shape"])


def _lifecycle_fixture(case, row, *, signal_row):
    return {
        "candidate_id": case["candidate_id"],
        "expected_setup_type": "Continuation",
        "setup_type": row["setup_type"],
        "signal_time": signal_row["timestamp"],
        "source_time": row["timestamp"],
        "candidate_state_inputs": {
            "symbol": row["symbol"],
            "stage": row["stage"],
            "trigger": row.get("trigger_level"),
            "invalidation": row.get("invalidation"),
            "trigger_state": row.get("trigger_state"),
            "current_state": row.get("current_state"),
            "prior_completed_break": row["final_verdict"] == "NO_TRADE"
            and row.get("trigger_state") == "spent",
            "follow_through_context": row.get("trigger_state") == "spent",
            "accepted_lifecycle_rule": "continuation_exact_signal_candle_freshness",
            "source_backed_row_ordering": True,
            "forbidden_future_inputs_present": False,
        },
    }


def _contract_fixture(case, signal_row):
    return {
        "signal_time": signal_row["timestamp"],
        "trigger_price": signal_row.get("trigger_level"),
        "expected_symbol": case["expected_symbol"],
        "expected_setup_type": "Continuation",
        "open_interest_required": False,
        "candidate_contracts": [],
    }


def _complete_caution_fixture(case, signal_row, lifecycle_status, execution_status):
    return {
        "component": "complete_caution_review_status",
        "expected_candidate_id": case["candidate_id"],
        "expected_symbol": case["expected_symbol"],
        "expected_setup_type": "Continuation",
        "candidate_id": case["candidate_id"],
        "symbol": case["expected_symbol"],
        "setup_type": "Continuation",
        "setup_time": signal_row["timestamp"],
        "component_inputs": {
            "gap_context_status": "unknown",
            "lifecycle_status": lifecycle_status,
            "option_context_status": "unknown",
            "headline_context_status": "unknown",
            "execution_context_status": execution_status,
        },
    }


def _run_continuation_starter_package():
    package_cases, _rule = _starter_cases()
    results = []
    for case in package_cases:
        grouped_fixture = _load_grouped_fixture(case["grouped_fixture"])
        rows = grouped_fixture["lifecycle_rows"]
        output_rows = [deepcopy(row["expected_output_shape"]) for row in rows]
        signal_row = _row_at(rows, case["signal_row_index"])
        spent_row = _row_at(rows, case["spent_row_index"])
        final_row = output_rows[-1]

        signal_lifecycle = cfb_lifecycle_calculator.calculate_lifecycle_from_fixture(
            _lifecycle_fixture(case, signal_row, signal_row=signal_row)
        )
        final_lifecycle = cfb_lifecycle_calculator.calculate_lifecycle_from_fixture(
            _lifecycle_fixture(case, spent_row, signal_row=signal_row)
        )
        contract_selection = cfb_contract_selector.select_contract_from_fixture(
            _contract_fixture(case, signal_row)
        )
        execution_context = (
            execution_context_calculator.calculate_execution_context_from_fixture(
                {
                    "signal_time": signal_row["timestamp"],
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
        complete_caution = context_caution_calculator.calculate_context_caution_from_fixture(
            _complete_caution_fixture(
                case,
                signal_row,
                signal_lifecycle["lifecycle_status"],
                execution_context["execution_context_status"],
            )
        )

        result = {
            "candidate_identifier": case["candidate_id"],
            "evidence_source": case["evidence_source"],
            "chronological_stage_path": [row["stage"] for row in output_rows],
            "session_boundary_behavior": sorted(
                {row["timestamp"][:10] for row in output_rows}
            ),
            "candidate_qualification_result": {
                "accepted_entry_stages": [
                    row["timestamp"]
                    for row in output_rows
                    if row["final_verdict"] == "TRADE"
                ],
                "final_outcome": final_row["final_verdict"],
                "final_reason": final_row["primary_blocker"],
            },
            "contract_selection_result": contract_selection,
            "execution_result": execution_context,
            "context_caution_result": complete_caution,
            "winner_result": final_row["winner_selection_result"],
            "lifecycle_signal_result": signal_lifecycle,
            "lifecycle_final_result": final_lifecycle,
            "summary": build_lifecycle_summary(output_rows),
            "remaining_missing_evidence": case["remaining_missing_evidence"],
        }
        results.append(result)

    return {
        "candidate_count": len(results),
        "candidates": results,
        "totals": _totals(results),
    }


def _totals(results):
    return {
        "candidates_found": len(results),
        "runnable_candidates": len(results),
        "accepted_entry_stages": sum(
            len(result["candidate_qualification_result"]["accepted_entry_stages"])
            for result in results
        ),
        "final_entries": sum(
            1
            for result in results
            if result["candidate_qualification_result"]["final_outcome"] == "TRADE"
        ),
        "no_trades": sum(
            1
            for result in results
            if result["candidate_qualification_result"]["final_outcome"] == "NO_TRADE"
        ),
        "unresolved_cases": sum(
            1
            for result in results
            if result["context_caution_result"]["context_caution_status"] == "unknown"
        ),
        "blocked_cases": sum(
            1
            for result in results
            if result["candidate_qualification_result"]["final_reason"]
        ),
        "stable_cases": len(results),
        "unstable_cases": 0,
        "failures": 0,
    }


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


class Day48ContinuationStarterCoverageTests(unittest.TestCase):
    def test_continuation_starter_package_is_deterministic_across_two_runs(self):
        first = _run_continuation_starter_package()
        second = _run_continuation_starter_package()

        self.assertEqual(first, second)
        self.assertEqual(
            first["totals"],
            {
                "candidates_found": 4,
                "runnable_candidates": 4,
                "accepted_entry_stages": 2,
                "final_entries": 0,
                "no_trades": 4,
                "unresolved_cases": 4,
                "blocked_cases": 4,
                "stable_cases": 4,
                "unstable_cases": 0,
                "failures": 0,
            },
        )

    def test_continuation_starter_package_preserves_unknowns_and_abstentions(self):
        result = _run_continuation_starter_package()
        by_id = {
            candidate["candidate_identifier"]: candidate
            for candidate in result["candidates"]
        }

        self.assertEqual(
            "unknown",
            by_id["GLD-REAL-HISTORICAL-CONTINUATION-001"][
                "lifecycle_signal_result"
            ]["lifecycle_status"],
        )
        self.assertEqual(
            "unknown",
            by_id["IWM-REAL-HISTORICAL-CONTINUATION-001"][
                "lifecycle_signal_result"
            ]["lifecycle_status"],
        )
        self.assertEqual(
            "fresh",
            by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"][
                "lifecycle_signal_result"
            ]["lifecycle_status"],
        )
        self.assertEqual(
            "spent",
            by_id["SPY-REAL-HISTORICAL-CONTINUATION-001"][
                "lifecycle_final_result"
            ]["lifecycle_status"],
        )

        for candidate in result["candidates"]:
            with self.subTest(candidate=candidate["candidate_identifier"]):
                self.assertEqual(
                    "abstain",
                    candidate["contract_selection_result"]["contract_selection_status"],
                )
                self.assertEqual(
                    "unknown",
                    candidate["execution_result"]["execution_context_status"],
                )
                self.assertEqual(
                    "unknown",
                    candidate["context_caution_result"]["context_caution_status"],
                )
                self.assertEqual(
                    "NO_TRADE",
                    candidate["candidate_qualification_result"]["final_outcome"],
                )

    def test_continuation_starter_package_keeps_scope_clean(self):
        result = _run_continuation_starter_package()

        self.assertTrue(
            all(
                len(candidate["chronological_stage_path"]) == 6
                for candidate in result["candidates"]
            )
        )
        self.assertTrue(
            all(
                len(candidate["session_boundary_behavior"]) > 1
                for candidate in result["candidates"]
            )
        )
        self.assertEqual(
            [],
            _find_key_paths(
                result,
                {field.lower() for field in FORBIDDEN_EXECUTION_FIELDS},
            ),
        )


if __name__ == "__main__":
    unittest.main()
