from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"


class Day47CFBExecutionRealismRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline_text = PIPELINE.read_text(encoding="utf-8")

    def test_canonical_pipeline_defines_required_execution_realism_rules(self):
        self.assertIn("## Clean Fast Break Execution Realism Rules", self.pipeline_text)

        required_rules = [
            "Signal-to-decision latency",
            "Usable quote age",
            "Order size and minimum quote size",
            "Partial-fill behavior",
            "Target-touch recognition",
            "Stop-touch recognition",
            "Same-interval target/stop ordering",
            "Bid/ask/spread handling",
            "No-fallback selected-contract discipline",
            "Missing, delayed, crossed, locked, zero, or malformed quotes",
        ]
        for rule in required_rules:
            with self.subTest(rule=rule):
                self.assertIn(rule, self.pipeline_text)

    def test_execution_rules_have_evidence_regression_failure_and_no_proof_columns(self):
        required_columns = [
            "Required evidence",
            "Required regression cases",
            "Automatic failure conditions",
            "Current replay-output effect",
            "No-proof boundary",
        ]
        for column in required_columns:
            with self.subTest(column=column):
                self.assertIn(column, self.pipeline_text)

        required_no_proof_phrases = [
            "Existing CFB replay outputs remain review-only",
            "does not become proof, profitability, readiness, paper eligibility, or live readiness",
            "does not prove expectancy, paper eligibility, or live fill quality",
            "not a broker-fill guarantee",
        ]
        for phrase in required_no_proof_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_frozen_quote_age_and_no_fallback_controls_are_preserved(self):
        required_phrases = [
            "older than `5` minutes",
            "quote_age_above_5_minutes",
            "Accepted and frozen",
            "No-fallback selected-contract discipline",
            "cannot scan to a later or better-performing contract",
            "selecting the best-performing contract retrospectively",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_countability_rules_cover_size_partial_fill_touch_ordering_and_bad_quotes(self):
        required_phrases = [
            "The only countable replay size is `1` option contract.",
            "Partial fills cannot be counted unless an exact broker or exchange fill log is later authorized",
            "selected-contract bid minus `0.02` is at or above the frozen `+25%` target threshold",
            "selected-contract bid minus `0.02` is at or below the frozen `-15%` stop threshold",
            "If target and stop have distinct selected-contract quote timestamps, the earliest timestamp wins.",
            "If both are touched at the same timestamp or only inside the same unresolved interval, the stop wins",
            "spread no more than `0.15`",
            "spread percent no more than `2.00%`",
            "Missing, delayed beyond the allowed decision/quote-age window, crossed, zero, negative, unparsable, wrong-symbol, wrong-instrument, or malformed",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_control_files_agree_on_result_canonical_doc_and_next_task(self):
        result = "SAFE_FAST_DAY47_CFB_EXECUTION_REALISM_RULES_RESULT.md"
        canonical = "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"
        next_task = "SAFE_FAST_DAY47_RISK_CAPITAL_RULES_CODEX_TASK.md"

        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
            "SAFE_FAST_DAY47_CFB_EXECUTION_REALISM_RULES_RESULT.md",
        ]:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path, item=result):
                self.assertIn(result, text)
            with self.subTest(path=relative_path, item=canonical):
                self.assertIn(canonical, text)
            with self.subTest(path=relative_path, item=next_task):
                self.assertIn(next_task, text)


if __name__ == "__main__":
    unittest.main()
