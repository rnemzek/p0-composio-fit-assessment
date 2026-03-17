# API Reference — Composio Slugs

This project uses the Composio SDK as its integration layer. There are no internally-exposed API endpoints. All external communication is via Composio action "slugs."

---

## GitHub Actions (Read)

### `GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY`

Retrieves issue events for a repository.

**Used in:** `src/tools/github_connector.py` → `poll()`

**Input arguments:**
```python
{
    "owner": str,          # GitHub repo owner (GH_REPO_OWNER)
    "repo": str,           # GitHub repo name (GH_REPO_NAME)
    "since": str,          # ISO8601 UTC — NOTE: GitHub ignores this for issue events
    "state": str,          # "open", "closed", or "all"
    "per_page": int        # Results per page (e.g. 30)
}
```

**Response shape:**
```json
{
  "data": {
    "details": [
      {
        "issue": {
          "number": 42,
          "title": "Bug: ...",
          "state": "open",
          "updated_at": "2026-03-10T14:22:00Z",
          "created_at": "2026-03-10T12:00:00Z",
          "closed_at": null,
          "labels": [{ "name": "bug" }],
          "body": "...",
          "html_url": "https://github.com/owner/repo/issues/42"
        }
      }
    ]
  },
  "error": null,
  "successful": true
}
```

**Known limitation:** The `since` parameter is silently ignored by the GitHub issue events endpoint. Client-side filtering by `updated_at` is required downstream in `_notify_issues()`.

---

### `GITHUB_LIST_COMMITS`

Retrieves commits for a repository.

**Used in:** `src/tools/github_connector.py` → `poll()`

**Input arguments:**
```python
{
    "owner": str,          # GitHub repo owner
    "repo": str,           # GitHub repo name
    "since": str,          # ISO8601 UTC — honored by this endpoint
    "per_page": int        # Results per page
    # NOTE: "state" argument is NOT sent for this slug
}
```

**Response shape:**
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
          "message": "Fix null pointer in auth module\n\nDetails..."
        }
      }
    ]
  },
  "error": null,
  "successful": true
}
```

---

### `GITHUB_LIST_PULL_REQUESTS`

Retrieves pull requests for a repository.

**Used in:** `src/tools/github_connector.py` → `poll()`

**Input arguments:**
```python
{
    "owner": str,          # GitHub repo owner
    "repo": str,           # GitHub repo name
    "since": str,          # ISO8601 UTC (may or may not be honored)
    "state": str,          # "open", "closed", or "all"
    "per_page": int        # Results per page
}
```

**Response shape:**
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
        "body": "This PR adds...",
        "diff_url": "https://github.com/owner/repo/pull/17.diff",
        "head": { "user": { "login": "janedev" } },
        "base": { "repo": { "full_name": "owner/repo" } }
      }
    ]
  },
  "error": null,
  "successful": true
}
```

---

## Gmail Actions (Write)

### `GMAIL_SEND_EMAIL`

Sends an email via Gmail.

**Used in:** `src/tools/gmail_connector.py` → `send_mail()`

**Input arguments:**
```python
{
    "recipient_email": str,   # From GMAIL_TO env var
    "subject": str,           # Constructed per event type
    "body": str,              # Constructed per event type (plaintext)
    "is_html": bool           # Always False
}
```

**Response shape:**
```json
{
  "data": { "message_id": "..." },
  "error": null,
  "successful": true
}
```

**Auth:** Requires a Composio connection account linked to Gmail via OAuth. Uses `override_user_id` = `GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID`.

---

## Slack Actions (Write — Deferred)

### `SLACK_SEND_MESSAGE`

Posts a message to a Slack channel.

**Used in:** `src/tools/slack_connector.py` → `send_message()`

**Status:** Non-functional — Composio Slack connectivity issue (deferred).

**Input arguments:**
```python
{
    "channel": str,    # From SLACK_CHANNEL_ID env var (e.g. "C01234567")
    "text": str        # Message text
}
```

**Expected response shape:**
```json
{
  "data": { "ts": "1234567890.123456" },
  "error": null,
  "successful": true
}
```

---

## Skunkworks / Testing Actions

These slugs are used only in `src/tests/skunkworks/` and are not part of the production execution path.

| Slug | Purpose | File |
|---|---|---|
| `GITHUB_CREATE_ISSUE` | Create a real GitHub issue for testing | `github_simulator.py` |
| `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS` | Create a file commit for testing | `github_simulator.py` |
| `github_get_repository` | Verify GitHub connection is live | `verify_github_link.py` |

---

## Composio SDK Invocation Pattern

All slugs are invoked through `ComposioWrapper.execute()`:

```python
# Standard call
response = wrapper.execute(slug="GITHUB_LIST_COMMITS", arguments={
    "owner": "rnemzek",
    "repo": "streaming-service-search-engine",
    "since": "2026-03-10T00:00:00Z",
    "per_page": 30
})

# With user_id override (Gmail, GitHub)
response = wrapper.execute(
    slug="GMAIL_SEND_EMAIL",
    arguments={ "recipient_email": "...", "subject": "...", "body": "..." },
    override_user_id="gmail-connection-user-id"
)
```

**SDK flags:** All production calls use `dangerously_skip_version_check=True` to allow use of pinned toolkit versions.

---

## Error Handling

Composio errors are indicated by `response["successful"] == False` and a non-null `response["error"]`. The system logs errors but continues execution — a failed notification does not halt the polling loop.

```python
if not response.get("successful"):
    logger.error(f"Composio call failed: {response.get('error')}")
```
