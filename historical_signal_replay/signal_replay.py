import json
from pathlib import Path

try:
    from .metrics import build_summary
except ImportError:
    from metrics import build_summary


BASE_DIR = Path(__file__).resolve().parent
FIXTURE_PATH = BASE_DIR / "fixtures" / "no_hindsight_sample_signal_replay_fixture.json"
DEFAULT_FIXTURE_PATHS = (
    FIXTURE_PATH,
    BASE_DIR / "fixtures" / "no_hindsight_clean_fast_break_signal_replay_fixture.json",
)
REPORTS_DIR = BASE_DIR / "reports"
SIGNAL_LOG_PATH = REPORTS_DIR / "no_hindsight_sample_signal_log.jsonl"
SUMMARY_PATH = REPORTS_DIR / "no_hindsight_sample_summary.json"
REGRESSION_CANDIDATES_PATH = REPORTS_DIR / "no_hindsight_regression_candidates.json"

REQUIRED_INPUT_KEYS = {
    "symbol",
    "timestamp",
    "candles_1h_rth",
    "context_24h_daily",
    "market_calendar_session",
    "macro_context",
    "iv_context",
    "event_context",
}

REQUIRED_OUTPUT_KEYS = {
    "timestamp",
    "symbol",
    "setup_type",
    "setup_state",
    "stage",
    "trigger_state",
    "trigger_level",
    "invalidation",
    "room_status",
    "extension_status",
    "context_24h",
    "wall_thesis_fit",
    "final_verdict",
    "primary_blocker",
    "cautions_watchouts",
    "winner_selection_result",
    "human_next_step",
    "first_seen",
    "last_seen",
    "state_changed",
    "prior_state",
    "current_state",
    "trigger_changed",
    "blocker_changed",
    "duplicate_alert_suppression_key",
}


def load_fixture(path=FIXTURE_PATH):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate_required_keys(payload, required_keys, label):
    missing = sorted(required_keys - set(payload))
    if missing:
        raise ValueError(f"{label} missing required keys: {', '.join(missing)}")


def validate_fixture(fixture):
    _validate_required_keys(fixture, {"input", "expected_output_shape"}, "fixture")
    _validate_required_keys(fixture["input"], REQUIRED_INPUT_KEYS, "fixture.input")
    _validate_required_keys(
        fixture["expected_output_shape"],
        REQUIRED_OUTPUT_KEYS,
        "fixture.expected_output_shape",
    )


def run_signal_replay(fixture_paths=None):
    if fixture_paths is None:
        fixture_paths = DEFAULT_FIXTURE_PATHS

    fixtures = []
    for fixture_path in fixture_paths:
        fixture = load_fixture(fixture_path)
        validate_fixture(fixture)
        fixtures.append(fixture)

    signal_rows = [fixture["expected_output_shape"] for fixture in fixtures]
    summary = build_summary(signal_rows)
    regression_candidates = {
        "purpose": "Signal/stage replay regression candidates only; no profitability, P&L, account sizing, or trade outcomes.",
        "candidates": [],
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with SIGNAL_LOG_PATH.open("w", encoding="utf-8") as handle:
        for row in signal_rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    REGRESSION_CANDIDATES_PATH.write_text(
        json.dumps(regression_candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "signal_rows": signal_rows,
        "summary": summary,
        "regression_candidates": regression_candidates,
        "signal_log_path": str(SIGNAL_LOG_PATH),
        "summary_path": str(SUMMARY_PATH),
        "regression_candidates_path": str(REGRESSION_CANDIDATES_PATH),
    }
