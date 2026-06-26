import hashlib
import io
import json
import shutil
import unittest
from copy import deepcopy
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from scripts import safe_fast_day52_spy_670c_databento_download as download


def valid_rows(schema, *, count=1, symbol=download.RAW_SYMBOL, ts=None):
    default_ts = {
        "cmbp-1": "2026-03-16T13:31:00.000000001Z",
        "tcbbo": "2026-03-16T13:31:00.000000001Z",
        "trades": "2026-03-16T13:30:00.000000001Z",
        "statistics": "2026-03-16T13:30:00.000000001Z",
    }[schema]
    return [
        {
            "ts_event": ts or default_ts,
            "symbol": symbol,
            "instrument_id": str(download.INSTRUMENT_ID),
            "publisher_id": str(download.PUBLISHER_ID),
            "price": "1.00",
        }
        for _ in range(count)
    ]


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    header = "ts_event,symbol,instrument_id,publisher_id,price\n"
    body = "".join(
        f"{row['ts_event']},{row['symbol']},{row['instrument_id']},{row['publisher_id']},{row['price']}\n"
        for row in rows
    )
    path.write_text(header + body, encoding="utf-8")


def write_fake_dbn(path, schema, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema": schema, "rows": rows}
    path.write_text(json.dumps(payload), encoding="utf-8")


def parse_fake_dbn(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = payload["rows"]
    instruments = {int(row["instrument_id"]) for row in rows}
    publishers = {int(row["publisher_id"]) for row in rows}
    return {
        "schema": payload["schema"],
        "record_count": len(rows),
        "instrument_id": next(iter(instruments)) if len(instruments) == 1 else "__MULTIPLE__",
        "publisher_id": next(iter(publishers)) if len(publishers) == 1 else "__MULTIPLE__",
        "symbol": None,
        "min_ts_event": min((row["ts_event"] for row in rows), default=None),
        "max_ts_event": max((row["ts_event"] for row in rows), default=None),
    }


class FakeStore:
    def __init__(self, schema, rows, fail_csv=False):
        self.schema = schema
        self.rows = rows
        self.fail_csv = fail_csv

    def to_csv(self, path, schema):
        if self.fail_csv:
            raise KeyboardInterrupt()
        write_csv(path, self.rows)


class FakeTimeseries:
    def __init__(self, calls, rows_by_schema, *, interrupt_schema=None, fail_csv=False):
        self.calls = calls
        self.rows_by_schema = rows_by_schema
        self.interrupt_schema = interrupt_schema
        self.fail_csv = fail_csv

    def get_range(self, **kwargs):
        self.calls.append(kwargs)
        schema = kwargs["schema"]
        rows = self.rows_by_schema.get(schema, [])
        write_fake_dbn(kwargs["path"], schema, rows)
        if self.interrupt_schema == schema:
            raise KeyboardInterrupt()
        return FakeStore(schema, rows, fail_csv=self.fail_csv and self.interrupt_schema == schema)


class FakeClient:
    def __init__(self, calls, rows_by_schema, **kwargs):
        self.timeseries = FakeTimeseries(calls, rows_by_schema, **kwargs)


class FlushTrackingStream(io.StringIO):
    def __init__(self):
        super().__init__()
        self.flush_count = 0

    def flush(self):
        self.flush_count += 1
        super().flush()


class Day52Spy670cDatabentoDownloadTests(unittest.TestCase):
    def setUp(self):
        self.inputs = download.load_inputs()
        self.contract = deepcopy(self.inputs["contract_resolution"])
        self.cost = deepcopy(self.inputs["cost_result"])

    @contextmanager
    def _workspace_tmp(self):
        path = (
            download.REPO_ROOT
            / "historical_signal_replay"
            / "results"
            / f"day52_download_test_{uuid4().hex}"
        )
        path.mkdir(parents=True, exist_ok=False)
        try:
            yield path
        finally:
            shutil.rmtree(path)

    def _write_pair(self, output_root, schema, *, rows=None, dbn_schema=None):
        request = next(row for row in self.cost["requests"] if row["schema"] == schema)
        paths = download.planned_output_files([request], output_root=output_root)[schema]
        actual_rows = rows if rows is not None else valid_rows(schema)
        write_fake_dbn(paths["dbn"], dbn_schema or schema, actual_rows)
        write_csv(paths["csv"], actual_rows)
        return paths

    def _run(self, tmp, *, rows_by_schema=None, client_kwargs=None, api_key="test-key", stream=None):
        output_root = tmp / "day52_spy_670c"
        manifest_path = output_root / "manifest.json"
        calls = []
        rows = rows_by_schema or {schema: valid_rows(schema) for schema in download.EXPECTED_SCHEMAS}
        kwargs = client_kwargs or {}
        code, manifest = download.run_download(
            api_key=api_key,
            output_root=output_root,
            manifest_path=manifest_path,
            client_factory=lambda key: FakeClient(calls, rows, **kwargs),
            git_ignore_checker=lambda paths: True,
            dbn_parser=parse_fake_dbn,
            output_stream=stream,
        )
        return code, manifest, calls, manifest_path

    def test_exact_four_schema_request_set_and_definition_absent(self):
        requests = download.validate_preflight(
            contract_resolution=self.contract,
            cost_result=self.cost,
            check_ignore=False,
        )
        self.assertEqual([request["schema"] for request in requests], list(download.EXPECTED_SCHEMAS))
        self.assertNotIn("definition", [request["schema"] for request in requests])
        self.assertTrue(all(request["symbols"] == download.RAW_SYMBOL for request in requests))

    def test_contract_resolution_consistency(self):
        requests = download.validate_preflight(
            contract_resolution=self.contract,
            cost_result=self.cost,
            check_ignore=False,
        )
        self.assertEqual(len(requests), 4)
        self.assertEqual(self.contract["selected_contract"]["instrument_id"], 1241515301)
        self.assertEqual(self.contract["selected_contract"]["publisher_id"], 30)

    def test_approval_ceiling_enforced(self):
        self.cost["grouped_cost"] = "0.010000000001"
        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                check_ignore=False,
            )
        self.assertEqual(raised.exception.classification, "PREFLIGHT_FAILED")
        self.assertIn("grouped_cost_exceeds_approved_ceiling", raised.exception.detail)

    def test_invalid_cost_result_rejection(self):
        self.cost["status"] = "FAILURE"
        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                check_ignore=False,
            )
        self.assertIn("cost_result_status_not_SUCCESS", raised.exception.detail)

    def test_wrong_symbol_rejection(self):
        self.cost["requests"][0]["symbols"] = "SPY   260330C00671000"
        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                check_ignore=False,
            )
        self.assertIn("unexpected_raw_symbol", raised.exception.detail)

    def test_wrong_schema_rejection_and_definition_forbidden(self):
        self.cost["requests"][0]["schema"] = "definition"
        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                check_ignore=False,
            )
        self.assertIn("definition_schema_forbidden", raised.exception.detail)
        self.assertIn("unexpected_schema_set_or_order", raised.exception.detail)

    def test_ignored_output_root_enforcement(self):
        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                git_ignore_checker=lambda paths: False,
            )
        self.assertEqual(raised.exception.classification, "OUTPUT_NOT_GIT_IGNORED")

    def test_git_ignore_checker_receives_every_planned_file_path(self):
        seen = []

        def checker(paths):
            seen.extend(Path(path).name for path in paths)
            return True

        download.validate_preflight(
            contract_resolution=self.contract,
            cost_result=self.cost,
            git_ignore_checker=checker,
        )
        self.assertIn("day52_spy_670c_databento_download_manifest.json", seen)
        for schema in download.EXPECTED_SCHEMAS:
            self.assertIn(f"day52_spy_670c_{schema}.dbn.zst", seen)
            self.assertIn(f"day52_spy_670c_{schema}.csv", seen)

    def test_valid_existing_cmbp_pair_is_reused_and_not_requested(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            self._write_pair(output_root, "cmbp-1", rows=valid_rows("cmbp-1", count=2))
            code, manifest, calls, _ = self._run(tmp)
        self.assertEqual(code, 0)
        self.assertEqual(manifest["schema_status"]["cmbp-1"]["status"], "COMPLETED_REUSED")
        self.assertNotIn("cmbp-1", [call["schema"] for call in calls])
        self.assertEqual([call["schema"] for call in calls], ["tcbbo", "trades", "statistics"])

    def test_completed_schema_request_is_never_duplicated_on_resume(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            self._write_pair(output_root, "cmbp-1")
            self._write_pair(output_root, "tcbbo")
            code, manifest, calls, _ = self._run(tmp)
        self.assertEqual(code, 0)
        self.assertEqual([call["schema"] for call in calls], ["trades", "statistics"])
        self.assertEqual(manifest["completed_or_reused_schemas"], list(download.EXPECTED_SCHEMAS))

    def test_missing_pair_downloads_normally_and_final_success_requires_all_four(self):
        with self._workspace_tmp() as tmp:
            code, manifest, calls, manifest_path = self._run(tmp)
            output_root = tmp / "day52_spy_670c"
            paths = download.planned_output_files(self.cost["requests"], output_root=output_root)
            self.assertEqual(code, 0)
            self.assertEqual(manifest["status"], "SUCCESS")
            self.assertEqual([call["schema"] for call in calls], list(download.EXPECTED_SCHEMAS))
            self.assertTrue(manifest_path.exists())
            self.assertTrue(all(paths[schema]["dbn"].exists() and paths[schema]["csv"].exists() for schema in download.EXPECTED_SCHEMAS))

    def test_one_file_only_pair_causes_exact_refusal(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            paths = self._write_pair(output_root, "cmbp-1")
            paths["csv"].unlink()
            code, manifest, calls, _ = self._run(tmp)
        self.assertEqual(code, 1)
        self.assertEqual(manifest["vendor_failure"]["classification"], "EXISTING_PAIR_INCOMPLETE")
        self.assertEqual(calls, [])

    def test_invalid_dbn_causes_exact_refusal(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            paths = self._write_pair(output_root, "cmbp-1")
            paths["dbn"].write_text("not json", encoding="utf-8")
            code, manifest, calls, _ = self._run(tmp)
        self.assertEqual(code, 1)
        self.assertEqual(manifest["vendor_failure"]["classification"], "DBN_PARSE_FAILED")
        self.assertEqual(calls, [])

    def test_invalid_csv_causes_exact_refusal(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            paths = self._write_pair(output_root, "cmbp-1")
            paths["csv"].write_text("ts_event,symbol,instrument_id,publisher_id\nnot-a-time,x,y,z\n", encoding="utf-8")
            code, manifest, calls, _ = self._run(tmp)
        self.assertEqual(code, 1)
        self.assertEqual(manifest["vendor_failure"]["classification"], "CSV_PARSE_FAILED")
        self.assertEqual(calls, [])

    def test_count_mismatch_wrong_contract_wrong_schema_and_out_of_window_refuse(self):
        cases = [
            ("count", {}, lambda paths: paths["csv"].write_text("ts_event,symbol,instrument_id,publisher_id,price\n", encoding="utf-8"), "record_count_mismatch"),
            ("contract", {"rows": valid_rows("cmbp-1", symbol="BAD")}, None, "csv_wrong_symbol"),
            ("schema", {"dbn_schema": "trades"}, None, "wrong_dbn_schema_trades"),
            ("window", {"rows": valid_rows("cmbp-1", ts="2026-03-16T13:36:00Z")}, None, "out_of_window"),
        ]
        for _, kwargs, mutate, expected in cases:
            with self.subTest(expected=expected), self._workspace_tmp() as tmp:
                output_root = tmp / "day52_spy_670c"
                paths = self._write_pair(output_root, "cmbp-1", **kwargs)
                if mutate:
                    mutate(paths)
                code, manifest, calls, _ = self._run(tmp)
                self.assertEqual(code, 1)
                self.assertEqual(manifest["vendor_failure"]["classification"], "EXISTING_PAIR_INVALID")
                self.assertIn(expected, manifest["vendor_failure"]["detail"])
                self.assertEqual(calls, [])

    def test_progress_output_is_flushed_and_checkpoints_update(self):
        stream = FlushTrackingStream()
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            self._write_pair(output_root, "cmbp-1")
            code, manifest, _, manifest_path = self._run(tmp, stream=stream)
            loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(code, 0)
        text = stream.getvalue()
        self.assertIn("SCHEMA_REUSED=cmbp-1", text)
        self.assertIn("SCHEMA_START=tcbbo", text)
        self.assertIn("SCHEMA_COMPLETE=statistics", text)
        self.assertGreaterEqual(stream.flush_count, 7)
        self.assertEqual(loaded["status"], "SUCCESS")
        self.assertEqual(loaded["schema_status"]["cmbp-1"]["status"], "COMPLETED_REUSED")

    def test_checkpoint_manifest_is_written_before_first_request(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            manifest_path = output_root / "manifest.json"
            calls = []

            def factory(key):
                loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
                self.assertEqual(loaded["status"], "IN_PROGRESS")
                self.assertIn("remaining_schemas", loaded)
                return FakeClient(calls, {schema: valid_rows(schema) for schema in download.EXPECTED_SCHEMAS})

            code, _ = download.run_download(
                api_key="test-key",
                output_root=output_root,
                manifest_path=manifest_path,
                client_factory=factory,
                git_ignore_checker=lambda paths: True,
                dbn_parser=parse_fake_dbn,
            )
        self.assertEqual(code, 0)

    def test_ctrl_c_writes_interrupted_exit_130_current_schema_and_preserves_completed(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            self._write_pair(output_root, "cmbp-1")
            code, manifest, calls, manifest_path = self._run(
                tmp,
                client_kwargs={"interrupt_schema": "tcbbo"},
            )
            loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(code, 130)
        self.assertEqual(manifest["status"], "INTERRUPTED")
        self.assertEqual(loaded["status"], "INTERRUPTED")
        self.assertEqual(manifest["current_schema"], "tcbbo")
        self.assertIn("cmbp-1", manifest["completed_or_reused_schemas"])
        self.assertEqual([call["schema"] for call in calls], ["tcbbo"])

    def test_partial_temporary_files_do_not_become_final_evidence(self):
        with self._workspace_tmp() as tmp:
            code, manifest, _, _ = self._run(
                tmp,
                client_kwargs={"interrupt_schema": "cmbp-1"},
            )
            output_root = tmp / "day52_spy_670c"
            paths = download.planned_output_files(self.cost["requests"], output_root=output_root)["cmbp-1"]
            temp_files = list(output_root.glob("*.tmp.*"))
        self.assertEqual(code, 130)
        self.assertEqual(manifest["status"], "INTERRUPTED")
        self.assertFalse(paths["dbn"].exists())
        self.assertFalse(paths["csv"].exists())
        self.assertTrue(temp_files)

    def test_temporary_files_are_renamed_only_after_validation(self):
        bad_rows = {schema: valid_rows(schema) for schema in download.EXPECTED_SCHEMAS}
        bad_rows["cmbp-1"] = valid_rows("cmbp-1", symbol="BAD")
        with self._workspace_tmp() as tmp:
            code, manifest, _, _ = self._run(tmp, rows_by_schema=bad_rows)
            output_root = tmp / "day52_spy_670c"
            paths = download.planned_output_files(self.cost["requests"], output_root=output_root)["cmbp-1"]
        self.assertEqual(code, 1)
        self.assertEqual(manifest["vendor_failure"]["classification"], "EXISTING_PAIR_INVALID")
        self.assertFalse(paths["dbn"].exists())
        self.assertFalse(paths["csv"].exists())

    def test_safe_fast_db_auth_required_and_credential_never_leaked(self):
        with self._workspace_tmp() as tmp:
            code, manifest, calls, _ = self._run(tmp, api_key="")
            self.assertEqual(code, 1)
            self.assertEqual(manifest["vendor_failure"]["classification"], "AUTH_MISSING")
            self.assertEqual(calls, [])

        with self._workspace_tmp() as tmp:
            secret = "super-secret-test-key"
            code, manifest, _, _ = self._run(tmp, api_key=secret)
            self.assertEqual(code, 0)
            self.assertNotIn(secret, json.dumps(manifest, sort_keys=True))
            self.assertFalse(manifest["credential_value_printed"])
            self.assertFalse(manifest["credential_value_persisted"])

    def test_no_network_call_before_all_preflight_checks_pass(self):
        self.cost["requests"][0]["symbols"] = "BAD"
        with self._workspace_tmp() as tmp:
            cost_path = tmp / "bad_cost.json"
            contract_path = tmp / "contract.json"
            cost_path.write_text(json.dumps(self.cost), encoding="utf-8")
            contract_path.write_text(json.dumps(self.contract), encoding="utf-8")
            network_called = False

            def factory(key):
                nonlocal network_called
                network_called = True
                return FakeClient([], {})

            code, manifest = download.run_download(
                api_key="test-key",
                contract_resolution_path=contract_path,
                cost_result_path=cost_path,
                output_root=tmp / "out",
                manifest_path=tmp / "out" / "manifest.json",
                client_factory=factory,
                git_ignore_checker=lambda paths: True,
                dbn_parser=parse_fake_dbn,
            )
        self.assertEqual(code, 1)
        self.assertFalse(network_called)
        self.assertEqual(manifest["vendor_failure"]["classification"], "PREFLIGHT_FAILED")

    def test_deterministic_manifest_construction(self):
        args = {
            "status": "SUCCESS",
            "contract_resolution": self.contract,
            "cost_result": self.cost,
            "requests": self.cost["requests"],
            "schema_results": {},
            "created_utc": "2026-06-25T00:00:00Z",
        }
        self.assertEqual(download.build_manifest(**args), download.build_manifest(**deepcopy(args)))

    def test_file_hashes_byte_counts_and_record_counts(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            self._write_pair(output_root, "cmbp-1", rows=valid_rows("cmbp-1", count=2))
            code, manifest, _, _ = self._run(tmp)
            self.assertEqual(code, 0)
            cmbp = next(item for item in manifest["output_files"] if item["schema"] == "cmbp-1")
            csv_path = Path(cmbp["csv_path"])
            self.assertEqual(cmbp["parsed_record_count"], 2)
            self.assertEqual(cmbp["csv_bytes"], csv_path.stat().st_size)
            self.assertEqual(cmbp["csv_sha256"], hashlib.sha256(csv_path.read_bytes()).hexdigest())

    def test_no_git_mutation_or_trade_proof_pnl_fields_invented(self):
        source = Path(download.__file__).read_text(encoding="utf-8")
        for token in ("git add", "git commit", "git push", "merge_pull_request"):
            self.assertNotIn(token, source)
        manifest = download.build_manifest(
            status="FAILURE",
            contract_resolution=self.contract,
            cost_result=self.cost,
            failure={"classification": "TEST", "detail": "x"},
            created_utc="2026-06-25T00:00:00Z",
        )
        serialized = json.dumps(manifest, sort_keys=True).lower()
        self.assertNotIn("net_pnl", serialized)
        self.assertNotIn("entry_price", serialized)
        self.assertNotIn("exit_price", serialized)
        self.assertEqual(manifest["proof"], "NO")
        self.assertEqual(manifest["profitability_proof"], "NO")
        self.assertEqual(manifest["paper_live_eligibility"], "NO")


if __name__ == "__main__":
    unittest.main()
