from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_PATH = (
    ROOT
    / "historical_signal_replay"
    / "source_data"
    / "richer_export_package_work"
    / "day48_continuation_qqq_spy_option_context_request_manifest.json"
)

ALLOWED_REQUEST_CANDIDATES = {
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
}
REQUIRED_CONTROL_CANDIDATES = {
    "GLD-REAL-HISTORICAL-CONTINUATION-001",
    "IWM-REAL-HISTORICAL-CONTINUATION-001",
}
FORBIDDEN_KEY_FRAGMENTS = {
    "account",
    "api_key",
    "broker",
    "credential",
    "env",
    "fill",
    "live",
    "order",
    "password",
    "pnl",
    "profitability_label",
    "readiness_label",
    "secret",
    "token",
}
REQUIRED_REQUEST_FIELDS = {
    "candidate_id",
    "conditional_exit_path_window",
    "dataset",
    "decision_answered",
    "end_timestamp",
    "end_timestamp_utc",
    "expected_consumer",
    "missing_data_behavior",
    "request_id",
    "required_fields",
    "schema",
    "setup_time_window",
    "signal_timestamp",
    "signal_timestamp_utc",
    "start_timestamp",
    "start_timestamp_utc",
    "symbol_type",
    "timezone",
    "underlying",
    "why_narrower_request_is_insufficient",
}


def load_manifest(path: Path = DEFAULT_MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    package = manifest if manifest is not None else load_manifest()
    problems: list[str] = []

    if package.get("schema_version") != (
        "safe-fast-day48-continuation-option-context-request-package-v1"
    ):
        problems.append("schema_version is not the Day 48 request package schema")

    requests = package.get("requests")
    if not isinstance(requests, list) or not requests:
        problems.append("requests must be a non-empty list")
        requests = []

    frozen_candidates = package.get("frozen_candidates")
    if not isinstance(frozen_candidates, list):
        problems.append("frozen_candidates must be a list")
        frozen_candidates = []

    frozen_ids = {candidate.get("candidate_id") for candidate in frozen_candidates}
    if frozen_ids != ALLOWED_REQUEST_CANDIDATES:
        problems.append(f"frozen candidate ids are not exact QQQ/SPY set: {frozen_ids}")

    for candidate in frozen_candidates:
        _validate_frozen_candidate(candidate, problems)

    control_ids = {
        control.get("candidate_id")
        for control in package.get("controls_retained", [])
    }
    if control_ids != REQUIRED_CONTROL_CANDIDATES:
        problems.append(f"control ids are not exact GLD/IWM set: {control_ids}")
    for control in package.get("controls_retained", []):
        if control.get("request_included") is not False:
            problems.append(f"{control.get('candidate_id')} control is request-included")

    for request in requests:
        _validate_request(request, problems)

    requested_ids = {request.get("candidate_id") for request in requests}
    if not requested_ids <= ALLOWED_REQUEST_CANDIDATES:
        problems.append(f"requests include non-frozen candidates: {requested_ids}")
    if requested_ids & REQUIRED_CONTROL_CANDIDATES:
        problems.append("GLD/IWM controls are included in requests")

    not_requested_ids = {
        item.get("candidate_id") for item in package.get("not_requested", [])
    }
    if not REQUIRED_CONTROL_CANDIDATES <= not_requested_ids:
        problems.append("GLD/IWM controls are missing from not_requested")

    forbidden_paths = _find_forbidden_key_paths(package)
    if forbidden_paths:
        problems.append(f"forbidden key paths present: {forbidden_paths}")

    cost_check = package.get("cost_check", {})
    if cost_check.get("download_authorized") is not False:
        problems.append("cost_check.download_authorized must be false")
    if cost_check.get("purchase_approval_inferred") is not False:
        problems.append("purchase approval must not be inferred")

    for flag in (
        "proof_accepted",
        "profitability_claimed",
        "candidate_marked_ready",
        "intake_ready_count_changed",
    ):
        if package.get(flag) is not False:
            problems.append(f"{flag} must be false")

    return {
        "status": "pass" if not problems else "fail",
        "problem_count": len(problems),
        "problems": problems,
        "request_count": len(requests),
        "requested_candidate_ids": sorted(requested_ids),
        "control_candidate_ids": sorted(control_ids),
    }


def _validate_frozen_candidate(candidate: dict[str, Any], problems: list[str]) -> None:
    candidate_id = candidate.get("candidate_id")
    if candidate.get("setup_type") != "Continuation":
        problems.append(f"{candidate_id} setup_type is not Continuation")
    if candidate.get("direction") != "long_call":
        problems.append(f"{candidate_id} direction is not long_call")
    _parse_tz(candidate.get("signal_timestamp"), f"{candidate_id}.signal_timestamp", problems)
    _parse_tz(
        candidate.get("signal_timestamp_utc"),
        f"{candidate_id}.signal_timestamp_utc",
        problems,
    )

    source_ids = candidate.get("source_row_identifiers", {})
    if not source_ids.get("source_csv") or not source_ids.get("source_csv_line"):
        problems.append(f"{candidate_id} source row identifiers are incomplete")

    abstention = candidate.get("contract_selection_current_abstention", {})
    if abstention.get("status") != "abstain":
        problems.append(f"{candidate_id} current contract status is not abstain")
    if not abstention.get("reason"):
        problems.append(f"{candidate_id} current abstention reason is missing")

    if not candidate.get("exact_missing_execution_fields"):
        problems.append(f"{candidate_id} exact missing execution fields are missing")
    if not candidate.get("exact_missing_context_caution_fields"):
        problems.append(f"{candidate_id} exact missing context/caution fields are missing")

    evidence = candidate.get("local_evidence_review", {})
    for field in (
        "available_locally",
        "present_but_unusable",
        "missing",
        "contradictory",
        "outside_permitted_timestamp_window",
    ):
        if field not in evidence:
            problems.append(f"{candidate_id} local evidence review missing {field}")


def _validate_request(request: dict[str, Any], problems: list[str]) -> None:
    missing_fields = REQUIRED_REQUEST_FIELDS - set(request)
    if missing_fields:
        problems.append(f"{request.get('request_id')} missing fields: {sorted(missing_fields)}")

    candidate_id = request.get("candidate_id")
    if candidate_id not in ALLOWED_REQUEST_CANDIDATES:
        problems.append(f"{request.get('request_id')} candidate is not frozen QQQ/SPY")

    if request.get("dataset") != "OPRA.PILLAR":
        problems.append(f"{request.get('request_id')} dataset is not OPRA.PILLAR")
    if request.get("schema") not in {"tcbbo", "trades", "statistics", "definition"}:
        problems.append(f"{request.get('request_id')} schema is unsupported")
    if request.get("symbol_type") not in {"raw_symbol", "parent", "instrument_id"}:
        problems.append(f"{request.get('request_id')} symbol_type is unsupported")

    start = _parse_tz(request.get("start_timestamp"), "start_timestamp", problems)
    end = _parse_tz(request.get("end_timestamp"), "end_timestamp", problems)
    signal = _parse_tz(request.get("signal_timestamp"), "signal_timestamp", problems)
    start_utc = _parse_tz(request.get("start_timestamp_utc"), "start_timestamp_utc", problems)
    end_utc = _parse_tz(request.get("end_timestamp_utc"), "end_timestamp_utc", problems)
    signal_utc = _parse_tz(
        request.get("signal_timestamp_utc"),
        "signal_timestamp_utc",
        problems,
    )
    if start and end and signal and not (start <= end <= signal):
        problems.append(f"{request.get('request_id')} local timestamps are not chronological")
    if start_utc and end_utc and signal_utc and not (start_utc <= end_utc <= signal_utc):
        problems.append(f"{request.get('request_id')} UTC timestamps are not chronological")

    setup_window = request.get("setup_time_window")
    if not isinstance(setup_window, dict):
        problems.append(f"{request.get('request_id')} setup_time_window must be an object")
    elif setup_window.get("start") != request.get("start_timestamp") or setup_window.get(
        "end"
    ) != request.get("end_timestamp"):
        problems.append(f"{request.get('request_id')} setup window disagrees with request")

    if request.get("conditional_exit_path_window") is not None:
        problems.append(
            f"{request.get('request_id')} has conditional exit window before valid entry"
        )

    if not request.get("required_fields"):
        problems.append(f"{request.get('request_id')} required_fields is empty")
    if "selector" not in request.get("expected_consumer", "") and "contract" not in request.get(
        "expected_consumer", ""
    ):
        problems.append(f"{request.get('request_id')} expected consumer is not mapped")
    if not request.get("decision_answered"):
        problems.append(f"{request.get('request_id')} decision_answered is missing")


def _parse_tz(value: Any, field_name: str, problems: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value:
        problems.append(f"{field_name} is missing")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        problems.append(f"{field_name} is invalid")
        return None
    if parsed.tzinfo is None:
        problems.append(f"{field_name} is missing timezone")
        return None
    return parsed


def _find_forbidden_key_paths(value: Any, path: tuple[str, ...] = ()) -> list[str]:
    matches: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key).lower()
            nested_path = (*path, str(key))
            if any(fragment in key_text for fragment in FORBIDDEN_KEY_FRAGMENTS):
                allowed = {
                    "profitability_claimed",
                    "proof_accepted",
                    "purchase_approval_inferred",
                }
                if key_text not in allowed:
                    matches.append(".".join(nested_path))
            matches.extend(_find_forbidden_key_paths(nested, nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            matches.extend(_find_forbidden_key_paths(nested, (*path, str(index))))
    return matches


def main() -> int:
    result = validate_manifest()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
