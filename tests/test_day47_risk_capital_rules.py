from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"


class Day47RiskCapitalRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline_text = PIPELINE.read_text(encoding="utf-8")

    def test_canonical_pipeline_defines_required_risk_capital_rules(self):
        self.assertIn("## Risk And Capital Rules", self.pipeline_text)

        required_rules = [
            "Maximum loss per trade",
            "Maximum daily loss",
            "Maximum weekly loss",
            "Drawdown shutdown",
            "Consecutive-loss limits",
            "Concurrent-position limits",
            "De-risking and stop-after-failure behavior",
            "Capital competition among simultaneous candidates",
            "Missing, partial, breached, or unverifiable risk evidence",
        ]
        for rule in required_rules:
            with self.subTest(rule=rule):
                self.assertIn(rule, self.pipeline_text)

    def test_position_sizing_placeholders_cover_required_stages_and_block_paper_live(self):
        required_phrases = [
            "Development replay",
            "Protected holdout",
            "Controlled paper-validation planning",
            "Live-review eligibility",
            "`1` option contract maximum per frozen candidate",
            "Blocked until a later paper task maps the placeholder to a paper account value",
            "Blocked until completed paper logs, broker/order rollback plan, and explicit human approval exist",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_risk_rules_have_required_evidence_regression_failure_effect_and_no_proof_columns(self):
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
            "risk hygiene, not proof of positive expectancy",
            "Paper planning is not live readiness",
            "Live-review eligibility is not live trading authorization",
        ]
        for phrase in required_no_proof_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_existing_cfb_rules_are_preserved_and_risk_failures_block_countability(self):
        required_phrases = [
            "do not change any frozen Clean Fast Break trading or execution-realism rule",
            "entry from ask plus `0.02`",
            "exit from bid minus `0.02`",
            "`5` minute quote-age failure",
            "no-fallback selected-contract discipline",
            "Missing, partial, breached, or unverifiable risk evidence is an automatic blocker.",
            "keep all competing cases review-only until portfolio interaction rules exist",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_control_files_agree_on_result_canonical_doc_and_next_task(self):
        result = "SAFE_FAST_DAY47_RISK_CAPITAL_RULES_RESULT.md"
        canonical = "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"
        next_task = "SAFE_FAST_DAY47_PORTFOLIO_INTERACTION_RULES_CODEX_TASK.md"

        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
            "SAFE_FAST_DAY47_RISK_CAPITAL_RULES_RESULT.md",
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
