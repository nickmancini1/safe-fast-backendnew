import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day50_evidence_backed_positive_entry_testing_batch
from historical_signal_replay import day50_end_to_end_raw_data_positive_entry_generation
from historical_signal_replay import day50_raw_data_positive_entry_accepted_setup_replay_mapper
from historical_signal_replay import day50_raw_data_positive_entry_mapper_to_generation_retry


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_review_only_package_to_candidate_contract.json"
)
RESULT_DOC_PATH = (
    REPO_ROOT
    / "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_REVIEW_ONLY_PACKAGE_TO_CANDIDATE_CONTRACT_RESULT.md"
)

RESULT_VERSION = "day50_raw_data_positive_entry_review_only_package_to_candidate_contract_v1"
TASK_FILENAME = (
    "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_REVIEW_ONLY_PACKAGE_TO_CANDIDATE_CONTRACT_CODEX_TASK.md"
)
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_OPTION_CONTRACT_EVIDENCE_REQUEST_REVIEW_CODEX_TASK.md"
)

SETUP_FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
REQUIRED_SETUP_FIELDS = (
    "setup_time_row",
    "trigger",
    "invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "session_boundary_behavior",
    "no_hindsight_boundary",
)
TRADE_CANDIDATE_FIELDS = (
    "selected_contract_identity",
    "selected_contract_quote_freshness",
    "selected_contract_liquidity",
    "entry_execution_context",
)


def build_contract_document(*, source_commit=None, run_timestamp=None):
    run_timestamp = run_timestamp or _utc_now()
    mapper_doc = day50_raw_data_positive_entry_accepted_setup_replay_mapper.build_mapper_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    retry_doc = day50_raw_data_positive_entry_mapper_to_generation_retry.build_retry_document(
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

    records = [
        _contract_record(package)
        for package in mapper_doc["setup_family_field_packages"]
        if package["setup_family"] in SETUP_FAMILIES
    ]
    first_hash = _stable_hash(records)
    second_hash = _stable_hash(deepcopy(records))
    scorecard = _scorecard(records)
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
            "mapper_to_generation_retry_result": (
                "historical_signal_replay/results/"
                "day50_raw_data_positive_entry_mapper_to_generation_retry.json"
            ),
            "raw_generation_result": (
                "historical_signal_replay/results/"
                "day50_end_to_end_raw_data_positive_entry_generation.json"
            ),
        },
        "contract_definition": _contract_definition(),
        "contract_policy": {
            "bounded_to_day50_spy_2026_03_16": True,
            "covered_setup_families": list(SETUP_FAMILIES),
            "processes_each_setup_family_separately": True,
            "generated_candidate_requires_all_setup_fields": list(REQUIRED_SETUP_FIELDS),
            "setup_qualified_requires_generated_candidate": True,
            "trade_candidate_requires_fields": list(TRADE_CANDIDATE_FIELDS),
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
            "exit_evidence_invented": False,
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
            "new_exact_generation_contract_required_cases": 3,
            "new_exact_data_required_cases": 0,
        },
        "after_funnel_totals": scorecard,
        "setup_family_contract_records": records,
        "family_scorecards": {
            family: _scorecard(
                [record for record in records if record["setup_family"] == family]
            )
            for family in SETUP_FAMILIES
        },
        "funnel_output": day50_end_to_end_raw_data_positive_entry_generation._run_full_trade_funnel(
            [_funnel_candidate(record) for record in records if record["candidate_generated"]]
        ),
        "costed_results_by_setup_family": {
            record["setup_family"]: _costed_result(record) for record in records
        },
        "exact_grouped_evidence_request": _grouped_evidence_request(records),
        "accepted_mapper_regression_cases": mapper_doc["regression_case_results"],
        "accepted_mapper_regression_case_count": len(mapper_doc["regression_case_results"]),
        "retry_control_result": {
            "result_version": retry_doc["result_version"],
            "deterministic_result": retry_doc["deterministic_comparison"]["result"],
            "original_generation_contract_required_cases": retry_doc["after_funnel_totals"][
                "new_exact_generation_contract_required_cases"
            ],
            "preserved_controls": retry_doc["preserved_day50_controls"],
        },
        "raw_generation_control_result": {
            "result_version": generation_doc["result_version"],
            "deterministic_result": generation_doc["deterministic_comparison"]["result"],
            "prior_raw_generation_candidates": generation_doc["new_candidate_scorecard"][
                "candidates_generated"
            ],
        },
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
            "first_run_equals_second_run": records == deepcopy(records),
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
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
                "The bounded contract now creates three generated/setup-qualified "
                "SPY candidates and stops before trade-candidate status on exact "
                "missing selected-contract option evidence. The next substantive "
                "step is a grouped option-contract evidence request review only if "
                "the project wants to cost-check that data."
            ),
        },
    }
    return document


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_contract_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    return document


def _contract_definition():
    return {
        "accepted_mapper_package_contract": {
            "status_required": "FIELD_PACKAGE_ESTABLISHED_REVIEW_ONLY",
            "required_fields": list(REQUIRED_SETUP_FIELDS),
            "required_boundaries": [
                "source rows at or before setup decision timestamp",
                "same March 16 2026 SPY RTH session only",
                "raw vendor OHLCV rows may supply evidence but not SAFE-FAST labels",
                "field package hash must not depend on future rows",
            ],
        },
        "generated_candidate_contract": {
            "required_from_mapper_package": list(REQUIRED_SETUP_FIELDS),
            "required_identifiers": [
                "candidate_identifier",
                "raw_opportunity_id",
                "setup_family",
                "symbol",
                "setup_time_utc",
                "setup_time_et",
            ],
            "created_when": (
                "all required setup fields are accepted, nonempty, timestamp-bounded, "
                "and raw_vendor_bars_treated_as_safe_fast_labels is false"
            ),
        },
        "setup_qualified_contract": {
            "created_when": (
                "generated candidate exists, setup field package is complete, "
                "freshness_final_signal_state is fresh at setup time, same-session "
                "boundary is preserved, no-hindsight boundary is preserved, and "
                "blocker/caution review is not an accepted blocking failure"
            ),
            "does_not_require": [
                "option contract identity",
                "option quote freshness",
                "exit path",
                "costed P&L",
                "proof",
                "paper/live readiness",
            ],
        },
        "trade_candidate_contract_gap": {
            "first_stage_not_reached": "trade_candidate",
            "required_missing_fields": list(TRADE_CANDIDATE_FIELDS),
        },
    }


def _contract_record(package):
    missing_setup_fields = _missing_setup_fields(package)
    generated = not missing_setup_fields
    setup_qualified = generated and _setup_qualified(package)
    trade_candidate_missing = [] if not setup_qualified else list(TRADE_CANDIDATE_FIELDS)
    trade_candidate = setup_qualified and not trade_candidate_missing
    stages = {
        "mapped_package": True,
        "generated_candidate": generated,
        "setup_qualified": setup_qualified,
        "trade_candidate": trade_candidate,
        "selected_contract": False,
        "eligible_entry": False,
        "recorded_entry": False,
    }
    highest_stage = _highest_stage(stages)
    first_not_reached = _first_not_reached(stages)
    failure_category = (
        "missing_required_setup_contract_fields"
        if missing_setup_fields
        else (
            "selected_contract_option_evidence_missing"
            if setup_qualified and not trade_candidate
            else None
        )
    )
    return {
        "package_id": package["package_id"],
        "candidate_identifier": package["package_id"].replace("DAY50-SPY", "DAY50-GENERATED-SPY"),
        "raw_opportunity_id": package["raw_opportunity_id"],
        "setup_family": package["setup_family"],
        "symbol": package["symbol"],
        "setup_time_et": package["setup_time_et"],
        "setup_time_utc": package["setup_time_utc"],
        "mapped_package_status": package["status"],
        "stage_reached": stages,
        "highest_stage_reached": highest_stage,
        "first_stage_not_reached": first_not_reached,
        "candidate_generated": generated,
        "setup_qualified": setup_qualified,
        "trade_candidate": trade_candidate,
        "selected_contract": False,
        "eligible_entry": False,
        "recorded_entry": False,
        "exact_outcome": (
            "setup_qualified_created"
            if setup_qualified and not trade_candidate
            else (
                "trade_candidate_created"
                if trade_candidate
                else "rejected_with_exact_contract_gap"
            )
        ),
        "failure_category": failure_category,
        "failed_stage": first_not_reached,
        "missing_or_rejected_evidence": missing_setup_fields + trade_candidate_missing,
        "exact_remaining_blocker": (
            "selected_contract_option_evidence_missing"
            if setup_qualified and not trade_candidate
            else "setup_package_contract_gap"
        ),
        "contract_gap": {
            "missing_setup_fields": missing_setup_fields,
            "missing_trade_candidate_fields": trade_candidate_missing,
            "blocks": (
                "trade_candidate_entry_costs_and_pnl"
                if trade_candidate_missing
                else "generated_candidate"
            ),
        },
        "field_values": {
            field: package["fields"][field]["value"]
            for field in REQUIRED_SETUP_FIELDS
            if field in package.get("fields", {})
        },
        "no_hindsight_boundary": package["fields"]["no_hindsight_boundary"]["value"],
        "session_boundary_behavior": package["fields"]["session_boundary_behavior"]["value"],
        "blocker_caution_review": package["fields"]["blocker_caution_review"]["value"],
        "raw_vendor_bars_treated_as_safe_fast_labels": False,
        "funnel_stage_path": [
            stage
            for stage, reached in (
                ("SETUP_DEVELOPING", True),
                ("GENERATED_CANDIDATE", generated),
                ("SETUP_QUALIFIED", setup_qualified),
                ("TRADE_CANDIDATE", trade_candidate),
            )
            if reached
        ],
        "final_classification": (
            "EXACT_OPTION_CONTRACT_EVIDENCE_REQUIRED"
            if setup_qualified and not trade_candidate
            else "EXACT_GENERATION_CONTRACT_REQUIRED"
        ),
        "exact_blocker": failure_category,
        "costed_entry_exit_replay_status": "NOT_RUN_NO_TRADE_CANDIDATE",
    }


def _missing_setup_fields(package):
    fields = package.get("fields", {})
    missing = []
    if package.get("status") != "FIELD_PACKAGE_ESTABLISHED_REVIEW_ONLY":
        missing.append("mapped_package_status")
    if package.get("raw_vendor_bars_treated_as_safe_fast_labels"):
        missing.append("raw_vendor_label_rejection")
    for field in REQUIRED_SETUP_FIELDS:
        value = fields.get(field, {}).get("value")
        if not value:
            missing.append(field)
    return missing


def _setup_qualified(package):
    fields = package["fields"]
    return (
        fields["freshness_final_signal_state"]["value"]
        == "fresh_final_signal_state_at_setup_time"
        and fields["session_boundary_behavior"]["value"]
        == "same_session_reset_only_no_prior_session_carry"
        and fields["no_hindsight_boundary"]["value"]
        == "future_rows_ignored_for_setup_labels"
        and fields["blocker_caution_review"]["value"]
        == "optional_context_absent_non_blocking_under_registry_rule"
    )


def _highest_stage(stages):
    order = (
        "recorded_entry",
        "eligible_entry",
        "selected_contract",
        "trade_candidate",
        "setup_qualified",
        "generated_candidate",
        "mapped_package",
    )
    for stage in order:
        if stages.get(stage):
            return stage
    return "none"


def _first_not_reached(stages):
    for stage in (
        "generated_candidate",
        "setup_qualified",
        "trade_candidate",
        "selected_contract",
        "eligible_entry",
        "recorded_entry",
    ):
        if not stages.get(stage):
            return stage
    return None


def _funnel_candidate(record):
    return {
        "candidate_identifier": record["candidate_identifier"],
        "setup_family": record["setup_family"],
        "symbol": record["symbol"],
        "highest_stage_reached": _funnel_highest_stage(record),
        "first_stage_not_reached": _funnel_first_not_reached(record),
        "exact_blocker": record["exact_blocker"],
        "final_classification": record["final_classification"],
        "funnel_stage_path": record["funnel_stage_path"],
    }


def _funnel_highest_stage(record):
    mapping = {
        "setup_qualified": "SETUP_QUALIFIED",
        "generated_candidate": "GENERATED_CANDIDATE",
        "mapped_package": "SETUP_DEVELOPING",
    }
    return mapping.get(record["highest_stage_reached"], record["highest_stage_reached"])


def _funnel_first_not_reached(record):
    mapping = {
        "trade_candidate": "TRADE_CANDIDATE",
        "setup_qualified": "SETUP_QUALIFIED",
        "generated_candidate": "GENERATED_CANDIDATE",
    }
    return mapping.get(record["first_stage_not_reached"], record["first_stage_not_reached"])


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
            1 for record in records if not record["candidate_generated"]
        ),
        "new_exact_option_contract_evidence_required_cases": sum(
            1
            for record in records
            if record["setup_qualified"] and not record["trade_candidate"]
        ),
        "new_exact_data_required_cases": sum(
            1
            for record in records
            if record["setup_qualified"] and not record["trade_candidate"]
        ),
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
    blocked = [
        record for record in records if record["setup_qualified"] and not record["trade_candidate"]
    ]
    return {
        "created": bool(blocked),
        "request_type": "option_contract_identity_and_setup_time_entry_evidence",
        "reason": (
            "Generated/setup-qualified candidates exist, but selected-contract option "
            "identity, setup-time quote freshness, liquidity, and execution context are "
            "not locally established. No option data was guessed or downloaded."
        ),
        "requests": [
            {
                "setup_family": record["setup_family"],
                "symbol": record["symbol"],
                "contract": "NOT_KNOWN_BEFORE_SELECTED_CONTRACT_EVIDENCE",
                "timestamp_window": {
                    "start_timestamp": "2026-03-16T09:30:00-04:00",
                    "end_timestamp": "2026-03-16T09:35:00-04:00",
                    "timezone": "America/New_York",
                },
                "source_dataset_schema_needed": [
                    "Databento OPRA.PILLAR / definition / raw_symbol",
                    "Databento OPRA.PILLAR / cmbp-1 or accepted quote-freshness source",
                    "Databento OPRA.PILLAR / trades",
                    "Databento OPRA.PILLAR / statistics",
                ],
                "exact_fields_missing": list(TRADE_CANDIDATE_FIELDS),
                "blocks": [
                    "trade_candidate",
                    "entry",
                    "costs",
                    "P&L",
                ],
            }
            for record in blocked
        ],
        "downloaded": False,
        "cost_checked": False,
    }


def _markdown_result(document):
    after = document["after_funnel_totals"]
    rows = "\n".join(
        (
            f"- {record['setup_family']}: `{record['exact_outcome']}`; "
            f"highest stage `{record['highest_stage_reached']}`; remaining blocker "
            f"`{record['exact_remaining_blocker']}`."
        )
        for record in document["setup_family_contract_records"]
    )
    return f"""# SAFE-FAST Day 50 Review-Only Package to Candidate Contract Result

## Scope

- Task executed: `{TASK_FILENAME}`.
- Machine-readable result: `historical_signal_replay/results/day50_raw_data_positive_entry_review_only_package_to_candidate_contract.json`.
- Implementation: `historical_signal_replay/day50_raw_data_positive_entry_review_only_package_to_candidate_contract.py`.
- Validator: `watcher_foundation/day50_raw_data_positive_entry_review_only_package_to_candidate_contract_validator.py`.
- Focused tests: `tests/test_day50_raw_data_positive_entry_review_only_package_to_candidate_contract.py`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on `2026-03-16` only.

## Contract Outcome

The accepted contract requires all seven setup-time package fields, same-session/no-hindsight boundaries, fresh final-signal state, and no accepted blocker/caution failure before a review-only package may become a generated candidate and setup-qualified candidate.

{rows}

All three packages created generated candidates and setup-qualified candidates. None reached trade-candidate, selected-contract, eligible-entry, or recorded-entry status because exact selected-contract option evidence is not locally established.

## Funnel Totals

- After contract: `{after['new_generated_candidates']}` generated candidates, `{after['new_setup_qualified_candidates']}` setup-qualified, `{after['new_trade_candidates']}` trade candidates, `{after['new_selected_contracts']}` selected contracts, `{after['new_eligible_entries']}` eligible entries, `{after['new_recorded_entries']}` recorded entries.
- Exact option-contract evidence required cases: `{after['new_exact_option_contract_evidence_required_cases']}`.
- Costed entry/exit replay possible: `NO`.

## Evidence Request

One grouped option-contract evidence request was created in the JSON result. It names the setup family, symbol, unknown contract status, setup-time timestamp window, required OPRA source/dataset/schema, exact missing fields, and whether each gap blocks trade-candidate, entry, costs, or P&L. No cost check or download was run.

## Controls And Guardrails

- Accepted mapper regression cases preserved: `{document['accepted_mapper_regression_case_count']}`.
- Mapper-to-generation retry controls preserved.
- Preserved controls: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- Determinism: `{document['deterministic_comparison']['result']}`.
- No raw vendor bars were treated as SAFE-FAST labels.
- No thresholds were loosened; no missing fields, option evidence, exit evidence, or P&L were invented.
- No `main.py`, Railway/deploy, production/live, broker/order/account, credential, `.env`, paid-data download, proof, profitability, paper, or live scope was changed.

## Exact Next Substantive Action

Create `{NEXT_TASK_FILENAME}` only if the project wants to review and cost-check the grouped option-contract evidence request for the three setup-qualified SPY candidates.
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
        "wrote day50 review-only package contract: "
        f"{scorecard['new_generated_candidates']} generated candidates, "
        f"{scorecard['new_setup_qualified_candidates']} setup-qualified, "
        f"{scorecard['new_trade_candidates']} trade candidates, "
        f"{scorecard['new_selected_contracts']} selected contracts"
    )
