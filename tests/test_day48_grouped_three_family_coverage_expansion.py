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

LOCAL_RULE_STACKS = {
    ("Clean Fast Break", "QQQ"): {
        "lifecycle": "qqq_cfb_lifecycle_regression_fixtures.json",
        "contract_selection": "qqq_cfb_contract_selection_regression_fixtures.json",
        "execution_context": "qqq_cfb_execution_context_regression_fixtures.json",
        "context_caution": "qqq_cfb_context_caution_regression_fixtures.json",
    },
    ("Clean Fast Break", "SPY"): {
        "lifecycle": "spy_cfb_lifecycle_regression_fixtures.json",
        "contract_selection": "spy_cfb_contract_selection_regression_fixtures.json",
        "execution_context": "spy_cfb_execution_context_regression_fixtures.json",
        "context_caution": "spy_cfb_context_caution_regression_fixtures.json",
    },
    ("Ideal", "SPY"): {
        "lifecycle": "spy_ideal_lifecycle_regression_fixtures.json",
        "contract_selection": "spy_ideal_contract_selection_regression_fixtures.json",
        "execution_context": "spy_ideal_execution_context_regression_fixtures.json",
        "context_caution": "spy_ideal_context_caution_regression_fixtures.json",
    },
}

MISSING_EXPANSION_DEPENDENCIES = {
    ("Continuation", "GLD"): (
        "Continuation-specific lifecycle rule fixtures",
        "Continuation contract-selection fixtures",
        "Continuation execution-context fixtures",
        "Continuation complete-caution fixtures",
        "setup-time-safe selected option data",
    ),
    ("Continuation", "IWM"): (
        "Continuation-specific lifecycle rule fixtures",
        "Continuation contract-selection fixtures",
        "Continuation execution-context fixtures",
        "Continuation complete-caution fixtures",
        "setup-time-safe selected option data",
    ),
    ("Continuation", "QQQ"): (
        "Continuation-specific lifecycle rule fixtures",
        "Continuation contract-selection fixtures",
        "Continuation execution-context fixtures",
        "Continuation complete-caution fixtures",
        "setup-time-safe selected option data",
    ),
    ("Continuation", "SPY"): (
        "Continuation-specific lifecycle rule fixtures",
        "Continuation contract-selection fixtures",
        "Continuation execution-context fixtures",
        "Continuation complete-caution fixtures",
        "setup-time-safe selected option data",
    ),
    ("Ideal", "GLD"): (
        "Ideal GLD starter option/rule fixtures",
        "setup-time-safe selected option data",
    ),
    ("Ideal", "IWM"): (
        "Ideal IWM starter option/rule fixtures",
        "setup-time-safe selected option data",
    ),
    ("Ideal", "QQQ"): (
        "Ideal QQQ starter option/rule fixtures",
        "setup-time-safe selected option data",
    ),
    ("Clean Fast Break", "GLD"): (
        "Clean Fast Break GLD starter option/rule fixtures",
        "setup-time-safe selected option data",
    ),
    ("Clean Fast Break", "IWM"): (
        "Clean Fast Break IWM starter option/rule fixtures",
        "setup-time-safe selected option data",
    ),
}


def _load_json_fixture(name):
    path = HISTORICAL_REPLAY_DIR / "fixtures" / name
    return json.loads(path.read_text(encoding="utf-8"))


def _load_lifecycle_fixture(name):
    path = HISTORICAL_REPLAY_DIR / "fixtures" / name
    fixture = json.loads(path.read_text(encoding="utf-8"))
    validate_lifecycle_fixture(fixture)
    return fixture


def _grouped_candidates():
    candidates = []
    for name in GROUPED_FIXTURE_NAMES:
        fixture = _load_lifecycle_fixture(name)
        rows = [deepcopy(row["expected_output_shape"]) for row in fixture["lifecycle_rows"]]
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
                "pending_rows": sum(1 for row in rows if row["final_verdict"] == "PENDING"),
                "summary": build_lifecycle_summary(rows),
            }
        )
    return candidates


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


class Day48GroupedThreeFamilyCoverageExpansionTests(unittest.TestCase):
    def test_inventory_identifies_only_existing_local_stronger_rule_stacks(self):
        candidates = _grouped_candidates()
        stack_supported = [
            candidate
            for candidate in candidates
            if (candidate["setup_family"], candidate["symbol"]) in LOCAL_RULE_STACKS
        ]

        self.assertEqual(len(candidates), 12)
        self.assertEqual(
            [
                (candidate["setup_family"], candidate["symbol"])
                for candidate in stack_supported
            ],
            [
                ("Clean Fast Break", "QQQ"),
                ("Ideal", "SPY"),
                ("Clean Fast Break", "SPY"),
            ],
        )
        self.assertEqual(
            {candidate["setup_family"] for candidate in stack_supported},
            {"Clean Fast Break", "Ideal"},
        )
        self.assertFalse(
            any(candidate["setup_family"] == "Continuation" for candidate in stack_supported)
        )

        for stack in LOCAL_RULE_STACKS.values():
            for fixture_name in stack.values():
                with self.subTest(fixture_name=fixture_name):
                    self.assertTrue((HISTORICAL_REPLAY_DIR / "fixtures" / fixture_name).exists())

    def test_spy_ideal_existing_stack_runs_as_blocker_preserving_expansion(self):
        lifecycle = _load_json_fixture("spy_ideal_lifecycle_regression_fixtures.json")
        contract = _load_json_fixture("spy_ideal_contract_selection_regression_fixtures.json")
        execution = _load_json_fixture("spy_ideal_execution_context_regression_fixtures.json")
        context = _load_json_fixture("spy_ideal_context_caution_regression_fixtures.json")

        lifecycle_by_id = {row["fixture_id"]: row for row in lifecycle["fixtures"]}
        contract_by_id = {row["fixture_id"]: row for row in contract["fixtures"]}
        execution_by_id = {row["fixture_id"]: row for row in execution["fixtures"]}
        context_by_id = {row["fixture_id"]: row for row in context["fixtures"]}

        fresh_lifecycle = cfb_lifecycle_calculator.calculate_lifecycle_from_fixture(
            lifecycle_by_id["spy_ideal_lifecycle_fresh_trigger_signal_2026_05_13_1130"]
        )
        spent_lifecycle = cfb_lifecycle_calculator.calculate_lifecycle_from_fixture(
            lifecycle_by_id["spy_ideal_lifecycle_spent_follow_through_2026_05_13_1430"]
        )
        contract_result = cfb_contract_selector.select_contract_from_fixture(
            contract_by_id["spy_ideal_starter_top_contract_quote_after_signal_abstains"]
        )
        execution_result = execution_context_calculator.calculate_execution_context_from_fixture(
            execution_by_id["spy_ideal_starter_execution_unknown_no_selected_quote"]
        )
        complete_context = context_caution_calculator.calculate_context_caution_from_fixture(
            context_by_id["spy_ideal_complete_caution_unknown_components"]
        )

        self.assertEqual(fresh_lifecycle["lifecycle_status"], "fresh")
        self.assertEqual(spent_lifecycle["lifecycle_status"], "spent")
        self.assertEqual(contract_result["contract_selection_status"], "abstain")
        self.assertEqual(contract_result["rejection_reason"], "quote_ts_event_after_signal")
        self.assertEqual(execution_result["execution_context_status"], "unknown")
        self.assertEqual(execution_result["rejection_reason"], "missing_source_data")
        self.assertEqual(complete_context["complete_caution_review_status"], "unknown")
        self.assertEqual(complete_context["rejection_reason"], "required_component_unknown")

        combined = {
            "fresh_lifecycle": fresh_lifecycle,
            "spent_lifecycle": spent_lifecycle,
            "contract_result": contract_result,
            "execution_result": execution_result,
            "complete_context": complete_context,
        }
        self.assertEqual(
            [],
            _find_key_paths(combined, {field.lower() for field in FORBIDDEN_EXECUTION_FIELDS}),
        )

    def test_no_trade_controls_and_missing_dependency_inventory_are_preserved(self):
        candidates = _grouped_candidates()
        missing_by_candidate = {
            candidate["candidate_identifier"]: MISSING_EXPANSION_DEPENDENCIES[
                (candidate["setup_family"], candidate["symbol"])
            ]
            for candidate in candidates
            if (candidate["setup_family"], candidate["symbol"])
            in MISSING_EXPANSION_DEPENDENCIES
        }

        self.assertEqual(12, sum(1 for candidate in candidates if candidate["final_result"] == "NO_TRADE"))
        self.assertEqual(7, sum(len(candidate["accepted_entry_rows"]) for candidate in candidates))
        self.assertEqual(9, len(missing_by_candidate))
        self.assertIn(
            "Continuation-specific lifecycle rule fixtures",
            missing_by_candidate["first_real_spy_continuation_replay_v1_fixture"],
        )
        self.assertIn(
            "setup-time-safe selected option data",
            missing_by_candidate["first_real_iwm_ideal_replay_v1_fixture"],
        )
        self.assertIn(
            "Clean Fast Break GLD starter option/rule fixtures",
            missing_by_candidate["first_real_gld_clean_fast_break_replay_v1_fixture"],
        )


if __name__ == "__main__":
    unittest.main()
