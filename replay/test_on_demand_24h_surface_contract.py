from pathlib import Path

text = Path("main.py").read_text(encoding="utf-8")

checks = {
    "24h_caution_key_exists": "twentyfour_hour_countertrend" in text,
    "caution_items_returned": '"caution_items": caution_items' in text,
    "caution_items_used_after_checklist": text.count("caution_items") >= 5,
    "countertrend_human_text_exists": "24H countertrend" in text or "countertrend caution" in text,
}

for name, ok in checks.items():
    print(f"{name}: {'PASS' if ok else 'FAIL'}")

if not all(checks.values()):
    print("24H SURFACE CONTRACT FAIL")
    raise SystemExit(2)

print("24H SURFACE CONTRACT PASS")
