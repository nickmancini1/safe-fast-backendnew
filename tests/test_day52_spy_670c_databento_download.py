import hashlib
import json
import shutil
import unittest
from copy import deepcopy
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from scripts import safe_fast_day52_spy_670c_databento_download as download


class FakeStore:
    def __init__(self, rows):
        self.rows = rows

    def to_csv(self, path, schema):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        header = "ts_event,symbol,price\n"
        body = "".join(
            f"{row['ts_event']},{row['symbol']},{row['price']}\n"
            for row in self.rows
        )
        path.write_text(header + body, encoding="utf-8")


class FakeTimeseries:
    def __init__(self, calls, rows_by_schema):
        self.calls = calls
        self.rows_by_schema = rows_by_schema

    def get_range(self, **kwargs):
        self.calls.append(kwargs)
        path = Path(kwargs["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"dbn:{kwargs['schema']}".encode("utf-8"))
        return FakeStore(self.rows_by_schema.get(kwargs["schema"], []))


class FakeClient:
    def __init__(self, calls, rows_by_schema):
        self.timeseries = FakeTimeseries(calls, rows_by_schema)


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

    def test_exact_four_schema_request_set_and_definition_absent(self):
        requests = download.validate_preflight(
            contract_resolution=self.contract,
            cost_result=self.cost,
            check_ignore=False,
            path_exists=lambda path: False,
        )

        self.assertEqual([request["schema"] for request in requests], [
            "cmbp-1",
            "tcbbo",
            "trades",
            "statistics",
        ])
        self.assertNotIn("definition", [request["schema"] for request in requests])
        self.assertTrue(all(request["symbols"] == download.RAW_SYMBOL for request in requests))

    def test_contract_resolution_consistency(self):
        requests = download.validate_preflight(
            contract_resolution=self.contract,
            cost_result=self.cost,
            check_ignore=False,
            path_exists=lambda path: False,
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
                path_exists=lambda path: False,
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
                path_exists=lambda path: False,
            )

        self.assertIn("cost_result_status_not_SUCCESS", raised.exception.detail)

    def test_wrong_symbol_rejection(self):
        self.cost["requests"][0]["symbols"] = "SPY   260330C00671000"

        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                check_ignore=False,
                path_exists=lambda path: False,
            )

        self.assertIn("unexpected_raw_symbol", raised.exception.detail)

    def test_wrong_schema_rejection(self):
        self.cost["requests"][0]["schema"] = "definition"

        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                check_ignore=False,
                path_exists=lambda path: False,
            )

        self.assertIn("definition_schema_forbidden", raised.exception.detail)
        self.assertIn("unexpected_schema_set_or_order", raised.exception.detail)

    def test_ignored_output_root_enforcement(self):
        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                git_ignore_checker=lambda paths: False,
                path_exists=lambda path: False,
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
            path_exists=lambda path: False,
        )

        self.assertIn("day52_spy_670c_databento_download_manifest.json", seen)
        for schema in download.EXPECTED_SCHEMAS:
            self.assertIn(f"day52_spy_670c_{schema}.dbn.zst", seen)
            self.assertIn(f"day52_spy_670c_{schema}.csv", seen)
        self.assertFalse(any(isinstance(item, dict) for item in seen))

    def test_overwrite_refusal(self):
        manifest = Path("manifest.json")

        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(
                contract_resolution=self.contract,
                cost_result=self.cost,
                output_root=Path("out"),
                manifest_path=manifest,
                git_ignore_checker=lambda paths: True,
                path_exists=lambda path: str(path).endswith("tcbbo.csv"),
            )

        self.assertEqual(raised.exception.classification, "OUTPUT_OVERWRITE_REFUSED")

    def test_successful_per_schema_file_and_manifest_creation(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            manifest_path = output_root / "manifest.json"
            calls = []
            rows = {
                "cmbp-1": [{"ts_event": "2026-03-16T13:31:00Z", "symbol": download.RAW_SYMBOL, "price": "1.00"}],
                "tcbbo": [{"ts_event": "2026-03-16T13:31:00Z", "symbol": download.RAW_SYMBOL, "price": "1.01"}],
                "trades": [{"ts_event": "2026-03-16T13:30:00Z", "symbol": download.RAW_SYMBOL, "price": "1.02"}],
                "statistics": [],
            }

            code, manifest = download.run_download(
                api_key="test-key",
                output_root=output_root,
                manifest_path=manifest_path,
                client_factory=lambda key: FakeClient(calls, rows),
                git_ignore_checker=lambda paths: True,
            )

            self.assertEqual(code, 0)
            self.assertEqual(manifest["status"], "SUCCESS")
            self.assertTrue(manifest_path.exists())
            loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded, manifest)
            self.assertEqual([call["schema"] for call in calls], list(download.EXPECTED_SCHEMAS))
            self.assertEqual(len(manifest["output_files"]), 4)
            self.assertEqual(manifest["schema_status"]["statistics"]["status"], "empty")
            self.assertEqual(manifest["schema_status"]["cmbp-1"]["status"], "nonempty")

    def test_file_hashes_byte_counts_and_record_counts(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            manifest_path = output_root / "manifest.json"
            rows = {schema: [] for schema in download.EXPECTED_SCHEMAS}
            rows["cmbp-1"] = [
                {"ts_event": "2026-03-16T13:31:00Z", "symbol": download.RAW_SYMBOL, "price": "1.00"},
                {"ts_event": "2026-03-16T13:32:00Z", "symbol": download.RAW_SYMBOL, "price": "1.01"},
            ]

            code, manifest = download.run_download(
                api_key="test-key",
                output_root=output_root,
                manifest_path=manifest_path,
                client_factory=lambda key: FakeClient([], rows),
                git_ignore_checker=lambda paths: True,
            )

            self.assertEqual(code, 0)
            cmbp = next(item for item in manifest["output_files"] if item["schema"] == "cmbp-1")
            csv_path = download.REPO_ROOT / cmbp["csv_path"]
            self.assertEqual(cmbp["parsed_record_count"], 2)
            self.assertEqual(cmbp["csv_bytes"], csv_path.stat().st_size)
            self.assertEqual(
                cmbp["csv_sha256"],
                hashlib.sha256(csv_path.read_bytes()).hexdigest(),
            )

    def test_parseable_failure_manifest_and_reliable_exit_status(self):
        with self._workspace_tmp() as tmp:
            output_root = tmp / "day52_spy_670c"
            manifest_path = output_root / "manifest.json"

            code, manifest = download.run_download(
                api_key=None,
                output_root=output_root,
                manifest_path=manifest_path,
                client_factory=lambda key: self.fail("network should not run without auth"),
                git_ignore_checker=lambda paths: True,
            )

            self.assertEqual(code, 1)
            self.assertEqual(manifest["status"], "FAILURE")
            self.assertEqual(manifest["vendor_failure"]["classification"], "AUTH_MISSING")
            loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["status"], "FAILURE")

    def test_safe_fast_db_auth_enforcement(self):
        with self._workspace_tmp() as tmp:
            code, manifest = download.run_download(
                api_key="",
                output_root=tmp / "day52_spy_670c",
                manifest_path=tmp / "day52_spy_670c" / "manifest.json",
                client_factory=lambda key: self.fail("network should not run without auth"),
                git_ignore_checker=lambda paths: True,
            )

        self.assertEqual(code, 1)
        self.assertEqual(manifest["vendor_failure"]["classification"], "AUTH_MISSING")

    def test_no_credential_leakage(self):
        with self._workspace_tmp() as tmp:
            secret = "super-secret-test-key"
            code, manifest = download.run_download(
                api_key=secret,
                output_root=tmp / "day52_spy_670c",
                manifest_path=tmp / "day52_spy_670c" / "manifest.json",
                client_factory=lambda key: FakeClient([], {schema: [] for schema in download.EXPECTED_SCHEMAS}),
                git_ignore_checker=lambda paths: True,
            )

            self.assertEqual(code, 0)
            self.assertNotIn(secret, json.dumps(manifest, sort_keys=True))
            self.assertFalse(manifest["credential_value_printed"])
            self.assertFalse(manifest["credential_value_persisted"])

    def test_no_network_call_before_all_preflight_checks_pass(self):
        self.cost["requests"][0]["symbols"] = "BAD"
        network_called = False

        def factory(key):
            nonlocal network_called
            network_called = True
            return FakeClient([], {})

        with self._workspace_tmp() as tmp:
            cost_path = tmp / "bad_cost.json"
            contract_path = tmp / "contract.json"
            cost_path.write_text(json.dumps(self.cost), encoding="utf-8")
            contract_path.write_text(json.dumps(self.contract), encoding="utf-8")
            code, manifest = download.run_download(
                api_key="test-key",
                contract_resolution_path=contract_path,
                cost_result_path=cost_path,
                output_root=tmp / "out",
                manifest_path=tmp / "out" / "manifest.json",
                client_factory=factory,
                git_ignore_checker=lambda paths: True,
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
            "outputs": [],
            "created_utc": "2026-06-25T00:00:00Z",
        }

        first = download.build_manifest(**args)
        second = download.build_manifest(**deepcopy(args))

        self.assertEqual(first, second)

    def test_no_git_mutation_or_trade_proof_pnl_fields_invented(self):
        source = Path(download.__file__).read_text(encoding="utf-8")
        forbidden = ["git add", "git commit", "git push", "merge_pull_request"]
        for token in forbidden:
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
