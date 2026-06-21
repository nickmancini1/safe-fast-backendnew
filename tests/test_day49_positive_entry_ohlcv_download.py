import json
import unittest
from pathlib import Path
from unittest import mock

from historical_signal_replay import day49_positive_entry_ohlcv_download as ohlcv


class Day49PositiveEntryOhlcvDownloadTests(unittest.TestCase):
    def test_builds_exact_authorized_ohlcv_requests(self):
        manifest = ohlcv.load_request_manifest()
        requests = ohlcv.build_ohlcv_requests(manifest)

        self.assertEqual(ohlcv.validate_ohlcv_request_scope(manifest), [])
        self.assertEqual(len(requests), 7)
        self.assertEqual({request["dataset"] for request in requests}, {"DBEQ.BASIC"})
        self.assertEqual({request["schema"] for request in requests}, {"ohlcv-1h"})
        self.assertEqual({request["stype_in"] for request in requests}, {"raw_symbol"})
        self.assertEqual({request["symbol"] for request in requests}, {"GLD", "SPY", "QQQ", "IWM"})
        for request in requests:
            self.assertIn("options", request["forbidden_scope"])
            self.assertIn("exit_path", request["forbidden_scope"])
            self.assertIn("setup_labels", request["forbidden_scope"])

    def test_end_exclusive_repair_advances_manifest_end_by_one_hour(self):
        request = ohlcv.build_ohlcv_requests(ohlcv.load_request_manifest())[1]

        self.assertEqual(request["original_manifest_end_timestamp"], "2026-03-31T09:30:00-04:00")
        self.assertEqual(request["end_timestamp"], "2026-03-31T10:30:00-04:00")
        self.assertEqual(request["end_exclusive_repair"], "manifest_end_plus_one_hour")

    def test_download_validation_rejects_wrong_symbol_or_window(self):
        root = Path(__file__).resolve().parents[1] / "historical_signal_replay" / "results" / "day49_ohlcv_tmp"
        root.mkdir(parents=True, exist_ok=True)
        csv_path = root / "bad.csv"
        dbn_path = root / "bad.dbn.zst"
        try:
            csv_path.write_text(
                "\n".join(
                    [
                        "ts_event,symbol,open,high,low,close,volume",
                        "2026-03-31T15:30:00Z,QQQ,1,2,1,2,100",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            dbn_path.write_bytes(b"dbn")
            request = {
                "request_id": "test",
                "candidate_identifier": "SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003",
                "dataset": "DBEQ.BASIC",
                "schema": "ohlcv-1h",
                "stype_in": "raw_symbol",
                "symbol": "SPY",
                "start_timestamp": "2026-03-31T09:30:00-04:00",
                "end_timestamp": "2026-03-31T10:30:00-04:00",
            }
            cost_check = {"requests": [{"request_id": "test", "checked_cost": "0.0001"}]}

            result = ohlcv._validate_downloaded_request(request, dbn_path, csv_path, cost_check)
        finally:
            for path in (csv_path, dbn_path):
                if path.exists():
                    path.unlink()
            if root.exists():
                root.rmdir()

        self.assertIn("contradictory_symbol", result["validation_problems"])
        self.assertIn("row_outside_authorized_window", result["validation_problems"])

    def test_cost_check_uses_only_authorized_dataset_schema_and_stype(self):
        manifest = ohlcv.load_request_manifest()
        calls = []

        class FakeMetadata:
            def get_cost(self, **kwargs):
                calls.append(kwargs)
                return "0.0001"

        class FakeHistorical:
            def __init__(self, key):
                self.metadata = FakeMetadata()

        fake_db = mock.Mock(Historical=FakeHistorical)
        with mock.patch.dict("sys.modules", {"databento": fake_db}):
            result = ohlcv.check_ohlcv_cost(api_key="not-a-real-key", manifest=manifest)

        self.assertEqual(result["checked_total"], "0.0007")
        self.assertTrue(result["checked_total_at_or_below_limit"])
        for call in calls:
            self.assertEqual(call["dataset"], "DBEQ.BASIC")
            self.assertEqual(call["schema"], "ohlcv-1h")
            self.assertEqual(call["stype_in"], "raw_symbol")
            self.assertIn(call["symbols"], ohlcv.AUTHORIZED_SYMBOLS)

    def test_affected_candidate_replay_summary_preserves_no_proof_boundary(self):
        manifest = {
            "downloaded_requests": [
                {
                    "request_id": request["request_id"],
                    "validation_problems": [],
                }
                for request in ohlcv.build_ohlcv_requests(ohlcv.load_request_manifest())
            ]
        }

        summary = ohlcv.affected_candidate_replay_summary(manifest)

        self.assertEqual(summary["affected_candidate_count"], 7)
        self.assertFalse(summary["proof_accepted"])
        self.assertFalse(summary["profitability_claimed"])
        self.assertTrue(
            all(
                "setup_qualified_still_blocked" in item["replay_effect"]
                for item in summary["affected_candidates"]
            )
        )


if __name__ == "__main__":
    unittest.main()
