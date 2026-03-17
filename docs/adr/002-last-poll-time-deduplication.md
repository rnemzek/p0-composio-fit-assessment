# ADR-002: Use last_poll_time as Primary Deduplication Mechanism

**Status:** Accepted
**Date:** 2026-03-10

---

## Context

The polling agent must not send duplicate notifications for the same GitHub event. Two approaches were considered: tracking individual seen IDs, or using a watermark timestamp.

## Decision

Use `last_poll_time` (an ISO8601 UTC timestamp) as the primary deduplication gate. Advance the timestamp only when at least one notification is successfully sent.

Seen ID arrays (`issues`, `pull_requests`, `commits`) in `Memory` are populated as a secondary mechanism but are not the primary dedup path.

## Rationale

- Timestamp-based deduplication is simple to reason about and debug (one value to inspect).
- Advancing only on successful send prevents event loss during error cycles or quiet periods.
- Individual ID tracking would require unbounded growth of the `notified_ids.json` file over time.

## Consequences

**Positive:**
- Simple state: one timestamp to check.
- Natural handling of quiet periods (timestamp stays put, no events missed).
- Easy to manually reset by editing `notified_ids.json`.

**Negative:**
- If the poll window crosses a timestamp boundary (e.g., an event's `updated_at` moves backward due to a GitHub quirk), events could be re-notified.
- If `last_poll_time` doesn't advance (e.g., no send on several consecutive cycles), the next successful cycle may pick up a large batch of old events.

## Alternatives Considered

- **ID-only deduplication:** Simpler but requires unbounded set growth and does not handle the GitHub issue events `since` parameter being ignored.
- **Both timestamp + ID sets as co-primary:** More robust but complex; deferred to a future iteration.
