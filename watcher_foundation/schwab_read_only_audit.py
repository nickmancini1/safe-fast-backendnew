"""Read-only Charles Schwab Trader API audit helpers.

This module is intentionally isolated from trading logic. It can build the
OAuth URL, refresh stored tokens, and call allow-listed GET endpoints only.
It never submits, previews, replaces, or cancels orders.
"""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from urllib.parse import urlencode

import httpx


REPO_ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_API_BASE = "https://api.schwabapi.com"
OFFICIAL_AUTHORIZATION_ENDPOINT = f"{OFFICIAL_API_BASE}/v1/oauth/authorize"
OFFICIAL_TOKEN_ENDPOINT = f"{OFFICIAL_API_BASE}/v1/oauth/token"

DEFAULT_TOKEN_PATH = Path.home() / ".safe_fast" / "schwab_read_only_tokens.json"

READ_ONLY_ENDPOINTS = {
    "account_numbers": ("GET", "/trader/v1/accounts/accountNumbers"),
    "accounts_positions": ("GET", "/trader/v1/accounts"),
    "account_detail_positions": ("GET", "/trader/v1/accounts/{account_hash}"),
    "transactions": ("GET", "/trader/v1/accounts/{account_hash}/transactions"),
    "orders": ("GET", "/trader/v1/accounts/{account_hash}/orders"),
    "quotes": ("GET", "/marketdata/v1/quotes"),
    "option_chains": ("GET", "/marketdata/v1/chains"),
    "price_history": ("GET", "/marketdata/v1/pricehistory"),
}

FORBIDDEN_ORDER_MUTATION_WORDS = (
    "preview",
    "place",
    "submit",
    "cancel",
    "replace",
    "savedorders",
)


class SchwabReadOnlyAuditError(ValueError):
    pass


@dataclass(frozen=True)
class SchwabReadOnlyConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    token_path: Path = DEFAULT_TOKEN_PATH
    api_base: str = OFFICIAL_API_BASE

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "SchwabReadOnlyConfig":
        env = env or os.environ
        client_id = env.get("SCHWAB_CLIENT_ID") or env.get("SCHWAB_APP_KEY")
        client_secret = env.get("SCHWAB_CLIENT_SECRET") or env.get("SCHWAB_APP_SECRET")
        redirect_uri = env.get("SCHWAB_REDIRECT_URI")
        token_path = Path(env.get("SCHWAB_TOKEN_PATH") or DEFAULT_TOKEN_PATH)

        missing = [
            name
            for name, value in (
                ("SCHWAB_CLIENT_ID or SCHWAB_APP_KEY", client_id),
                ("SCHWAB_CLIENT_SECRET or SCHWAB_APP_SECRET", client_secret),
                ("SCHWAB_REDIRECT_URI", redirect_uri),
            )
            if not value
        ]
        if missing:
            raise SchwabReadOnlyAuditError(
                "missing Schwab OAuth configuration: " + ", ".join(missing)
            )

        return cls(
            client_id=str(client_id),
            client_secret=str(client_secret),
            redirect_uri=str(redirect_uri),
            token_path=validate_token_path_outside_repo(token_path),
        )


def validate_token_path_outside_repo(token_path: Path | str) -> Path:
    path = Path(token_path).expanduser()
    resolved = path.resolve()
    repo = REPO_ROOT.resolve()
    if resolved == repo or repo in resolved.parents:
        raise SchwabReadOnlyAuditError(
            "Schwab token path must be outside the repository and outside Git"
        )
    return resolved


def build_authorization_url(config: SchwabReadOnlyConfig, *, state: str) -> str:
    if not state:
        raise SchwabReadOnlyAuditError("state is required for OAuth authorization")
    query = urlencode(
        {
            "response_type": "code",
            "client_id": config.client_id,
            "redirect_uri": config.redirect_uri,
            "state": state,
        }
    )
    return f"{OFFICIAL_AUTHORIZATION_ENDPOINT}?{query}"


def exchange_authorization_code(
    config: SchwabReadOnlyConfig,
    authorization_code: str,
    *,
    client: httpx.Client | None = None,
) -> dict[str, object]:
    if not authorization_code:
        raise SchwabReadOnlyAuditError("authorization_code is required")
    close_client = client is None
    client = client or httpx.Client(timeout=20)
    try:
        response = client.post(
            OFFICIAL_TOKEN_ENDPOINT,
            data={
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": config.redirect_uri,
            },
            headers=_oauth_headers(config),
        )
        response.raise_for_status()
        token_payload = response.json()
        write_token_payload(config.token_path, token_payload)
        return redacted_token_payload(token_payload)
    finally:
        if close_client:
            client.close()


def refresh_access_token(
    config: SchwabReadOnlyConfig,
    *,
    client: httpx.Client | None = None,
) -> dict[str, object]:
    token_payload = read_token_payload(config.token_path)
    refresh_token = token_payload.get("refresh_token")
    if not refresh_token:
        raise SchwabReadOnlyAuditError("stored refresh token is unavailable")

    close_client = client is None
    client = client or httpx.Client(timeout=20)
    try:
        response = client.post(
            OFFICIAL_TOKEN_ENDPOINT,
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            headers=_oauth_headers(config),
        )
        response.raise_for_status()
        refreshed = response.json()
        if "refresh_token" not in refreshed:
            refreshed["refresh_token"] = refresh_token
        write_token_payload(config.token_path, refreshed)
        return redacted_token_payload(refreshed)
    finally:
        if close_client:
            client.close()


def read_token_payload(token_path: Path | str) -> dict[str, object]:
    path = validate_token_path_outside_repo(token_path)
    if not path.exists():
        raise SchwabReadOnlyAuditError("Schwab token file does not exist")
    return json.loads(path.read_text(encoding="utf-8"))


def write_token_payload(token_path: Path | str, payload: Mapping[str, object]) -> None:
    path = validate_token_path_outside_repo(token_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def redacted_token_payload(payload: Mapping[str, object]) -> dict[str, object]:
    redacted = {}
    for key, value in payload.items():
        if "token" in key.lower() or key.lower() in {"code", "client_secret"}:
            redacted[key] = "REDACTED" if value else value
        else:
            redacted[key] = value
    return redacted


def build_read_only_request(
    endpoint_name: str,
    *,
    account_hash: str | None = None,
    params: Mapping[str, object] | None = None,
    api_base: str = OFFICIAL_API_BASE,
) -> dict[str, object]:
    try:
        method, path_template = READ_ONLY_ENDPOINTS[endpoint_name]
    except KeyError as exc:
        raise SchwabReadOnlyAuditError(f"unknown read-only endpoint: {endpoint_name}") from exc
    if method != "GET":
        raise SchwabReadOnlyAuditError("only GET endpoints are allowed")
    if any(word in path_template.lower() for word in FORBIDDEN_ORDER_MUTATION_WORDS):
        raise SchwabReadOnlyAuditError("order mutation endpoints are forbidden")
    if "{account_hash}" in path_template and not account_hash:
        raise SchwabReadOnlyAuditError(f"account_hash is required for {endpoint_name}")
    path = path_template.format(account_hash=account_hash or "")
    return {
        "method": method,
        "url": f"{api_base}{path}",
        "params": dict(params or {}),
        "endpoint_name": endpoint_name,
    }


def call_read_only_endpoint(
    config: SchwabReadOnlyConfig,
    endpoint_name: str,
    *,
    account_hash: str | None = None,
    params: Mapping[str, object] | None = None,
    client: httpx.Client | None = None,
) -> object:
    token_payload = read_token_payload(config.token_path)
    access_token = token_payload.get("access_token")
    if not access_token:
        raise SchwabReadOnlyAuditError("stored access token is unavailable")
    request = build_read_only_request(
        endpoint_name,
        account_hash=account_hash,
        params=params,
        api_base=config.api_base,
    )
    close_client = client is None
    client = client or httpx.Client(timeout=20)
    try:
        response = client.request(
            str(request["method"]),
            str(request["url"]),
            params=request["params"],
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        return response.json()
    finally:
        if close_client:
            client.close()


def build_capability_audit_plan() -> dict[str, object]:
    return {
        "official_api_base": OFFICIAL_API_BASE,
        "official_authorization_endpoint": OFFICIAL_AUTHORIZATION_ENDPOINT,
        "official_token_endpoint": OFFICIAL_TOKEN_ENDPOINT,
        "read_only_endpoints": {
            name: {"method": method, "path": path}
            for name, (method, path) in READ_ONLY_ENDPOINTS.items()
        },
        "forbidden_order_behavior": [
            "submit_order",
            "preview_order",
            "replace_order",
            "cancel_order",
            "saved_order_mutation",
        ],
        "token_storage_rule": "outside repository and outside Git",
        "future_archive_rule": (
            "local Schwab archive should store redacted read-only snapshots under "
            "a future ignored local archive, with account hashes/token values excluded"
        ),
    }


def unauthenticated_audit_status(env: Mapping[str, str] | None = None) -> dict[str, object]:
    env = env or os.environ
    required = {
        "SCHWAB_CLIENT_ID or SCHWAB_APP_KEY": bool(
            env.get("SCHWAB_CLIENT_ID") or env.get("SCHWAB_APP_KEY")
        ),
        "SCHWAB_CLIENT_SECRET or SCHWAB_APP_SECRET": bool(
            env.get("SCHWAB_CLIENT_SECRET") or env.get("SCHWAB_APP_SECRET")
        ),
        "SCHWAB_REDIRECT_URI": bool(env.get("SCHWAB_REDIRECT_URI")),
    }
    token_path = Path(env.get("SCHWAB_TOKEN_PATH") or DEFAULT_TOKEN_PATH)
    token_path_valid = True
    token_path_reason = "outside_repo"
    try:
        validate_token_path_outside_repo(token_path)
    except SchwabReadOnlyAuditError as exc:
        token_path_valid = False
        token_path_reason = str(exc)

    blocked_reasons = [
        name for name, present in required.items() if not present
    ]
    if not token_path_valid:
        blocked_reasons.append("SCHWAB_TOKEN_PATH outside repository")

    return {
        "created_utc": _utc_now(),
        "official_source_scope": "Schwab Developer Portal and api.schwabapi.com official endpoints",
        "oauth_config_present": required,
        "token_path_rule": token_path_reason,
        "oauth_browser_action_required_now": False,
        "live_schwab_verification_attempted": False,
        "blocked": bool(blocked_reasons),
        "blocked_reasons": blocked_reasons,
        "read_only_plan": build_capability_audit_plan(),
        "broker_mutation_attempted": False,
        "orders_submitted_or_previewed": False,
        "tokens_printed_or_saved_in_repo": False,
        "proof_profitability_readiness_claimed": False,
    }


def _oauth_headers(config: SchwabReadOnlyConfig) -> dict[str, str]:
    raw = f"{config.client_id}:{config.client_secret}".encode("utf-8")
    encoded = base64.b64encode(raw).decode("ascii")
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded",
    }


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


if __name__ == "__main__":
    print(json.dumps(unauthenticated_audit_status(), indent=2, sort_keys=True))
