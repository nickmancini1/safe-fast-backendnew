import json
from pathlib import Path

from metrics import build_lifecycle_summary
from signal_replay import (
    REPORTS_DIR,
    validate_lifecycle_fixture,
    run_lifecycle_signal_replay,
    run_repeated_state_signal_replay,
    run_signal_replay,
)


BASE_DIR = Path(__file__).resolve().parent
FIRST_REAL_FIXTURE_PATH = (
    BASE_DIR / "fixtures" / "first_real_spy_continuation_replay_v1_fixture.json"
)
FIRST_REAL_SIGNAL_LOG_PATH = (
    REPORTS_DIR / "first_real_spy_continuation_replay_v1_signal_log.jsonl"
)
FIRST_REAL_SUMMARY_PATH = (
    REPORTS_DIR / "first_real_spy_continuation_replay_v1_summary.json"
)
FIRST_REAL_REGRESSION_CANDIDATES_PATH = (
    REPORTS_DIR / "first_real_spy_continuation_replay_v1_regression_candidates.json"
)
SECOND_REAL_FIXTURE_PATH = (
    BASE_DIR / "fixtures" / "second_real_spy_ideal_replay_v1_fixture.json"
)
SECOND_REAL_SIGNAL_LOG_PATH = (
    REPORTS_DIR / "second_real_spy_ideal_replay_v1_signal_log.jsonl"
)
SECOND_REAL_SUMMARY_PATH = (
    REPORTS_DIR / "second_real_spy_ideal_replay_v1_summary.json"
)
SECOND_REAL_REGRESSION_CANDIDATES_PATH = (
    REPORTS_DIR / "second_real_spy_ideal_replay_v1_regression_candidates.json"
)
THIRD_REAL_FIXTURE_PATH = (
    BASE_DIR / "fixtures" / "third_real_spy_clean_fast_break_replay_v1_fixture.json"
)
THIRD_REAL_SIGNAL_LOG_PATH = (
    REPORTS_DIR / "third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl"
)
THIRD_REAL_SUMMARY_PATH = (
    REPORTS_DIR / "third_real_spy_clean_fast_break_replay_v1_summary.json"
)
THIRD_REAL_REGRESSION_CANDIDATES_PATH = (
    REPORTS_DIR
    / "third_real_spy_clean_fast_break_replay_v1_regression_candidates.json"
)
FIRST_REAL_QQQ_IDEAL_FIXTURE_PATH = (
    BASE_DIR / "fixtures" / "first_real_qqq_ideal_replay_v1_fixture.json"
)
FIRST_REAL_QQQ_IDEAL_SIGNAL_LOG_PATH = (
    REPORTS_DIR / "first_real_qqq_ideal_replay_v1_signal_log.jsonl"
)
FIRST_REAL_QQQ_IDEAL_SUMMARY_PATH = (
    REPORTS_DIR / "first_real_qqq_ideal_replay_v1_summary.json"
)
FIRST_REAL_QQQ_IDEAL_REGRESSION_CANDIDATES_PATH = (
    REPORTS_DIR / "first_real_qqq_ideal_replay_v1_regression_candidates.json"
)
FIRST_REAL_QQQ_CLEAN_FAST_BREAK_FIXTURE_PATH = (
    BASE_DIR / "fixtures" / "first_real_qqq_clean_fast_break_replay_v1_fixture.json"
)
FIRST_REAL_QQQ_CLEAN_FAST_BREAK_SIGNAL_LOG_PATH = (
    REPORTS_DIR / "first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl"
)
FIRST_REAL_QQQ_CLEAN_FAST_BREAK_SUMMARY_PATH = (
    REPORTS_DIR / "first_real_qqq_clean_fast_break_replay_v1_summary.json"
)
FIRST_REAL_QQQ_CLEAN_FAST_BREAK_REGRESSION_CANDIDATES_PATH = (
    REPORTS_DIR
    / "first_real_qqq_clean_fast_break_replay_v1_regression_candidates.json"
)


def _load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_signal_log(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _build_first_real_regression_candidates(rows):
    return {
        "purpose": (
            "First-real SPY Continuation signal/stage/lifecycle replay "
            "regression candidates only; no profitability, P&L, account sizing, "
            "trade outcomes, live trade decisions, or auto-trading."
        ),
        "candidates": [
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
            for row in rows
        ],
    }


def _build_second_real_regression_candidates(rows):
    return {
        "purpose": (
            "Second-real SPY Ideal signal/stage/lifecycle replay "
            "regression candidates only; no profitability, P&L, account sizing, "
            "trade outcomes, live trade decisions, or auto-trading."
        ),
        "candidates": [
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
            for row in rows
        ],
    }


def _build_third_real_regression_candidates(rows):
    return {
        "purpose": (
            "Third-real SPY Clean Fast Break signal/stage/lifecycle replay "
            "regression candidates only; no profitability, P&L, account sizing, "
            "trade outcomes, live trade decisions, or auto-trading."
        ),
        "candidates": [
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
            for row in rows
        ],
    }


def _build_first_real_qqq_ideal_regression_candidates(rows):
    return {
        "purpose": (
            "First-real QQQ Ideal signal/stage/lifecycle replay "
            "regression candidates only; no profitability, P&L, account sizing, "
            "trade outcomes, live trade decisions, or auto-trading."
        ),
        "candidates": [
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
            for row in rows
        ],
    }


def _build_first_real_qqq_clean_fast_break_regression_candidates(rows):
    return {
        "purpose": (
            "First-real QQQ Clean Fast Break signal/stage/lifecycle replay "
            "regression candidates only; no profitability, P&L, account sizing, "
            "trade outcomes, live trade decisions, or auto-trading."
        ),
        "candidates": [
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
            for row in rows
        ],
    }


def run_first_real_spy_continuation_replay():
    fixture = _load_json(FIRST_REAL_FIXTURE_PATH)
    validate_lifecycle_fixture(fixture)

    signal_rows = [
        row["expected_output_shape"] for row in fixture["lifecycle_rows"]
    ]
    summary = build_lifecycle_summary(signal_rows)
    regression_candidates = _build_first_real_regression_candidates(signal_rows)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_signal_log(FIRST_REAL_SIGNAL_LOG_PATH, signal_rows)
    FIRST_REAL_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    FIRST_REAL_REGRESSION_CANDIDATES_PATH.write_text(
        json.dumps(regression_candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "signal_rows": signal_rows,
        "summary": summary,
        "regression_candidates": regression_candidates,
        "signal_log_path": str(FIRST_REAL_SIGNAL_LOG_PATH),
        "summary_path": str(FIRST_REAL_SUMMARY_PATH),
        "regression_candidates_path": str(FIRST_REAL_REGRESSION_CANDIDATES_PATH),
    }


def run_second_real_spy_ideal_replay():
    fixture = _load_json(SECOND_REAL_FIXTURE_PATH)
    validate_lifecycle_fixture(fixture)

    signal_rows = [
        row["expected_output_shape"] for row in fixture["lifecycle_rows"]
    ]
    summary = build_lifecycle_summary(signal_rows)
    regression_candidates = _build_second_real_regression_candidates(signal_rows)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_signal_log(SECOND_REAL_SIGNAL_LOG_PATH, signal_rows)
    SECOND_REAL_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    SECOND_REAL_REGRESSION_CANDIDATES_PATH.write_text(
        json.dumps(regression_candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "signal_rows": signal_rows,
        "summary": summary,
        "regression_candidates": regression_candidates,
        "signal_log_path": str(SECOND_REAL_SIGNAL_LOG_PATH),
        "summary_path": str(SECOND_REAL_SUMMARY_PATH),
        "regression_candidates_path": str(SECOND_REAL_REGRESSION_CANDIDATES_PATH),
    }


def run_third_real_spy_clean_fast_break_replay():
    fixture = _load_json(THIRD_REAL_FIXTURE_PATH)
    validate_lifecycle_fixture(fixture)

    signal_rows = [
        row["expected_output_shape"] for row in fixture["lifecycle_rows"]
    ]
    summary = build_lifecycle_summary(signal_rows)
    regression_candidates = _build_third_real_regression_candidates(signal_rows)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_signal_log(THIRD_REAL_SIGNAL_LOG_PATH, signal_rows)
    THIRD_REAL_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    THIRD_REAL_REGRESSION_CANDIDATES_PATH.write_text(
        json.dumps(regression_candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "signal_rows": signal_rows,
        "summary": summary,
        "regression_candidates": regression_candidates,
        "signal_log_path": str(THIRD_REAL_SIGNAL_LOG_PATH),
        "summary_path": str(THIRD_REAL_SUMMARY_PATH),
        "regression_candidates_path": str(THIRD_REAL_REGRESSION_CANDIDATES_PATH),
    }


def run_first_real_qqq_ideal_replay():
    fixture = _load_json(FIRST_REAL_QQQ_IDEAL_FIXTURE_PATH)
    validate_lifecycle_fixture(fixture)

    signal_rows = [
        row["expected_output_shape"] for row in fixture["lifecycle_rows"]
    ]
    summary = build_lifecycle_summary(signal_rows)
    regression_candidates = _build_first_real_qqq_ideal_regression_candidates(
        signal_rows
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_signal_log(FIRST_REAL_QQQ_IDEAL_SIGNAL_LOG_PATH, signal_rows)
    FIRST_REAL_QQQ_IDEAL_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    FIRST_REAL_QQQ_IDEAL_REGRESSION_CANDIDATES_PATH.write_text(
        json.dumps(regression_candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "signal_rows": signal_rows,
        "summary": summary,
        "regression_candidates": regression_candidates,
        "signal_log_path": str(FIRST_REAL_QQQ_IDEAL_SIGNAL_LOG_PATH),
        "summary_path": str(FIRST_REAL_QQQ_IDEAL_SUMMARY_PATH),
        "regression_candidates_path": str(
            FIRST_REAL_QQQ_IDEAL_REGRESSION_CANDIDATES_PATH
        ),
    }


def run_first_real_qqq_clean_fast_break_replay():
    fixture = _load_json(FIRST_REAL_QQQ_CLEAN_FAST_BREAK_FIXTURE_PATH)
    validate_lifecycle_fixture(fixture)

    signal_rows = [
        row["expected_output_shape"] for row in fixture["lifecycle_rows"]
    ]
    summary = build_lifecycle_summary(signal_rows)
    regression_candidates = (
        _build_first_real_qqq_clean_fast_break_regression_candidates(signal_rows)
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _write_signal_log(FIRST_REAL_QQQ_CLEAN_FAST_BREAK_SIGNAL_LOG_PATH, signal_rows)
    FIRST_REAL_QQQ_CLEAN_FAST_BREAK_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    FIRST_REAL_QQQ_CLEAN_FAST_BREAK_REGRESSION_CANDIDATES_PATH.write_text(
        json.dumps(regression_candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "signal_rows": signal_rows,
        "summary": summary,
        "regression_candidates": regression_candidates,
        "signal_log_path": str(FIRST_REAL_QQQ_CLEAN_FAST_BREAK_SIGNAL_LOG_PATH),
        "summary_path": str(FIRST_REAL_QQQ_CLEAN_FAST_BREAK_SUMMARY_PATH),
        "regression_candidates_path": str(
            FIRST_REAL_QQQ_CLEAN_FAST_BREAK_REGRESSION_CANDIDATES_PATH
        ),
    }


def main():
    result = run_signal_replay()
    lifecycle_result = run_lifecycle_signal_replay()
    repeated_state_result = run_repeated_state_signal_replay()
    first_real_result = run_first_real_spy_continuation_replay()
    second_real_result = run_second_real_spy_ideal_replay()
    third_real_result = run_third_real_spy_clean_fast_break_replay()
    first_real_qqq_ideal_result = run_first_real_qqq_ideal_replay()
    first_real_qqq_clean_fast_break_result = (
        run_first_real_qqq_clean_fast_break_replay()
    )
    print("Historical Signal Replay v1 complete")
    print("Signal/stage replay only")
    print("No trade outcome / no P&L / no account sizing / no auto-trading")
    print("Lifecycle replay complete")
    print("Repeated-state duplicate suppression replay complete")
    print("First-real SPY Continuation replay complete")
    print("Second-real SPY Ideal replay complete")
    print("Third-real SPY Clean Fast Break replay complete")
    print("First-real QQQ Ideal replay complete")
    print("First-real QQQ Clean Fast Break replay complete")
    print(f"Signal log: {result['signal_log_path']}")
    print(f"Summary: {result['summary_path']}")
    print(f"Regression candidates: {result['regression_candidates_path']}")
    print(f"Lifecycle signal log: {lifecycle_result['signal_log_path']}")
    print(f"Lifecycle summary: {lifecycle_result['summary_path']}")
    print(
        "Lifecycle regression candidates: "
        f"{lifecycle_result['regression_candidates_path']}"
    )
    print(f"Repeated-state signal log: {repeated_state_result['signal_log_path']}")
    print(f"Repeated-state summary: {repeated_state_result['summary_path']}")
    print(
        "Repeated-state regression candidates: "
        f"{repeated_state_result['regression_candidates_path']}"
    )
    print(f"First-real signal log: {first_real_result['signal_log_path']}")
    print(f"First-real summary: {first_real_result['summary_path']}")
    print(
        "First-real regression candidates: "
        f"{first_real_result['regression_candidates_path']}"
    )
    print(f"Second-real signal log: {second_real_result['signal_log_path']}")
    print(f"Second-real summary: {second_real_result['summary_path']}")
    print(
        "Second-real regression candidates: "
        f"{second_real_result['regression_candidates_path']}"
    )
    print(f"Third-real signal log: {third_real_result['signal_log_path']}")
    print(f"Third-real summary: {third_real_result['summary_path']}")
    print(
        "Third-real regression candidates: "
        f"{third_real_result['regression_candidates_path']}"
    )
    print(
        "First-real QQQ Ideal signal log: "
        f"{first_real_qqq_ideal_result['signal_log_path']}"
    )
    print(
        "First-real QQQ Ideal summary: "
        f"{first_real_qqq_ideal_result['summary_path']}"
    )
    print(
        "First-real QQQ Ideal regression candidates: "
        f"{first_real_qqq_ideal_result['regression_candidates_path']}"
    )
    print(
        "First-real QQQ Clean Fast Break signal log: "
        f"{first_real_qqq_clean_fast_break_result['signal_log_path']}"
    )
    print(
        "First-real QQQ Clean Fast Break summary: "
        f"{first_real_qqq_clean_fast_break_result['summary_path']}"
    )
    print(
        "First-real QQQ Clean Fast Break regression candidates: "
        f"{first_real_qqq_clean_fast_break_result['regression_candidates_path']}"
    )


if __name__ == "__main__":
    main()
