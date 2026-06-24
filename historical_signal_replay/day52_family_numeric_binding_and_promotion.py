import json
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day52_full_session_recognition_manifest
from historical_signal_replay import day52_numeric_trigger_invalidation


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_family_numeric_binding_and_promotion.json"
)
RESULT_DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY52_FAMILY_NUMERIC_BINDING_AND_PROMOTION_RESULT.md"

RESULT_VERSION = "day52_family_numeric_binding_and_promotion_v1"
IMPLEMENTATION_VERSION = "day52_family_numeric_binding_and_promotion_impl_v1"
TASK_FILENAME = "SAFE_FAST_DAY52_FAMILY_NUMERIC_BINDING_AND_PROMOTION_CODEX_TASK.md"


def build_family_numeric_binding_and_promotion_document(*, source_commit=None, run_timestamp=None):
    run_timestamp = run_timestamp or _utc_now()
    numeric = day52_numeric_trigger_invalidation.build_numeric_trigger_invalidation_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    manifest = day52_full_session_recognition_manifest.build_manifest_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    session = manifest["sessions"][0]
    accounting = manifest["complete_session_accounting"]
    return {
        "result_version": RESULT_VERSION,
        "implementation_version": IMPLEMENTATION_VERSION,
        "source_commit": source_commit or day52_numeric_trigger_invalidation._git_short_head(),
        "run_timestamp": run_timestamp,
        "task": TASK_FILENAME,
        "scope": {
            "symbol": "SPY",
            "session_date": "2026-03-16",
            "layer": "accepted_underlying_recognition_only",
            "option_contract_selection": False,
            "entry_exit_costs_or_net_result": False,
            "profitability_proof": "NO",
            "paper_live_eligibility": "NO",
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "broker_account_order_fill_alert_touched": False,
            "credentials_or_env_changed": False,
            "sizing_changed": False,
            "frozen_patch8_thresholds_changed": False,
        },
        "binding_audit_result": "LEGITIMATE_SHARED_SETUP_TIME_ROW",
        "binding_audit": numeric["binding_audit"],
        "family_decision_matrix": numeric["family_decision_matrix"],
        "accepted_numeric_summary": numeric["summary"],
        "accepted_mode_full_session_counts": {
            "counts_by_setup_family_and_final_disposition": session[
                "counts_by_setup_family_and_final_disposition"
            ],
            "stage_transition_summary": session["stage_transition_summary"],
            "winner_selection": session["winner_selection"],
            "complete_session_accounting": accounting,
        },
        "separation_from_provisional_mode": {
            "accepted_result_path": "historical_signal_replay/results/day52_numeric_trigger_invalidation.json",
            "accepted_manifest_path": "historical_signal_replay/results/day52_full_session_recognition_manifest.json",
            "provisional_result_path": "historical_signal_replay/results/day52_replay_only_numeric_rule_candidates.json",
            "accepted_and_provisional_modes_remain_separate": True,
        },
        "guardrails": {
            "future_rows_used": False,
            "post_cutoff_mutation_influenced_values": False,
            "opra_downloaded": False,
            "option_selection_performed": False,
            "trade_candidate_created": False,
            "selected_contract_created": False,
            "entry_or_exit_recorded": False,
            "pnl_calculated": False,
            "profitability_claimed": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "remaining_blockers": [
            "selected_contract_option_evidence_missing",
            "opra_definition_quote_trade_statistics_evidence_missing",
            "entry_exit_costs_net_result_missing",
            "profitability_proof_missing",
            "paper_live_eligibility_missing",
        ],
    }


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_family_numeric_binding_and_promotion_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    day52_numeric_trigger_invalidation.write_outputs(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    day52_full_session_recognition_manifest.write_outputs(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    return document


def _markdown_result(document):
    decisions = "\n".join(
        (
            f"- {item['family']}: `{item['decision']}`, trigger `{item['trigger']}`, "
            f"invalidation `{item['invalidation']}`, setup `{item['setup_time_timestamp']}`, "
            f"source row `{item['source_row_index']}`."
        )
        for item in document["family_decision_matrix"]
    )
    counts = document["accepted_mode_full_session_counts"]["complete_session_accounting"]
    return f"""# SAFE-FAST Day 52 Family Numeric Binding and Promotion Result

## Binding Audit

Result: `{document['binding_audit_result']}`. Ideal, Clean Fast Break, and Continuation are separate accepted mapper packages that intentionally bind to the same publisher-collapsed setup-time decision row.

## Family Decisions

{decisions}

## Accepted-Mode Counts

- Sessions scanned: `{counts['sessions_scanned']}`.
- Rows scanned: `{counts['rows_scanned']}`.
- Recognition records: `{counts['recognition_records']}`.
- Setup-qualified layer-1 records: `{counts['setup_qualified_records']}`.
- Selected winner records: `{counts['selected_winner_records']}`.
- Suppressed records: `{counts['suppressed_records']}`.
- Trade candidates: `0`; selected contracts: `0`; eligible entries: `0`; recorded entries: `0`.

## Guardrails

No OPRA download, option selection, entry, exit, P&L, proof, profitability, paper/live eligibility, `main.py`, Railway/deploy, broker/account/order/fill/alert, credential, `.env`, sizing, or frozen `patch8` threshold change was made.
"""


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    doc = write_outputs()
    counts = doc["accepted_mode_full_session_counts"]["complete_session_accounting"]
    print(
        "wrote day52 family numeric binding and promotion: "
        f"{counts['setup_qualified_records']} setup-qualified layer-1 records, "
        f"{counts['selected_winner_records']} selected winner, "
        f"{counts['trade_candidates']} trade candidates"
    )
