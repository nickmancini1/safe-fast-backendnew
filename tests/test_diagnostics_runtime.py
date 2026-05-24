import copy
import subprocess
import unittest

from watcher_foundation.constants import (
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SESSION_DATE_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.diagnostics import (
    DIAGNOSTIC_REASON_CODE_GROUPS,
    build_diagnostics,
)


class DiagnosticsRuntimeTests(unittest.TestCase):
    def _card(self, **overrides):
        card = {
            "candidate_id": "SPY-Ideal-1",
            "symbol": "SPY",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "trigger_level_or_zone": "SPY reclaim zone",
            "confirmation_timeframe_rule": "completed 5m hold",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": "fail below reclaim base",
            "fresh_stale_spent_state": "fresh",
            "regular_session_date": "2026-05-24",
            "source_as_of": "2026-05-24T09:35:00-04:00",
            "evidence_rows": ["row-1"],
            "evidence_refs": ["source:row-1"],
            "evidence_quality": "deterministic",
            "blockers": [],
            "cautions": [],
            "unavailable_fields": [],
            "headline_news_status": NEWS_UNCONFIRMED,
            "no_trade_reason": "watch_only_no_live_trade_approval",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "watch_only": True,
        }
        card.update(overrides)
        return card

    def test_diagnostics_returns_required_fields_and_groups(self):
        diagnostics = build_diagnostics(self._card())

        required = {
            "diagnostic_reason_codes",
            "diagnostic_explanation",
            "diagnostic_scope",
            "evidence_refs",
            "unavailable_fields",
            "no_trade_reason",
            "next_check_or_next_alert_condition",
            "focus_rank_reason",
            "suppression_reason",
            "watch_only",
        }
        self.assertTrue(required.issubset(diagnostics))
        self.assertEqual(
            set(diagnostics["diagnostic_reason_codes"]),
            set(DIAGNOSTIC_REASON_CODE_GROUPS),
        )

    def test_watch_only_true_is_preserved(self):
        diagnostics = build_diagnostics(self._card())

        self.assertIs(diagnostics["watch_only"], True)

    def test_watch_only_false_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            build_diagnostics(self._card(watch_only=False))

    def test_forbidden_execution_account_order_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            build_diagnostics(self._card(order_id="abc"))

        with self.assertRaisesRegex(ValueError, "account_id"):
            build_diagnostics(self._card(nested={"account_id": "abc"}))

    def test_input_is_not_mutated(self):
        card = self._card(blockers=[{"reason_code": "accepted_blocker"}])
        before = copy.deepcopy(card)

        diagnostics = build_diagnostics(card)
        diagnostics["evidence_refs"].append("changed")

        self.assertEqual(card, before)

    def test_news_unconfirmed_defaults_and_does_not_create_news_blocker(self):
        card = self._card()
        card.pop("headline_news_status")

        diagnostics = build_diagnostics(card)

        self.assertEqual(diagnostics["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertIn(
            "headline_news_status.news_unconfirmed",
            diagnostics["diagnostic_reason_codes"]["headline_news_status"],
        )
        self.assertNotIn(
            "blocker.news_source_confirmed_block",
            diagnostics["diagnostic_reason_codes"]["blocker"],
        )

    def test_unavailable_markers_are_preserved(self):
        diagnostics = build_diagnostics(
            self._card(
                trigger_level_or_zone=TRIGGER_LEVEL_UNCONFIRMED,
                distance_to_trigger=DISTANCE_TO_TRIGGER_UNCONFIRMED,
                invalidation_level_or_condition=INVALIDATION_UNCONFIRMED,
                source_as_of=SOURCE_AS_OF_UNCONFIRMED,
                regular_session_date=SESSION_DATE_UNCONFIRMED,
                evidence_rows=[EVIDENCE_ROWS_UNCONFIRMED],
                evidence_refs=[EVIDENCE_ROWS_UNCONFIRMED],
                unavailable_fields=[
                    TRIGGER_LEVEL_UNCONFIRMED,
                    DISTANCE_TO_TRIGGER_UNCONFIRMED,
                    INVALIDATION_UNCONFIRMED,
                    SOURCE_AS_OF_UNCONFIRMED,
                    SESSION_DATE_UNCONFIRMED,
                    EVIDENCE_ROWS_UNCONFIRMED,
                ],
            )
        )

        self.assertIn(TRIGGER_LEVEL_UNCONFIRMED, diagnostics["unavailable_fields"])
        self.assertEqual(diagnostics["evidence_refs"], [EVIDENCE_ROWS_UNCONFIRMED])
        self.assertIn(
            "unavailable_field.trigger_level_unconfirmed",
            diagnostics["diagnostic_reason_codes"]["unavailable_field"],
        )

    def test_missing_critical_fields_produces_unavailable_no_trade_diagnostics(self):
        diagnostics = build_diagnostics(
            {
                "candidate_id": "missing",
                "symbol": "QQQ",
                "setup_type": "UNCONFIRMED",
                "stage": "unavailable/unconfirmed",
                "trigger_status": "unconfirmed",
                "watch_only": True,
            }
        )

        self.assertIn(
            "no_trade_boundary.unavailable_critical_field",
            diagnostics["diagnostic_reason_codes"]["no_trade_boundary"],
        )
        self.assertIn(
            "next_condition.resolve_unavailable_field",
            diagnostics["diagnostic_reason_codes"]["next_condition"],
        )
        self.assertIn("unconfirmed", diagnostics["diagnostic_explanation"].lower())
        self.assertIn("no_trade", diagnostics["no_trade_reason"])

    def test_triggered_signal_stage_is_explained_as_shadow_only(self):
        diagnostics = build_diagnostics(
            self._card(
                stage="triggered_signal_stage",
                trigger_status="triggered",
                no_trade_reason="triggered_for_review",
            )
        )

        self.assertIn(
            "lifecycle_stage.triggered_signal_stage_shadow_only",
            diagnostics["diagnostic_reason_codes"]["lifecycle_stage"],
        )
        self.assertIn(
            "no_trade_boundary.triggered_shadow_only",
            diagnostics["diagnostic_reason_codes"]["no_trade_boundary"],
        )
        self.assertIn("shadow signal review only", diagnostics["diagnostic_explanation"])
        self.assertIn("not live trade approval", diagnostics["diagnostic_explanation"])

    def test_stale_spent_no_fresh_trigger_is_explained_as_no_trade(self):
        diagnostics = build_diagnostics(
            self._card(
                stage="stale/spent/no-fresh-trigger",
                trigger_status="stale",
                fresh_stale_spent_state="stale",
                no_trade_reason="stale_context",
            )
        )

        self.assertIn(
            "stale_spent.stale_no_fresh_trigger",
            diagnostics["diagnostic_reason_codes"]["stale_spent"],
        )
        self.assertIn("no fresh trigger", diagnostics["diagnostic_explanation"])
        self.assertIn("no-trade", diagnostics["diagnostic_explanation"])

    def test_focus_rank_reason_is_included_when_supplied(self):
        diagnostics = build_diagnostics(
            self._card(candidate_id="SPY-Ideal-1"),
            focus_context={
                "watch_only": True,
                "ranked_candidates": [
                    {
                        "candidate_id": "SPY-Ideal-1",
                        "focus_rank_bucket": "primary_focus",
                        "focus_rank_reason": (
                            "cleanest_current_candidate_after_no_trade_discipline"
                        ),
                    }
                ],
            },
        )

        self.assertEqual(
            diagnostics["focus_rank_reason"],
            "cleanest_current_candidate_after_no_trade_discipline",
        )
        self.assertIn(
            "focus_ranking.primary_focus_selected",
            diagnostics["diagnostic_reason_codes"]["focus_ranking"],
        )

    def test_suppression_reason_is_included_when_supplied(self):
        diagnostics = build_diagnostics(
            self._card(),
            duplicate_suppression_context={
                "watch_only": True,
                "alert_decision": "suppress_duplicate",
                "suppression_reason": "same_state_repeat_no_material_change",
                "material_change_flags": [],
            },
        )

        self.assertEqual(
            diagnostics["suppression_reason"], "same_state_repeat_no_material_change"
        )
        self.assertIn(
            "duplicate_suppression.suppress_same_state_repeat",
            diagnostics["diagnostic_reason_codes"]["duplicate_suppression"],
        )
        self.assertIn(
            "next_condition.no_repeat_alert_until_change",
            diagnostics["diagnostic_reason_codes"]["next_condition"],
        )

    def test_diagnostics_do_not_override_setup_type_or_stage(self):
        diagnostics = build_diagnostics(
            self._card(setup_type="Continuation", stage="blocked/no-trade")
        )

        self.assertEqual(diagnostics["setup_type"], "Continuation")
        self.assertEqual(diagnostics["stage"], "blocked/no-trade")

    def test_evidence_rows_are_preserved_when_refs_are_unavailable(self):
        card = self._card(evidence_rows=["row-7"])
        card.pop("evidence_refs")

        diagnostics = build_diagnostics(card)

        self.assertEqual(diagnostics["evidence_refs"], ["row-7"])
        self.assertEqual(diagnostics["evidence_rows"], ["row-7"])

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
