from historical_signal_replay import cfb_trade_rule_checker


class CfbBacktestPrepHarnessError(ValueError):
    """Base error for non-running CFB backtest-prep harness failures."""


class BacktestRunNotAuthorizedError(CfbBacktestPrepHarnessError):
    pass


def prepare_cfb_backtest_prep_rows(fixtures):
    """Classify CFB prep rows without running a backtest or calculating P&L."""
    prepared_rows = []
    for fixture in fixtures:
        result = cfb_trade_rule_checker.check_cfb_trade_rules_from_fixture(fixture)
        prepared_rows.append(
            {
                "fixture_id": fixture.get("fixture_id"),
                "candidate_id": fixture.get("candidate_id"),
                "trade_rule_status": result["trade_rule_status"],
                "rejection_reason": result["rejection_reason"],
                "entry_fill_basis": result.get("entry_fill_basis"),
                "exit_fill_basis": result.get("exit_fill_basis"),
                "exit_reason": result.get("exit_reason"),
                "blocking_reasons": result["blocking_reasons"],
            }
        )
    return {
        "harness_status": "prepared_not_run",
        "backtest_run": False,
        "pnl_calculated": False,
        "candidate_marked_ready": False,
        "rows": prepared_rows,
    }


def run_backtest(*_args, **_kwargs):
    raise BacktestRunNotAuthorizedError(
        "CFB backtest-prep harness is structure only; backtest runs are not authorized."
    )


def calculate_pnl(*_args, **_kwargs):
    raise BacktestRunNotAuthorizedError(
        "CFB backtest-prep harness must not calculate P&L."
    )
