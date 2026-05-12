import json
from pathlib import Path

try:
    from .metrics import (
        build_lifecycle_summary,
        build_repeated_state_summary,
        build_summary,
    )
except ImportError:
    from metrics import build_lifecycle_summary, build_repeated_state_summary, build_summary


BASE_DIR = Path(__file__).resolve().parent
FIXTURE_PATH = BASE_DIR / "fixtures" / "no_hindsight_sample_signal_replay_fixture.json"
DEFAULT_FIXTURE_PATHS = (
    FIXTURE_PATH,
    BASE_DIR / "fixtures" / "no_hindsight_clean_fast_break_signal_replay_fixture.json",
    BASE_DIR / "fixtures" / "no_hindsight_ideal_signal_replay_fixture.json",
)
REPORTS_DIR = BASE_DIR / "reports"
SIGNAL_LOG_PATH = REPORTS_DIR / "no_hindsight_sample_signal_log.jsonl"
SUMMARY_PATH = REPORTS_DIR / "no_hindsight_sample_summary.json"
REGRESSION_CANDIDATES_PATH = REPORTS_DIR / "no_hindsight_regression_candidates.json"
LIFECYCLE_FIXTURE_PATH = (
    BASE_DIR
    / "fixtures"
    / "no_hindsight_continuation_lifecycle_signal_replay_fixture.json"
)
LIFECYCLE_SIGNAL_LOG_PATH = (
    REPORTS_DIR / "no_hindsight_continuation_lifecycle_signal_log.jsonl"
)
LIFECYCLE_SUMMARY_PATH = (
    REPORTS_DIR / "no_hindsight_continuation_lifecycle_summary.json"
)
LIFECYCLE_REGRESSION_CANDIDATES_PATH = (
    REPORTS_DIR / "no_hindsight_continuation_lifecycle_regression_candidates.json"
)
REPEATED_STATE_FIXTURE_PATH = (
    BASE_DIR
    / "fixtures"
    / "no_hindsight_continuation_repeated_state_duplicate_suppression_fixture.json"
)
REPEATED_STATE_SIGNAL_LOG_PATH = (
    REPORTS_DIR
    / "no_hindsight_continuation_repeated_state_duplicate_suppression_signal_log.jsonl"
)
REPEATED_STATE_SUMMARY_PATH = (
    REPORTS_DIR
    / "no_hindsight_continuation_repeated_state_duplicate_suppression_summary.json"
)
REPEATED_STATE_REGRESSION_CANDIDATES_PATH = (
    REPORTS_DIR
    / "no_hindsight_continuation_repeated_state_duplicate_suppression_regression_candidates.json"
)

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

REQUIRED_REPEATED_STATE_OUTPUT_KEYS = {
    "timestamp",
    "symbol",
    "setup_type",
    "setup_state",
    "stage",
    "trigger_state",
    "trigger_level",
    "invalidation",
    "final_verdict",
    "primary_blocker",
    "human_next_step",
    "first_seen",
    "last_seen",
    "state_changed",
    "prior_state",
    "current_state",
    "trigger_changed",
    "blocker_changed",
    "duplicate_alert_suppression_key",
    "meaningful_alert_candidate",
    "duplicate_suppressed",
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


def validate_lifecycle_fixture(fixture):
    _validate_required_keys(fixture, {"lifecycle_rows"}, "lifecycle fixture")
    if not isinstance(fixture["lifecycle_rows"], list) or not fixture["lifecycle_rows"]:
        raise ValueError("lifecycle fixture lifecycle_rows must be a non-empty list")

    for index, row in enumerate(fixture["lifecycle_rows"], start=1):
        label = f"lifecycle fixture row {index}"
        _validate_required_keys(row, {"input", "expected_output_shape"}, label)
        _validate_required_keys(row["input"], REQUIRED_INPUT_KEYS, f"{label}.input")
        _validate_required_keys(
            row["expected_output_shape"],
            REQUIRED_OUTPUT_KEYS,
            f"{label}.expected_output_shape",
        )


def validate_repeated_state_fixture(fixture):
    _validate_required_keys(
        fixture,
        {"repeated_state_rows"},
        "repeated-state fixture",
    )
    rows = fixture["repeated_state_rows"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("repeated-state fixture repeated_state_rows must be a non-empty list")

    for index, row in enumerate(rows, start=1):
        label = f"repeated-state fixture row {index}"
        _validate_required_keys(row, {"input", "expected_output_shape"}, label)
        _validate_required_keys(row["input"], REQUIRED_INPUT_KEYS, f"{label}.input")
        _validate_required_keys(
            row["expected_output_shape"],
            REQUIRED_REPEATED_STATE_OUTPUT_KEYS,
            f"{label}.expected_output_shape",
        )


def _write_signal_log(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _build_regression_candidates(purpose, rows=None):
    candidates = []
    for row in rows or []:
        candidates.append(
            {
                "timestamp": row.get("timestamp"),
                "symbol": row.get("symbol"),
                "setup_type": row.get("setup_type"),
                "stage": row.get("stage"),
                "setup_state": row.get("setup_state"),
                "trigger_state": row.get("trigger_state"),
                "final_verdict": row.get("final_verdict"),
                "primary_blocker": row.get("primary_blocker"),
                "state_changed": row.get("state_changed"),
                "trigger_changed": row.get("trigger_changed"),
                "blocker_changed": row.get("blocker_changed"),
                "duplicate_alert_suppression_key": row.get(
                    "duplicate_alert_suppression_key"
                ),
            }
        )
    return {
        "purpose": purpose,
        "candidates": candidates,
    }


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
    regression_candidates = _build_regression_candidates(
        "Signal/stage replay regression candidates only; no profitability, P&L, account sizing, or trade outcomes."
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_signal_log(SIGNAL_LOG_PATH, signal_rows)

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


def run_lifecycle_signal_replay(fixture_path=LIFECYCLE_FIXTURE_PATH):
    fixture = load_fixture(fixture_path)
    validate_lifecycle_fixture(fixture)

    signal_rows = [
        row["expected_output_shape"] for row in fixture["lifecycle_rows"]
    ]
    summary = build_lifecycle_summary(signal_rows)
    regression_candidates = _build_regression_candidates(
        "Signal/stage/lifecycle replay regression candidates only; no profitability, P&L, account sizing, trade outcomes, live trade decisions, or auto-trading.",
        signal_rows,
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_signal_log(LIFECYCLE_SIGNAL_LOG_PATH, signal_rows)
    LIFECYCLE_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    LIFECYCLE_REGRESSION_CANDIDATES_PATH.write_text(
        json.dumps(regression_candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "signal_rows": signal_rows,
        "summary": summary,
        "regression_candidates": regression_candidates,
        "signal_log_path": str(LIFECYCLE_SIGNAL_LOG_PATH),
        "summary_path": str(LIFECYCLE_SUMMARY_PATH),
        "regression_candidates_path": str(LIFECYCLE_REGRESSION_CANDIDATES_PATH),
    }


def run_repeated_state_signal_replay(fixture_path=REPEATED_STATE_FIXTURE_PATH):
    fixture = load_fixture(fixture_path)
    validate_repeated_state_fixture(fixture)

    signal_rows = [
        row["expected_output_shape"] for row in fixture["repeated_state_rows"]
    ]
    summary = build_repeated_state_summary(signal_rows)
    regression_candidates = _build_regression_candidates(
        "Signal/stage/lifecycle duplicate-suppression regression candidates only; no profitability, P&L, account sizing, trade outcomes, live trade decisions, or auto-trading.",
        signal_rows,
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_signal_log(REPEATED_STATE_SIGNAL_LOG_PATH, signal_rows)
    REPEATED_STATE_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    REPEATED_STATE_REGRESSION_CANDIDATES_PATH.write_text(
        json.dumps(regression_candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "signal_rows": signal_rows,
        "summary": summary,
        "regression_candidates": regression_candidates,
        "signal_log_path": str(REPEATED_STATE_SIGNAL_LOG_PATH),
        "summary_path": str(REPEATED_STATE_SUMMARY_PATH),
        "regression_candidates_path": str(REPEATED_STATE_REGRESSION_CANDIDATES_PATH),
    }
