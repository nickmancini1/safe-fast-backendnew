import copy
import subprocess
import unittest

from watcher_foundation.constants import (
    EVIDENCE_ROWS_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
)
from watcher_foundation.headline_news import (
    REQUIRED_HEADLINE_NEWS_POLICY_FIELDS,
    evaluate_headline_news_policy,
)


class HeadlineNewsPolicyPlaceholderTests(unittest.TestCase):
    def _valid_source(self, **overrides):
        source = {
            "headline_news_status": "NEWS_CLEAR",
            "source_status": "source_confirmed",
            "source_as_of": "2026-05-24T09:35:00-04:00",
            "evidence_refs": ["accepted-source-row-1"],
            "unavailable_fields": [],
            "watch_only": True,
        }
        source.update(overrides)
        return source

    def test_missing_source_returns_news_unconfirmed(self):
        result = evaluate_headline_news_policy()

        self.assertEqual(result["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertEqual(result["source_as_of"], SOURCE_AS_OF_UNCONFIRMED)
        self.assertEqual(result["evidence_refs"], [EVIDENCE_ROWS_UNCONFIRMED])
        self.assertTrue(set(REQUIRED_HEADLINE_NEWS_POLICY_FIELDS).issubset(result))

    def test_empty_source_returns_news_unconfirmed(self):
        result = evaluate_headline_news_policy({})

        self.assertEqual(result["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertIn("source_payload_empty", result["policy_reason_codes"])

    def test_invalid_source_returns_news_unconfirmed(self):
        result = evaluate_headline_news_policy(
            self._valid_source(headline_news_status="NEWS_GOOD")
        )

        self.assertEqual(result["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertIn("source_payload_invalid_status", result["policy_reason_codes"])

    def test_missing_source_as_of_returns_news_unconfirmed(self):
        source = self._valid_source()
        source.pop("source_as_of")

        result = evaluate_headline_news_policy(source)

        self.assertEqual(result["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertIn("source_as_of_missing", result["policy_reason_codes"])
        self.assertIn(SOURCE_AS_OF_UNCONFIRMED, result["unavailable_fields"])

    def test_missing_evidence_refs_returns_news_unconfirmed(self):
        source = self._valid_source()
        source.pop("evidence_refs")

        result = evaluate_headline_news_policy(source)

        self.assertEqual(result["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertIn("evidence_refs_missing", result["policy_reason_codes"])
        self.assertEqual(result["evidence_refs"], [EVIDENCE_ROWS_UNCONFIRMED])

    def test_valid_news_clear_payload_returns_news_clear(self):
        result = evaluate_headline_news_policy(
            self._valid_source(headline_news_status="NEWS_CLEAR")
        )

        self.assertEqual(result["headline_news_status"], "NEWS_CLEAR")
        self.assertTrue(result["headline_news_source_confirmed"])
        self.assertFalse(result["news_blocker"])

    def test_valid_news_caution_payload_returns_news_caution(self):
        result = evaluate_headline_news_policy(
            self._valid_source(headline_news_status="NEWS_CAUTION")
        )

        self.assertEqual(result["headline_news_status"], "NEWS_CAUTION")
        self.assertTrue(result["headline_news_source_confirmed"])
        self.assertFalse(result["news_blocker"])

    def test_valid_news_block_payload_returns_news_block(self):
        result = evaluate_headline_news_policy(
            self._valid_source(headline_news_status="NEWS_BLOCK")
        )

        self.assertEqual(result["headline_news_status"], "NEWS_BLOCK")
        self.assertTrue(result["headline_news_source_confirmed"])
        self.assertTrue(result["news_blocker"])

    def test_news_unconfirmed_does_not_create_blocker_by_itself(self):
        result = evaluate_headline_news_policy()

        self.assertEqual(result["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertFalse(result["news_blocker"])
        self.assertIn("not a news blocker", result["policy_explanation"])

    def test_news_block_stays_watch_only_and_does_not_imply_trade_approval(self):
        result = evaluate_headline_news_policy(
            self._valid_source(headline_news_status="NEWS_BLOCK")
        )

        self.assertIs(result["watch_only"], True)
        self.assertIs(result["live_trade_approval"], False)
        self.assertIs(result["trade_approval"], False)
        self.assertIn("does not approve a trade", result["policy_explanation"])

    def test_watch_only_false_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            evaluate_headline_news_policy(self._valid_source(watch_only=False))

    def test_forbidden_execution_account_order_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            evaluate_headline_news_policy(self._valid_source(order_id="abc"))

        with self.assertRaisesRegex(ValueError, "account_id"):
            evaluate_headline_news_policy(
                self._valid_source(nested={"account_id": "abc"})
            )

    def test_input_is_not_mutated(self):
        source = self._valid_source(
            evidence_refs=["source-row-1"],
            unavailable_fields=[NEWS_UNCONFIRMED],
        )
        before = copy.deepcopy(source)

        result = evaluate_headline_news_policy(source)
        result["evidence_refs"].append("changed")

        self.assertEqual(source, before)

    def test_explicit_unavailable_markers_are_preserved(self):
        result = evaluate_headline_news_policy(
            self._valid_source(unavailable_fields=[NEWS_UNCONFIRMED])
        )

        self.assertIn(NEWS_UNCONFIRMED, result["unavailable_fields"])

    def test_unconfirmed_status_from_valid_source_remains_unconfirmed(self):
        result = evaluate_headline_news_policy(
            self._valid_source(headline_news_status=NEWS_UNCONFIRMED)
        )

        self.assertEqual(result["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertFalse(result["news_blocker"])
        self.assertFalse(result["trade_approval"])

    def test_main_py_has_no_change(self):
        result = subprocess.run(
            ["git", "diff", "--quiet", "--", "main.py"],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
