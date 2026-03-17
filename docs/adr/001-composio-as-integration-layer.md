# ADR-001: Use Composio as the Unified Integration Layer

**Status:** Accepted
**Date:** 2026-03-03

---

## Context

Cintara's agentic workflows will need to integrate with many external services (GitHub, Gmail, Slack, Jira, etc.). We needed to evaluate whether a unified tool-integration platform could reduce the boilerplate of managing OAuth flows, API versioning, and credential management across multiple services.

Composio was identified as a candidate platform. This P0 POC was designed specifically to validate that hypothesis.

## Decision

Use the Composio SDK (`composio-openai==0.11.1`) as the sole integration layer for all external service calls in this POC. No direct API calls to GitHub, Gmail, or Slack — all external communication goes through Composio's `tools.execute(slug, arguments)` interface.

## Rationale

- Composio provides a unified credential store — OAuth tokens for GitHub, Gmail, and Slack are managed by Composio, not stored locally.
- Single SDK surface area for all integrations reduces per-service boilerplate.
- Slug-based action model maps naturally to agentic tool-use patterns.
- Toolkit version pinning (`GH_VERSION`, `GMAIL_VERSION`) allows controlled upgrades.

## Consequences

**Positive:**
- GitHub polling, Gmail sending, and (intended) Slack messaging all use the same `wrapper.execute()` call pattern.
- Adding a new integration (e.g. Jira) would follow the same pattern with a new slug.
- OAuth complexity is moved to the Composio dashboard, not the codebase.

**Negative:**
- Composio SDK quirks surface as edge cases (e.g., `dangerously_skip_version_check=True` needed for pinned versions).
- Slack integration is currently broken due to Composio platform connectivity issue — we have no fallback.
- The `since` parameter inconsistency for GitHub issue events was not documented by Composio and required independent discovery.
- Dual `user_id` management (GitHub + Gmail share one account, Slack has another) adds complexity.

## Alternatives Considered

- **Direct REST API calls:** Would give full control but require managing OAuth tokens, refresh logic, and per-service HTTP client setup.
- **LangChain tools:** More complex setup, heavier dependency, not Composio.
- **GitHub webhooks:** Would eliminate polling but requires a publicly-accessible server.
