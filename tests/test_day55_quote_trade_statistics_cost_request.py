import inspect
import json
import shutil
import unittest
import uuid
from pathlib import Path

from historical_signal_replay import day55_quote_trade_statistics_cost_request as request
from watcher_foundation import day55_quote_trade_statistics_cost_request_validator as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
TEST_TMP_ROOT = REPO_ROOT / "historical_signal_replay" / "results" / "day55_qts_request_test_tmp"


class Day55QuoteTradeStatisticsCostRequestTests(unittest.TestCase):
    def test_real_selected_contract_result_builds_operator_ready_cost_request(self):
        doc = request.build_document(
            run_timestamp="2026-06-26T00:00:00Z",
            source_commit="testsha",
        )

        self.assertEqual(
            doc["decision"],
            "QUOTE_TRADE_STATISTICS_COST_REQUEST_READY_FOR_OPERATOR_REVIEW",
        )
        self.assertTrue(doc["cost_only"])
        self.assertFalse(doc["vendor_call_performed"])
        self.assertFalse(doc["download_performed"])
        self.assertFalse(doc["credential_env_var_read"])
        self.assertEqual(set(doc["required_schemas"]), set(request.REQUIRED_SCHEMAS))
        self.assertIn("definition", doc["forbidden_schemas"])
        self.assertEqual(doc["selected_candidate_count"], 6)
        self.assertEqual(doc["selected_contract_leg_count"], 12)
        self.assertEqual(doc["profitability_proof"], "NO")
        self.assertEqual(doc["paper_live_eligibility"], "NO")
        self.assertIsNone(doc["gross_pnl"])
        self.assertIsNone(doc["net_pnl"])

    def test_requests_use_only_quote_trade_statistics_schemas(self):
        doc = request.build_document(
            run_timestamp="2026-06-26T00:00:00Z",
            source_commit="testsha",
        )
        schemas = {item["schema"] for item in doc["requests"]}

        self.assertEqual(schemas, {"cmbp-1", "tcbbo", "trades", "statistics"})
        self.assertNotIn("definition", schemas)
        for item in doc["requests"]:
            self.assertEqual(item["dataset"], "OPRA.PILLAR")
            self.assertEqual(item["stype_in"], "raw_symbol")
            self.assertTrue(item["symbols"])
            self.assertTrue(item["start"].endswith("Z"))
            self.assertTrue(item["end"].endswith("Z"))
            self.assertIn(item["leg"], {"long", "short"})
            self.assertTrue(item["candidate_ids"])
            self.assertTrue(item["contract_identities"])

    def test_selected_contract_identities_are_preserved(self):
        doc = request.build_document(
            run_timestamp="2026-06-26T00:00:00Z",
            source_commit="testsha",
        )
        identities = [
            identity
            for item in doc["requests"]
            for identity in item["contract_identities"]
        ]

        self.assertIn("QQQ   260501C00650000", {row["raw_symbol"] for row in identities})
        self.assertIn("SPY   260414C00645000", {row["raw_symbol"] for row in identities})
        self.assertIn("SPY   260501C00707000", {row["raw_symbol"] for row in identities})
        for row in identities:
            self.assertTrue(row["instrument_id"])
            self.assertTrue(row["publisher_id"])
            self.assertEqual(row["entry_status"], "NOT_EVALUATED")
            self.assertEqual(row["exit_status"], "NOT_EVALUATED")
            self.assertIsNone(row["gross_pnl"])
            self.assertIsNone(row["net_pnl"])
            self.assertEqual(row["profitability_proof"], "NO")
            self.assertEqual(row["paper_live_eligibility"], "NO")

    def test_no_vendor_credentials_or_network_calls(self):
        source = inspect.getsource(request)

        self.assertNotIn("databento", source)
        self.assertNotIn("import requests", source)
        self.assertNotIn("os.environ", source)
        self.assertNotIn("SAFE_FAST_DB_AUTH", source)

    def test_source_must_preserve_no_profitability_or_live_claim(self):
        with self._temp_source() as path:
            source = json.loads(path.read_text(encoding="utf-8"))
            source["profitability_proof"] = "YES"
            path.write_text(json.dumps(source), encoding="utf-8")

            with self.assertRaises(request.CostRequestBuildError) as raised:
                request.build_document(input_path=path)

        self.assertEqual(str(raised.exception), "profitability_proof_not_no")

    def test_writer_and_validator_accept_result(self):
        temp_dir = self._normal_temp_dir()
        result_path = temp_dir / "result.json"
        doc_path = temp_dir / "result.md"
        original_result = request.RESULT_PATH
        original_doc = request.RESULT_DOC_PATH
        original_validator_result = validator.RESULT_PATH
        try:
            request.RESULT_PATH = result_path
            request.RESULT_DOC_PATH = doc_path
            validator.RESULT_PATH = result_path
            written = request.write_outputs(
                run_timestamp="2026-06-26T00:00:00Z",
                source_commit="testsha",
            )
            validation = validator.validate_result_document(result_path)
        finally:
            request.RESULT_PATH = original_result
            request.RESULT_DOC_PATH = original_doc
            validator.RESULT_PATH = original_validator_result
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.assertGreater(written["request_count"], 0)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])

    def _temp_source(self):
        return _TempSource()

    def _normal_temp_dir(self):
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        path.mkdir()
        return path


class _TempSource:
    def __enter__(self):
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.root = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        self.root.mkdir()
        self.path = self.root / "source.json"
        self.path.write_text(request.INPUT_PATH.read_text(encoding="utf-8-sig"), encoding="utf-8")
        return self.path

    def __exit__(self, exc_type, exc, tb):
        shutil.rmtree(self.root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
