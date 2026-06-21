import json
import unittest
from pathlib import Path

from watcher_foundation import safe_fast_data_source_resolver as resolver


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "historical_signal_replay" / "config" / "safe_fast_data_source_registry.json"


class SafeFastDataSourceRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        cls.entries = {entry["field_identifier"]: entry for entry in cls.registry["entries"]}

    def test_registry_entries_are_schema_complete_without_vague_sources(self):
        required = set(self.registry["required_entry_fields"])
        allowed_classes = {
            "REQUIRED_FOR_SETUP_LABEL",
            "REQUIRED_FOR_TRADE_ELIGIBILITY",
            "REQUIRED_FOR_EXECUTION",
            "REQUIRED_FOR_EXIT",
            "OPTIONAL_CONTEXT",
            "REVIEW_ONLY",
        }
        vague_tokens = ("TBD", "UNKNOWN_SOURCE", "sufficient source")

        self.assertGreaterEqual(len(self.entries), 20)
        for entry in self.registry["entries"]:
            self.assertEqual(set(entry), required)
            self.assertIn(entry["requirement_class"], allowed_classes)
            for key, value in entry.items():
                if isinstance(value, str):
                    self.assertTrue(value.strip(), f"{entry['field_identifier']} {key} is blank")
                    self.assertFalse(
                        any(token in value for token in vague_tokens),
                        f"{entry['field_identifier']} {key} contains vague source text",
                    )

    def test_every_current_required_setup_field_has_exact_source(self):
        for field in (
            "setup_time_row",
            "trigger",
            "invalidation",
            "freshness_final_signal_state",
            "blocker_caution_review",
            "no_hindsight_boundary",
            "session_boundary_behavior",
        ):
            entry = self.entries[field]
            self.assertIn("SAFE-FAST", entry["primary_source"])
            self.assertTrue(entry["consumer_module"])
            self.assertTrue(entry["validation_test"])

    def test_setup_labels_map_only_to_safe_fast_not_external_vendors(self):
        for field in (
            "setup_time_row",
            "trigger",
            "invalidation",
            "freshness_final_signal_state",
            "no_hindsight_boundary",
            "session_boundary_behavior",
        ):
            entry = self.entries[field]
            combined = " ".join([entry["primary_source"], entry["historical_authority"]])
            self.assertIn("SAFE-FAST", combined)
            self.assertNotIn("Databento", entry["primary_source"])
            self.assertNotIn("Schwab", entry["primary_source"])

    def test_options_history_maps_primarily_to_databento_and_not_tcbbo_alone(self):
        for field in (
            "option_contract_definition",
            "option_quote_freshness_cmbp1",
            "option_trades",
            "option_statistics_volume_open_interest",
        ):
            self.assertEqual(self.entries[field]["historical_authority"].split()[0], "Databento")
            self.assertIn("OPRA.PILLAR", self.entries[field]["dataset_schema_api_series_endpoint_or_calculator"])

        tcbbo = self.entries["option_tcbbo_trade_linked_context"]
        self.assertEqual(tcbbo["requirement_class"], "REVIEW_ONLY")
        self.assertIn("Cannot be sole quote freshness source", tcbbo["historical_vintage_rule"])
        self.assertFalse(tcbbo["may_block_trade_eligibility"])

    def test_live_schwab_fills_remain_authoritative(self):
        entry = self.entries["schwab_live_fill"]
        self.assertEqual(entry["primary_source"], "Charles Schwab")
        self.assertEqual(entry["live_authority"], "Charles Schwab")
        self.assertIn("cannot override an actual Schwab fill", entry["fallback_behavior"])

    def test_revised_macro_data_cannot_replace_historical_vintages(self):
        entry = self.entries["macro_historical_vintage"]
        self.assertIn("ALFRED", entry["primary_source"])
        self.assertIn("Revised present-day macro values cannot silently replace", entry["historical_vintage_rule"])

    def test_optional_context_cannot_silently_block_setup(self):
        optional = [
            entry for entry in self.registry["entries"]
            if entry["requirement_class"] in {"OPTIONAL_CONTEXT", "REVIEW_ONLY"}
        ]
        self.assertTrue(optional)
        for entry in optional:
            self.assertFalse(entry["may_block_setup_qualification"], entry["field_identifier"])

    def test_resolver_returns_read_only_plan_and_unavailable_action(self):
        plan = resolver.resolve_unavailable_field(
            "option_quote_freshness_cmbp1",
            "2026-04-13T16:30:00Z",
            "cmbp-1 quote entitlement not confirmed for this exact request",
        )

        self.assertFalse(plan["vendor_contacted"])
        self.assertFalse(plan["secrets_read"])
        self.assertFalse(plan["missing_data_label_allowed"])
        self.assertEqual(plan["field_identifier"], "option_quote_freshness_cmbp1")
        self.assertIn("OPRA.PILLAR / cmbp-1", plan["dataset_schema_api_series_endpoint_or_calculator"])
        self.assertIn("trade", plan["blocking_targets"])
        self.assertIn("verify entitlement", plan["unavailable_next_action"])
        self.assertEqual(
            plan["required_report_fields"]["exact_reason_unavailable"],
            "cmbp-1 quote entitlement not confirmed for this exact request",
        )

    def test_current_candidate_blockers_are_mapped_without_ohlcv_overclaim(self):
        blockers = self.registry["current_candidate_blockers"]
        self.assertEqual(len(blockers), 8)
        for blocker in blockers:
            self.assertFalse(blocker["ohlcv_should_have_resolved"])
            self.assertIn("setup_time_row", blocker["proper_fields"])
            self.assertIn(
                blocker["candidate_action"],
                {
                    "EXACT_EXTERNAL_SETUP_DATA_REQUIRED",
                    "SOURCE_CONFLICT",
                    "SOURCE_UNAVAILABLE_CANDIDATE_EXCLUDED",
                },
            )

    def test_control_files_point_to_canonical_registry_and_schwab_task(self):
        dashboard = (ROOT / "SAFE_FAST_PROJECT_DASHBOARD.md").read_text(encoding="utf-8")
        rule_index = (ROOT / "SAFE_FAST_PROJECT_RULE_INDEX.md").read_text(encoding="utf-8")
        next_chat = (ROOT / "SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt").read_text(encoding="utf-8")
        for text in (dashboard, rule_index, next_chat):
            self.assertIn("SAFE_FAST_DATA_SOURCE_REGISTRY.md", text)
            self.assertIn("SAFE_FAST_DAY50_SCHWAB_READ_ONLY_AUTH_AND_CAPABILITY_AUDIT_CODEX_TASK.md", text)
            self.assertIn("Do not report vague MISSING_DATA", text)


if __name__ == "__main__":
    unittest.main()
