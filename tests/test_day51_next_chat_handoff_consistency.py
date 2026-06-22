import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CANONICAL_HANDOFF = "SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md"
CANONICAL_INTRO = "SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt"
STARTUP_SCRIPT = "scripts/safe_fast_new_chat_status.ps1"
ACTIVE_TASK = "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_CODEX_TASK.md"


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class Day51NextChatHandoffConsistencyTests(unittest.TestCase):
    def test_canonical_files_exist(self):
        self.assertTrue((ROOT / CANONICAL_HANDOFF).is_file())
        self.assertTrue((ROOT / CANONICAL_INTRO).is_file())
        self.assertTrue((ROOT / STARTUP_SCRIPT).is_file())

    def test_rule_index_names_exactly_one_current_handoff_intro_and_script(self):
        rule_index = read_text("SAFE_FAST_PROJECT_RULE_INDEX.md")
        self.assertEqual(rule_index.count(f"Current full handoff: `{CANONICAL_HANDOFF}`"), 1)
        self.assertEqual(rule_index.count(f"Current intro block: `{CANONICAL_INTRO}`"), 1)
        self.assertEqual(rule_index.count(f"Current startup script: `{STARTUP_SCRIPT}`"), 1)
        self.assertIn("Historical handoffs", rule_index)

    def test_older_handoffs_are_historical(self):
        rule_index = read_text("SAFE_FAST_PROJECT_RULE_INDEX.md")
        for historical in (
            "SAFE_FAST_DAY46_NEXT_CHAT_HANDOFF_START_HERE.md",
            "SAFE_FAST_DAY46_NEXT_CHAT_START_BLOCK.txt",
            "SAFE_FAST_DAY41_RAW_TASTYTRADE_NEXT_CHAT_HANDOFF.md",
            "SAFE_FAST_DAY39_COMBINED_HANDOFF_AND_FAST_CANDIDATE_FUNNEL.md",
            "SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md",
            "SAFE_FAST_DAY46_HANDOFF_POWER_SHELL_CODEX_WORKFLOW.md",
            "SAFE_FAST_DAY46_HANDOFF_CURRENT_STATE_AND_FINAL_SPRINT_PLAN.md",
            "SAFE_FAST_DAY60_PRODUCT_BUSINESS_HANDOFF_ADDENDUM.md",
        ):
            self.assertIn(historical, rule_index)
            self.assertTrue(
                read_text(historical)
                .lstrip("\ufeff")
                .startswith("SUPERSEDED: Read SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md")
            )

    def test_intro_points_to_handoff_and_startup_script(self):
        intro = read_text(CANONICAL_INTRO)
        self.assertIn(CANONICAL_HANDOFF, intro)
        self.assertIn("SAFE_FAST_BUILD_STATE.md", intro)
        self.assertIn(STARTUP_SCRIPT.replace("/", "\\"), intro)
        self.assertIn("powershell -NoProfile -ExecutionPolicy Bypass -File", intro)

    def test_build_state_current_section_has_required_fields_and_active_task_exists(self):
        build_state = read_text("SAFE_FAST_BUILD_STATE.md")
        match = re.search(
            r"<!-- SAFE_FAST_CURRENT_STATE_BEGIN -->(.*?)<!-- SAFE_FAST_CURRENT_STATE_END -->",
            build_state,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        section = match.group(1)
        for field in (
            "PROJECT_DAY",
            "PROJECT_DATE",
            "ACTIVE_OBJECTIVE",
            "ACTIVE_TASK",
            "ACTIVE_TASK_PURPOSE",
            "PROVEN_SUMMARY",
            "UNPROVEN_SUMMARY",
            "CURRENT_FUNNEL_TOTALS",
            "CURRENT_TECHNICAL_PACKAGE",
            "CURRENT_TECHNICAL_RESULT",
            "SCHWAB_STATUS",
            "DATA_SOURCE_REGISTRY",
            "NEXT_ACTION",
        ):
            self.assertRegex(section, rf"- {field}: .+")
        self.assertIn(ACTIVE_TASK, section)
        self.assertTrue((ROOT / ACTIVE_TASK).is_file())

    def test_active_task_references_agree_across_control_files(self):
        for relative_path in (
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
            CANONICAL_HANDOFF,
        ):
            with self.subTest(path=relative_path):
                self.assertIn(ACTIVE_TASK, read_text(relative_path))

    def test_handoff_required_contracts_and_state(self):
        handoff = read_text(CANONICAL_HANDOFF)
        for phrase in (
            "Communication contract",
            "PowerShell contract",
            "Real progress measurement",
            "Data-source hierarchy",
            "Schwab Trader API access is pending approval",
            "Current technical objective",
            "raw one-minute underlying OHLCV evidence",
        ):
            self.assertIn(phrase, handoff)

    def test_startup_script_dynamic_and_bounded(self):
        script = read_text(STARTUP_SCRIPT)
        self.assertIn("git --no-pager branch --show-current", script)
        self.assertIn("git --no-pager rev-parse --short HEAD", script)
        self.assertIn("log -3 --oneline", script)
        self.assertNotIn("50ed53e2eaa044a0c6e25425334a1b8f9f013a84", script)
        self.assertLessEqual(len(script.splitlines()), 120)

    def test_current_package_has_no_stale_current_commit_claim(self):
        for relative_path in (
            "SAFE_FAST_BUILD_STATE.md",
            CANONICAL_HANDOFF,
            CANONICAL_INTRO,
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
        ):
            text = read_text(relative_path)
            with self.subTest(path=relative_path):
                self.assertNotIn("Latest known local HEAD", text)
                self.assertNotIn("current commit:", text.lower())


if __name__ == "__main__":
    unittest.main()
