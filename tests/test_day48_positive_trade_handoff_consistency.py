from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Day48PositiveTradeHandoffConsistencyTests(unittest.TestCase):
    def test_current_control_files_agree_on_active_positive_entry_task(self):
        active_task = (
            "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXACT_SETUP_DATA_APPROVAL_DOWNLOAD_CODEX_TASK.md"
        )
        result_doc = (
            "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_EVIDENCE_COMPLETION_OR_REPLACEMENT_RESULT.md"
        )
        funnel_json = "historical_signal_replay/results/day48_positive_trade_capture_funnel.json"

        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
            "SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt",
            "SAFE_FAST_DAY46_NEXT_CHAT_HANDOFF_START_HERE.md",
            "SAFE_FAST_DAY46_NEXT_CHAT_START_BLOCK.txt",
        ]:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn(active_task, text)
                self.assertIn(result_doc, text)
                self.assertIn(funnel_json, text)

    def test_handoff_requires_build_state_first_and_funnel_scorecards(self):
        handoff = (ROOT / "SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt").read_text(
            encoding="utf-8"
        )

        self.assertIn("Read SAFE_FAST_BUILD_STATE.md first", handoff)
        self.assertIn("funnel scorecard", handoff)
        self.assertIn("VALID_TRADE_CAPTURED", handoff)
        self.assertIn("TRUE_NO_TRADE", handoff)
        self.assertIn("MISSING_DATA", handoff)
        self.assertIn("MISSED_VALID_TRADE", handoff)
        self.assertIn("INVALID_TRADE_ALLOWED", handoff)
        self.assertIn("UNRESOLVED", handoff)
        self.assertIn("exact cost check and user approval", handoff)

    def test_current_files_preserve_positive_trade_completion_plan(self):
        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
        ]:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn("positive", text.lower())
                self.assertIn("valid trade", text.lower())
                self.assertIn("true no-trade", text.lower())
                self.assertIn("missing-data", text.lower())
                self.assertIn("missed valid", text.lower())
                self.assertIn("invalid trades allowed", text.lower())


if __name__ == "__main__":
    unittest.main()
