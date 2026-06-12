# SAFE-FAST Day 41 QQQ Gap-Context Threshold Gap

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

This document records the remaining threshold gap after defining the no-hindsight QQQ Clean Fast Break gap-context rule shape.

## What The Repo Supports Now

The repo supports measuring a chart gap from source-backed QQQ candles:

- Previous regular-session final exported close: `611.02`.
- Signal-day regular-session open: `609.455`.
- Gap points: `-1.565`.
- Gap percent: approximately `-0.2561%`.
- Gap direction: `down`.

Existing calculation-plan language permits recording gap direction, points, and percent from chart candles. It also forbids inferring gap cause from price action.

## What The Repo Does Not Support Yet

The repo does not yet define numeric QQQ Clean Fast Break thresholds for:

- `clean`
- `caution`
- `fail`

The repo also does not define whether the `-0.2561%` down gap for this candidate is small enough to be clean, material enough to be caution, or disqualifying enough to fail.

## Decision

No numeric threshold is invented in this task.

Until threshold fixtures are accepted, a future calculator must not convert the measured target gap into `clean`, `caution`, or `fail`. The safe status remains `unknown` for threshold-dependent evidence.

## Required Threshold Evidence Before Promotion

Before any calculator can emit a non-`unknown` `gap_context_status`, SAFE-FAST needs accepted threshold fixtures covering:

- Flat or near-flat gap behavior.
- Small favorable gap behavior.
- Small adverse gap behavior.
- Material favorable gap behavior.
- Material adverse gap behavior.
- Disqualifying gap behavior.
- Exact boundary values between clean/caution/fail.
- QQQ Clean Fast Break examples where the gap is visible but cause is unknown.
- Cases proving headline, macro, IV, event, option, execution, and outcome evidence cannot override the raw gap threshold label.

No QQQ CFB evidence row should pass gap-context content validation until these thresholds and regression cases exist.
