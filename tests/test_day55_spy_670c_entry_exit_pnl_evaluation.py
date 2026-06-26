import hashlib
import inspect
import json
import shutil
import unittest
import uuid
from pathlib import Path

from historical_signal_replay import day55_spy_670c_entry_exit_pnl_evaluation as day55
from watcher_foundation import day55_spy_670c_entry_exit_pnl_evaluation_validator as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
TEST_TMP_ROOT = REPO_ROOT / "historical_signal_replay" / "results" / "day55_test_tmp"


class Day55Spy670CEntryExitPnlEvaluationTests(unittest.TestCase):
    def test_real_local_package_rejects_on_zero_statistics_rows(self):
        document = day55.build_document(
            run_timestamp="2026-06-26T00:00:00Z",
            source_commit="testsha",
        )
        evaluation = document["evaluation"]

        self.assertEqual(evaluation["entry_status"], day55.NO_ENTRY_EXACT_REJECTION)
        self.assertEqual(evaluation["first_blocker"], "open_interest_statistics_zero_rows")
        self.assertEqual(
            evaluation["statistics_open_interest_status"]["status"],
            "STATISTICS_ZERO_ROWS",
        )
        self.assertEqual(evaluation["exit_status"], day55.EXIT_BLOCKED)
        self.assertEqual(evaluation["net_pnl_status"], day55.ECONOMIC_REPLAY_BLOCKED)
        self.assertIsNone(evaluation["gross_pnl"])
        self.assertIsNone(evaluation["net_pnl"])
        self.assertEqual(document["proof_status"]["complete_end_to_end_backtest"], "NO")
        self.assertEqual(document["proof_status"]["profitability_proof"], "NO")
        self.assertEqual(document["proof_status"]["paper_live_eligibility"], "NO")

    def test_manifest_success_required(self):
        with self._fixture_package() as paths:
            manifest = self._json(paths["manifest"])
            manifest["status"] = "FAILURE"
            paths["manifest"].write_text(json.dumps(manifest), encoding="utf-8")

            document = self._build(paths)

        self.assertEqual(document["input_validation"]["status"], day55.ECONOMIC_REPLAY_BLOCKED)
        self.assertEqual(document["input_validation"]["first_blocker"], "manifest_status_not_success")
        self.assertEqual(document["evaluation"]["entry_status"], day55.ECONOMIC_REPLAY_BLOCKED)

    def test_missing_manifest_rejected(self):
        with self._fixture_package() as paths:
            paths["manifest"].unlink()
            with self.assertRaises(day55.Day55EvaluationError) as raised:
                self._build(paths)

        self.assertEqual(str(raised.exception), "missing_manifest")

    def test_missing_schema_files_rejected(self):
        with self._fixture_package() as paths:
            (paths["source_root"] / "day52_spy_670c_tcbbo.csv").unlink()
            document = self._build(paths)

        self.assertEqual(document["input_validation"]["first_blocker"], "tcbbo_csv_missing")
        self.assertEqual(document["evaluation"]["entry_status"], day55.ECONOMIC_REPLAY_BLOCKED)

    def test_selected_raw_symbol_required_and_wrong_symbol_rejected(self):
        with self._fixture_package() as paths:
            manifest = self._json(paths["manifest"])
            manifest["contract_identity"]["raw_symbol"] = "SPY   260330C00671000"
            paths["manifest"].write_text(json.dumps(manifest), encoding="utf-8")
            document = self._build(paths)

        self.assertIn("manifest_raw_symbol_mismatch", document["input_validation"]["problems"])

    def test_wrong_instrument_id_rejected(self):
        with self._fixture_package() as paths:
            manifest = self._json(paths["manifest"])
            manifest["contract_identity"]["instrument_id"] = 1
            paths["manifest"].write_text(json.dumps(manifest), encoding="utf-8")
            document = self._build(paths)

        self.assertIn("manifest_instrument_id_mismatch", document["input_validation"]["problems"])

    def test_valid_entry_exit_and_net_pnl_path_when_fixture_supports_it(self):
        with self._fixture_package(statistics_rows=True, exit_bid="12.70") as paths:
            document = self._build(paths)
        evaluation = document["evaluation"]

        self.assertEqual(evaluation["entry_status"], day55.VALID_ENTRY_FOUND)
        self.assertEqual(evaluation["entry_timestamp"], "2026-03-16T13:31:00Z")
        self.assertEqual(evaluation["entry_price"], "10.06")
        self.assertEqual(evaluation["exit_status"], day55.EXIT_EVALUATED)
        self.assertEqual(evaluation["exit_result"]["exit_reason"], "profit_target")
        self.assertEqual(evaluation["gross_pnl"], "2.66")
        self.assertEqual(evaluation["net_pnl_status"], day55.NET_PNL_EVALUATED)
        self.assertEqual(evaluation["net_pnl"], "2.62")
        self.assertEqual(document["proof_status"]["complete_end_to_end_backtest"], "YES")
        self.assertEqual(document["proof_status"]["profitability_proof"], "NO")
        self.assertEqual(document["proof_status"]["paper_live_eligibility"], "NO")

    def test_exact_rejection_if_statistics_oi_blocks_entry(self):
        with self._fixture_package(statistics_rows=False) as paths:
            document = self._build(paths)

        self.assertEqual(document["evaluation"]["entry_status"], day55.NO_ENTRY_EXACT_REJECTION)
        self.assertEqual(document["evaluation"]["first_blocker"], "open_interest_statistics_zero_rows")

    def test_exact_rejection_if_quote_freshness_blocks_entry(self):
        with self._fixture_package(quote_ts="2026-03-16T13:32:01Z", statistics_rows=True) as paths:
            document = self._build(paths)

        self.assertEqual(
            document["evaluation"]["first_blocker"],
            "quote_age_above_clean_entry_limit_or_above_5_minutes",
        )

    def test_exact_rejection_if_spread_blocks_entry(self):
        with self._fixture_package(bid="9.00", ask="10.00", statistics_rows=True) as paths:
            document = self._build(paths)

        self.assertEqual(document["evaluation"]["first_blocker"], "spread_above_0_15")

    def test_exact_rejection_if_trade_volume_blocks_entry(self):
        with self._fixture_package(trade_rows=False, statistics_rows=True) as paths:
            document = self._build(paths)

        self.assertEqual(document["evaluation"]["first_blocker"], "trade_volume_below_1")

    def test_no_hindsight_boundary_rejects_pre_trigger_quote_and_late_entry_window(self):
        with self._fixture_package(quote_ts="2026-03-16T13:30:59Z", statistics_rows=True) as paths:
            document = self._build(paths)
        self.assertEqual(document["evaluation"]["first_blocker"], "complete_entry_window_quote_missing")

        with self._fixture_package(quote_ts="2026-03-16T13:36:00Z", statistics_rows=True) as paths:
            document = self._build(paths)
        self.assertEqual(document["evaluation"]["first_blocker"], "complete_entry_window_quote_missing")
        self.assertFalse(document["accepted_setup"]["entry_window"]["end_inclusive"])

    def test_time_exit_path_if_no_target_or_stop(self):
        with self._fixture_package(statistics_rows=True, exit_bid="10.20") as paths:
            document = self._build(paths)

        self.assertEqual(document["evaluation"]["exit_status"], day55.EXIT_EVALUATED)
        self.assertEqual(
            document["evaluation"]["exit_result"]["exit_reason"],
            "time_exit_1545_et",
        )
        self.assertEqual(document["evaluation"]["net_pnl_status"], day55.NET_PNL_EVALUATED)

    def test_deterministic_rerun(self):
        with self._fixture_package(statistics_rows=True, exit_bid="12.70") as paths:
            first = self._build(paths)
            second = self._build(paths)

        self.assertEqual(first, second)

    def test_no_mutation_of_raw_vendor_files(self):
        raw_path = day55.SOURCE_ROOT / "day52_spy_670c_cmbp-1.csv"
        before = self._sha256(raw_path)
        day55.build_document(run_timestamp="2026-06-26T00:00:00Z", source_commit="testsha")
        after = self._sha256(raw_path)

        self.assertEqual(before, after)

    def test_no_git_operation_no_credentials_no_vendor_network_calls(self):
        source = inspect.getsource(day55)

        self.assertNotIn("subprocess", source)
        self.assertNotIn("requests.", source)
        self.assertNotIn("SAFE_FAST_DB_AUTH", source)
        self.assertNotIn("os.environ", source)

    def test_writer_and_validator_accept_result(self):
        temp_dir = self._normal_temp_dir()
        result_path = temp_dir / "result.json"
        doc_path = temp_dir / "result.md"
        original_result = day55.RESULT_PATH
        original_doc = day55.RESULT_DOC_PATH
        try:
            day55.RESULT_PATH = result_path
            day55.RESULT_DOC_PATH = doc_path
            written = day55.write_outputs(
                run_timestamp="2026-06-26T00:00:00Z",
                source_commit="testsha",
            )
            validation = validator.validate_result_document(result_path)
        finally:
            day55.RESULT_PATH = original_result
            day55.RESULT_DOC_PATH = original_doc
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.assertEqual(written["evaluation"]["first_blocker"], "open_interest_statistics_zero_rows")
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])

    def _build(self, paths):
        return day55.build_document(
            manifest_path=paths["manifest"],
            contract_resolution_path=paths["contract_resolution"],
            cost_output_path=paths["cost_output"],
            day52_e2e_path=paths["day52_e2e"],
            source_root=paths["source_root"],
            run_timestamp="2026-06-26T00:00:00Z",
            source_commit="testsha",
        )

    def _fixture_package(
        self,
        *,
        quote_ts="2026-03-16T13:31:00Z",
        bid="10.03",
        ask="10.04",
        trade_rows=True,
        statistics_rows=False,
        exit_bid="12.70",
    ):
        return _FixturePackage(
            quote_ts=quote_ts,
            bid=bid,
            ask=ask,
            trade_rows=trade_rows,
            statistics_rows=statistics_rows,
            exit_bid=exit_bid,
        )

    def _json(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def _sha256(self, path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def _normal_temp_dir(self):
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        path.mkdir()
        return path


class _FixturePackage:
    def __init__(
        self,
        *,
        quote_ts,
        bid,
        ask,
        trade_rows,
        statistics_rows,
        exit_bid,
    ):
        self.quote_ts = quote_ts
        self.bid = bid
        self.ask = ask
        self.trade_rows = trade_rows
        self.statistics_rows = statistics_rows
        self.exit_bid = exit_bid
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.root = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        self.root.mkdir()

    def __enter__(self):
        source_root = self.root / "source"
        source_root.mkdir()
        self._write_csvs(source_root)
        paths = {
            "source_root": source_root,
            "manifest": self.root / "manifest.json",
            "contract_resolution": self.root / "contract_resolution.json",
            "cost_output": self.root / "cost_output.json",
            "day52_e2e": self.root / "day52_e2e.json",
        }
        paths["manifest"].write_text(json.dumps(self._manifest(source_root)), encoding="utf-8")
        paths["contract_resolution"].write_text(
            json.dumps(self._contract_resolution()),
            encoding="utf-8",
        )
        paths["cost_output"].write_text(json.dumps(self._cost_output()), encoding="utf-8")
        paths["day52_e2e"].write_text(json.dumps(self._day52_e2e()), encoding="utf-8")
        return paths

    def __exit__(self, exc_type, exc, tb):
        shutil.rmtree(self.root, ignore_errors=True)

    def _write_csvs(self, source_root):
        self._write(
            source_root / "day52_spy_670c_cmbp-1.csv",
            "ts_recv,ts_event,rtype,publisher_id,instrument_id,action,side,price,size,flags,ts_in_delta,bid_px_00,ask_px_00,bid_sz_00,ask_sz_00,bid_pb_00,ask_pb_00,symbol\n"
            f"{self.quote_ts},{self.quote_ts},177,30,1241515301,A,A,{self.ask},1,192,0,{self.bid},{self.ask},5,5,1,1,SPY   260330C00670000\n",
        )
        self._write(
            source_root / "day52_spy_670c_tcbbo.csv",
            "ts_recv,ts_event,rtype,publisher_id,instrument_id,side,price,size,flags,bid_px_00,ask_px_00,bid_sz_00,ask_sz_00,bid_pb_00,ask_pb_00,symbol\n"
            f"2026-03-16T13:32:00Z,2026-03-16T13:32:00Z,194,30,1241515301,N,{self.exit_bid},1,192,{self.exit_bid},{self.exit_bid},5,5,1,1,SPY   260330C00670000\n"
            f"2026-03-16T19:44:00Z,2026-03-16T19:44:00Z,194,30,1241515301,N,{self.exit_bid},1,192,{self.exit_bid},{self.exit_bid},5,5,1,1,SPY   260330C00670000\n",
        )
        trades_body = ""
        if self.trade_rows:
            trades_body = (
                "2026-03-16T13:31:30Z,2026-03-16T13:31:30Z,0,30,1241515301,T,N,0,10.04,1,192,0,1,SPY   260330C00670000\n"
            )
        self._write(
            source_root / "day52_spy_670c_trades.csv",
            "ts_recv,ts_event,rtype,publisher_id,instrument_id,action,side,depth,price,size,flags,ts_in_delta,sequence,symbol\n"
            + trades_body,
        )
        stats_body = ""
        if self.statistics_rows:
            stats_body = (
                "2026-03-16T13:30:00Z,2026-03-16T13:30:00Z,0,1241515301,2026-03-16T13:30:00Z,0,1,1,0,9,1,A,0,SPY   260330C00670000\n"
            )
        self._write(
            source_root / "day52_spy_670c_statistics.csv",
            "ts_recv,ts_event,rtype,instrument_id,ts_ref,price,quantity,sequence,ts_in_delta,stat_type,channel_id,update_action,stat_flags,symbol\n"
            + stats_body,
        )

    def _manifest(self, source_root):
        output_files = []
        schema_status = {}
        counts = {
            "cmbp-1": 1,
            "tcbbo": 2,
            "trades": 1 if self.trade_rows else 0,
            "statistics": 1 if self.statistics_rows else 0,
        }
        for schema in day55.REQUIRED_SCHEMAS:
            request = {
                "dataset": "OPRA.PILLAR",
                "schema": schema,
                "symbols": "SPY   260330C00670000",
                "stype_in": "raw_symbol",
            }
            output_files.append(
                {
                    "schema": schema,
                    "csv_path": str(source_root / day55.CSV_BY_SCHEMA[schema]),
                    "parsed_record_count": counts[schema],
                    "empty": counts[schema] == 0,
                    **request,
                }
            )
            schema_status[schema] = {
                "status": "COMPLETED_REUSED",
                "parsed_record_count": counts[schema],
                "request": request,
            }
        return {
            "status": "SUCCESS",
            "completed_or_reused_schemas": list(day55.REQUIRED_SCHEMAS),
            "contract_identity": {
                "raw_symbol": "SPY   260330C00670000",
                "instrument_id": 1241515301,
                "publisher_id": 30,
            },
            "output_files": output_files,
            "schema_status": schema_status,
        }

    def _contract_resolution(self):
        return {
            "selected_contract": {
                "raw_symbol": "SPY   260330C00670000",
                "instrument_id": 1241515301,
                "publisher_id": 30,
            },
        }

    def _cost_output(self):
        return {
            "selected_contract": {
                "vendor_symbol": "SPY   260330C00670000",
                "instrument_id": 1241515301,
                "publisher_id": 30,
            },
        }

    def _day52_e2e(self):
        return {
            "contract_selection_result": {
                "selected_contract": {
                    "raw_symbol": "SPY   260330C00670000",
                    "instrument_id": 1241515301,
                    "publisher_id": 30,
                },
            },
        }

    def _write(self, path, content):
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
