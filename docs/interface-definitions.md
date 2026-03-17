# Interface Definitions

Typed Python interface definitions for all major classes. These reflect the actual implementation and serve as a reference for extending or replacing components.

---

## ComposioWrapper

**File:** `src/tools/composio_wrapper.py`

```python
from typing import Any

class ComposioWrapper:
    """
    Unified Composio SDK client. Wraps the Composio tools.execute() API
    with version pinning and per-call user_id override support.
    """

    def __init__(self) -> None:
        """
        Reads from environment:
          - COMPOSIO_API_KEY       : str  — Composio API key (prefix: ak_)
          - COMPOSIO_USER_ID       : str  — Default Composio user ID
          - SLACK_VERSION          : str  — Composio Slack toolkit version
          - GH_VERSION             : str  — Composio GitHub toolkit version
          - GMAIL_VERSION          : str  — Composio Gmail toolkit version
        """
        ...

    def execute(
        self,
        slug: str,
        arguments: dict[str, Any],
        override_user_id: str | None = None
    ) -> dict[str, Any]:
        """
        Execute a Composio action by slug.

        Args:
            slug:             Composio action slug (e.g. 'GITHUB_LIST_COMMITS')
            arguments:        Action-specific parameters
            override_user_id: If provided, use this user_id instead of COMPOSIO_USER_ID.
                              Required when calling Gmail or GitHub (different connection accounts).

        Returns:
            Composio response envelope: {
                "data": { ... },
                "error": str | None,
                "successful": bool
            }
        """
        ...
```

---

## GitHubConnector

**File:** `src/tools/github_connector.py`

```python
from typing import Any

class GitHubConnector:
    """
    Polls GitHub via the Composio SDK. Reads poll slug list from GH_POLL_SLUGS env var.
    """

    def __init__(self) -> None:
        """
        Reads from environment:
          - COMPOSIO_API_KEY                        : str — Composio API key
          - GH_REPO_OWNER                           : str — GitHub repo owner
          - GH_REPO_NAME                            : str — GitHub repo name
          - GH_POLL_SLUGS                           : str — Comma-separated Composio slugs
          - GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID: str — User ID for Composio calls
          - GH_VERSION                              : str — Composio GitHub toolkit version
        """
        ...

    def poll(self, since: str) -> dict[str, dict[str, Any]]:
        """
        Poll all configured GitHub event types.

        Args:
            since: ISO8601 UTC timestamp. Used as the 'since' parameter for
                   commits (honored by GitHub). Issue events ignore this param —
                   client-side filtering is applied downstream.

        Returns:
            Dict keyed by Composio slug, values are raw Composio response envelopes.
            Example:
            {
                "GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY": { "data": {...}, ... },
                "GITHUB_LIST_COMMITS": { "data": {...}, ... },
                "GITHUB_LIST_PULL_REQUESTS": { "data": {...}, ... },
            }
        """
        ...
```

---

## GmailConnector

**File:** `src/tools/gmail_connector.py`

```python
from typing import Any

class GmailConnector:
    """
    Sends email notifications via Composio's Gmail integration.
    """

    def __init__(self, wrapper: ComposioWrapper) -> None:
        """
        Args:
            wrapper: Initialized ComposioWrapper instance.

        Reads from environment:
          - GMAIL_TO      : str — Recipient email address
          - GMAIL_FROM    : str — Sender display name + address (e.g. 'Bot <bot@example.com>')
          - GMAIL_SLUG    : str — Composio slug (GMAIL_SEND_EMAIL)
          - GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID : str — Composio user ID for Gmail account
        """
        ...

    def send_mail(self, subject: str, body: str) -> dict[str, Any]:
        """
        Send a plaintext email.

        Args:
            subject: Email subject line
            body:    Email body (plaintext)

        Returns:
            Composio response envelope.
        """
        ...
```

---

## SlackConnector

**File:** `src/tools/slack_connector.py`

```python
from typing import Any

class SlackConnector:
    """
    Sends Slack notifications via Composio's Slack integration.
    NOTE: Currently non-functional due to a Composio connectivity issue.
    """

    def __init__(self, wrapper: ComposioWrapper) -> None:
        """
        Args:
            wrapper: Initialized ComposioWrapper instance.

        Reads from environment:
          - SLACK_CHANNEL_ID : str — Target Slack channel ID (e.g. 'C01234567')
          - SLACK_USER_ID    : str — Composio user ID for Slack connection account
        """
        ...

    def send_message(self, text: str) -> dict[str, Any]:
        """
        Post a message to the configured Slack channel.

        Args:
            text: Message text

        Returns:
            Composio response envelope.
        """
        ...
```

---

## Memory

**File:** `src/cognition/memory.py`

```python
class Memory:
    """
    JSON-backed persistent state manager. Tracks last_poll_time and seen event IDs.
    State file: src/cognition/notified_ids.json
    """

    def __init__(self) -> None:
        """
        Loads state from notified_ids.json.
        Creates file with defaults if it does not exist:
            { "issues": [], "pull_requests": [], "commits": [], "last_poll_time": "2026-01-01T00:00:00Z" }
        """
        ...

    def get_last_poll_time(self) -> str:
        """
        Returns:
            ISO8601 UTC string of the last successful poll time.
            Example: "2026-03-12T19:42:39Z"
        """
        ...

    def set_last_poll_time(self, timestamp: str) -> None:
        """
        Persist a new last_poll_time to disk.

        Args:
            timestamp: ISO8601 UTC string.
        """
        ...

    def add_seen_id(self, category: str, id_value: str) -> None:
        """
        Record a seen event ID (secondary dedup mechanism).

        Args:
            category:  One of "issues", "pull_requests", "commits"
            id_value:  The event ID or SHA
        """
        ...

    def has_seen_id(self, category: str, id_value: str) -> bool:
        """
        Check if an event ID has been seen before.

        Args:
            category:  One of "issues", "pull_requests", "commits"
            id_value:  The event ID or SHA

        Returns:
            True if already seen.
        """
        ...
```

---

## GitHubMonitor

**File:** `src/agents/github_monitor.py`

```python
class GitHubMonitor:
    """
    Core business logic for GitHub polling and notification dispatch.
    Coordinates between Memory, GitHubConnector, GmailConnector, and SlackConnector.
    """

    def __init__(self) -> None:
        """Initializes all sub-components."""
        ...

    def check_for_updates(self) -> None:
        """
        Main poll-filter-notify pipeline. Called once per cycle by Executor.

        1. Reads last_poll_time from Memory
        2. Calls GitHubConnector.poll(last_poll_time)
        3. Routes results to _notify_issues(), _notify_commits(), _notify_prs()
        4. Advances last_poll_time if any notifications were sent
        """
        ...

    def _notify_issues(self, data: dict, last_poll: str) -> int:
        """
        Process issue events and send notifications.

        Args:
            data:       Raw Composio response for GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY
            last_poll:  ISO8601 timestamp for client-side time filter

        Returns:
            Number of notifications sent.
        """
        ...

    def _notify_commits(self, data: dict, last_poll: str) -> int:
        """
        Process commit events and send notifications.

        Args:
            data:       Raw Composio response for GITHUB_LIST_COMMITS
            last_poll:  ISO8601 timestamp for guard filter

        Returns:
            Number of notifications sent.
        """
        ...

    def _notify_prs(self, data: dict, last_poll: str) -> int:
        """
        Process pull request events and send notifications.
        Also fetches the raw unified diff from pr.diff_url.

        Args:
            data:       Raw Composio response for GITHUB_LIST_PULL_REQUESTS
            last_poll:  ISO8601 timestamp for time filter

        Returns:
            Number of notifications sent.
        """
        ...
```

---

## Executor

**File:** `src/agents/executor.py`

```python
class Executor:
    """
    Thin orchestration wrapper. Drives GitHubMonitor and isolates per-cycle errors.
    """

    def __init__(self) -> None:
        """Instantiates GitHubMonitor."""
        ...

    def run_cycle(self) -> None:
        """
        Execute one poll cycle.
        Calls GitHubMonitor.check_for_updates().
        Logs and swallows exceptions so the main loop continues on failure.
        """
        ...
```

---

## Utility Functions

**File:** `src/utils/util.py`

```python
def getDateTimestamp() -> str:
    """Returns current UTC datetime as a formatted string."""
    ...

def get_environ_variable_as_array(key: str) -> list[str]:
    """
    Reads an environment variable and splits it by comma.

    Args:
        key: Environment variable name.

    Returns:
        List of stripped string values.

    Raises:
        ValueError: If the variable is not set.
    """
    ...

def raiseError(v_name: str, v_value: Any, env_variable: str) -> None:
    """
    Validate that a required value is not None/empty.

    Args:
        v_name:       Human-readable name for error messages.
        v_value:      The value to check.
        env_variable: Environment variable name (for error message context).

    Raises:
        ValueError: If v_value is falsy.
    """
    ...

def pretty_json(data: dict | str) -> str:
    """Returns indented JSON string. Accepts dict or JSON string."""
    ...

def dictify_json(data: dict | str) -> dict:
    """Ensures data is a dict. Parses JSON string if needed."""
    ...

def fetch_url(url: str) -> str | None:
    """
    Perform a plain HTTP GET request.
    Used to fetch raw PR diffs from GitHub's diff_url.

    Args:
        url: URL to fetch.

    Returns:
        Response body as string, or None on failure.
    """
    ...

def json_contains_data_items(data: dict) -> bool:
    """
    Check if a Composio response has non-empty data values.

    Args:
        data: Composio response envelope.

    Returns:
        True if data['data'] contains at least one non-empty value.
    """
    ...
```
