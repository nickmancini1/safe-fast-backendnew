import unittest
from pathlib import Path
from unittest import mock

from historical_signal_replay import (
    day50_raw_data_positive_entry_underlying_setup_time_request as request,
)


class Day50RawDataPositiveEntryUnderlyingSetupTimeRequestTests(unittest.TestCase):
    def test_builds_exact_approved_request_scope(self):
        exact = request.build_exact_request()

        self.assertEqual(request.validate_exact_request_scope(exact), [])
        self.assertEqual(exact["request_id"], request.REQUEST_ID)
        self.assertEqual(exact["symbol"], "SPY")
        self.assertEqual(exact["dataset"], "DBEQ.BASIC")
        self.assertEqual(exact["schema"], "ohlcv-1m")
        self.assertEqual(exact["stype_in"], "raw_symbol")
        self.assertEqual(exact["start_timestamp"], "2026-03-16T09:30:00-04:00")
        self.assertEqual(exact["end_timestamp"], "2026-03-16T16:00:00-04:00")
        self.assertIn("option data", exact["forbidden_scope"])
        self.assertIn("exit-path data", exact["forbidden_scope"])

    def test_scope_validation_rejects_changed_cost_or_schema(self):
        changed = request.build_exact_request()
        changed["schema"] = "ohlcv-1h"
        changed["checked_cost"] = "0.01"

        problems = request.validate_exact_request_scope(changed)

        self.assertIn("unexpected_schema", problems)
        self.assertIn("checked_cost_changed_from_approved_scope", problems)

    def test_cost_check_uses_only_exact_authorized_scope(self):
        calls = []

        class FakeMetadata:
            def get_cost(self, **kwargs):
                calls.append(kwargs)
                return request.EXPECTED_CHECKED_COST

        class FakeHistorical:
            def __init__(self, key):
                self.metadata = FakeMetadata()

        fake_db = mock.Mock(Historical=FakeHistorical)
        with mock.patch.dict("sys.modules", {"databento": fake_db}):
            cost = request.check_cost(api_key="not-a-real-key")

        self.assertTrue(cost["matches_prior_checked_cost"])
        self.assertTrue(cost["checked_cost_at_or_below_authorized_ceiling"])
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["dataset"], "DBEQ.BASIC")
        self.assertEqual(calls[0]["schema"], "ohlcv-1m")
        self.assertEqual(calls[0]["stype_in"], "raw_symbol")
        self.assertEqual(calls[0]["symbols"], "SPY")

    def test_downloaded_csv_validation_rejects_wrong_symbol_or_window(self):
        root = (
            Path(__file__).resolve().parents[1]
            / "historical_signal_replay"
            / "results"
            / "day50_underlying_setup_time_tmp"
        )
        root.mkdir(parents=True, exist_ok=True)
        csv_path = root / "bad.csv"
        dbn_path = root / "bad.dbn.zst"
        try:
            csv_path.write_text(
                "\n".join(
                    [
                        "ts_event,symbol,open,high,low,close,volume",
                        "2026-03-16T20:01:00Z,QQQ,1,2,1,2,100",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            dbn_path.write_bytes(b"dbn")
            cost_check = {"checked_cost": str(request.EXPECTED_CHECKED_COST)}

            result = request._validate_downloaded_file(
                request.build_exact_request(),
                dbn_path,
                csv_path,
                cost_check,
            )
        finally:
            for path in (csv_path, dbn_path):
                if path.exists():
                    path.unlink()
            if root.exists():
                root.rmdir()

        self.assertIn("contradictory_symbol", result["validation_problems"])
        self.assertIn("row_outside_authorized_window", result["validation_problems"])


if __name__ == "__main__":
    unittest.main()
