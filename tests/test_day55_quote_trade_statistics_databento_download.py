import json
import shutil
import unittest
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from scripts import safe_fast_day55_quote_trade_statistics_databento_download as download
from watcher_foundation import day55_quote_trade_statistics_download_manifest_validator as validator


def fake_rows(source_request, request, *, count=1, symbol=None, ts=None):
    identity = source_request["contract_identities"][0]
    return [
        {
            "ts_event": ts or request["start"].replace("Z", ".000000001Z"),
            "symbol": symbol or request["symbols"],
            "instrument_id": str(identity["instrument_id"]),
            "publisher_id": str(identity["publisher_id"]),
            "price": "1.00",
        }
        for _ in range(count)
    ]


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "ts_event,symbol,instrument_id,publisher_id,price\n"
        + "".join(
            f"{row['ts_event']},{row['symbol']},{row['instrument_id']},{row['publisher_id']},{row['price']}\n"
            for row in rows
        ),
        encoding="utf-8",
    )


def write_fake_dbn(path, schema, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": schema, "rows": rows}), encoding="utf-8")


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
    def __init__(self, schema, rows):
        self.schema = schema
        self.rows = rows

    def to_csv(self, path, schema):
        write_csv(path, self.rows)


class FakeTimeseries:
    def __init__(self, calls, rows_by_key):
        self.calls = calls
        self.rows_by_key = rows_by_key

    def get_range(self, **kwargs):
        self.calls.append(kwargs)
        request = {
            "dataset": kwargs["dataset"],
            "schema": kwargs["schema"],
            "stype_in": kwargs["stype_in"],
            "symbols": kwargs["symbols"],
            "start": kwargs["start"],
            "end": kwargs["end"],
        }
        rows = self.rows_by_key[download.request_key(request)]
        write_fake_dbn(kwargs["path"], kwargs["schema"], rows)
        return FakeStore(kwargs["schema"], rows)


class FakeClient:
    def __init__(self, calls, rows_by_key):
        self.timeseries = FakeTimeseries(calls, rows_by_key)


class Day55QuoteTradeStatisticsDatabentoDownloadTests(unittest.TestCase):
    def setUp(self):
        self.inputs = download.load_inputs()
        self.source = deepcopy(self.inputs["source_request"])
        self.cost = deepcopy(self.inputs["cost_check"])
        self.source_requests, self.cost_requests = download.validate_preflight(
            source_request=self.source,
            cost_check=self.cost,
        )

    def tearDown(self):
        shutil.rmtree(
            download.REPO_ROOT / "historical_signal_replay" / "results" / "day55_download_test_tmp",
            ignore_errors=True,
        )

    def temp_root(self):
        root = download.REPO_ROOT / "historical_signal_replay" / "results" / "day55_download_test_tmp"
        path = root / f"case_{uuid4().hex}"
        path.mkdir(parents=True)
        return path

    def rows_by_key(self):
        return {
            download.request_key(request): fake_rows(self.source_requests[index], request)
            for index, request in enumerate(self.cost_requests)
        }

    def run_fake(self, tmp, *, api_key="test-key", source=None, cost=None):
        source = source or self.source
        cost = cost or self.cost
        source_path = tmp / "source.json"
        cost_path = tmp / "cost.json"
        source_path.write_text(json.dumps(source), encoding="utf-8")
        cost_path.write_text(json.dumps(cost), encoding="utf-8")
        calls = []
        output_root = tmp / "out"
        manifest_path = output_root / "manifest.json"
        rows = self.rows_by_key()
        code, manifest = download.run_download(
            api_key=api_key,
            source_request_path=source_path,
            cost_check_path=cost_path,
            output_root=output_root,
            manifest_path=manifest_path,
            client_factory=lambda key: FakeClient(calls, rows),
            dbn_parser=parse_fake_dbn,
        )
        return code, manifest, calls, manifest_path

    def test_preflight_accepts_only_exact_32_approved_cost_checked_requests(self):
        self.assertEqual(len(self.cost_requests), 32)
        self.assertEqual(
            self.cost_requests,
            [download.vendor_request(request) for request in self.source_requests],
        )
        self.assertEqual({request["schema"] for request in self.cost_requests}, download.REQUIRED_SCHEMAS)
        self.assertNotIn("definition", {request["schema"] for request in self.cost_requests})

    def test_preflight_rejects_cost_drift_definition_and_request_drift(self):
        cases = []
        changed_cost = deepcopy(self.cost)
        changed_cost["grouped_cost"] = "0.054846107959"
        cases.append((self.source, changed_cost, "grouped_cost_not_operator_approved_amount"))
        definition_cost = deepcopy(self.cost)
        definition_cost["requests"][0]["schema"] = "definition"
        cases.append((self.source, definition_cost, "definition_schema_forbidden"))
        changed_source = deepcopy(self.source)
        changed_source["requests"][0]["symbols"] = "SPY   260414C00646000"
        cases.append((changed_source, self.cost, "cost_check_requests_do_not_match_source_request"))

        for source, cost, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaises(download.DownloadError) as raised:
                    download.validate_preflight(source_request=source, cost_check=cost)
                self.assertEqual(raised.exception.classification, "PREFLIGHT_FAILED")
                self.assertIn(expected, raised.exception.detail)

    def test_downloads_all_32_requests_and_manifest_validator_passes(self):
        tmp = self.temp_root()
        code, manifest, calls, manifest_path = self.run_fake(tmp)

        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 32)
        self.assertEqual(manifest["status"], "SUCCESS")
        self.assertEqual(len(manifest["output_files"]), 32)
        self.assertEqual(manifest["profitability_proof"], "NO")
        self.assertEqual(manifest["paper_live_eligibility"], "NO")
        self.assertIsNone(manifest["gross_pnl"])
        self.assertIsNone(manifest["net_pnl"])
        validation = validator.validate_manifest(manifest_path)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])

    def test_reuses_existing_pair_and_does_not_duplicate_request(self):
        tmp = self.temp_root()
        output_root = tmp / "out"
        first_request = self.cost_requests[0]
        first_source = self.source_requests[0]
        first_id = download.request_id(0, first_request)
        paths = {
            "dbn": output_root / f"{first_id}.dbn.zst",
            "csv": output_root / f"{first_id}.csv",
        }
        rows = fake_rows(first_source, first_request, count=2)
        write_fake_dbn(paths["dbn"], first_request["schema"], rows)
        write_csv(paths["csv"], rows)

        code, manifest, calls, _ = self.run_fake(tmp)

        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 31)
        self.assertEqual(manifest["request_status"][first_id]["status"], "COMPLETED_REUSED")
        self.assertEqual(manifest["output_files"][0]["parsed_record_count"], 2)

    def test_recovers_interrupted_publish_without_repeating_paid_request(self):
        tmp = self.temp_root()
        output_root = tmp / "out"
        first_request = self.cost_requests[0]
        first_source = self.source_requests[0]
        first_id = download.request_id(0, first_request)
        dbn_path = output_root / f"{first_id}.dbn.zst"
        csv_temp_path = output_root / f"{first_id}.csv.tmp.1234"
        rows = fake_rows(first_source, first_request, count=2)
        write_fake_dbn(dbn_path, first_request["schema"], rows)
        write_csv(csv_temp_path, rows)

        code, manifest, calls, _ = self.run_fake(tmp)

        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 31)
        self.assertTrue((output_root / f"{first_id}.csv").exists())
        self.assertFalse(csv_temp_path.exists())
        self.assertEqual(manifest["request_status"][first_id]["status"], "COMPLETED_REUSED")

    def test_bad_existing_pair_refuses_before_network_call(self):
        tmp = self.temp_root()
        output_root = tmp / "out"
        first_request = self.cost_requests[0]
        first_id = download.request_id(0, first_request)
        paths = {
            "dbn": output_root / f"{first_id}.dbn.zst",
            "csv": output_root / f"{first_id}.csv",
        }
        rows = fake_rows(self.source_requests[0], first_request, symbol="BAD")
        write_fake_dbn(paths["dbn"], first_request["schema"], rows)
        write_csv(paths["csv"], rows)

        code, manifest, calls, _ = self.run_fake(tmp)

        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertEqual(manifest["vendor_failure"]["classification"], "EXISTING_PAIR_INVALID")

    def test_missing_auth_writes_failure_manifest_without_leaking_credentials(self):
        tmp = self.temp_root()
        code, manifest, calls, manifest_path = self.run_fake(tmp, api_key="")

        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertEqual(manifest["vendor_failure"]["classification"], "AUTH_MISSING")
        self.assertTrue(manifest_path.exists())
        self.assertFalse(manifest["credential_value_printed"])
        self.assertFalse(manifest["credential_value_persisted"])
        self.assertNotIn("net_pnl", json.dumps(manifest["output_files"], sort_keys=True))


if __name__ == "__main__":
    unittest.main()
