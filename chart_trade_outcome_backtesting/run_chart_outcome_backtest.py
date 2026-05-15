from chart_outcome_backtest import run_scaffold


if __name__ == "__main__":
    result = run_scaffold()
    if result.passed:
        print("PASS chart outcome backtest runner scaffold")
        print("scaffold_only: true")
        print("outcome_calculation_started: false")
        print("option_pnl_modeled: false")
        print("account_sizing_added: false")
        print("watcher_implementation_started: false")
        print(f"report: {result.report_path}")
        raise SystemExit(0)

    print("FAIL chart outcome backtest runner scaffold")
    for error in result.errors:
        print(f"- {error}")
    raise SystemExit(1)
