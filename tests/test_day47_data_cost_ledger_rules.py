from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"


class Day47DataCostLedgerRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline_text = PIPELINE.read_text(encoding="utf-8")

    def test_canonical_pipeline_defines_required_data_cost_rules(self):
        self.assertIn("## Data-Cost Ledger Rules", self.pipeline_text)

        required_rules = [
            "Expected decision value before every purchase",
            "Checked cost before every purchase",
            "Actual billed cost when available",
            "Files produced by each purchase",
            "Whether the purchase changed a decision",
            "Approval and no-download behavior",
            "Missing, partial, contradictory, or unverifiable cost evidence",
        ]
        for rule in required_rules:
            with self.subTest(rule=rule):
                self.assertIn(rule, self.pipeline_text)

    def test_data_cost_rules_have_required_evidence_regression_failure_effect_and_no_proof_columns(self):
        required_columns = [
            "Required evidence",
            "Required regression or consistency cases",
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
            "spend hygiene, not proof",
            "not validation, proof, readiness, or promotion",
            "not proof, profitability, paper eligibility, or live readiness",
        ]
        for phrase in required_no_proof_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_approval_no_download_and_billing_reconciliation_are_blocker_preserving(self):
        required_phrases = [
            "User approval is required before any paid download",
            "Stop at cost check/planning; do not download.",
            "`NOT_AVAILABLE` allowed only when billing has not posted",
            "must be reconciled later when available",
            "SPY CFB 003 remains a useful no-trade control because the approved data cured `quote_after_signal` but confirmed `quote_age_above_5_minutes`",
            "Missing, partial, contradictory, or unverifiable data-cost evidence is an automatic blocker.",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_frozen_cfb_risk_and_portfolio_rules_are_preserved(self):
        required_phrases = [
            "do not change any frozen Clean Fast Break trading, execution-realism, risk/capital, or portfolio-interaction rule",
            "entry from ask plus `0.02`",
            "exit from bid minus `0.02`",
            "`5` minute quote-age failure",
            "one-contract CFB countability",
            "one open option position",
            "no-fallback selected-contract discipline",
            "They did not change any accepted CFB trading rule, execution-realism rule, risk/capital threshold, or portfolio-interaction rule",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_control_files_agree_on_result_canonical_doc_and_next_task(self):
        result = "SAFE_FAST_DAY47_DATA_COST_LEDGER_RULES_RESULT.md"
        canonical = "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"
        next_task = "SAFE_FAST_DAY47_GROUPED_REPLAY_REGRESSION_RULES_CODEX_TASK.md"

        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
            "SAFE_FAST_DAY47_DATA_COST_LEDGER_RULES_RESULT.md",
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
