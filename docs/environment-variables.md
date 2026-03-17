# Environment Variables Reference

All configuration is via environment variables loaded from `.env` using `python-dotenv`. Variables marked **Required** will raise a `ValueError` at startup if missing.

---

## Core / Application

| Variable | Required | Default | Type | Description |
|---|---|---|---|---|
| `COMPOSIO_P0_DIR` | **Yes** | — | `str` | Absolute path to the project root directory. Used to construct log file paths. |
| `COMPOSIO_P0_LOGGER_NAME` | No | `agent_logger` | `str` | Name for the Python logger instance. |
| `COMPOSIO_P0_LOG_NAME` | No | `agent_activity.log` | `str` | Log file name (placed inside `logs/` subdirectory). |
| `COMPOSIO_P0_LOG_CONFIG_WHEN` | No | `midnight` | `str` | `TimedRotatingFileHandler` rotation trigger. Options: `S`, `M`, `H`, `D`, `midnight`, `W0`-`W6`. |
| `COMPOSIO_P0_LOG_CONFIG_INTERVAL` | No | `1` | `int` | Rotation interval (in units of `WHEN`). |
| `COMPOSIO_P0_LOG_CONFIG_BACKUPCOUNT` | No | `7` | `int` | Number of rotated log files to retain. |
| `COMPOSIO_P0_LOG_CONFIG_ENCODING` | No | `utf-8` | `str` | Log file encoding. |
| `COMPOSIO_MAIN_LOOP_DELAY` | No | `10` | `int` | Seconds to sleep between poll cycles. |

---

## Composio API

| Variable | Required | Default | Type | Description |
|---|---|---|---|---|
| `COMPOSIO_API_KEY` | **Yes** | — | `str` | Composio API key. Format: `ak_...`. |
| `COMPOSIO_USER_ID` | **Yes** | — | `str` | Default Composio connection user ID. Used when no `override_user_id` is specified. |

---

## GitHub

| Variable | Required | Default | Type | Description |
|---|---|---|---|---|
| `GH_REPO_OWNER` | **Yes** | — | `str` | GitHub repository owner (e.g. `rnemzek`). |
| `GH_REPO_NAME` | **Yes** | — | `str` | GitHub repository name (e.g. `streaming-service-search-engine`). |
| `GH_REPO` | No | — | `str` | Full repo slug `owner/repo`. Used in tests only. |
| `GH_POLL_SLUGS` | **Yes** | — | `str` | Comma-separated Composio slugs to poll each cycle. Example: `GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY,GITHUB_LIST_COMMITS,GITHUB_LIST_PULL_REQUESTS` |
| `GH_VERSION` | **Yes** | — | `str` | Composio GitHub toolkit version pin (e.g. `20260227_00`). |

---

## Gmail

| Variable | Required | Default | Type | Description |
|---|---|---|---|---|
| `GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID` | **Yes** | — | `str` | Composio user ID for the Gmail-connected account. Also used as the `user_id` for GitHub Composio calls (historical). |
| `GMAIL_TO` | **Yes** | — | `str` | Recipient email address for notifications. |
| `GMAIL_FROM` | **Yes** | — | `str` | Sender display name + address (e.g. `GitHub Monitor Bot <bot@example.com>`). |
| `GMAIL_SLUG` | **Yes** | — | `str` | Composio slug for sending email. Value: `GMAIL_SEND_EMAIL`. |
| `GMAIL_VERSION` | **Yes** | — | `str` | Composio Gmail toolkit version pin. |
| `GMAIL_BOT_VERSION` | No | — | `str` | Alternate Gmail toolkit version reference (used in some scripts). |

### Gmail — Skunkworks / SMTP Only

These are only used in exploratory scripts (`src/tests/skunkworks/`). Not required for production.

| Variable | Required | Description |
|---|---|---|
| `GMAIL_USER` | No | Gmail address for direct SMTP auth. |
| `GMAIL_APP_PASSWORD` | No | Gmail app password for SMTP. |
| `GMAIL_ACCOUNT_USER_ID` | No | Composio account user ID (alternate naming, skunkworks scripts). |
| `GMAIL_AUTH_CONFIG_ID` | No | Composio auth config ID for OAuth flow initiation. |

---

## Slack

| Variable | Required | Default | Type | Description |
|---|---|---|---|---|
| `SLACK_CHANNEL_ID` | **Yes** | — | `str` | Target Slack channel ID (e.g. `C01234567`). |
| `SLACK_USER_ID` | **Yes** | — | `str` | Composio user ID for the Slack-connected account. |
| `SLACK_VERSION` | **Yes** | — | `str` | Composio Slack toolkit version pin. |

> **Note:** Slack notifications are currently deferred due to a Composio connectivity issue. These variables are still read at startup.

---

## Example `.env`

```dotenv
# Application
COMPOSIO_P0_DIR=/Users/yourname/Projects/cintara/p0-composio-fit-assessment
COMPOSIO_MAIN_LOOP_DELAY=60

# Composio API
COMPOSIO_API_KEY=ak_your_key_here
COMPOSIO_USER_ID=your_default_user_id

# GitHub
GH_REPO_OWNER=your_github_username
GH_REPO_NAME=your-repo-name
GH_POLL_SLUGS=GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY,GITHUB_LIST_COMMITS,GITHUB_LIST_PULL_REQUESTS
GH_VERSION=20260227_00

# Gmail
GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID=your_gmail_connection_user_id
GMAIL_TO=recipient@example.com
GMAIL_FROM=GitHub Monitor <monitor@example.com>
GMAIL_SLUG=GMAIL_SEND_EMAIL
GMAIL_VERSION=your_gmail_version

# Slack
SLACK_CHANNEL_ID=C01234567
SLACK_USER_ID=your_slack_connection_user_id
SLACK_VERSION=your_slack_version
```

---

## Validation Behavior

Variables are validated at component initialization time, not at startup. If a required variable is missing:

```python
# util.py
def raiseError(v_name, v_value, env_variable):
    if not v_value:
        raise ValueError(f"{v_name} is not set. Check env var: {env_variable}")
```

This means missing variables will surface as `ValueError` exceptions during the first `Executor.__init__()` call, which propagates up through `main.py`.
