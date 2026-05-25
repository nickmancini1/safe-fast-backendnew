import importlib
import unittest


WATCHER_FOUNDATION_TEST_MODULES = (
    "tests.test_watcher_foundation_scaffold",
    "tests.test_watcher_state_tracking",
    "tests.test_trigger_card_projection",
    "tests.test_shadow_log_writer",
    "tests.test_duplicate_suppression_runtime",
    "tests.test_focus_ranking_runtime",
    "tests.test_diagnostics_runtime",
    "tests.test_headline_news_policy_placeholder",
    "tests.test_watcher_pipeline_integration",
    "tests.test_watcher_pipeline_sequence_regression",
    "tests.test_watcher_batch_runner",
    "tests.test_watcher_fixture_regression_pack",
    "tests.test_watcher_replay_regression_runner",
    "tests.test_watcher_replay_regression_hardening",
    "tests.test_watcher_stable_winner_selection_replay",
)


def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    for module_name in WATCHER_FOUNDATION_TEST_MODULES:
        module = importlib.import_module(module_name)
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


if __name__ == "__main__":
    unittest.main()
