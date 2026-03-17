# Architecture Overview

## Purpose

This system is a P0 proof-of-concept that evaluates [Composio](https://composio.dev) as a unified tool-integration platform for agentic workflows. The concrete use case is monitoring a GitHub repository for new Issues, Pull Requests, and Commits, then delivering notifications via Gmail (and Slack, once resolved).

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        main.py (Entry Point)                    │
│         Infinite polling loop · configurable sleep delay        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Executor   │  Thin orchestrator
                    │ executor.py │  Catches and logs errors
                    └──────┬──────┘
                           │
               ┌───────────▼───────────┐
               │    GitHubMonitor      │  Core business logic
               │  github_monitor.py    │  Poll → Filter → Notify
               └───┬──────────────┬-───┘
                   │              │
        ┌──────────▼──┐    ┌──────▼─────────--─┐
        │   Memory    │    │ GitHubConnector   │
        │  memory.py  │    │github_connector.py│
        │ (JSON state)│    │(Composio polling) │
        └─────────────┘    └────────┬───────-──┘
                                    │
                         ┌──────────▼────────-──┐
                         │   ComposioWrapper    │
                         │ composio_wrapper.py  │
                         │  Unified SDK client  │
                         └──────┬──────────┬─-──┘
                                │          │
                   ┌────────────▼──┐  ┌────▼─-─────────┐
                   │GmailConnector │  │SlackConnector  │
                   │gmail_connector│  │slack_connector │
                   │   (working)   │  │  (deferred)    │
                   └───────────────┘  └────────────────┘
```

---

## Component Responsibilities

### `main.py`
- Configures rotating file logger (via `TimedRotatingFileHandler`)
- Bootstraps `Executor`
- Runs infinite poll loop with configurable sleep (`COMPOSIO_MAIN_LOOP_DELAY`, default 10s)
- Handles `KeyboardInterrupt` for graceful shutdown

### `src/agents/executor.py` — Executor
- Thin orchestration wrapper around `GitHubMonitor`
- Isolates errors per cycle — a failure in one cycle does not crash the loop

### `src/agents/github_monitor.py` — GitHubMonitor
- The system's core business logic module
- Reads `last_poll_time` from `Memory` at the start of each cycle
- Delegates polling to `GitHubConnector`
- Routes results to `_notify_issues()`, `_notify_commits()`, `_notify_prs()`
- Applies client-side deduplication and time filters
- Advances `last_poll_time` only when at least one notification was sent

### `src/cognition/memory.py` — Memory
- JSON-backed persistent state (`src/cognition/notified_ids.json`)
- Stores `last_poll_time` and seen ID arrays for issues, PRs, and commits
- Acts as the primary deduplication mechanism

### `src/tools/composio_wrapper.py` — ComposioWrapper
- Instantiates the `Composio` SDK client once with API key and toolkit version pins
- Exposes a single `execute(slug, arguments, override_user_id=None)` method
- Supports per-call `user_id` override (needed because Gmail and GitHub use different Composio connection accounts)

### `src/tools/github_connector.py` — GitHubConnector
- Reads `GH_POLL_SLUGS` from environment to determine which event types to poll
- Calls the Composio SDK for each slug with `owner`, `repo`, `since`, `state`, and `per_page`
- Special-cases `GITHUB_LIST_COMMITS` (no `state` argument)
- Returns a dict keyed by slug

### `src/tools/gmail_connector.py` — GmailConnector
- Sends plaintext email via Composio slug `GMAIL_SEND_EMAIL`
- Uses `override_user_id` to target the Gmail-specific Composio connection account

### `src/tools/slack_connector.py` — SlackConnector
- Calls Composio slug `SLACK_SEND_MESSAGE`
- Currently non-functional due to a Composio Slack connectivity issue (deferred)

### `src/utils/util.py` — Utilities
- `getDateTimestamp()` — current UTC timestamp string
- `get_environ_variable_as_array(key)` — splits an env var by comma
- `raiseError(v_name, v_value, env_variable)` — validation helper
- `pretty_json(data)` / `dictify_json(data)` — JSON helpers
- `fetch_url(url)` — plain HTTP GET (used to fetch PR raw diffs)
- `json_contains_data_items(data)` — checks Composio response for non-empty data

### `src/ui/visualizer.py` — Streamlit Log Viewer
- Reads `logs/agent_activity.log` and displays the last 15 lines
- Auto-refreshes every second
- Run with: `streamlit run src/ui/visualizer.py`

---

## Key Design Decisions

### 1. Composio as the Integration Layer
All GitHub reads and Gmail/Slack writes go through the Composio SDK. This is the core hypothesis being validated: can Composio reduce integration boilerplate for agentic workflows?

### 2. `last_poll_time` as Primary Deduplication
Rather than tracking individual seen IDs as the primary filter, `last_poll_time` is the gate. ID arrays in `Memory` exist but are secondary. The timestamp only advances when a notification is successfully sent, preventing event loss during quiet periods.

### 3. Client-Side Filtering for Issues
GitHub's issue events endpoint does not honor the `since` parameter. The monitor applies a manual `updated_at > last_poll` filter client-side, then deduplicates by issue number (latest event per issue wins).

### 4. Dual `user_id` Pattern
GitHub and Gmail use different Composio connection accounts. `ComposioWrapper` supports an `override_user_id` on each call. `GitHubConnector` uses `GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID` as its user ID (naming is historical — this is the account that has both GitHub and Gmail connected).

### 5. PR Diff Fetching
For pull request notifications, the system fetches the raw unified diff from `pr.diff_url` via a plain HTTP GET (bypassing Composio) and includes it in the email body. This provides immediate context in the notification.

### 6. Dormant Researcher Agent
`src/agents/researcher.py` contains an early design using OpenAI function-calling to drive Composio tools agenetically. It is not wired into the execution path and represents a potential future direction.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Integration layer | Composio SDK (`composio-openai==0.11.1`) |
| HTTP client | `httpx` (transitive), `requests` (PR diff fetch) |
| State persistence | JSON file (`notified_ids.json`) |
| Configuration | `python-dotenv` + environment variables |
| Monitoring UI | Streamlit |
| Logging | Python `logging.handlers.TimedRotatingFileHandler` |
