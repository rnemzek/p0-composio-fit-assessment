# ADR-005: Defer Slack Integration

**Status:** Deferred
**Date:** 2026-03-10

---

## Context

The original design called for notifications to be delivered via both Gmail and Slack. The Slack connector (`src/tools/slack_connector.py`) is fully implemented and wired into all three notification paths (`_notify_issues`, `_notify_commits`, `_notify_prs`). However, all Slack calls fail due to a Composio platform-level connectivity issue with the Slack integration.

## Decision

Defer Slack integration. The `SlackConnector` remains in the codebase and is invoked on every notification cycle, but failures are logged and swallowed — they do not halt execution. The Slack issue is tracked as a known limitation of the Composio platform evaluation.

## Rationale

- The root cause is in Composio's Slack integration, not in the application code.
- The Gmail notification path is fully functional and meets minimum notification requirements for the POC.
- Removing the Slack call would require code changes that would need to be reverted later.
- Leaving it in place allows the issue to be retested against future Composio versions.

## Consequences

**Positive:**
- No loss of core POC functionality (GitHub monitoring + Gmail notification).
- Slack calls continue to run on each cycle — once Composio fixes the issue, Slack will work without code changes.

**Negative:**
- Every notification cycle logs a Slack error, which adds noise to the logs.
- The POC result for Slack integration is "blocked" rather than "passed" or "failed."

## Resolution Path

1. Check Composio release notes / changelog for Slack fixes.
2. Test with an updated `SLACK_VERSION` toolkit pin.
3. If still failing, open a support ticket with Composio.
4. If Composio cannot resolve, evaluate direct Slack API as a fallback.
