"""Accepted local watcher scaffold constants.

These constants are inert data-contract values for local watch-only projection.
They do not approve live data, alerts, broker execution, orders, options, or
account/account-sizing behavior.
"""

ACCEPTED_SETUP_TYPES = (
    "Ideal",
    "Clean Fast Break",
    "Continuation",
    "UNCONFIRMED",
)

ACCEPTED_DIRECTIONS = (
    "bullish/call-side",
    "bearish/put-side",
    "neutral/unknown",
    "UNCONFIRMED",
)

ACCEPTED_STAGES = (
    "forming/developing",
    "near-trigger",
    "pending_completed_candle_approval",
    "triggered_signal_stage",
    "blocked/no-trade",
    "stale/spent/no-fresh-trigger",
    "rebuilding",
    "unavailable/unconfirmed",
)

ACCEPTED_TRIGGER_STATUSES = (
    "no_valid_trigger",
    "waiting_for_trigger",
    "near_trigger",
    "pending_completed_candle",
    "triggered",
    "failed_hold",
    "stale",
    "spent",
    "unconfirmed",
)

ACCEPTED_HEADLINE_NEWS_STATUSES = (
    "NEWS_CLEAR",
    "NEWS_CAUTION",
    "NEWS_BLOCK",
    "NEWS_UNCONFIRMED",
)

TRIGGER_LEVEL_UNCONFIRMED = "TRIGGER_LEVEL_UNCONFIRMED"
DISTANCE_TO_TRIGGER_UNCONFIRMED = "DISTANCE_TO_TRIGGER_UNCONFIRMED"
INVALIDATION_UNCONFIRMED = "INVALIDATION_UNCONFIRMED"
SOURCE_AS_OF_UNCONFIRMED = "SOURCE_AS_OF_UNCONFIRMED"
EVIDENCE_ROWS_UNCONFIRMED = "EVIDENCE_ROWS_UNCONFIRMED"
SESSION_DATE_UNCONFIRMED = "SESSION_DATE_UNCONFIRMED"
FRESHNESS_UNCONFIRMED = "FRESHNESS_UNCONFIRMED"
NEWS_UNCONFIRMED = "NEWS_UNCONFIRMED"

EXPLICIT_UNCONFIRMED_MARKERS = (
    TRIGGER_LEVEL_UNCONFIRMED,
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    SESSION_DATE_UNCONFIRMED,
    FRESHNESS_UNCONFIRMED,
    NEWS_UNCONFIRMED,
)

DEFAULT_UNAVAILABLE_FIELDS = EXPLICIT_UNCONFIRMED_MARKERS

FORBIDDEN_EXECUTION_FIELD_NAMES = frozenset(
    {
        "account",
        "account_balance",
        "account_id",
        "account_number",
        "account_size",
        "account_sizing",
        "broker",
        "broker_account_id",
        "contract",
        "contracts",
        "execution",
        "fill",
        "fill_id",
        "fill_price",
        "fills",
        "option",
        "option_contract",
        "option_pnl",
        "option_symbol",
        "order",
        "order_id",
        "order_status",
        "order_type",
        "orders",
        "pnl",
        "position",
        "position_size",
        "profit_loss",
        "quantity",
        "shares",
    }
)
