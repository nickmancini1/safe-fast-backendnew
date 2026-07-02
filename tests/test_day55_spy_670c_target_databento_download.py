import json
import shutil
import unittest
from copy import deepcopy
from pathlib import Path

from historical_signal_replay import day55_spy_670c_target_databento_download as download


def fake_rows(request, *, count=1, symbol=None, ts=None):
    return [
        {
            "ts_event": ts or request["start"].replace("Z", ".000000001Z"),
            "symbol": symbol or request["symbols"],
            "price": "1.00",
        }
        for _ in range(count)
    ]


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "ts_event,symbol,price\n"
        + "".join(f"{row['ts_event']},{row['symbol']},{row['price']}\n" for row in rows),
        encoding="utf-8",
    )


def write_fake_dbn(path, schema, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": schema, "rows": rows}), encoding="utf-8")


def parse_fake_dbn(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = payload["rows"]
    symbols = {row["symbol"] for row in rows}
    return {
        "schema": payload["schema"],
        "record_count": len(rows),
        "symbol": next(iter(symbols)) if len(symbols) == 1 else "__MULTIPLE__",
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


class Day55Spy670CTargetDatabentoDownloadTests(unittest.TestCase):
    def setUp(self):
        self.source = download.load_source_request()
        self.requests = download.validate_preflight(self.source)
        self.output_root = download.OUTPUT_ROOT
        shutil.rmtree(self.output_root, ignore_errors=True)

    def tearDown(self):
        shutil.rmtree(self.output_root, ignore_errors=True)

    def write_source(self, source):
        self.output_root.mkdir(parents=True, exist_ok=True)
        path = self.output_root / "day55_spy_670c_target_download_test_source.json"
        path.write_text(json.dumps(source), encoding="utf-8")
        return path

    def rows_by_key(self):
        return {
            download.request_key(request): fake_rows(request)
            for request in self.requests
        }

    def run_fake(self, *, api_key="test-key", source=None):
        source_path = download.SOURCE_REQUEST_PATH if source is None else self.write_source(source)
        calls = []
        code, manifest = download.run_download(
            api_key=api_key,
            source_request_path=source_path,
            output_root=self.output_root,
            manifest_path=download.MANIFEST_PATH,
            client_factory=lambda key: FakeClient(calls, self.rows_by_key()),
            dbn_parser=parse_fake_dbn,
        )
        if source_path != download.SOURCE_REQUEST_PATH:
            source_path.unlink()
        return code, manifest, calls

    def assert_preflight_rejects(self, source, expected):
        with self.assertRaises(download.DownloadError) as raised:
            download.validate_preflight(source)
        self.assertEqual(raised.exception.classification, "PREFLIGHT_FAILED")
        self.assertIn(expected, raised.exception.detail)

    def test_preflight_accepts_exact_4_target_requests(self):
        self.assertEqual(len(self.requests), 4)
        self.assertEqual([request["schema"] for request in self.requests], list(download.REQUIRED_SCHEMAS))
        self.assertEqual({request["symbols"] for request in self.requests}, {download.EXACT_SYMBOL})
        self.assertEqual({request["dataset"] for request in self.requests}, {download.DATASET})
        self.assertNotIn("definition", {request["schema"] for request in self.requests})

    def test_preflight_rejects_wrong_symbol(self):
        source = deepcopy(self.source)
        source["requests"][0]["symbols"] = "SPY   260330C00669000"
        self.assert_preflight_rejects(source, "request_symbol_mismatch")

    def test_preflight_rejects_definition_schema(self):
        source = deepcopy(self.source)
        source["requests"][0]["schema"] = "definition"
        self.assert_preflight_rejects(source, "definition_schema_forbidden")

    def test_preflight_rejects_wrong_cost(self):
        source = deepcopy(self.source)
        source["exact_estimated_cost"] = "0.006495481731"
        self.assert_preflight_rejects(source, "exact_estimated_cost_not_operator_approved_amount")

    def test_preflight_rejects_wrong_destination(self):
        source = deepcopy(self.source)
        source["destination_for_approved_download"] = "historical_signal_replay/source_data/external_option_data_drop/wrong"
        self.assert_preflight_rejects(source, "destination_for_approved_download_mismatch")

    def test_preflight_rejects_download_performed_true(self):
        source = deepcopy(self.source)
        source["download_performed"] = True
        self.assert_preflight_rejects(source, "source_request_download_already_performed")

    def test_preflight_rejects_vendor_call_performed_true(self):
        source = deepcopy(self.source)
        source["vendor_call_performed"] = True
        self.assert_preflight_rejects(source, "source_request_vendor_call_already_performed")

    def test_fake_client_download_writes_manifest_under_target_only_destination(self):
        code, manifest, calls = self.run_fake()

        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 4)
        self.assertTrue(download.MANIFEST_PATH.exists())
        self.assertEqual(manifest["status"], "SUCCESS")
        self.assertEqual(manifest["output_root"], download._relative(download.OUTPUT_ROOT))
        self.assertEqual(len(manifest["output_files"]), 4)
        self.assertTrue(
            all(row["dbn_path"].startswith(manifest["output_root"]) for row in manifest["output_files"])
        )
        self.assertEqual(manifest["profitability_proof"], "NO")
        self.assertEqual(manifest["paper_live_eligibility"], "NO")
        self.assertIsNone(manifest["gross_pnl"])
        self.assertIsNone(manifest["net_pnl"])

    def test_no_credential_leak_in_failure_output(self):
        code, manifest, calls = self.run_fake(api_key="")

        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertEqual(manifest["vendor_failure"]["classification"], "AUTH_MISSING")
        serialized = json.dumps(manifest, sort_keys=True)
        self.assertNotIn("super-secret", serialized)
        self.assertFalse(manifest["credential_value_printed"])
        self.assertFalse(manifest["credential_value_persisted"])


if __name__ == "__main__":
    unittest.main()
