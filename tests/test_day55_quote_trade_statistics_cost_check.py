import inspect
import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts import safe_fast_day55_quote_trade_statistics_cost_check as checker
from watcher_foundation import day55_quote_trade_statistics_cost_check_validator as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
TEST_TMP_ROOT = REPO_ROOT / "historical_signal_replay" / "results" / "day55_qts_cost_check_test_tmp"


class Day55QuoteTradeStatisticsCostCheckTests(unittest.TestCase):
    def test_source_request_builds_blocked_cost_only_output_without_credentials(self):
        source = checker._load_source()
        output = checker.build_blocked_output(
            source,
            "SAFE_FAST_DB_AUTH_NOT_CONFIGURED",
            checked_at_utc="2026-06-26T00:00:00Z",
        )

        self.assertEqual(output["status"], "BLOCKED")
        self.assertTrue(output["cost_only"])
        self.assertFalse(output["vendor_metadata_call_performed"])
        self.assertFalse(output["download_performed"])
        self.assertEqual(output["request_count"], 32)
        self.assertEqual(set(output["required_schemas"]), checker.REQUIRED_SCHEMAS)
        self.assertIn("definition", output["forbidden_schemas"])
        self.assertEqual(output["profitability_proof"], "NO")
        self.assertEqual(output["paper_live_eligibility"], "NO")
        self.assertIsNone(output["gross_pnl"])
        self.assertIsNone(output["net_pnl"])

    def test_vendor_requests_strip_local_review_metadata(self):
        source = checker._load_source()
        output = checker.build_blocked_output(source, "NO_KEY")

        for request in output["requests"]:
            self.assertEqual(
                sorted(request),
                ["dataset", "end", "schema", "start", "stype_in", "symbols"],
            )
            self.assertNotIn("definition", request["schema"])
            self.assertEqual(request["dataset"], "OPRA.PILLAR")
            self.assertEqual(request["stype_in"], "raw_symbol")

    def test_success_output_sums_schema_costs_without_economic_claims(self):
        source = checker._load_source()
        schema_costs = [
            {**checker.vendor_request(request), "checked_cost": "0.10", "currency": "USD"}
            for request in source["requests"]
        ]

        output = checker.build_success_output(
            source,
            schema_costs,
            checked_at_utc="2026-06-26T00:00:00Z",
        )

        self.assertEqual(output["status"], "SUCCESS")
        self.assertTrue(output["vendor_metadata_call_performed"])
        self.assertFalse(output["download_performed"])
        self.assertEqual(output["grouped_cost"], "3.20")
        self.assertEqual(output["profitability_proof"], "NO")
        self.assertEqual(output["paper_live_eligibility"], "NO")

    def test_source_uses_metadata_get_cost_only_and_no_download_api(self):
        source = inspect.getsource(checker)

        self.assertIn("metadata.get_cost", source)
        self.assertNotIn("timeseries.get_range", source)
        self.assertNotIn(".get_range(", source)
        self.assertNotIn("download(", source)

    def test_writer_and_validator_accept_blocked_output(self):
        temp_dir = self._normal_temp_dir()
        result_path = temp_dir / checker.OUTPUT_PATH.name
        doc_path = temp_dir / checker.DOC_PATH.name
        try:
            source = checker._load_source()
            output = checker.build_blocked_output(
                source,
                "SAFE_FAST_DB_AUTH_NOT_CONFIGURED",
                checked_at_utc="2026-06-26T00:00:00Z",
            )
            checker.write_output(output, output_path=result_path, doc_path=doc_path)
            validation = validator.validate_result_document(result_path)
            self.assertTrue(result_path.exists())
            self.assertTrue(doc_path.exists())
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])

    def _normal_temp_dir(self):
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        path.mkdir()
        return path


if __name__ == "__main__":
    unittest.main()
