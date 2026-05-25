import unittest

from watcher_foundation.constants import FORBIDDEN_EXECUTION_FIELD_NAMES
from watcher_foundation.focus_ranking import rank_focus_candidates
from watcher_foundation.pipeline import run_local_watcher_pipeline
from watcher_foundation.replay_regression import (
    ReplayRegressionCase,
    run_local_replay_regression,
)


FORBIDDEN_WINNER_OUTPUT_FIELDS = FORBIDDEN_EXECUTION_FIELD_NAMES | {
    "live_trade_decision",
    "live_trade_decisions",
    "trade_decision",
    "trade_decision_status",
    "trade_decisions",
}


class WatcherStableWinnerSelectionReplayTests(unittest.TestCase):
    def _candidate(self, candidate_id, setup_type="Ideal", **overrides):
        fixture_slug = setup_type.lower().replace(" ", "-")
        candidate = {
            "candidate_id": candidate_id,
            "symbol": "SYNW",
            "watch_session_id": "synthetic-winner-session",
            "setup_type": setup_type,
            "direction": "bullish/call-side",
            "regular_session_date": "2099-03-01",
            "first_seen_at": "2099-03-01T09:33:00-04:00",
            "last_seen_at": "2099-03-01T09:33:00-04:00",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "trigger_level_or_zone": f"{fixture_slug}-synthetic-zone",
            "trigger_zone_bucket": f"{fixture_slug}-synthetic-zone-bucket",
            "confirmation_timeframe_rule": "synthetic completed-candle review",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": "synthetic invalidation condition",
            "invalidation_bucket": f"{fixture_slug}-synthetic-invalidation",
            "source_kind": "local_fixture",
            "source_as_of": "2099-03-01T09:33:00-04:00",
            "evidence_rows": [f"{candidate_id}-synthetic-evidence-1"],
            "evidence_quality": "deterministic",
            "unavailable_fields": [],
            "blockers": [],
            "cautions": [],
            "primary_blocker": "synthetic_local_review_only",
            "no_trade_reason": "watch_only_shadow_review_no_live_trade_approval",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "trigger_path_identifier": f"{candidate_id}-path",
            "fresh_trigger_path_present": True,
            "watch_only": True,
        }
        candidate.update(overrides)
        return candidate

    def _find_key_paths(self, value, field_name, path=()):
        matches = []
        if isinstance(value, dict):
            for key, nested_value in value.items():
                nested_path = (*path, str(key))
                if str(key).lower() == field_name:
                    matches.append(".".join(nested_path))
                matches.extend(
                    self._find_key_paths(nested_value, field_name, nested_path)
                )
        elif isinstance(value, (list, tuple)):
            for index, nested_value in enumerate(value):
                matches.extend(
                    self._find_key_paths(nested_value, field_name, (*path, str(index)))
                )
        return matches

    def _assert_no_forbidden_winner_output_fields(self, value):
        for field_name in FORBIDDEN_WINNER_OUTPUT_FIELDS:
            self.assertEqual(
                [],
                self._find_key_paths(value, field_name),
                f"Forbidden winner output field leaked: {field_name}",
            )

    def _run_pipeline_step(
        self,
        observation,
        focus_candidates,
        previous_result=None,
    ):
        return run_local_watcher_pipeline(
            observation,
            previous_state=previous_result["state"] if previous_result else None,
            previous_suppression_state=(
                previous_result["duplicate_suppression"] if previous_result else None
            ),
            focus_candidates=focus_candidates,
            previous_primary_focus_candidate_id=(
                previous_result["focus_ranking"]["primary_focus_candidate_id"]
                if previous_result
                else None
            ),
        )

    def test_repeated_replay_regression_selects_same_stable_winner_fields(self):
        replay_case = ReplayRegressionCase(
            name="synthetic-stable-winner-repeat",
            observations=[self._candidate("SYNW-ideal-alpha", "Ideal")],
            expected_values={
                "final_focus_ranking.primary_focus_candidate_id": "SYNW-ideal-alpha",
                "final_focus_ranking.ranked_candidates.0.focus_rank_bucket": (
                    "primary_focus"
                ),
                "watch_only": True,
                "no_trade_boundary.trade_approval": False,
            },
        )

        first = run_local_replay_regression([replay_case])
        second = run_local_replay_regression([replay_case])
        stable_fields = (
            "cases_processed",
            "cases_passed",
            "cases_failed",
            "case_results",
            "no_trade_boundary",
        )

        self.assertEqual(
            {field: first[field] for field in stable_fields},
            {field: second[field] for field in stable_fields},
        )
        self.assertEqual(first["cases_failed"], 0, first["case_results"])

    def test_equivalent_candidates_use_candidate_id_tie_breaker_not_input_order(self):
        continuation = self._candidate("SYNW-B-continuation", "Continuation")
        clean_fast_break = self._candidate(
            "SYNW-A-clean-fast-break", "Clean Fast Break"
        )

        first_order = rank_focus_candidates([continuation, clean_fast_break])
        reversed_order = rank_focus_candidates([clean_fast_break, continuation])

        self.assertEqual(
            first_order["primary_focus_candidate_id"], "SYNW-A-clean-fast-break"
        )
        self.assertEqual(
            reversed_order["primary_focus_candidate_id"], "SYNW-A-clean-fast-break"
        )
        self.assertEqual(
            first_order["ranked_candidates"][0]["focus_rank_score"][-1],
            "SYNW-A-clean-fast-break",
        )

    def test_materially_better_candidate_wins_when_not_first_observation(self):
        weaker_first = self._candidate(
            "SYNW-weak-first",
            "Ideal",
            distance_to_trigger="far",
            evidence_quality="partial",
        )
        stronger_second = self._candidate(
            "SYNW-strong-second",
            "Clean Fast Break",
            distance_to_trigger="near",
            evidence_quality="deterministic",
        )

        result = rank_focus_candidates([weaker_first, stronger_second])

        self.assertEqual(result["primary_focus_candidate_id"], "SYNW-strong-second")
        self.assertEqual(
            result["ranked_candidates"][0]["candidate_id"], "SYNW-strong-second"
        )

    def test_winner_carries_forward_until_stronger_candidate_appears(self):
        observation = self._candidate("SYNW-observed-state", "Ideal")
        prior_winner = self._candidate("SYNW-prior-winner", "Ideal")
        equivalent_other = self._candidate(
            "SYNW-secondary-watch",
            "Continuation",
            distance_to_trigger="medium",
        )
        stronger_later = self._candidate(
            "SYNW-stronger-later",
            "Clean Fast Break",
            distance_to_trigger="near",
            source_as_of="2099-03-01T10:33:00-04:00",
        )

        first = self._run_pipeline_step(
            observation,
            [prior_winner, equivalent_other],
        )
        second = self._run_pipeline_step(
            {**observation, "last_seen_at": "2099-03-01T10:03:00-04:00"},
            [prior_winner, equivalent_other],
            previous_result=first,
        )
        third = self._run_pipeline_step(
            {
                **observation,
                "last_seen_at": "2099-03-01T10:33:00-04:00",
                "trigger_status": "pending_completed_candle",
                "stage": "pending_completed_candle_approval",
            },
            [
                {**prior_winner, "distance_to_trigger": "medium"},
                equivalent_other,
                stronger_later,
            ],
            previous_result=second,
        )

        self.assertEqual(
            first["focus_ranking"]["primary_focus_candidate_id"],
            "SYNW-prior-winner",
        )
        self.assertEqual(
            second["focus_ranking"]["primary_focus_candidate_id"],
            "SYNW-prior-winner",
        )
        self.assertFalse(second["focus_ranking"]["best_candidate_changed"])
        self.assertEqual(
            third["focus_ranking"]["primary_focus_candidate_id"],
            "SYNW-stronger-later",
        )
        self.assertTrue(third["focus_ranking"]["best_candidate_changed"])
        self.assertEqual(
            third["focus_ranking"]["ranked_candidates"][0]["trigger_proximity_rank"],
            0,
        )

    def test_setup_type_coverage_preserves_stable_winners(self):
        cases = [
            ReplayRegressionCase(
                name=f"synthetic-{setup_type.lower().replace(' ', '-')}-stable-winner",
                observations=[self._candidate(candidate_id, setup_type)],
                expected_values={
                    "final_state.setup_type": setup_type,
                    "final_focus_ranking.primary_focus_candidate_id": candidate_id,
                },
            )
            for setup_type, candidate_id in (
                ("Ideal", "SYNW-ideal-winner"),
                ("Clean Fast Break", "SYNW-clean-fast-break-winner"),
                ("Continuation", "SYNW-continuation-winner"),
            )
        ]

        result = run_local_replay_regression(cases)

        self.assertEqual(result["cases_processed"], 3)
        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self.assertEqual(result["cases_passed"], 3)

    def test_session_boundary_preserves_identity_first_seen_and_last_seen(self):
        replay_case = ReplayRegressionCase(
            name="synthetic-session-boundary-stable-winner",
            observations=[
                self._candidate(
                    "SYNW-session-winner",
                    "Continuation",
                    regular_session_date="2099-03-01",
                    first_seen_at="2099-03-01T15:53:00-04:00",
                    last_seen_at="2099-03-01T15:53:00-04:00",
                ),
                self._candidate(
                    "SYNW-session-winner",
                    "Continuation",
                    regular_session_date="2099-03-02",
                    last_seen_at="2099-03-02T09:33:00-04:00",
                ),
            ],
            expected_values={
                "final_state.candidate_id": "SYNW-session-winner",
                "final_state.first_seen_at": "2099-03-01T15:53:00-04:00",
                "final_state.last_seen_at": "2099-03-02T09:33:00-04:00",
                "final_state.regular_session_date": "2099-03-01",
                "final_focus_ranking.primary_focus_candidate_id": (
                    "SYNW-session-winner"
                ),
            },
        )

        result = run_local_replay_regression([replay_case])

        self.assertEqual(result["cases_failed"], 0, result["case_results"])

    def test_no_trade_boundary_has_no_execution_trade_or_sizing_fields(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-stable-winner-no-trade-boundary",
                    observations=[
                        self._candidate(
                            "SYNW-no-trade-winner",
                            "Clean Fast Break",
                            stage="triggered_signal_stage",
                            trigger_status="triggered",
                            no_trade_reason=(
                                "triggered_for_shadow_signal_review_only_no_live_trade_approval"
                            ),
                        )
                    ],
                    expected_absent_fields=sorted(FORBIDDEN_WINNER_OUTPUT_FIELDS),
                    expected_values={
                        "no_trade_boundary.watch_only": True,
                        "no_trade_boundary.no_live_trade_approval": True,
                        "no_trade_boundary.trade_approval": False,
                        "no_trade_boundary.live_trade_approval": False,
                    },
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self._assert_no_forbidden_winner_output_fields(result)

    def test_wrong_expected_winner_failure_includes_path_expected_and_actual(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-wrong-expected-winner",
                    observations=[self._candidate("SYNW-actual-winner", "Ideal")],
                    expected_values={
                        "final_focus_ranking.primary_focus_candidate_id": (
                            "SYNW-incorrect-winner"
                        )
                    },
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 1)
        failure = result["case_results"][0]["failures"][0]
        self.assertEqual(failure["check"], "expected_value")
        self.assertEqual(
            failure["path"], "final_focus_ranking.primary_focus_candidate_id"
        )
        self.assertEqual(failure["expected"], "SYNW-incorrect-winner")
        self.assertEqual(failure["actual"], "SYNW-actual-winner")


if __name__ == "__main__":
    unittest.main()
