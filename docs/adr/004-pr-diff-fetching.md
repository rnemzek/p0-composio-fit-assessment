# ADR-004: Fetch PR Diffs Outside of Composio

**Status:** Accepted
**Date:** 2026-03-10

---

## Context

Pull request notifications are more useful when they include the actual code changes. GitHub provides a `diff_url` field on each PR (e.g., `https://github.com/owner/repo/pull/17.diff`) that returns the raw unified diff.

Composio does not provide a slug for fetching raw diffs. Using the `GITHUB_LIST_PULL_REQUESTS` slug returns PR metadata but not the diff content.

## Decision

Fetch the raw unified diff for each PR by calling `util.fetch_url(pr["diff_url"])` directly using the `requests` library, bypassing Composio entirely. Append the diff to the email body.

## Rationale

- The diff is publicly accessible via plain HTTP GET on public repos — no auth required.
- There is no Composio slug that provides this data.
- The value to the recipient of seeing the actual diff in the notification is high.

## Consequences

**Positive:**
- Rich PR notifications include the actual code diff.
- Simple implementation using `requests.get()`.

**Negative:**
- Introduces a direct HTTP dependency outside the Composio abstraction layer.
- For private repositories, the `diff_url` would require authentication — this would need a GitHub token or Composio-mediated fetch.
- Large diffs can produce very long email bodies.

## Alternatives Considered

- **Skip the diff:** Simpler, but reduces notification value.
- **Fetch via Composio:** No slug available for this.
- **Truncate diff:** Could be added as a future improvement (e.g., first N lines only).
