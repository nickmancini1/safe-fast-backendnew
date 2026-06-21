import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from watcher_foundation import schwab_read_only_audit as schwab


class SchwabReadOnlyAuditTests(unittest.TestCase):
    def test_missing_env_blocks_before_oauth_browser_action(self):
        status = schwab.unauthenticated_audit_status(env={})

        self.assertTrue(status["blocked"])
        self.assertFalse(status["oauth_browser_action_required_now"])
        self.assertFalse(status["live_schwab_verification_attempted"])
        self.assertFalse(status["broker_mutation_attempted"])
        self.assertIn("SCHWAB_REDIRECT_URI", status["blocked_reasons"])

    def test_token_path_must_stay_outside_repository(self):
        repo_token_path = schwab.REPO_ROOT / "schwab_tokens.json"

        with self.assertRaises(schwab.SchwabReadOnlyAuditError):
            schwab.validate_token_path_outside_repo(repo_token_path)

    def test_authorization_url_uses_official_endpoint_and_required_fields(self):
        config = schwab.SchwabReadOnlyConfig(
            client_id="client-id",
            client_secret="client-secret",
            redirect_uri="https://127.0.0.1/callback",
            token_path=Path.home() / ".safe_fast" / "test_tokens.json",
        )
        url = schwab.build_authorization_url(config, state="state-value")

        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        self.assertEqual(
            f"{parsed.scheme}://{parsed.netloc}{parsed.path}",
            schwab.OFFICIAL_AUTHORIZATION_ENDPOINT,
        )
        self.assertEqual(query["response_type"], ["code"])
        self.assertEqual(query["client_id"], ["client-id"])
        self.assertEqual(query["redirect_uri"], ["https://127.0.0.1/callback"])
        self.assertEqual(query["state"], ["state-value"])

    def test_only_get_allowlisted_requests_can_be_built(self):
        request = schwab.build_read_only_request(
            "price_history",
            params={"symbol": "SPY", "periodType": "day"},
        )

        self.assertEqual(request["method"], "GET")
        self.assertEqual(
            request["url"],
            "https://api.schwabapi.com/marketdata/v1/pricehistory",
        )
        for endpoint_name in schwab.READ_ONLY_ENDPOINTS:
            built = schwab.build_read_only_request(
                endpoint_name,
                account_hash="hash-value",
                params={"symbol": "SPY"},
            )
            self.assertEqual(built["method"], "GET")
            forbidden = " ".join(
                [built["url"], built["endpoint_name"]]
            ).lower()
            for word in schwab.FORBIDDEN_ORDER_MUTATION_WORDS:
                self.assertNotIn(word, forbidden)

    def test_account_hash_is_required_for_account_specific_history(self):
        with self.assertRaises(schwab.SchwabReadOnlyAuditError):
            schwab.build_read_only_request("transactions")

    def test_token_payload_redaction_never_returns_tokens(self):
        redacted = schwab.redacted_token_payload(
            {
                "access_token": "access-secret",
                "refresh_token": "refresh-secret",
                "expires_in": 1800,
            }
        )

        self.assertEqual(redacted["access_token"], "REDACTED")
        self.assertEqual(redacted["refresh_token"], "REDACTED")
        self.assertEqual(redacted["expires_in"], 1800)

    def test_read_only_plan_names_no_order_mutation_behavior(self):
        plan = schwab.build_capability_audit_plan()

        self.assertIn("orders", plan["read_only_endpoints"])
        self.assertEqual(plan["read_only_endpoints"]["orders"]["method"], "GET")
        self.assertIn("submit_order", plan["forbidden_order_behavior"])
        self.assertIn("preview_order", plan["forbidden_order_behavior"])


if __name__ == "__main__":
    unittest.main()
