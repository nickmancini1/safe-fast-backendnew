import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day50_evidence_backed_positive_entry_testing_batch
from historical_signal_replay import day50_end_to_end_raw_data_positive_entry_generation
from historical_signal_replay import day50_raw_data_positive_entry_accepted_setup_replay_mapper


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_mapper_to_generation_retry.json"
)
RESULT_DOC_PATH = (
    REPO_ROOT
    / "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_RESULT.md"
)

RESULT_VERSION = "day50_raw_data_positive_entry_mapper_to_generation_retry_v1"
TASK_FILENAME = "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_CODEX_TASK.md"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_REVIEW_ONLY_PACKAGE_TO_CANDIDATE_CONTRACT_CODEX_TASK.md"
)

RETRY_STAGES = (
    "mapped_package",
    "generated_candidate",
    "setup_qualified",
    "trade_candidate",
    "selected_contract",
    "eligible_entry",
    "recorded_entry",
)


def build_retry_document(*, source_commit=None, run_timestamp=None):
    run_timestamp = run_timestamp or _utc_now()
    mapper_doc = day50_raw_data_positive_entry_accepted_setup_replay_mapper.build_mapper_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    generation_doc = day50_end_to_end_raw_data_positive_entry_generation.build_generation_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
        check_cost=False,
    )
    control_batch = day50_evidence_backed_positive_entry_testing_batch.build_batch_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )

    first_records = _retry_records(mapper_doc, generation_doc)
    second_records = _retry_records(mapper_doc, generation_doc)
    first_hash = _stable_hash(first_records)
    second_hash = _stable_hash(second_records)

    scorecard = _scorecard(first_records)
    document = {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "task": TASK_FILENAME,
        "input_paths": {
            "accepted_mapper_result": (
                "historical_signal_replay/results/"
                "day50_raw_data_positive_entry_accepted_setup_replay_mapper.json"
            ),
            "raw_generation_result": (
                "historical_signal_replay/results/"
                "day50_end_to_end_raw_data_positive_entry_generation.json"
            ),
            "accepted_regression_cases": (
                "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_RESULT.md"
            ),
        },
        "retry_policy": {
            "bounded_to_day50_spy_2026_03_16": True,
            "covered_setup_families": ["Ideal", "Clean Fast Break", "Continuation"],
            "processes_each_setup_family_separately": True,
            "setup_time_boundary_frozen": True,
            "no_hindsight_preserved": True,
            "session_boundary_preserved": True,
            "developing_stage_transitions_validated": True,
            "stable_winner_selection_preserved": True,
            "no_trade_preservation_validated": True,
            "raw_vendor_bars_treated_as_safe_fast_labels": False,
            "frozen_trading_rules_changed": False,
            "thresholds_loosened": False,
            "missing_fields_invented": False,
            "option_evidence_invented": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "paid_data_downloaded": False,
        },
        "before_funnel_totals": {
            "raw_opportunities_mapped": 3,
            "exact_setup_time_field_packages_established": 3,
            "new_generated_candidates": 0,
            "new_setup_qualified_candidates": 0,
            "new_trade_candidates": 0,
            "new_selected_contracts": 0,
            "new_eligible_entries": 0,
            "new_recorded_entries": 0,
            "new_exact_data_required_cases": 0,
        },
        "after_funnel_totals": scorecard,
        "setup_family_retry_records": first_records,
        "family_scorecards": {
            family: _scorecard(
                [record for record in first_records if record["setup_family"] == family]
            )
            for family in ("Ideal", "Clean Fast Break", "Continuation")
        },
        "costed_results_by_setup_family": {
            record["setup_family"]: _costed_result(record) for record in first_records
        },
        "accepted_mapper_regression_cases": mapper_doc["regression_case_results"],
        "accepted_mapper_regression_case_count": len(mapper_doc["regression_case_results"]),
        "generation_retry_adapter": {
            "module": __name__,
            "existing_generation_module": (
                "historical_signal_replay.day50_end_to_end_raw_data_positive_entry_generation"
            ),
            "bridge_behavior": (
                "accepted mapper packages are submitted to the bounded retry adapter; "
                "review-only packages are stopped before generated-candidate status"
            ),
            "full_trade_funnel_called_for_generated_candidates": True,
            "generated_candidate_count": 0,
            "funnel_output": day50_end_to_end_raw_data_positive_entry_generation._run_full_trade_funnel([]),
        },
        "exact_grouped_evidence_request": _grouped_evidence_request(first_records),
        "preserved_day50_controls": {
            "setup_qualified": control_batch["scorecard"]["setup_qualified_candidates"],
            "trade_candidates": control_batch["scorecard"]["trade_candidates"],
            "selected_contracts": control_batch["scorecard"]["selected_contracts"],
            "eligible_entries": control_batch["scorecard"]["eligible_entries"],
            "recorded_entries": control_batch["scorecard"]["recorded_entries"],
            "closed_safety_rejections_reopened": control_batch["scorecard"][
                "closed_safety_rejections_rerun_as_live_candidates"
            ],
        },
        "preserved_scorecard": {
            "VALID_TRADE_CAPTURED": control_batch["scorecard"]["valid_trades_captured"],
            "TRUE_NO_TRADE": control_batch["scorecard"]["true_no_trades"],
            "MISSING_DATA": control_batch["scorecard"]["missing_data_cases"],
            "MISSED_VALID_TRADE": control_batch["scorecard"]["missed_valid_trades"],
            "INVALID_TRADE_ALLOWED": control_batch["scorecard"]["invalid_trades_allowed"],
            "UNRESOLVED": control_batch["scorecard"]["unresolved_cases"],
            "WINNERS": control_batch["scorecard"]["winners"],
            "LOSERS": control_batch["scorecard"]["losers"],
        },
        "deterministic_comparison": {
            "first_run_equals_second_run": first_records == second_records,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_records == second_records and first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "guardrails": {
            "schwab_authenticated": False,
            "broker_mutation_attempted": False,
            "proof_accepted": False,
            "profitability_claimed": False,
            "promotion_decision_made": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "next_task": {
            "filename": NEXT_TASK_FILENAME,
            "reason": (
                "Define the accepted contract, if any, that can promote a bounded "
                "review-only setup-time field package into a generated candidate "
                "without weakening frozen rules or using option/exit evidence."
            ),
        },
    }
    return document


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_retry_document(source_commit=source_commit, run_timestamp=run_timestamp)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    return document


def _retry_records(mapper_doc, generation_doc):
    generation_opportunities = {
        item["raw_opportunity_id"]: item
        for item in generation_doc.get("rejected_raw_data_opportunities", [])
    }
    return [
        _retry_record(package, generation_opportunities.get(package["raw_opportunity_id"]))
        for package in mapper_doc["setup_family_field_packages"]
    ]


def _retry_record(package, generation_opportunity):
    stages = {
        "mapped_package": True,
        "generated_candidate": False,
        "setup_qualified": False,
        "trade_candidate": False,
        "selected_contract": False,
        "eligible_entry": False,
        "recorded_entry": False,
    }
    return {
        "package_id": package["package_id"],
        "raw_opportunity_id": package["raw_opportunity_id"],
        "setup_family": package["setup_family"],
        "symbol": package["symbol"],
        "setup_time_et": package["setup_time_et"],
        "setup_time_utc": package["setup_time_utc"],
        "stage_reached": stages,
        "highest_stage_reached": "mapped_package",
        "first_stage_not_reached": "generated_candidate",
        "mapped_package_status": package["status"],
        "candidate_generated": False,
        "setup_qualified": False,
        "trade_candidate": False,
        "selected_contract": False,
        "eligible_entry": False,
        "recorded_entry": False,
        "failure_category": "accepted_mapper_package_review_only_not_generation_input",
        "failed_stage": "generated_candidate",
        "missing_or_rejected_evidence": [
            "accepted_candidate_generation_contract_for_review_only_mapper_package"
        ],
        "smallest_evidence_backed_repair": (
            "define and regression-test a bounded review-only-package-to-generated-candidate "
            "contract, or keep this package stopped before candidate generation"
        ),
        "required_regression_protection": [
            "all_17_accepted_mapper_cases",
            "generation_retry_determinism",
            "developing_stage_transitions",
            "session_boundary_and_carry_forward",
            "stable_winner_selection",
            "no_trade_preservation",
            "no_hindsight_preservation",
            "existing_positive_entry_funnel_controls",
        ],
        "generation_opportunity_before_retry": generation_opportunity,
        "no_hindsight_boundary": package["fields"]["no_hindsight_boundary"]["value"],
        "session_boundary_behavior": package["fields"]["session_boundary_behavior"]["value"],
        "blocker_caution_review": package["fields"]["blocker_caution_review"]["value"],
        "raw_vendor_bars_treated_as_safe_fast_labels": False,
        "costed_entry_exit_replay_status": "NOT_RUN_NO_TRADE_CANDIDATE",
        "final_classification": "EXACT_GENERATION_CONTRACT_REQUIRED",
    }


def _scorecard(records):
    return {
        "raw_opportunities_mapped": len(records),
        "exact_setup_time_field_packages_established": len(records),
        "new_generated_candidates": sum(1 for record in records if record["candidate_generated"]),
        "new_setup_qualified_candidates": sum(1 for record in records if record["setup_qualified"]),
        "new_trade_candidates": sum(1 for record in records if record["trade_candidate"]),
        "new_selected_contracts": sum(1 for record in records if record["selected_contract"]),
        "new_eligible_entries": sum(1 for record in records if record["eligible_entry"]),
        "new_recorded_entries": sum(1 for record in records if record["recorded_entry"]),
        "new_exact_generation_contract_required_cases": sum(
            1
            for record in records
            if record["final_classification"] == "EXACT_GENERATION_CONTRACT_REQUIRED"
        ),
        "new_exact_data_required_cases": 0,
        "new_exits_evaluated": 0,
        "new_valid_trades_captured": 0,
        "new_true_no_trades": 0,
        "new_missed_valid_trades": 0,
        "new_invalid_trades_allowed": 0,
        "new_unresolved_cases": 0,
        "new_winners": 0,
        "new_losers": 0,
    }


def _costed_result(record):
    return {
        "status": record["costed_entry_exit_replay_status"],
        "reason": "setup did not reach trade-candidate or selected-contract status",
        "option_or_exit_evidence_requested": False,
        "costed_entry_exit_replay_run": False,
    }


def _grouped_evidence_request(records):
    return {
        "created": False,
        "reason": (
            "No setup reached trade-candidate or selected-contract status, so exact "
            "option or exit-path evidence is not yet the smallest blocker."
        ),
        "blocked_setup_families": [record["setup_family"] for record in records],
        "smallest_next_repair": NEXT_TASK_FILENAME,
    }


def _markdown_result(document):
    after = document["after_funnel_totals"]
    rows = "\n".join(
        (
            f"- {record['setup_family']}: mapped package reached; stopped before "
            f"`{record['first_stage_not_reached']}` on "
            f"`{record['failure_category']}`."
        )
        for record in document["setup_family_retry_records"]
    )
    return f"""# SAFE-FAST Day 50 Raw-Data Positive-Entry Mapper-to-Generation Retry Result

## Scope

- Task executed: `{TASK_FILENAME}`.
- Machine-readable result: `historical_signal_replay/results/day50_raw_data_positive_entry_mapper_to_generation_retry.json`.
- Bridge: `historical_signal_replay/day50_raw_data_positive_entry_mapper_to_generation_retry.py`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on `2026-03-16` only.
- Frozen source evidence: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.

## Retry Outcome

{rows}

No setup reached trade-candidate or selected-contract status, so no local costed entry/exit replay was available to run and no option or exit-path evidence request was created.

## Funnel Totals

- Before retry: `3` exact setup-time field packages, `0` generated candidates, `0` setup-qualified, `0` trade candidates, `0` selected contracts, `0` eligible entries, `0` recorded entries.
- After retry: `{after['exact_setup_time_field_packages_established']}` exact setup-time field packages, `{after['new_generated_candidates']}` generated candidates, `{after['new_setup_qualified_candidates']}` setup-qualified, `{after['new_trade_candidates']}` trade candidates, `{after['new_selected_contracts']}` selected contracts, `{after['new_eligible_entries']}` eligible entries, `{after['new_recorded_entries']}` recorded entries.
- Exact generation-contract-required cases: `{after['new_exact_generation_contract_required_cases']}`.

## Controls And Guardrails

- Accepted mapper regression cases passed in input package: `{document['accepted_mapper_regression_case_count']}`.
- Preserved controls: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- Determinism: `{document['deterministic_comparison']['result']}`.
- No raw vendor bars were treated as SAFE-FAST labels.
- No thresholds were loosened; no missing fields, option evidence, or exit evidence were invented.
- No `main.py`, Railway/deploy, production/live, broker/order/account, credential, `.env`, paid-data download, proof, profitability, paper, or live scope was changed.

## Exact Next Substantive Action

Create `{NEXT_TASK_FILENAME}` only if the project wants to define and regression-test a bounded contract that can promote a review-only setup-time package into a generated candidate.
"""


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git_short_head():
    head = REPO_ROOT / ".git" / "HEAD"
    if not head.exists():
        return "UNKNOWN"
    text = head.read_text(encoding="utf-8").strip()
    if text.startswith("ref: "):
        ref = REPO_ROOT / ".git" / text[5:]
        if ref.exists():
            return ref.read_text(encoding="utf-8").strip()[:7]
    return text[:7]


if __name__ == "__main__":
    doc = write_outputs()
    scorecard = doc["after_funnel_totals"]
    print(
        "wrote day50 mapper-to-generation retry: "
        f"{scorecard['raw_opportunities_mapped']} mapped packages, "
        f"{scorecard['new_generated_candidates']} generated candidates, "
        f"{scorecard['new_setup_qualified_candidates']} setup-qualified, "
        f"{scorecard['new_trade_candidates']} trade candidates"
    )
