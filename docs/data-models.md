# Data Models

All data in this system flows as Python dicts. No formal Pydantic models are defined. This document describes the expected shapes of all key data structures.

---

## 1. Composio Response Envelope

Every Composio SDK call returns this top-level envelope:

```json
{
  "data": { ... },
  "error": null,
  "successful": true
}
```

| Field | Type | Description |
|---|---|---|
| `data` | `object` | The payload; shape varies by slug |
| `error` | `string \| null` | Error message if `successful` is false |
| `successful` | `boolean` | Whether the call succeeded |

**Check used in code:**
```python
# util.py
def json_contains_data_items(data: dict) -> bool:
    """Returns True if any value in data['data'] is non-empty."""
```

---

## 2. GitHub Issue Event

Returned by `GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY`.

**Composio response shape:**
```json
{
  "data": {
    "details": [
      {
        "issue": {
          "number": 42,
          "title": "Bug: login fails on mobile",
          "state": "open",
          "updated_at": "2026-03-10T14:22:00Z",
          "created_at": "2026-03-10T12:00:00Z",
          "closed_at": null,
          "labels": [{ "name": "bug" }, { "name": "mobile" }],
          "body": "Steps to reproduce...",
          "html_url": "https://github.com/owner/repo/issues/42"
        }
      }
    ]
  }
}
```

**Fields used by `_notify_issues()`:**

| Field path | Type | Used for |
|---|---|---|
| `issue.number` | `int` | Deduplication key |
| `issue.title` | `str` | Email subject |
| `issue.state` | `str` | Email body |
| `issue.updated_at` | `str` (ISO8601) | Time filter gate |
| `issue.created_at` | `str` (ISO8601) | Email body |
| `issue.closed_at` | `str \| null` | Email body |
| `issue.labels[].name` | `str` | Email body |
| `issue.body` | `str` | Email body |
| `issue.html_url` | `str` | Email body link |

**Note:** GitHub issue events also include pull_request objects (PRs masquerade as issues). These are filtered by checking for the presence of a `pull_request` field on the issue object.

---

## 3. GitHub Commit

Returned by `GITHUB_LIST_COMMITS`.

**Composio response shape:**
```json
{
  "data": {
    "commits": [
      {
        "sha": "abc123def456...",
        "html_url": "https://github.com/owner/repo/commit/abc123",
        "commit": {
          "author": {
            "name": "Jane Dev",
            "date": "2026-03-10T15:30:00Z"
          },
          "message": "Fix null pointer in auth module\n\nDetailed description..."
        }
      }
    ]
  }
}
```

**Fields used by `_notify_commits()`:**

| Field path | Type | Used for |
|---|---|---|
| `sha` | `str` | Deduplication key, email body |
| `html_url` | `str` | Email body link |
| `commit.author.date` | `str` (ISO8601) | Time filter gate |
| `commit.author.name` | `str` | Email body |
| `commit.message` | `str` | Email subject (first line), body (full) |

---

## 4. GitHub Pull Request

Returned by `GITHUB_LIST_PULL_REQUESTS`.

**Composio response shape:**
```json
{
  "data": {
    "pull_requests": [
      {
        "number": 17,
        "title": "Add OAuth2 support",
        "state": "open",
        "created_at": "2026-03-08T09:00:00Z",
        "updated_at": "2026-03-10T16:00:00Z",
        "html_url": "https://github.com/owner/repo/pull/17",
        "body": "This PR adds OAuth2 support...",
        "diff_url": "https://github.com/owner/repo/pull/17.diff",
        "head": {
          "user": {
            "login": "janedev"
          }
        },
        "base": {
          "repo": {
            "full_name": "owner/repo"
          }
        }
      }
    ]
  }
}
```

**Fields used by `_notify_prs()`:**

| Field path | Type | Used for |
|---|---|---|
| `number` | `int` | Deduplication key, email subject |
| `title` | `str` | Email subject |
| `state` | `str` | Email body |
| `created_at` | `str` (ISO8601) | Email body |
| `updated_at` | `str` (ISO8601) | Time filter gate |
| `html_url` | `str` | Email body link |
| `body` | `str` | Email body |
| `diff_url` | `str` | Fetched via `util.fetch_url()` for raw diff |
| `head.user.login` | `str` | Email body (author) |
| `base.repo.full_name` | `str` | Email body (target repo) |

---

## 5. Memory State (`notified_ids.json`)

Persisted to `src/cognition/notified_ids.json`.

```json
{
  "issues": [],
  "pull_requests": [],
  "commits": [],
  "last_poll_time": "2026-03-12T19:42:39Z"
}
```

| Field | Type | Description |
|---|---|---|
| `issues` | `array<string>` | Seen issue IDs (secondary dedup — not primary path) |
| `pull_requests` | `array<string>` | Seen PR IDs (secondary dedup) |
| `commits` | `array<string>` | Seen commit SHAs (secondary dedup) |
| `last_poll_time` | `string` (ISO8601 UTC) | Primary deduplication gate; only advances on successful notification |

**Default value if file is missing:**
```json
{ "last_poll_time": "2026-01-01T00:00:00Z" }
```

---

## 6. Gmail Send Payload

Arguments passed to Composio slug `GMAIL_SEND_EMAIL`:

```json
{
  "recipient_email": "recipient@example.com",
  "subject": "[GitHub] Issue #42: Bug: login fails on mobile",
  "body": "Issue #42 ...",
  "is_html": false
}
```

| Field | Type | Description |
|---|---|---|
| `recipient_email` | `str` | From `GMAIL_TO` env var |
| `subject` | `str` | Constructed per event type |
| `body` | `str` | Constructed per event type |
| `is_html` | `bool` | Always `false` (plaintext) |

---

## 7. Slack Message Payload

Arguments passed to Composio slug `SLACK_SEND_MESSAGE`:

```json
{
  "channel": "C01234567",
  "text": "[GitHub] Issue #42: Bug: login fails on mobile\n..."
}
```

| Field | Type | Description |
|---|---|---|
| `channel` | `str` | From `SLACK_CHANNEL_ID` env var |
| `text` | `str` | Notification text (similar to email body) |

---

## 8. GitHubConnector Poll Result

Internal dict returned by `GitHubConnector.poll()`:

```python
{
    "GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY": { ...composio_response... },
    "GITHUB_LIST_COMMITS": { ...composio_response... },
    "GITHUB_LIST_PULL_REQUESTS": { ...composio_response... },
}
```

Keys are the Composio slug strings from `GH_POLL_SLUGS`. Values are the raw Composio response dicts.
