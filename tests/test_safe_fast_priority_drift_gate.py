import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "SAFE_FAST_SOURCE_TO_DECISION_OPERATING_LOOP.md",
    "SAFE_FAST_BUILD_STATE.md",
    "SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md",
    "SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt",
    "SAFE_FAST_PROJECT_DASHBOARD.md",
    "SAFE_FAST_PROJECT_RULE_INDEX.md",
]

class TestSafeFastPriorityDriftGate(unittest.TestCase):
    def test_gate_is_at_top_of_canonical_files(self):
        for name in FILES:
            text = (ROOT / name).read_text(encoding="utf-8-sig")
            self.assertIn("SAFE_FAST_PRIORITY_DRIFT_GATE_BEGIN", text[:2000], name)
            self.assertIn("Priority check: Am I efficiently working on the current priority task and not drifting?", text, name)
            self.assertIn("This step is: Substance or busy work.", text, name)
            self.assertIn("Busy work is forbidden unless current `git status --short` proves it physically blocks the priority task.", text, name)

    def test_startup_script_prints_priority_gate(self):
        text = (ROOT / "scripts" / "safe_fast_new_chat_status.ps1").read_text(encoding="utf-8-sig")
        self.assertIn("PRIORITY_DRIFT_GATE:", text)
        self.assertIn("PRIORITY_ALLOWED_STEPS:", text)
        self.assertIn("entry/exit/P&L", text)

    def test_vertical_execution_gate_blocks_fragmented_busy_work(self):
        for name in FILES:
            text = (ROOT / name).read_text(encoding="utf-8-sig")
            self.assertIn("### Vertical execution gate", text, name)
            self.assertIn("A substance command must complete the full vertical step whenever possible", text, name)
            self.assertIn("Do not split a substance step into repeated readback", text, name)
            self.assertIn("After one read-only gate command, the next response must either", text, name)
            self.assertIn("if the information already exists in the latest machine-readable result, do not ask for another readback", text, name)

    def test_startup_script_prints_vertical_execution_gate(self):
        text = (ROOT / "scripts" / "safe_fast_new_chat_status.ps1").read_text(encoding="utf-8-sig")
        self.assertIn("PRIORITY_VERTICAL_EXECUTION_GATE:", text)
        self.assertIn("Substance commands must complete result, tests, diff check, commit", text)

if __name__ == "__main__":
    unittest.main()
