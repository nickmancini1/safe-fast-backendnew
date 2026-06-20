import copy
import unittest

from watcher_foundation import day48_continuation_option_context_request_validator as validator


class Day48ContinuationOptionContextRequestValidatorTests(unittest.TestCase):
    def test_manifest_passes_with_exact_frozen_request_scope(self):
        result = validator.validate_manifest()

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["problem_count"], 0)
        self.assertEqual(
            result["requested_candidate_ids"],
            ["SPY-REAL-HISTORICAL-CONTINUATION-001"],
        )
        self.assertEqual(
            result["control_candidate_ids"],
            [
                "GLD-REAL-HISTORICAL-CONTINUATION-001",
                "IWM-REAL-HISTORICAL-CONTINUATION-001",
            ],
        )
        self.assertEqual(result["request_count"], 2)

    def test_controls_cannot_be_added_to_requests(self):
        manifest = copy.deepcopy(validator.load_manifest())
        manifest["requests"][0]["candidate_id"] = "GLD-REAL-HISTORICAL-CONTINUATION-001"

        result = validator.validate_manifest(manifest)

        self.assertEqual(result["status"], "fail")
        self.assertTrue(
            any("candidate is not frozen QQQ/SPY" in problem for problem in result["problems"])
        )

    def test_exit_path_is_rejected_before_valid_entry_exists(self):
        manifest = copy.deepcopy(validator.load_manifest())
        manifest["requests"][0]["conditional_exit_path_window"] = {
            "start": "2026-04-30T12:30:00-04:00",
            "end": "2026-04-30T15:45:00-04:00",
        }

        result = validator.validate_manifest(manifest)

        self.assertEqual(result["status"], "fail")
        self.assertTrue(
            any("conditional exit window" in problem for problem in result["problems"])
        )

    def test_secret_or_live_fields_are_rejected(self):
        manifest = copy.deepcopy(validator.load_manifest())
        manifest["requests"][0]["api_key"] = "SHOULD_NOT_EXIST"

        result = validator.validate_manifest(manifest)

        self.assertEqual(result["status"], "fail")
        self.assertTrue(any("forbidden key paths" in problem for problem in result["problems"]))


if __name__ == "__main__":
    unittest.main()
