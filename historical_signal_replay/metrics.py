from collections import Counter


def _count_values(rows, key):
    return dict(Counter(row.get(key) for row in rows if row.get(key) is not None))


def _count_cautions(rows):
    counter = Counter()
    for row in rows:
        for caution in row.get("cautions_watchouts", []):
            counter[caution] += 1
    return dict(counter)


def _count_lifecycle_changes(rows):
    counter = Counter()
    for row in rows:
        if row.get("state_changed"):
            counter["state_changed"] += 1
        if row.get("trigger_changed"):
            counter["trigger_changed"] += 1
        if row.get("blocker_changed"):
            counter["blocker_changed"] += 1
    return dict(counter)


def _count_meaningful_alert_candidates(rows):
    return sum(
        1
        for row in rows
        if row.get("state_changed")
        or row.get("trigger_changed")
        or row.get("blocker_changed")
    )


def build_summary(rows):
    return {
        "total_rows": len(rows),
        "symbols": sorted({row["symbol"] for row in rows if row.get("symbol")}),
        "setup_type_counts": _count_values(rows, "setup_type"),
        "final_verdict_counts": _count_values(rows, "final_verdict"),
        "blocker_counts": _count_values(rows, "primary_blocker"),
        "caution_counts": _count_cautions(rows),
        "stage_counts": _count_values(rows, "stage"),
        "lifecycle_change_counts": _count_lifecycle_changes(rows),
    }


def build_lifecycle_summary(rows):
    summary = build_summary(rows)
    summary["duplicate_alert_suppression_key_counts"] = _count_values(
        rows,
        "duplicate_alert_suppression_key",
    )
    summary["meaningful_alert_candidate_count"] = _count_meaningful_alert_candidates(
        rows
    )
    return summary
