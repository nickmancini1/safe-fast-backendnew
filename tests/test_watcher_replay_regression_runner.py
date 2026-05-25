import subprocess
import unittest

from watcher_foundation.constants import NEWS_UNCONFIRMED
from watcher_foundation.replay_regression import (
    REPLAY_REGRESSION_RESULT_FIELDS,
    ReplayRegressionCase,
    run_local_replay_regression,
)


class WatcherReplayRegressionRunnerTests(unittest.TestCase):
    def _fixture_observation(self, setup_type="Ideal", **overrides):
        fixture_slug = setup_type.lower().replace(" ", "-")
        observation = {
            "candidate_id": f"SYN-{fixture_slug}-replay",
            "symbol": "SYN",
            "watch_session_id": f"{fixture_slug}-session-alpha",
            "setup_type": setup_type,
            "direction": "bullish/call-side",
            "regular_session_date": "2099-01-10",
            "first_seen_at": "2099-01-10T09:35:00-04:00",
            "last_seen_at": "2099-01-10T09:35:00-04:00",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "trigger_level_or_zone": f"{fixture_slug}-synthetic-zone",
            "trigger_zone_bucket": f"{fixture_slug}-synthetic-zone-bucket",
            "confirmation_timeframe_rule": "synthetic completed-candle review",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": "synthetic structure invalidation",
            "invalidation_bucket": f"{fixture_slug}-synthetic-invalidation",
            "source_kind": "local_fixture",
            "source_as_of": "2099-01-10T09:35:00-04:00",
            "evidence_rows": [f"{fixture_slug}-synthetic-row-1"],
            "evidence_quality": "deterministic",
            "unavailable_fields": [],
            "blockers": [],
            "cautions": [],
            "primary_blocker": "UNCONFIRMED",
            "no_trade_reason": "watch_only_shadow_review_no_live_trade_approval",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "trigger_path_identifier": f"{fixture_slug}-initial-path",
            "fresh_trigger_path_present": True,
            "watch_only": True,
        }
        observation.update(overrides)
        return observation

    def _run_single_case(self, replay_case):
        result = run_local_replay_regression([replay_case])
        self.assertEqual(set(result), set(REPLAY_REGRESSION_RESULT_FIELDS))
        self.assertEqual(result["cases_processed"], 1)
        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self.assertEqual(result["cases_passed"], 1)
        self.assertTrue(result["watch_only"])
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])
        return result["case_results"][0]["result"]

    def test_ideal_setup_replay_fixture_passes_expected_checks(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-ideal-replay",
                observations=[self._fixture_observation("Ideal")],
                expected_values={
                    "final_state.setup_type": "Ideal",
                    "final_trigger_card.setup_type": "Ideal",
                    "final_diagnostics.setup_type": "Ideal",
                    "final_focus_ranking.primary_focus_candidate_id": (
                        "SYN-ideal-replay"
                    ),
                    "final_duplicate_suppression.alert_decision": (
                        "emit_material_change"
                    ),
                    "watch_only": True,
                    "no_trade_boundary.trade_approval": False,
                },
            )
        )

        self.assertEqual(result["final_state"]["setup_type"], "Ideal")

    def test_clean_fast_break_setup_replay_fixture_passes_expected_checks(self):
        result = self._run_single_case(
            {
                "name": "synthetic-clean-fast-break-replay",
                "observations": [self._fixture_observation("Clean Fast Break")],
                "expected_values": {
                    "final_state.setup_type": "Clean Fast Break",
                    "final_trigger_card.setup_type": "Clean Fast Break",
                    "final_diagnostics.setup_type": "Clean Fast Break",
                    "final_focus_ranking.primary_focus_candidate_id": (
                        "SYN-clean-fast-break-replay"
                    ),
                    "final_duplicate_suppression.alert_decision": (
                        "emit_material_change"
                    ),
                },
            }
        )

        self.assertEqual(result["observations_processed"], 1)

    def test_continuation_setup_replay_fixture_passes_expected_checks(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-continuation-replay",
                observations=[self._fixture_observation("Continuation")],
                expected_values={
                    "final_state.setup_type": "Continuation",
                    "final_trigger_card.setup_type": "Continuation",
                    "final_diagnostics.setup_type": "Continuation",
                    "final_focus_ranking.primary_focus_candidate_id": (
                        "SYN-continuation-replay"
                    ),
                    "final_duplicate_suppression.alert_decision": (
                        "emit_material_change"
                    ),
                },
            )
        )

        self.assertEqual(result["final_trigger_card"]["setup_type"], "Continuation")

    def test_developing_stage_transition_fixture_detects_progression(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-developing-stage-transition",
                observations=[
                    self._fixture_observation(
                        "Ideal",
                        stage="forming/developing",
                        trigger_status="waiting_for_trigger",
                        distance_to_trigger="medium",
                        trigger_path_identifier="ideal-forming-path",
                    ),
                    self._fixture_observation(
                        "Ideal",
                        last_seen_at="2099-01-10T10:35:00-04:00",
                        stage="pending_completed_candle_approval",
                        trigger_status="pending_completed_candle",
                        trigger_path_identifier="ideal-pending-candle-path",
                    ),
                ],
                expected_values={
                    "final_state.previous_stage": "forming/developing",
                    "final_state.stage": "pending_completed_candle_approval",
                    "final_state.previous_trigger_status": "waiting_for_trigger",
                    "final_trigger_card.trigger_status": (
                        "pending_completed_candle"
                    ),
                    "final_duplicate_suppression.alert_decision": (
                        "emit_material_change"
                    ),
                },
                expected_contains={
                    "final_duplicate_suppression.material_change_flags": [
                        "stage_changed",
                        "trigger_status_changed",
                    ],
                },
            )
        )

        self.assertEqual(result["alert_decisions"], ["emit_material_change"] * 2)

    def test_session_boundary_carry_forward_fixture_preserves_existing_identity(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-session-boundary-carry-forward",
                observations=[
                    self._fixture_observation(
                        "Ideal",
                        regular_session_date="2099-01-10",
                        first_seen_at="2099-01-10T15:55:00-04:00",
                        last_seen_at="2099-01-10T15:55:00-04:00",
                    ),
                    self._fixture_observation(
                        "Ideal",
                        regular_session_date="2099-01-11",
                        last_seen_at="2099-01-11T09:35:00-04:00",
                    ),
                ],
                expected_values={
                    "final_state.regular_session_date": "2099-01-10",
                    "final_state.first_seen_at": "2099-01-10T15:55:00-04:00",
                    "final_state.last_seen_at": "2099-01-11T09:35:00-04:00",
                    "final_state.previous_stage": "near-trigger",
                    "final_duplicate_suppression.alert_decision": (
                        "suppress_duplicate"
                    ),
                    "final_duplicate_suppression.repeat_count": 1,
                },
            )
        )

        self.assertEqual(result["alert_decisions"][-1], "suppress_duplicate")

    def test_duplicate_suppression_fixture_exposes_repeat_behavior(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-duplicate-suppression",
                observations=[
                    self._fixture_observation("Clean Fast Break"),
                    self._fixture_observation("Clean Fast Break"),
                ],
                expected_values={
                    "final_duplicate_suppression.alert_decision": (
                        "suppress_duplicate"
                    ),
                    "final_duplicate_suppression.suppression_reason": (
                        "same_state_repeat_no_material_change"
                    ),
                    "final_duplicate_suppression.repeat_count": 1,
                },
            )
        )

        self.assertEqual(
            result["alert_decisions"],
            ["emit_material_change", "suppress_duplicate"],
        )

    def test_strict_no_trade_boundary_fixture_emits_no_execution_fields(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-strict-no-trade-boundary",
                observations=[
                    self._fixture_observation(
                        "Clean Fast Break",
                        stage="triggered_signal_stage",
                        trigger_status="triggered",
                        no_trade_reason=(
                            "triggered_for_shadow_signal_review_only_no_live_trade_approval"
                        ),
                    )
                ],
                expected_values={
                    "no_trade_boundary.watch_only": True,
                    "no_trade_boundary.trade_approval": False,
                    "no_trade_boundary.live_trade_approval": False,
                    "no_trade_boundary.no_live_trade_approval": True,
                    "no_trade_boundary.shadow_signal_review_only": True,
                },
                expected_absent_fields=[
                    "account_id",
                    "broker",
                    "order_id",
                    "option_symbol",
                    "pnl",
                    "trade_decision",
                ],
            )
        )

        self.assertTrue(result["no_trade_boundary"]["shadow_signal_review_only"])

    def test_news_unconfirmed_preservation_fixture_keeps_default_without_source(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-news-unconfirmed-preservation",
                observations=[self._fixture_observation("Continuation")],
                expected_values={
                    "final_state.headline_news_status": NEWS_UNCONFIRMED,
                    "final_trigger_card.headline_news_status": NEWS_UNCONFIRMED,
                    "final_diagnostics.headline_news_status": NEWS_UNCONFIRMED,
                    "final_state.headline_news_source_confirmed": False,
                },
                expected_contains={
                    "final_state.news_policy_reason_codes": [
                        "news_unconfirmed_default"
                    ],
                    "final_state.unavailable_fields": [NEWS_UNCONFIRMED],
                },
            )
        )

        self.assertEqual(
            result["final_diagnostics"]["headline_news_status"],
            NEWS_UNCONFIRMED,
        )

    def test_source_confirmed_news_fixture_can_override_unconfirmed_status(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-source-confirmed-news",
                observations=[
                    self._fixture_observation(
                        "Ideal",
                        headline_news_source={
                            "headline_news_status": "NEWS_CAUTION",
                            "source_status": "source_confirmed",
                            "source_as_of": "2099-01-10T09:40:00-04:00",
                            "evidence_refs": ["synthetic-caller-news-ref"],
                            "watch_only": True,
                        },
                    )
                ],
                expected_values={
                    "final_state.headline_news_status": "NEWS_CAUTION",
                    "final_state.headline_news_source_confirmed": True,
                    "final_diagnostics.headline_news_status": "NEWS_CAUTION",
                },
                expected_contains={
                    "final_state.news_evidence_refs": [
                        "synthetic-caller-news-ref"
                    ],
                    "final_diagnostics.diagnostic_reason_codes.caution": [
                        "caution.news_source_confirmed_caution"
                    ],
                },
            )
        )

        self.assertEqual(result["final_state"]["headline_news_status"], "NEWS_CAUTION")

    def test_runner_returns_failure_details_for_mismatched_expectation(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-mismatch",
                    observations=[self._fixture_observation("Ideal")],
                    expected_values={"final_state.setup_type": "Continuation"},
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 1)
        failure = result["case_results"][0]["failures"][0]
        self.assertEqual(failure["check"], "expected_value")
        self.assertEqual(failure["path"], "final_state.setup_type")
        self.assertEqual(failure["actual"], "Ideal")

    def test_forbidden_trade_decision_input_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "trade-decision"):
            run_local_replay_regression(
                [
                    ReplayRegressionCase(
                        name="synthetic-forbidden-trade-decision",
                        observations=[
                            self._fixture_observation(
                                "Ideal",
                                trade_decision="not_allowed",
                            )
                        ],
                    )
                ]
            )

    def test_main_py_has_no_change(self):
        result = subprocess.run(
            ["git", "diff", "--quiet", "--", "main.py"],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
