import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_REPLAY_DIR = ROOT / "historical_signal_replay"
if str(HISTORICAL_REPLAY_DIR) not in sys.path:
    sys.path.insert(0, str(HISTORICAL_REPLAY_DIR))

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


def _load_fixture(name):
    path = HISTORICAL_REPLAY_DIR / "fixtures" / name
    with path.open("r", encoding="utf-8") as handle:
        fixture = json.load(handle)
    validate_lifecycle_fixture(fixture)
    return path, fixture


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


def _run_grouped_replay():
    candidates = []
    for name in GROUPED_FIXTURE_NAMES:
        path, fixture = _load_fixture(name)
        rows = [deepcopy(row["expected_output_shape"]) for row in fixture["lifecycle_rows"]]
        first_row = rows[0]
        final_row = rows[-1]
        source_data = fixture.get("source_data", {})
        candidates.append(
            {
                "candidate_identifier": fixture["fixture_name"],
                "fixture_path": path.as_posix(),
                "setup_family": final_row["setup_type"],
                "symbol": source_data.get("symbol", final_row["symbol"]),
                "evidence_source": source_data.get("source_csv"),
                "chronological_stage_path": [row["stage"] for row in rows],
                "session_dates": sorted(
                    {
                        row["timestamp"][:10]
                        for row in rows
                        if isinstance(row.get("timestamp"), str)
                    }
                ),
                "final_result": final_row["final_verdict"],
                "final_reason": final_row["primary_blocker"],
                "accepted_entry_rows": [
                    {
                        "timestamp": row["timestamp"],
                        "stage": row["stage"],
                        "primary_blocker": row["primary_blocker"],
                    }
                    for row in rows
                    if row["final_verdict"] == "TRADE"
                ],
                "pending_rows": sum(1 for row in rows if row["final_verdict"] == "PENDING"),
                "no_trade_rows": sum(
                    1 for row in rows if row["final_verdict"] == "NO_TRADE"
                ),
                "summary": build_lifecycle_summary(rows),
                "winner_selection_result": final_row["winner_selection_result"],
            }
        )
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "family_totals": _family_totals(candidates),
    }


def _family_totals(candidates):
    totals = {}
    for candidate in candidates:
        family = candidate["setup_family"]
        family_total = totals.setdefault(
            family,
            {
                "candidates_found": 0,
                "candidates_runnable": 0,
                "entries": 0,
                "no_trades": 0,
                "ambiguous_cases": 0,
                "blocked_cases": 0,
                "stable_cases": 0,
                "unstable_cases": 0,
            },
        )
        family_total["candidates_found"] += 1
        family_total["candidates_runnable"] += 1
        family_total["entries"] += len(candidate["accepted_entry_rows"])
        if candidate["final_result"] == "NO_TRADE":
            family_total["no_trades"] += 1
        if candidate["pending_rows"]:
            family_total["ambiguous_cases"] += 1
        if candidate["final_reason"]:
            family_total["blocked_cases"] += 1
        family_total["stable_cases"] += 1
    return totals


class Day48ActualGroupedThreeFamilyReplayTests(unittest.TestCase):
    def test_grouped_three_family_replay_is_deterministic_across_two_runs(self):
        first = _run_grouped_replay()
        second = _run_grouped_replay()

        self.assertEqual(first, second)
        self.assertEqual(first["candidate_count"], 12)
        self.assertEqual(
            first["family_totals"],
            {
                "Clean Fast Break": {
                    "candidates_found": 4,
                    "candidates_runnable": 4,
                    "entries": 3,
                    "no_trades": 4,
                    "ambiguous_cases": 1,
                    "blocked_cases": 4,
                    "stable_cases": 4,
                    "unstable_cases": 0,
                },
                "Continuation": {
                    "candidates_found": 4,
                    "candidates_runnable": 4,
                    "entries": 2,
                    "no_trades": 4,
                    "ambiguous_cases": 3,
                    "blocked_cases": 4,
                    "stable_cases": 4,
                    "unstable_cases": 0,
                },
                "Ideal": {
                    "candidates_found": 4,
                    "candidates_runnable": 4,
                    "entries": 2,
                    "no_trades": 4,
                    "ambiguous_cases": 4,
                    "blocked_cases": 4,
                    "stable_cases": 4,
                    "unstable_cases": 0,
                },
            },
        )

    def test_grouped_replay_preserves_stage_boundary_and_no_execution_scope(self):
        result = _run_grouped_replay()
        candidates = result["candidates"]

        self.assertTrue(
            all(len(candidate["chronological_stage_path"]) == 6 for candidate in candidates)
        )
        self.assertEqual(
            12,
            sum(1 for candidate in candidates if len(candidate["session_dates"]) > 1),
        )
        self.assertEqual(
            7,
            sum(len(candidate["accepted_entry_rows"]) for candidate in candidates),
        )
        self.assertEqual(
            [],
            _find_key_paths(result, {field.lower() for field in FORBIDDEN_EXECUTION_FIELDS}),
        )


if __name__ == "__main__":
    unittest.main()
