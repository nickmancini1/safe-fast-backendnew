import inspect
import json
import shutil
import unittest
import uuid
from pathlib import Path

from historical_signal_replay import day55_spy_670c_target_cost_only_request as request
from watcher_foundation import day55_spy_670c_target_cost_only_request_validator as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
TEST_TMP_ROOT = REPO_ROOT / "historical_signal_replay" / "results" / "day55_spy_670c_target_request_test_tmp"


class Day55Spy670cTargetCostOnlyRequestTests(unittest.TestCase):
    def test_builds_exact_target_cost_only_request(self):
        doc = request.build_document(
            run_timestamp="2026-06-30T00:00:00Z",
            source_commit="testsha",
        )

        self.assertEqual(
            doc["decision"],
            "TARGET_COST_ONLY_REQUEST_READY_FOR_OPERATOR_APPROVAL",
        )
        self.assertEqual(doc["exact_symbol"], "SPY   260330C00670000")
        self.assertTrue(doc["cost_only"])
        self.assertFalse(doc["vendor_call_performed"])
        self.assertFalse(doc["download_performed"])
        self.assertFalse(doc["credential_env_var_read"])
        self.assertEqual(doc["exact_estimated_cost"], "0.006495481730")
        self.assertEqual(doc["currency"], "USD")
        self.assertEqual(doc["profitability_proof"], "NO")
        self.assertEqual(doc["paper_live_eligibility"], "NO")

    def test_requests_use_exact_schema_windows_and_no_definition(self):
        doc = request.build_document(
            run_timestamp="2026-06-30T00:00:00Z",
            source_commit="testsha",
        )
        windows = {item["schema"]: (item["start"], item["end"]) for item in doc["requests"]}

        self.assertEqual(set(windows), {"cmbp-1", "tcbbo", "trades", "statistics"})
        self.assertNotIn("definition", windows)
        self.assertEqual(windows["cmbp-1"], ("2026-03-16T13:31:00Z", "2026-03-16T13:36:00Z"))
        self.assertEqual(windows["tcbbo"], ("2026-03-16T13:31:00Z", "2026-03-16T19:45:00Z"))
        self.assertEqual(windows["trades"], ("2026-03-16T13:30:00Z", "2026-03-16T19:45:00Z"))
        self.assertEqual(windows["statistics"], ("2026-03-16T13:30:00Z", "2026-03-16T13:36:00Z"))
        for item in doc["requests"]:
            self.assertEqual(item["dataset"], "OPRA.PILLAR")
            self.assertEqual(item["stype_in"], "raw_symbol")
            self.assertEqual(item["symbols"], "SPY   260330C00670000")

    def test_exact_window_not_found_blocks_request(self):
        temp_dir = self._normal_temp_dir()
        evaluation_path = temp_dir / "evaluation.json"
        evaluation = json.loads(request.EVALUATION_PATH.read_text(encoding="utf-8"))
        evaluation["accepted_setup"]["entry_window"]["end"] = "2026-03-16T13:35:00Z"
        evaluation_path.write_text(json.dumps(evaluation), encoding="utf-8")

        try:
            doc = request.build_document(
                evaluation_path=evaluation_path,
                run_timestamp="2026-06-30T00:00:00Z",
                source_commit="testsha",
            )
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.assertEqual(doc["decision"], "EXACT_WINDOW_NOT_FOUND")
        self.assertEqual(doc["request_count"], 0)
        self.assertEqual(doc["exact_estimated_cost"], None)

    def test_no_vendor_credentials_network_or_download_code(self):
        source = inspect.getsource(request)

        self.assertNotIn("import databento", source)
        self.assertNotIn("Historical(", source)
        self.assertNotIn("import requests", source)
        self.assertNotIn("os.environ", source)
        self.assertNotIn("SAFE_FAST_DB_AUTH", source)

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
                run_timestamp="2026-06-30T00:00:00Z",
                source_commit="testsha",
            )
            validation = validator.validate_result_document(result_path)
        finally:
            request.RESULT_PATH = original_result
            request.RESULT_DOC_PATH = original_doc
            validator.RESULT_PATH = original_validator_result
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.assertEqual(written["request_count"], 4)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])

    def _normal_temp_dir(self):
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        path.mkdir()
        return path


if __name__ == "__main__":
    unittest.main()
