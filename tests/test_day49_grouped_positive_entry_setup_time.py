import json
import unittest
from pathlib import Path
from unittest import mock

from historical_signal_replay import day49_grouped_positive_entry_setup_time as day49


class Day49GroupedPositiveEntrySetupTimeTests(unittest.TestCase):
    def test_manifest_is_exact_four_setup_time_requests(self):
        manifest = day49.load_request_manifest()

        self.assertEqual([], day49.validate_request_manifest(manifest))
        self.assertEqual(len(manifest["requests"]), 4)
        self.assertTrue(all(request["schema"] in {"tcbbo", "trades"} for request in manifest["requests"]))
        self.assertTrue(all(request["conditional_exit_path_window"] is None for request in manifest["requests"]))
        self.assertEqual(
            day49.manifest_sha256(),
            day49.EXPECTED_MANIFEST_SHA256,
        )

    def test_download_manifest_evidence_classifies_stale_quote_as_entry_blocker(self):
        root = Path(__file__).resolve().parents[1] / "historical_signal_replay" / "results" / "day49_test_tmp"
        root.mkdir(parents=True, exist_ok=True)
        try:
            manifest_path = root / "request_manifest.json"
            quote_path = root / "quote.csv"
            trades_path = root / "trades.csv"
            manifest_path.write_text(
                json.dumps(
                    {
                        "requests": [
                            _request("tcbbo", "quote.csv"),
                            _request("trades", "trades.csv"),
                        ]
                    }
                ),
                encoding="utf-8",
            )
            quote_path.write_text(
                "\n".join(
                    [
                        "ts_recv,ts_event,instrument_id,bid_px_00,ask_px_00,bid_sz_00,ask_sz_00,symbol",
                        "2026-05-13T15:22:37.366273Z,2026-05-13T15:22:37.366073Z,1224739213,5.72,5.75,198,126,SPY   260527C00745000",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            trades_path.write_text(
                "\n".join(
                    [
                        "ts_recv,ts_event,instrument_id,price,size,symbol",
                        "2026-05-13T15:22:37.366273Z,2026-05-13T15:22:37.366073Z,1224739213,5.73,45,SPY   260527C00745000",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            download_manifest = {
                "downloaded_requests": [
                    {
                        "request_id": "SPY-REAL-HISTORICAL-IDEAL-001-SETUP-TCBBO-RAW-SYMBOL-OPEN-TO-SIGNAL",
                        "schema": "tcbbo",
                        "csv_path": "quote.csv",
                        "row_count": 1,
                        "validation_problems": [],
                    },
                    {
                        "request_id": "SPY-REAL-HISTORICAL-IDEAL-001-SETUP-TRADES-RAW-SYMBOL-OPEN-TO-SIGNAL",
                        "schema": "trades",
                        "csv_path": "trades.csv",
                        "row_count": 1,
                        "validation_problems": [],
                    },
                ]
            }

            with mock.patch.object(day49, "REPO_ROOT", root), mock.patch.object(
                day49,
                "MANIFEST_PATH",
                manifest_path,
            ):
                evidence = day49.build_setup_time_evidence(download_manifest)
        finally:
            for path in (root / "request_manifest.json", root / "quote.csv", root / "trades.csv"):
                if path.exists():
                    path.unlink()
            if root.exists():
                root.rmdir()

        row = evidence["second_real_spy_ideal_replay_v1_fixture"]
        self.assertEqual(row["contract_selection_result"]["contract_selection_status"], "selected")
        self.assertEqual(
            row["price_acceptability_result"]["rejection_reason"],
            "quote_age_above_5_minutes",
        )
        self.assertEqual(
            row["entry_eligibility_result"]["entry_eligibility_status"],
            "blocked",
        )


def _request(schema, _csv_name):
    return {
        "request_id": f"SPY-REAL-HISTORICAL-IDEAL-001-SETUP-{schema.upper()}-RAW-SYMBOL-OPEN-TO-SIGNAL",
        "candidate_id": "SPY-REAL-HISTORICAL-IDEAL-001",
        "funnel_candidate_identifier": "second_real_spy_ideal_replay_v1_fixture",
        "setup_family": "Ideal",
        "dataset": "OPRA.PILLAR",
        "schema": schema,
        "symbol_type": "raw_symbol",
        "raw_symbol": "SPY   260527C00745000",
        "instrument_id_when_known": 1224739213,
        "signal_timestamp_utc": "2026-05-13T15:30:00Z",
        "start_timestamp_utc": "2026-05-13T13:30:00Z",
        "end_timestamp_utc": "2026-05-13T15:30:00Z",
        "conditional_exit_path_window": None,
    }


if __name__ == "__main__":
    unittest.main()
