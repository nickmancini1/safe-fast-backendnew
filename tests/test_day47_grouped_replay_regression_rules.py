from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"


class Day47GroupedReplayRegressionRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline_text = PIPELINE.read_text(encoding="utf-8")

    def test_canonical_pipeline_defines_required_grouped_replay_rules(self):
        self.assertIn("## Grouped Replay And Regression Rules", self.pipeline_text)

        required_rules = [
            "Planning versus actual run gate",
            "Frozen prerequisites before countability",
            "Accepted, rejected, ambiguous, and no-trade case handling",
            "Loser and no-trade control preservation",
            "Reproducible command and fixture mapping",
            "Stale, missing, contradictory, or unverifiable replay/regression evidence",
        ]
        for rule in required_rules:
            with self.subTest(rule=rule):
                self.assertIn(rule, self.pipeline_text)

    def test_grouped_replay_rules_have_required_evidence_regression_failure_effect_and_no_proof_columns(self):
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
            "Existing CFB replay outputs remain review-only unless rerun or reclassified",
            "does not prove profitability, readiness, paper eligibility, or live readiness",
            "not proof, profitability, readiness, paper eligibility, live readiness, or promotion",
            "it does not prove the remaining evidence is profitable",
            "not proof, profitability, readiness, promotion, paper eligibility, or live readiness",
        ]
        for phrase in required_no_proof_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_planning_run_prerequisites_controls_and_reproducibility_are_blocker_preserving(self):
        required_phrases = [
            "Grouped replay may be planned when the repo is only mapping candidates",
            "Grouped replay may actually run only after frozen candidates",
            "A planning document is not a run authorization",
            "Loser and no-trade controls must be preserved",
            "Every grouped replay/regression package must map each included row to the exact command",
            "Stale, missing, partial, contradictory, unverifiable, wrong-symbol, wrong-contract, wrong-window, post-outcome, or non-reproducible replay/regression evidence blocks countability",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_frozen_prior_rule_packages_are_preserved(self):
        required_phrases = [
            "preserve all accepted and frozen rules from the promotion ladder",
            "They did not change any accepted CFB trading rule, execution-realism rule, risk/capital threshold, portfolio-interaction rule, or data-cost ledger rule",
            "entry from ask plus `0.02`",
            "exit from bid minus `0.02`",
            "`5` minute quote-age failure",
            "one-contract CFB countability",
            "one open option position",
            "no-fallback selected-contract discipline",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.pipeline_text)

    def test_control_files_agree_on_result_canonical_doc_and_next_task(self):
        result = "SAFE_FAST_DAY47_GROUPED_REPLAY_REGRESSION_RULES_RESULT.md"
        canonical = "SAFE_FAST_PROJECT_PROOF_PIPELINE.md"
        next_task = "SAFE_FAST_DAY47_REPAIR_RETIREMENT_INVALIDATION_RULES_CODEX_TASK.md"

        for relative_path in [
            "SAFE_FAST_BUILD_STATE.md",
            "SAFE_FAST_PROJECT_DASHBOARD.md",
            "SAFE_FAST_PROJECT_RULE_INDEX.md",
            "SAFE_FAST_DAY47_GROUPED_REPLAY_REGRESSION_RULES_RESULT.md",
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
