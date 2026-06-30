# SAFE-FAST Day 55 Entry Quote Rule Decision Task

Read SAFE_FAST_BUILD_STATE.md first.

Goal:
Define and protect the entry quote rule for option replay.

Question:
When the first quote fails spread <= 0.15, but a later quote inside the accepted entry window passes, is entry allowed?

Current evidence:
SPY 707C first quote spread was 0.18.
Later quote inside the same downloaded window reached 0.15.

Required output:
- Rule decision: first quote only OR first valid quote inside accepted window.
- Explain why from existing SAFE-FAST docs.
- If docs do not define it, mark RULE_DEFINITION_GAP.
- Add regression test proving replay does not silently change behavior.
- No vendor download. No Schwab. No Railway. No live backend.
