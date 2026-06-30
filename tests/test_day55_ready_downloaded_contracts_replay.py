import inspect
import json
import shutil
import unittest
import uuid
from pathlib import Path

from historical_signal_replay import day55_ready_downloaded_contracts_replay as day55
from watcher_foundation import day55_ready_downloaded_contracts_replay_validator as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
TEST_TMP_ROOT = REPO_ROOT / "historical_signal_replay" / "results" / "day55_ready_contracts_test_tmp"


class Day55ReadyDownloadedContractsReplayTests(unittest.TestCase):
    def test_real_day55_downloaded_contracts_replay_exactly_rejects_all_ready_contracts(self):
        document = day55.build_document(
            run_timestamp="2026-06-29T00:00:00Z",
            source_commit="testsha",
        )

        self.assertEqual(document["input_validation"]["status"], "INPUTS_VALIDATED")
        self.assertEqual(document["input_validation"]["request_count"], 32)
        self.assertEqual(document["input_validation"]["completed_or_reused_request_count"], 32)
        self.assertEqual(document["input_validation"]["remaining_request_count"], 0)
        self.assertEqual(document["input_validation"]["ready_contract_count"], 8)
        self.assertEqual(document["summary"]["ready_contracts_evaluated"], 8)
        self.assertEqual(document["summary"]["valid_entries"], 0)
        self.assertEqual(document["summary"]["evaluated_exits"], 0)
        self.assertEqual(document["summary"]["net_pnl_results"], 0)
        self.assertEqual(document["summary"]["exact_no_entry_rejections"], 8)
        self.assertEqual(document["summary"]["profitability_proof"], "NO")
        self.assertEqual(document["summary"]["paper_live_eligibility"], "NO")

        blockers = {
            item["raw_symbol"]: item["first_blocker"]
            for item in document["contract_results"]
        }
        self.assertEqual(
            blockers,
            {
                "QQQ   260416C00585000": "open_interest_statistics_zero_rows",
                "QQQ   260416C00590000": "trade_volume_below_1",
                "QQQ   260501C00650000": "open_interest_statistics_zero_rows",
                "QQQ   260501C00655000": "open_interest_statistics_zero_rows",
                "SPY   260414C00645000": "trade_volume_below_1",
                "SPY   260414C00650000": "trade_volume_below_1",
                "SPY   260501C00702000": "spread_above_0_15",
                "SPY   260501C00707000": "spread_above_0_15",
            },
        )
        for result in document["contract_results"]:
            self.assertEqual(result["entry_status"], day55.NO_ENTRY_EXACT_REJECTION)
            self.assertEqual(result["exit_status"], day55.EXIT_BLOCKED)
            self.assertEqual(result["net_pnl_status"], day55.ECONOMIC_REPLAY_BLOCKED)
            self.assertIsNone(result["gross_pnl"])
            self.assertIsNone(result["net_pnl"])

    def test_spy_670c_target_mismatch_rejection_is_preserved(self):
        document = day55.build_document(
            run_timestamp="2026-06-29T00:00:00Z",
            source_commit="testsha",
        )
        rejection = document["baseline"]["preserved_spy_670c_rejection"]

        self.assertTrue(rejection["preserved"])
        self.assertEqual(rejection["raw_symbol"], "SPY   260330C00670000")
        self.assertFalse(rejection["target_contract_in_manifest"])
        self.assertEqual(rejection["entry_status"], day55.NO_ENTRY_EXACT_REJECTION)
        self.assertEqual(
            rejection["first_blocker"],
            "target_contract_not_in_day55_download_manifest",
        )
        self.assertIsNone(rejection["gross_pnl"])
        self.assertIsNone(rejection["net_pnl"])

    def test_writer_and_validator_accept_ready_contract_replay_result(self):
        temp_dir = self._normal_temp_dir()
        result_path = temp_dir / "result.json"
        doc_path = temp_dir / "result.md"
        original_result = day55.RESULT_PATH
        original_doc = day55.RESULT_DOC_PATH
        try:
            day55.RESULT_PATH = result_path
            day55.RESULT_DOC_PATH = doc_path
            written = day55.write_outputs(
                run_timestamp="2026-06-29T00:00:00Z",
                source_commit="testsha",
            )
            validation = validator.validate_result_document(result_path)
        finally:
            day55.RESULT_PATH = original_result
            day55.RESULT_DOC_PATH = original_doc
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.assertEqual(written["summary"]["ready_contracts_evaluated"], 8)
        self.assertEqual(written["summary"]["exact_no_entry_rejections"], 8)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])

    def test_no_credentials_vendor_network_schwab_or_git_operations(self):
        source = inspect.getsource(day55)

        self.assertNotIn("subprocess", source)
        self.assertNotIn("requests.", source)
        self.assertNotIn("SAFE_FAST_DB_AUTH", source)
        self.assertNotIn("os.environ", source)
        self.assertNotIn("schwab.", source.lower())

    def test_result_json_contains_no_credentials(self):
        document = day55.build_document(
            run_timestamp="2026-06-29T00:00:00Z",
            source_commit="testsha",
        )
        serialized = json.dumps(document, sort_keys=True).lower()

        self.assertNotIn("safe_fast_db_auth=", serialized)
        self.assertNotIn("api_key", serialized)
        self.assertNotIn("secret", serialized)
        self.assertNotIn("token", serialized)

    def _normal_temp_dir(self):
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        path.mkdir()
        return path


if __name__ == "__main__":
    unittest.main()
