from signal_replay import run_signal_replay


def main():
    result = run_signal_replay()
    print("Historical Signal Replay v1 complete")
    print("Signal/stage replay only")
    print("No trade outcome / no P&L / no account sizing / no auto-trading")
    print(f"Signal log: {result['signal_log_path']}")
    print(f"Summary: {result['summary_path']}")
    print(f"Regression candidates: {result['regression_candidates_path']}")


if __name__ == "__main__":
    main()
