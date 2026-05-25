import unittest

from watcher_foundation.constants import (
    FORBIDDEN_EXECUTION_FIELD_NAMES,
    NEWS_UNCONFIRMED,
)
from watcher_foundation.replay_regression import (
    ReplayRegressionCase,
    run_local_replay_regression,
)


FORBIDDEN_REPLAY_OUTPUT_FIELDS = FORBIDDEN_EXECUTION_FIELD_NAMES | {
    "live_trade_decision",
    "live_trade_decisions",
    "trade_decision",
    "trade_decision_status",
    "trade_decisions",
}


class WatcherReplayRegressionHardeningTests(unittest.TestCase):
    def _fixture_observation(self, setup_type="Ideal", **overrides):
        fixture_slug = setup_type.lower().replace(" ", "-")
        observation = {
            "candidate_id": f"SYNH-{fixture_slug}-candidate",
            "symbol": "SYNH",
            "watch_session_id": f"{fixture_slug}-synthetic-session",
            "setup_type": setup_type,
            "direction": "bullish/call-side",
            "regular_session_date": "2099-02-01",
            "first_seen_at": "2099-02-01T09:31:00-04:00",
            "last_seen_at": "2099-02-01T09:31:00-04:00",
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
            "source_as_of": "2099-02-01T09:31:00-04:00",
            "evidence_rows": [f"{fixture_slug}-synthetic-evidence-1"],
            "evidence_quality": "deterministic",
            "unavailable_fields": [],
            "blockers": [],
            "cautions": [],
            "primary_blocker": "synthetic_local_review_only",
            "no_trade_reason": "watch_only_shadow_review_no_live_trade_approval",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "trigger_path_identifier": f"{fixture_slug}-path-near",
            "fresh_trigger_path_present": True,
            "watch_only": True,
        }
        observation.update(overrides)
        return observation

    def _run_single_case(self, replay_case):
        result = run_local_replay_regression([replay_case])
        self.assertEqual(result["cases_processed"], 1)
        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self.assertEqual(result["cases_passed"], 1)
        self.assertTrue(result["watch_only"])
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])
        return result["case_results"][0]["result"]

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

    def _assert_no_forbidden_replay_output_fields(self, value):
        for field_name in FORBIDDEN_REPLAY_OUTPUT_FIELDS:
            self.assertEqual(
                [],
                self._find_key_paths(value, field_name),
                f"Forbidden replay output field leaked: {field_name}",
            )

    def test_all_three_setup_types_remain_recognized_by_replay_runner(self):
        for setup_type in ("Ideal", "Clean Fast Break", "Continuation"):
            with self.subTest(setup_type=setup_type):
                result = self._run_single_case(
                    ReplayRegressionCase(
                        name=f"synthetic-{setup_type.lower().replace(' ', '-')}",
                        observations=[self._fixture_observation(setup_type)],
                        expected_values={
                            "final_state.setup_type": setup_type,
                            "final_trigger_card.setup_type": setup_type,
                            "final_diagnostics.setup_type": setup_type,
                            "final_focus_ranking.primary_focus_candidate_id": (
                                f"SYNH-{setup_type.lower().replace(' ', '-')}-candidate"
                            ),
                        },
                    )
                )

                self.assertEqual(result["final_state"]["setup_type"], setup_type)

    def test_developing_to_triggered_to_stale_transition_is_preserved(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-developing-trigger-stale-transition",
                observations=[
                    self._fixture_observation(
                        "Ideal",
                        stage="forming/developing",
                        trigger_status="waiting_for_trigger",
                        distance_to_trigger="far",
                        trigger_path_identifier="synthetic-ideal-forming-path",
                    ),
                    self._fixture_observation(
                        "Ideal",
                        last_seen_at="2099-02-01T10:31:00-04:00",
                        stage="near-trigger",
                        trigger_status="near_trigger",
                        distance_to_trigger="near",
                        trigger_path_identifier="synthetic-ideal-near-path",
                    ),
                    self._fixture_observation(
                        "Ideal",
                        last_seen_at="2099-02-01T11:31:00-04:00",
                        stage="pending_completed_candle_approval",
                        trigger_status="pending_completed_candle",
                        trigger_path_identifier="synthetic-ideal-pending-path",
                    ),
                    self._fixture_observation(
                        "Ideal",
                        last_seen_at="2099-02-01T12:31:00-04:00",
                        stage="triggered_signal_stage",
                        trigger_status="triggered",
                        no_trade_reason=(
                            "triggered_for_shadow_signal_review_only_no_live_trade_approval"
                        ),
                        trigger_path_identifier="synthetic-ideal-triggered-path",
                    ),
                    self._fixture_observation(
                        "Ideal",
                        last_seen_at="2099-02-01T13:31:00-04:00",
                        stage="stale/spent/no-fresh-trigger",
                        trigger_status="stale",
                        fresh_stale_spent_state="stale",
                        fresh_trigger_path_present=False,
                        no_trade_reason="watch_only_no_fresh_trigger_no_trade",
                        trigger_path_identifier="synthetic-ideal-stale-path",
                    ),
                ],
                expected_values={
                    "observations_processed": 5,
                    "final_state.previous_stage": "triggered_signal_stage",
                    "final_state.stage": "stale/spent/no-fresh-trigger",
                    "final_state.previous_trigger_status": "triggered",
                    "final_state.trigger_status": "stale",
                    "final_trigger_card.fresh_trigger_path_present": False,
                    "no_trade_boundary.shadow_signal_review_only": False,
                },
            )
        )

        observed_stages = [
            record["state_snapshot"]["stage"]
            for record in result["shadow_log_records"]
        ]
        self.assertEqual(
            observed_stages,
            [
                "forming/developing",
                "near-trigger",
                "pending_completed_candle_approval",
                "triggered_signal_stage",
                "stale/spent/no-fresh-trigger",
            ],
        )
        self.assertIn(
            "no fresh trigger",
            result["final_diagnostics"]["diagnostic_explanation"].lower(),
        )

    def test_session_boundary_preserves_identity_and_updates_last_seen(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-session-boundary-continuity",
                observations=[
                    self._fixture_observation(
                        "Continuation",
                        first_seen_at="2099-02-01T15:51:00-04:00",
                        last_seen_at="2099-02-01T15:51:00-04:00",
                    ),
                    self._fixture_observation(
                        "Continuation",
                        regular_session_date="2099-02-02",
                        last_seen_at="2099-02-02T09:31:00-04:00",
                    ),
                ],
                expected_values={
                    "final_state.candidate_id": "SYNH-continuation-candidate",
                    "final_state.watch_session_id": "continuation-synthetic-session",
                    "final_state.first_seen_at": "2099-02-01T15:51:00-04:00",
                    "final_state.last_seen_at": "2099-02-02T09:31:00-04:00",
                    "final_state.regular_session_date": "2099-02-01",
                    "final_state.previous_stage": "near-trigger",
                },
            )
        )

        self.assertEqual(
            result["final_focus_ranking"]["primary_focus_candidate_id"],
            "SYNH-continuation-candidate",
        )
        self.assertEqual(len(result["shadow_log_records"]), 2)

    def test_failure_diagnostics_include_expected_path_expected_and_actual(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-expected-value-mismatch",
                    observations=[self._fixture_observation("Ideal")],
                    expected_values={"final_state.setup_type": "Continuation"},
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 1)
        failure = result["case_results"][0]["failures"][0]
        self.assertEqual(failure["check"], "expected_value")
        self.assertEqual(failure["path"], "final_state.setup_type")
        self.assertEqual(failure["expected"], "Continuation")
        self.assertEqual(failure["actual"], "Ideal")

    def test_expected_contains_failure_reports_missing_items(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-contains-mismatch",
                    observations=[self._fixture_observation("Clean Fast Break")],
                    expected_contains={
                        "final_duplicate_suppression.material_change_flags": [
                            "synthetic_missing_flag"
                        ]
                    },
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 1)
        failure = result["case_results"][0]["failures"][0]
        self.assertEqual(failure["check"], "expected_contains")
        self.assertEqual(failure["path"], "final_duplicate_suppression.material_change_flags")
        self.assertEqual(failure["missing"], ["synthetic_missing_flag"])

    def test_expected_absent_fields_failure_reports_output_paths(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-absent-field-mismatch",
                    observations=[self._fixture_observation("Continuation")],
                    expected_absent_fields=["headline_news_status"],
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 1)
        failure = result["case_results"][0]["failures"][0]
        self.assertEqual(failure["check"], "expected_absent_field")
        self.assertEqual(failure["field"], "headline_news_status")
        self.assertTrue(failure["paths"])

    def test_forbidden_trade_decision_fields_are_rejected_anywhere_in_input(self):
        cases = (
            ("trade_decision", {"trade_decision": "forbidden"}),
            ("trade_decision_status", {"nested": {"trade_decision_status": "x"}}),
            ("live_trade_decision", {"items": [{"live_trade_decision": "x"}]}),
            ("trade_decisions", {"items": [{"nested": {"trade_decisions": []}}]}),
        )
        for field_name, payload in cases:
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, "trade-decision"):
                    run_local_replay_regression(
                        [
                            ReplayRegressionCase(
                                name=f"synthetic-forbidden-{field_name}",
                                observations=[
                                    self._fixture_observation("Ideal", **payload)
                                ],
                            )
                        ]
                    )

    def test_forbidden_execution_fields_are_rejected_anywhere_in_input(self):
        cases = (
            ("broker", {"broker": "forbidden"}),
            ("order_id", {"nested": {"order_id": "forbidden"}}),
            ("account_id", {"items": [{"account_id": "forbidden"}]}),
            ("option_symbol", {"items": [{"nested": {"option_symbol": "x"}}]}),
            ("pnl", {"nested": {"deeper": {"pnl": "forbidden"}}}),
        )
        for field_name, payload in cases:
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    run_local_replay_regression(
                        [
                            ReplayRegressionCase(
                                name=f"synthetic-forbidden-{field_name}",
                                observations=[
                                    self._fixture_observation(
                                        "Clean Fast Break", **payload
                                    )
                                ],
                            )
                        ]
                    )

    def test_replay_outputs_do_not_contain_execution_or_trade_decision_fields(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-output-no-forbidden-fields",
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
                    expected_absent_fields=sorted(FORBIDDEN_REPLAY_OUTPUT_FIELDS),
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self._assert_no_forbidden_replay_output_fields(result)

    def test_same_fixture_run_twice_produces_equal_stable_summaries(self):
        replay_case = ReplayRegressionCase(
            name="synthetic-deterministic-repeat",
            observations=[
                self._fixture_observation("Ideal"),
                self._fixture_observation(
                    "Ideal",
                    last_seen_at="2099-02-01T10:31:00-04:00",
                    stage="pending_completed_candle_approval",
                    trigger_status="pending_completed_candle",
                    trigger_path_identifier="synthetic-ideal-pending-path",
                ),
            ],
        )

        first = run_local_replay_regression([replay_case])["case_results"][0]["result"]
        second = run_local_replay_regression([replay_case])["case_results"][0]["result"]
        stable_fields = (
            "observations_processed",
            "alert_decisions",
            "final_state",
            "final_trigger_card",
            "final_duplicate_suppression",
            "final_focus_ranking",
            "no_trade_boundary",
        )
        self.assertEqual(
            {field: first[field] for field in stable_fields},
            {field: second[field] for field in stable_fields},
        )

    def test_case_order_does_not_leak_duplicate_state_across_cases(self):
        repeated_case = ReplayRegressionCase(
            name="synthetic-repeat-within-case",
            observations=[
                self._fixture_observation("Ideal"),
                self._fixture_observation("Ideal"),
            ],
            expected_values={
                "final_duplicate_suppression.alert_decision": "suppress_duplicate"
            },
        )
        fresh_case_after_repeat = ReplayRegressionCase(
            name="synthetic-fresh-case-after-repeat",
            observations=[self._fixture_observation("Ideal")],
            expected_values={
                "final_duplicate_suppression.alert_decision": "emit_material_change"
            },
        )

        result = run_local_replay_regression([repeated_case, fresh_case_after_repeat])

        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self.assertEqual(
            result["case_results"][0]["result"]["alert_decisions"],
            ["emit_material_change", "suppress_duplicate"],
        )
        self.assertEqual(
            result["case_results"][1]["result"]["alert_decisions"],
            ["emit_material_change"],
        )

    def test_headline_news_defaults_without_source_and_does_not_invent_facts(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-news-default-no-invented-facts",
                observations=[self._fixture_observation("Continuation")],
                expected_values={
                    "final_state.headline_news_status": NEWS_UNCONFIRMED,
                    "final_trigger_card.headline_news_status": NEWS_UNCONFIRMED,
                    "final_diagnostics.headline_news_status": NEWS_UNCONFIRMED,
                    "final_state.headline_news_source_confirmed": False,
                },
                expected_absent_fields=[
                    "headline_text",
                    "macro_event",
                    "earnings_event",
                    "filing",
                    "rumor",
                    "live_fact",
                ],
            )
        )

        self.assertIn(
            "news_unconfirmed_default",
            result["final_state"]["news_policy_reason_codes"],
        )

    def test_source_confirmed_news_metadata_remains_caller_provided_watch_only(self):
        result = self._run_single_case(
            ReplayRegressionCase(
                name="synthetic-source-confirmed-news-placeholder",
                observations=[
                    self._fixture_observation(
                        "Ideal",
                        headline_news_source={
                            "headline_news_status": "NEWS_CLEAR",
                            "source_status": "source_confirmed",
                            "source_as_of": "2099-02-01T09:41:00-04:00",
                            "evidence_refs": ["synthetic-caller-news-ref-a"],
                            "watch_only": True,
                        },
                    )
                ],
                expected_values={
                    "final_state.headline_news_status": "NEWS_CLEAR",
                    "final_state.headline_news_source_status": "source_confirmed",
                    "final_state.headline_news_source_confirmed": True,
                    "final_diagnostics.headline_news_status": "NEWS_CLEAR",
                    "watch_only": True,
                    "no_trade_boundary.trade_approval": False,
                },
                expected_contains={
                    "final_state.news_evidence_refs": [
                        "synthetic-caller-news-ref-a"
                    ],
                    "final_state.news_policy_reason_codes": [
                        "news_clear_source_confirmed"
                    ],
                },
                expected_absent_fields=[
                    "headline_text",
                    "macro_event",
                    "earnings_event",
                    "filing",
                    "rumor",
                    "live_fact",
                ],
            )
        )

        self.assertTrue(result["final_state"]["headline_news_source_confirmed"])
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])


if __name__ == "__main__":
    unittest.main()
