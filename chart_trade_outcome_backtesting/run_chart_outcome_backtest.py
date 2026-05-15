from chart_outcome_backtest import run_chart_outcome_backtest


if __name__ == "__main__":
    result = run_chart_outcome_backtest()
    if result.passed:
        print("PASS chart outcome backtest runner")
        print("scaffold_only: false")
        print("outcome_calculation_started: true")
        print("option_pnl_modeled: false")
        print("account_sizing_added: false")
        print("watcher_implementation_started: false")
        print(f"report: {result.report_path}")
        raise SystemExit(0)

    print("FAIL chart outcome backtest runner")
    for error in result.errors:
        print(f"- {error}")
    raise SystemExit(1)
