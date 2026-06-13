import csv
import unittest
import uuid
from contextlib import contextmanager
from datetime import timezone
from decimal import Decimal
from pathlib import Path

from historical_signal_replay import databento_opra_normalizer as normalizer


class DatabentoOpraNormalizerTests(unittest.TestCase):
    def test_symbol_parsing(self):
        parsed = normalizer.parse_opra_symbol("QQQ   260501C00610000")

        self.assertEqual(parsed.underlying, "QQQ")
        self.assertEqual(parsed.expiration, "2026-05-01")
        self.assertEqual(parsed.side, "C")
        self.assertEqual(parsed.strike, Decimal("610"))

    def test_definition_join_uses_instrument_id(self):
        definitions = [
            normalizer.normalize_definition(
                {
                    "instrument_id": "100",
                    "symbol": "QQQ   260501C00610000",
                    "expiration": "2026-05-01T00:00:00.000000000Z",
                    "instrument_class": "C",
                    "strike_price": "610.000000000",
                    "underlying": "QQQ",
                }
            )
        ]
        quote = normalizer.normalize_quote(_quote_row("2026-04-13T16:29:00Z"))

        joined = normalizer.join_rows_to_definitions([quote], definitions)

        self.assertEqual(joined[0]["definition"]["instrument_id"], "100")
        self.assertEqual(joined[0]["definition"]["expiration"], "2026-05-01")
        self.assertEqual(joined[0]["definition"]["side"], "C")
        self.assertEqual(joined[0]["definition"]["strike"], Decimal("610.000000000"))

    def test_quote_selection_rejects_post_signal_rows(self):
        quotes = [
            normalizer.normalize_quote(
                _quote_row("2026-04-13T16:29:30Z", bid="13.50", ask="13.60")
            ),
            normalizer.normalize_quote(
                _quote_row("2026-04-13T16:30:00Z", bid="13.51", ask="13.62")
            ),
            normalizer.normalize_quote(
                _quote_row("2026-04-13T16:30:01Z", bid="99.00", ask="100.00")
            ),
        ]

        selected = normalizer.select_quote_at_or_before(
            quotes,
            "2026-04-13T12:30:00-04:00",
            symbol="QQQ   260501C00610000",
        )

        self.assertEqual(selected["ts_event"].isoformat(), "2026-04-13T16:30:00+00:00")
        self.assertEqual(selected["bid"], Decimal("13.51"))
        self.assertEqual(selected["ask"], Decimal("13.62"))

    def test_spread_calculation(self):
        quote = normalizer.normalize_quote(
            _quote_row("2026-04-13T16:30:00Z", bid="13.50", ask="13.60")
        )

        self.assertEqual(quote["midpoint"], Decimal("13.55"))
        self.assertEqual(quote["spread"], Decimal("0.10"))
        self.assertEqual(quote["spread_pct"], Decimal("0.10") / Decimal("13.55"))

    def test_statistics_interpretation(self):
        rows = [
            normalizer.normalize_statistic(
                _stat_row("2026-04-13T10:30:00Z", stat_type="9", quantity="19")
            ),
            normalizer.normalize_statistic(
                _stat_row("2026-04-13T16:29:00Z", stat_type="6", quantity="44")
            ),
            normalizer.normalize_statistic(
                _stat_row("2026-04-13T16:31:00Z", stat_type="6", quantity="88")
            ),
        ]

        latest = normalizer.latest_statistics_by_symbol(
            rows,
            at_or_before="2026-04-13T16:30:00Z",
        )

        self.assertEqual(rows[0]["stat_name"], "open_interest")
        self.assertEqual(rows[1]["stat_name"], "cleared_volume")
        self.assertEqual(
            latest[("QQQ   260501C00610000", "open_interest")]["quantity"],
            Decimal("19"),
        )
        self.assertEqual(
            latest[("QQQ   260501C00610000", "cleared_volume")]["quantity"],
            Decimal("44"),
        )

    def test_timestamp_normalization_requires_timezone(self):
        normalized = normalizer.normalize_timestamp("2026-04-13T12:30:00-04:00")

        self.assertEqual(normalized.tzinfo, timezone.utc)
        self.assertEqual(normalized.isoformat(), "2026-04-13T16:30:00+00:00")
        with self.assertRaisesRegex(normalizer.DatabentoOpraNormalizerError, "timezone"):
            normalizer.normalize_timestamp("2026-04-13T12:30:00")

    def test_missing_columns_fail_clearly(self):
        with _fixture_directory() as directory:
            path = Path(directory) / "quotes.csv"
            _write_csv(
                path,
                ["instrument_id", "symbol", "ts_event"],
                [
                    {
                        "instrument_id": "100",
                        "symbol": "QQQ   260501C00610000",
                        "ts_event": "2026-04-13T16:30:00Z",
                    }
                ],
            )

            with self.assertRaisesRegex(
                normalizer.MissingColumnError,
                "ask_px_00",
            ):
                normalizer.load_quotes_csv(path)

    def test_loader_supports_definitions_quotes_trades_and_statistics(self):
        with _fixture_directory() as directory:
            base = Path(directory)
            definitions_path = base / "definitions.csv"
            quotes_path = base / "quotes.csv"
            trades_path = base / "trades.csv"
            stats_path = base / "stats.csv"
            _write_csv(
                definitions_path,
                [
                    "instrument_id",
                    "symbol",
                    "expiration",
                    "instrument_class",
                    "strike_price",
                    "underlying",
                ],
                [
                    {
                        "instrument_id": "100",
                        "symbol": "QQQ   260501C00610000",
                        "expiration": "2026-05-01T00:00:00.000000000Z",
                        "instrument_class": "C",
                        "strike_price": "610.000000000",
                        "underlying": "QQQ",
                    }
                ],
            )
            _write_csv(
                quotes_path,
                list(_quote_row("2026-04-13T16:30:00Z")),
                [_quote_row("2026-04-13T16:30:00Z")],
            )
            _write_csv(
                trades_path,
                list(_trade_row("2026-04-13T16:30:00Z")),
                [_trade_row("2026-04-13T16:30:00Z")],
            )
            _write_csv(
                stats_path,
                list(_stat_row("2026-04-13T10:30:00Z")),
                [_stat_row("2026-04-13T10:30:00Z")],
            )

            self.assertEqual(len(normalizer.load_definitions_csv(definitions_path)), 1)
            self.assertEqual(len(normalizer.load_quotes_csv(quotes_path)), 1)
            self.assertEqual(len(normalizer.load_trades_csv(trades_path)), 1)
            self.assertEqual(len(normalizer.load_statistics_csv(stats_path)), 1)

    def test_no_fill_pnl_readiness_or_proof_inference(self):
        for unsafe_call in (
            normalizer.infer_fill,
            normalizer.choose_trade,
            normalizer.calculate_pnl,
            normalizer.mark_ready,
            normalizer.accept_proof,
        ):
            with self.assertRaises(normalizer.UnsafeInferenceError):
                unsafe_call({})


def _quote_row(ts_event, bid="13.51", ask="13.60"):
    return {
        "instrument_id": "100",
        "symbol": "QQQ   260501C00610000",
        "ts_event": ts_event,
        "ts_recv": ts_event,
        "bid_px_00": bid,
        "ask_px_00": ask,
        "bid_sz_00": "10",
        "ask_sz_00": "20",
    }


def _trade_row(ts_event):
    return {
        "instrument_id": "100",
        "symbol": "QQQ   260501C00610000",
        "ts_event": ts_event,
        "ts_recv": ts_event,
        "price": "13.55",
        "size": "3",
    }


def _stat_row(ts_event, stat_type="9", quantity="19"):
    return {
        "instrument_id": "100",
        "symbol": "QQQ   260501C00610000",
        "ts_event": ts_event,
        "ts_recv": ts_event,
        "stat_type": stat_type,
        "quantity": quantity,
    }


def _write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


@contextmanager
def _fixture_directory():
    directory = Path.cwd() / f"codex_databento_fixture_{uuid.uuid4().hex}"
    directory.mkdir()
    try:
        yield directory
    finally:
        for path in directory.iterdir():
            path.unlink()
        directory.rmdir()


if __name__ == "__main__":
    unittest.main()
