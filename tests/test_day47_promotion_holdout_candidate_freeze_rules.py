from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"


class Day47PromotionHoldoutCandidateFreezeRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline_text = PIPELINE.read_text(encoding="utf-8")

    def test_promotion_ladder_has_all_required_gates(self):
        for gate in [
            "1. Development evidence",
            "2. Grouped replay eligibility",
            "3. Regression acceptance",
            "4. Protected-holdout evaluation",
            "5. Controlled paper-validation eligibility",
            "6. Paper-to-live review eligibility",
        ]:
            with self.subTest(gate=gate):
                self.assertIn(gate, self.pipeline_text)

        for required_column in [
            "Required evidence",
            "Required tests",
            "Minimum sample or coverage",
            "Execution-cost assumptions",
            "Risk requirements",
            "Automatic failure conditions",
            "Permitted next action",
            "Advancement approval",
        ]:
            with self.subTest(column=required_column):
                self.assertIn(required_column, self.pipeline_text)

    def test_exact_day90_outcomes_are_defined_without_open_ended_outcome(self):
        outcomes = re.findall(r"`([A-Z_]+)`", self.pipeline_text)
        expected = {
            "PAPER_VALIDATION_ELIGIBLE",
            "BOUNDED_REPAIR_REQUIRED",
            "NARROWED_PLAN",
            "REDESIGN_REQUIRED",
        }
        self.assertTrue(expected.issubset(set(outcomes)))
        self.assertNotIn("CONTINUE_DEVELOPING", outcomes)
        self.assertIn('Undefined outcomes such as "continue developing" are not allowed.', self.pipeline_text)

    def test_sample_contract_has_exact_family_counts_and_no_vague_placeholders(self):
        for family in ["Ideal", "Clean Fast Break", "Continuation"]:
            with self.subTest(family=family):
                self.assertRegex(self.pipeline_text, rf"\| {re.escape(family)} \| 20 \| 10 \| 5 \| 5 \| 5 \| 8 \| 4 \|")

        forbidden = ["TBD", "sufficient", "representative"]
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.pipeline_text)

    def test_holdout_and_candidate_freeze_rules_block_hindsight(self):
        required_phrases = [
            "selected before outcome inspection",
            "committed before reveal",
            "excluded from tuning, repair, threshold selection, candidate ranking, stable-winner selection",
            "post-reveal rule or configuration change invalidates the affected holdout result",
            "Candidate generation and option-contract selection must use only information available at the decision timestamp",
            "selecting candidates because they later looked profitable",
            "selecting the best-performing contract retrospectively",
            "using future bars, quotes, classifications, exit information, fills, P&L, or profitability",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_control_files_agree_on_canonical_rule_doc_and_next_task(self):
        canonical = "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"
        next_task = "SAFE_FAST_DAY47_CFB_EXECUTION_REALISM_RULES_CODEX_TASK.md"
        result = "SAFE_FAST_DAY47_PROMOTION_HOLDOUT_AND_CANDIDATE_FREEZE_RULES_RESULT.md"
        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
            "SAFE_FAST_DAY47_PROMOTION_HOLDOUT_AND_CANDIDATE_FREEZE_RULES_RESULT.md",
        ]:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path, item=canonical):
                self.assertIn(canonical, text)
            with self.subTest(path=relative_path, item=next_task):
                self.assertIn(next_task, text)
            with self.subTest(path=relative_path, item=result):
                self.assertIn(result, text)


if __name__ == "__main__":
    unittest.main()
