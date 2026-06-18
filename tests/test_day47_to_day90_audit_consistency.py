from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Day47ToDay90AuditConsistencyTest(unittest.TestCase):
    def test_audit_result_covers_required_control_sections(self):
        text = (ROOT / "SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_RESULT.md").read_text(
            encoding="utf-8"
        )

        required_sections = [
            "## Canonical Owners",
            "## Mandatory Requirement Classification",
            "## Contradictions And Duplicates To Resolve",
            "## Ordered Day 47 To Day 90 Completion Plan",
            "## Future-Chat Continuity Contract",
            "## Guardrail Result",
        ]
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, text)

        for index in range(1, 34):
            with self.subTest(requirement=index):
                self.assertIn(f"| {index} |", text)

        for classification in [
            "defined",
            "partially_defined",
            "missing",
            "contradictory",
            "proven_by_tests",
        ]:
            with self.subTest(classification=classification):
                self.assertIn(classification, text)

    def test_canonical_docs_reference_audit_result(self):
        result_name = "SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_RESULT.md"
        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
        ]:
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(result_name, text)


if __name__ == "__main__":
    unittest.main()
