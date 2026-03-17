# ADR-003: Client-Side Filtering for GitHub Issue Events

**Status:** Accepted
**Date:** 2026-03-10

---

## Context

The GitHub issue events endpoint (`GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY`) does not honor the `since` parameter. Passing `since` in the Composio call has no effect — the API returns all events regardless of the timestamp.

This was discovered empirically during development; it is not documented in the GitHub API docs or Composio's documentation.

Additionally, GitHub's API returns pull requests in the issues list (PRs are technically a superset of issues in GitHub's data model).

## Decision

1. Apply a client-side `updated_at > last_poll_time` filter after receiving the full issue events response.
2. Deduplicate by issue number (latest event per issue number wins) to collapse multiple events on the same issue.
3. Explicitly filter out items that have a `pull_request` field (these are PRs masquerading as issues).

## Rationale

The API's behavior cannot be changed. Client-side filtering is the only viable approach.

Deduplication by issue number is necessary because GitHub may emit multiple events (e.g., `labeled`, `commented`, `closed`) for the same issue in a single poll window — we want one notification per issue per poll cycle, not one per event.

## Consequences

**Positive:**
- Correct behavior despite API limitation.
- Single notification per issue per cycle even with multiple events.

**Negative:**
- The full event list is fetched from GitHub on every poll, even if none are new. This is unavoidable.
- Client-side filtering is more brittle — if `updated_at` field names change in Composio's response, filtering breaks silently.
- `per_page` limit (e.g., 30) means very active repositories could miss events in a single poll window.

## Alternatives Considered

- **Use a different endpoint** (e.g., `GITHUB_LIST_ISSUES`): Also ignores `since` for the same reason; doesn't provide event-level detail.
- **GitHub webhooks:** Would eliminate this problem entirely but requires a publicly-accessible server endpoint.
