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
    def test_real_day55_download_package_exactly_rejects_absent_spy_670c(self):
        document = day55.build_document(
            run_timestamp="2026-06-29T00:00:00Z",
            source_commit="testsha",
        )
        evaluation = document["evaluation"]
        input_validation = document["input_validation"]

        self.assertEqual(input_validation["status"], "INPUTS_VALIDATED")
        self.assertTrue(input_validation["download_performed"])
        self.assertEqual(input_validation["request_count"], 32)
        self.assertEqual(input_validation["completed_or_reused_request_count"], 32)
        self.assertEqual(input_validation["remaining_request_count"], 0)
        self.assertFalse(input_validation["target_contract_in_manifest"])
        self.assertEqual(input_validation["previous_blocker"], "open_interest_statistics_zero_rows")
        self.assertFalse(input_validation["old_blocker_closed_by_raw_statistics"])
        self.assertEqual(evaluation["entry_status"], day55.NO_ENTRY_EXACT_REJECTION)
        self.assertEqual(
            evaluation["first_blocker"],
            "target_contract_not_in_day55_download_manifest",
        )
        self.assertEqual(evaluation["exit_status"], day55.EXIT_BLOCKED)
        self.assertEqual(evaluation["net_pnl_status"], day55.ECONOMIC_REPLAY_BLOCKED)
        self.assertIsNone(evaluation["gross_pnl"])
        self.assertIsNone(evaluation["net_pnl"])
        self.assertEqual(document["proof_status"]["complete_end_to_end_backtest"], "NO")
        self.assertEqual(document["proof_status"]["profitability_proof"], "NO")
        self.assertEqual(document["proof_status"]["paper_live_eligibility"], "NO")

    def test_validates_all_downloaded_file_hashes_and_counts_before_use(self):
        with self._fixture_package(include_target=True, statistics_rows=True) as paths:
            manifest = self._json(paths["manifest"])
            target = next(
                output for output in manifest["output_files"]
                if output["symbols"] == day55.RAW_SYMBOL and output["schema"] == "cmbp-1"
            )
            target["csv_sha256"] = "0" * 64
            paths["manifest"].write_text(json.dumps(manifest), encoding="utf-8")

            document = self._build(paths)

        self.assertEqual(document["input_validation"]["status"], day55.ECONOMIC_REPLAY_BLOCKED)
        self.assertIn(
            f"{target['request_id']}_csv_sha256_mismatch",
            document["input_validation"]["problems"],
        )
        self.assertEqual(document["evaluation"]["entry_status"], day55.ECONOMIC_REPLAY_BLOCKED)

    def test_valid_entry_exit_and_net_pnl_path_when_day55_fixture_contains_target(self):
        with self._fixture_package(include_target=True, statistics_rows=True, exit_bid="12.70") as paths:
            document = self._build(paths)
        evaluation = document["evaluation"]

        self.assertTrue(document["input_validation"]["target_contract_in_manifest"])
        self.assertTrue(document["input_validation"]["old_blocker_closed_by_raw_statistics"])
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

    def test_old_statistics_blocker_stays_open_if_target_statistics_do_not_prove_oi(self):
        with self._fixture_package(include_target=True, statistics_rows=False) as paths:
            document = self._build(paths)

        self.assertTrue(document["input_validation"]["target_contract_in_manifest"])
        self.assertFalse(document["input_validation"]["old_blocker_closed_by_raw_statistics"])
        self.assertEqual(document["evaluation"]["entry_status"], day55.NO_ENTRY_EXACT_REJECTION)
        self.assertEqual(document["evaluation"]["first_blocker"], "open_interest_statistics_zero_rows")

    def test_manifest_success_and_cost_check_alignment_required(self):
        with self._fixture_package(include_target=True, statistics_rows=True) as paths:
            manifest = self._json(paths["manifest"])
            manifest["status"] = "FAILURE"
            paths["manifest"].write_text(json.dumps(manifest), encoding="utf-8")

            document = self._build(paths)

        self.assertEqual(document["input_validation"]["status"], day55.ECONOMIC_REPLAY_BLOCKED)
        self.assertEqual(document["input_validation"]["first_blocker"], "manifest_status_not_success")
        self.assertEqual(document["evaluation"]["entry_status"], day55.ECONOMIC_REPLAY_BLOCKED)

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
                run_timestamp="2026-06-29T00:00:00Z",
                source_commit="testsha",
            )
            validation = validator.validate_result_document(result_path)
        finally:
            day55.RESULT_PATH = original_result
            day55.RESULT_DOC_PATH = original_doc
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.assertEqual(
            written["evaluation"]["first_blocker"],
            "target_contract_not_in_day55_download_manifest",
        )
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])

    def test_no_git_operation_no_credentials_no_vendor_network_calls(self):
        source = inspect.getsource(day55)

        self.assertNotIn("subprocess", source)
        self.assertNotIn("requests.", source)
        self.assertNotIn("SAFE_FAST_DB_AUTH", source)
        self.assertNotIn("os.environ", source)

    def _build(self, paths):
        return day55.build_document(
            manifest_path=paths["manifest"],
            contract_selection_path=paths["contract_selection"],
            cost_output_path=paths["cost_output"],
            previous_result_path=paths["previous_result"],
            source_root=paths["source_root"],
            run_timestamp="2026-06-29T00:00:00Z",
            source_commit="testsha",
        )

    def _fixture_package(
        self,
        *,
        include_target,
        statistics_rows,
        exit_bid="12.70",
    ):
        return _FixturePackage(
            include_target=include_target,
            statistics_rows=statistics_rows,
            exit_bid=exit_bid,
        )

    def _json(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def _normal_temp_dir(self):
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        path.mkdir()
        return path


class _FixturePackage:
    def __init__(self, *, include_target, statistics_rows, exit_bid):
        self.include_target = include_target
        self.statistics_rows = statistics_rows
        self.exit_bid = exit_bid
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.root = TEST_TMP_ROOT / f"case_{uuid.uuid4().hex}"
        self.root.mkdir()

    def __enter__(self):
        source_root = self.root / "source"
        source_root.mkdir()
        outputs, exact_requests = self._write_outputs(source_root)
        paths = {
            "source_root": source_root,
            "manifest": self.root / "manifest.json",
            "contract_selection": self.root / "contract_selection.json",
            "cost_output": self.root / "cost_output.json",
            "previous_result": self.root / "previous_result.json",
        }
        paths["manifest"].write_text(
            json.dumps(self._manifest(outputs, exact_requests), indent=2),
            encoding="utf-8",
        )
        paths["contract_selection"].write_text(
            json.dumps(self._contract_selection(outputs), indent=2),
            encoding="utf-8",
        )
        paths["cost_output"].write_text(
            json.dumps(self._cost_output(exact_requests), indent=2),
            encoding="utf-8",
        )
        paths["previous_result"].write_text(
            json.dumps(
                {
                    "remaining_blocker": "open_interest_statistics_zero_rows",
                    "evaluation": {"first_blocker": "open_interest_statistics_zero_rows"},
                }
            ),
            encoding="utf-8",
        )
        return paths

    def __exit__(self, exc_type, exc, tb):
        shutil.rmtree(self.root, ignore_errors=True)

    def _write_outputs(self, source_root):
        symbols = [
            ("SPY   260414C00645000", 1275070451),
            ("SPY   260414C00650000", 1275070438),
            ("QQQ   260416C00585000", 989123001),
            ("QQQ   260416C00590000", 989123002),
            ("SPY   260501C00702000", 1224736926),
            ("SPY   260501C00707000", 1224738270),
            ("QQQ   260501C00650000", 989856791),
            ("QQQ   260501C00655000", 989855873),
        ]
        if self.include_target:
            symbols[0] = (day55.RAW_SYMBOL, day55.INSTRUMENT_ID)

        outputs = []
        exact_requests = []
        index = 1
        for symbol, instrument_id in symbols:
            for schema in day55.REQUIRED_SCHEMAS:
                start = "2026-03-16T13:31:00Z" if schema in {"cmbp-1", "tcbbo"} else "2026-03-16T13:30:00Z"
                end = "2026-03-16T13:36:00Z" if schema in {"cmbp-1", "statistics"} else "2026-03-16T19:45:00Z"
                request = {
                    "dataset": "OPRA.PILLAR",
                    "schema": schema,
                    "start": start,
                    "end": end,
                    "stype_in": "raw_symbol",
                    "symbols": symbol,
                }
                rows = self._rows(schema, symbol, instrument_id)
                request_id = f"{index:02d}_{schema.replace('-', '')}_{instrument_id}"
                csv_path = source_root / f"{request_id}.csv"
                dbn_path = source_root / f"{request_id}.dbn.zst"
                self._write_csv(csv_path, rows)
                dbn_path.write_text(json.dumps({"schema": schema, "rows": rows}), encoding="utf-8")
                output = {
                    **request,
                    "request_id": request_id,
                    "request_index": index - 1,
                    "status": "COMPLETED_DOWNLOADED",
                    "csv_path": str(csv_path),
                    "dbn_path": str(dbn_path),
                    "csv_sha256": self._sha256(csv_path),
                    "dbn_sha256": self._sha256(dbn_path),
                    "parsed_record_count": len(rows),
                    "empty": len(rows) == 0,
                    "contract_identity_validated": True,
                    "dbn_schema": schema,
                }
                outputs.append(output)
                exact_requests.append(request)
                index += 1
        return outputs, exact_requests

    def _rows(self, schema, symbol, instrument_id):
        if symbol != day55.RAW_SYMBOL:
            return [
                {
                    "ts_recv": "2026-03-16T13:31:00Z",
                    "ts_event": "2026-03-16T13:31:00Z",
                    "rtype": "0",
                    "publisher_id": "30",
                    "instrument_id": str(instrument_id),
                    "symbol": symbol,
                    "price": "1.00",
                    "size": "1",
                    "bid_px_00": "1.00",
                    "ask_px_00": "1.01",
                    "bid_sz_00": "1",
                    "ask_sz_00": "1",
                    "stat_type": "9",
                    "quantity": "1",
                }
            ]
        if schema == "cmbp-1":
            return [
                {
                    "ts_recv": "2026-03-16T13:31:00Z",
                    "ts_event": "2026-03-16T13:31:00Z",
                    "rtype": "177",
                    "publisher_id": "30",
                    "instrument_id": str(day55.INSTRUMENT_ID),
                    "symbol": day55.RAW_SYMBOL,
                    "bid_px_00": "10.03",
                    "ask_px_00": "10.04",
                    "bid_sz_00": "5",
                    "ask_sz_00": "5",
                }
            ]
        if schema == "tcbbo":
            return [
                {
                    "ts_recv": "2026-03-16T13:32:00Z",
                    "ts_event": "2026-03-16T13:32:00Z",
                    "rtype": "194",
                    "publisher_id": "30",
                    "instrument_id": str(day55.INSTRUMENT_ID),
                    "symbol": day55.RAW_SYMBOL,
                    "bid_px_00": self.exit_bid,
                    "ask_px_00": self.exit_bid,
                    "bid_sz_00": "5",
                    "ask_sz_00": "5",
                },
                {
                    "ts_recv": "2026-03-16T19:44:00Z",
                    "ts_event": "2026-03-16T19:44:00Z",
                    "rtype": "194",
                    "publisher_id": "30",
                    "instrument_id": str(day55.INSTRUMENT_ID),
                    "symbol": day55.RAW_SYMBOL,
                    "bid_px_00": self.exit_bid,
                    "ask_px_00": self.exit_bid,
                    "bid_sz_00": "5",
                    "ask_sz_00": "5",
                },
            ]
        if schema == "trades":
            return [
                {
                    "ts_recv": "2026-03-16T13:31:30Z",
                    "ts_event": "2026-03-16T13:31:30Z",
                    "rtype": "0",
                    "publisher_id": "30",
                    "instrument_id": str(day55.INSTRUMENT_ID),
                    "symbol": day55.RAW_SYMBOL,
                    "price": "10.04",
                    "size": "1",
                }
            ]
        if self.statistics_rows:
            return [
                {
                    "ts_recv": "2026-03-16T13:30:00Z",
                    "ts_event": "2026-03-16T13:30:00Z",
                    "rtype": "0",
                    "publisher_id": "30",
                    "instrument_id": str(day55.INSTRUMENT_ID),
                    "symbol": day55.RAW_SYMBOL,
                    "stat_type": "9",
                    "quantity": "1",
                }
            ]
        return []

    def _manifest(self, outputs, exact_requests):
        return {
            "result_version": "safe_fast_day55_quote_trade_statistics_download_manifest_v1",
            "status": "SUCCESS",
            "dataset": "OPRA.PILLAR",
            "download_performed": True,
            "request_count": 32,
            "required_schemas": sorted(day55.REQUIRED_SCHEMAS),
            "forbidden_schemas": ["definition"],
            "exact_requests": exact_requests,
            "output_files": outputs,
            "completed_or_reused_request_ids": [output["request_id"] for output in outputs],
            "remaining_request_ids": [],
            "checked_grouped_cost_usd": "0.054846107958",
            "operator_approved_grouped_cost_usd": "0.054846107958",
            "entry_status": "NOT_EVALUATED",
            "exit_status": "NOT_EVALUATED",
            "gross_pnl": None,
            "net_pnl": None,
            "profitability_proof": "NO",
            "paper_live_eligibility": "NO",
        }

    def _contract_selection(self, outputs):
        contracts = {}
        for output in outputs:
            contracts[output["symbols"]] = output
        symbols = list(contracts)
        return {
            "decision": "DEFINITION_CONTRACT_SELECTION_COMPLETE",
            "candidates": [
                {
                    "candidate_id": "fixture-candidate",
                    "long_contract": {
                        "raw_symbol": symbols[0],
                        "instrument_id": "1241515301" if symbols[0] == day55.RAW_SYMBOL else "1275070451",
                    },
                    "short_contract": {
                        "raw_symbol": symbols[1],
                        "instrument_id": "1275070438",
                    },
                }
            ],
        }

    def _cost_output(self, exact_requests):
        return {
            "result_version": "safe_fast_day55_quote_trade_statistics_cost_check_for_selected_contracts_v1",
            "status": "SUCCESS",
            "download_performed": False,
            "grouped_cost": "0.054846107958",
            "requests": exact_requests,
        }

    def _write_csv(self, path, rows):
        fieldnames = [
            "ts_recv",
            "ts_event",
            "rtype",
            "publisher_id",
            "instrument_id",
            "symbol",
            "price",
            "size",
            "bid_px_00",
            "ask_px_00",
            "bid_sz_00",
            "ask_sz_00",
            "stat_type",
            "quantity",
        ]
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = json_csv_writer(handle, fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _sha256(self, path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_csv_writer(handle, fieldnames):
    import csv

    return csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")


if __name__ == "__main__":
    unittest.main()
