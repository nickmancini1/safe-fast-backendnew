from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"


class Day47PortfolioInteractionRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline_text = PIPELINE.read_text(encoding="utf-8")

    def test_canonical_pipeline_defines_required_portfolio_rules(self):
        self.assertIn("## Portfolio And Setup-Family Interaction Rules", self.pipeline_text)

        required_rules = [
            "Overlapping signals",
            "Duplicate exposure",
            "Correlated underlying exposure",
            "Simultaneous candidate precedence",
            "Setup evolution and replacement",
            "Cross-family and same-family candidate conflicts",
            "Capital-slot competition using the risk/capital package",
            "Missing, partial, contradictory, or unverifiable portfolio-interaction evidence",
        ]
        for rule in required_rules:
            with self.subTest(rule=rule):
                self.assertIn(rule, self.pipeline_text)

    def test_portfolio_rules_have_required_evidence_regression_failure_effect_and_no_proof_columns(self):
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
            "not proof, profitability, paper eligibility, or live readiness",
            "not stable-winner selection",
            "does not prove expectancy or readiness",
        ]
        for phrase in required_no_proof_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_frozen_cfb_and_risk_rules_are_preserved(self):
        required_phrases = [
            "do not change any frozen Clean Fast Break trading or execution-realism rule",
            "entry from ask plus `0.02`",
            "exit from bid minus `0.02`",
            "`5` minute quote-age failure",
            "one-contract CFB countability",
            "no-fallback selected-contract discipline",
            "did not change the one-position limit",
            "did not change any accepted risk/capital numeric threshold",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_precedence_duplicate_correlation_and_replacement_are_blocker_preserving(self):
        required_phrases = [
            "first valid signal timestamp wins",
            "if still tied, block all tied candidates as unresolved",
            "A same-underlying, same-direction, same-or-equivalent selected-contract exposure cannot be counted twice",
            "must share the same one-position capital slot unless a later rule explicitly classifies them as independent",
            "A later candidate may replace an earlier watch/candidate only when the earlier setup is source-backed as stale, spent, invalidated, or blocked before the later signal",
            "No. The accepted portfolio/setup-family interaction rules keep one open option position and select at most one pre-outcome capital-slot winner.",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_control_files_agree_on_result_canonical_doc_and_next_task(self):
        result = "SAFE_FAST_DAY47_PORTFOLIO_INTERACTION_RULES_RESULT.md"
        canonical = "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"
        next_task = "SAFE_FAST_DAY47_DATA_COST_LEDGER_RULES_CODEX_TASK.md"

        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
            "SAFE_FAST_DAY47_PORTFOLIO_INTERACTION_RULES_RESULT.md",
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
