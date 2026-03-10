# Composio Fit Assessment — P0 POC

A proof-of-concept agentic system that monitors a GitHub repository for new Issues, Pull Requests, and Commits, then delivers notifications via Gmail (and Slack, coming soon). Built on [Composio](https://composio.dev) to evaluate its fitness as a tool-integration layer.

---

## How It Works

```
main.py  →  Executor (timed loop)  →  GitHubMonitor  →  GitHubConnector  →  Composio  →  GitHub
                                             │
                                             └──  GmailConnector  →  Composio  →  Gmail
```

- **Executor** — drives a configurable polling loop (default: 60s)
- **GitHubMonitor** — business logic: filters new events, deduplicates by issue number, dispatches notifications
- **GitHubConnector** — Composio SDK calls for each configured GitHub slug
- **GmailConnector** — sends formatted email notifications via Composio's Gmail integration
- **Memory** — persists `last_poll_time` to `src/cognition/notified_ids.json`; only advances when new events are actually notified

---

## Prerequisites

- Python 3.12+
- A [Composio](https://composio.dev) account with connected GitHub and Gmail integrations
- Environment variables configured (see below)

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Configuration

Set the following in your `.bash_profile` or `.env`:

| Variable | Description |
|---|---|
| `COMPOSIO_API_KEY` | Composio API key |
| `COMPOSIO_USER_ID` | Composio default user ID |
| `COMPOSIO_P0_DIR` | Absolute path to project root (required) |
| `GH_REPO_OWNER` | GitHub repo owner (e.g. `rnemzek`) |
| `GH_REPO_NAME` | GitHub repo name |
| `GH_POLL_SLUGS` | Comma-separated Composio slugs to poll (e.g. `GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY,GITHUB_LIST_COMMITS,GITHUB_LIST_PULL_REQUESTS`) |
| `GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID` | Composio user ID for Gmail connection |
| `GMAIL_TO` | Notification recipient email |
| `GMAIL_FROM` | Sender display name + address (e.g. `Composio Bot <you@gmail.com>`) |
| `GMAIL_SLUG` | Composio slug for sending email (e.g. `GMAIL_SEND_EMAIL`) |
| `GMAIL_BOT_VERSION` | Composio Gmail toolkit version |
| `SLACK_CHANNEL_ID` | Target Slack channel ID (for future use) |
| `COMPOSIO_MAIN_LOOP_DELAY` | Seconds between poll cycles (default: `60`) |

---

## Running

```bash
python3 -m main
```

To monitor logs in real time:

```bash
streamlit run src/ui/visualizer.py
```

---

## Project Structure

```
├── main.py                          # Entry point, logging setup, main loop
├── src/
│   ├── agents/
│   │   ├── executor.py              # Orchestration loop
│   │   └── github_monitor.py        # GitHub event business logic + notifications
│   ├── tools/
│   │   ├── composio_wrapper.py      # Unified Composio SDK wrapper
│   │   ├── github_connector.py      # GitHub polling via Composio
│   │   ├── gmail_connector.py       # Gmail sending via Composio
│   │   └── slack_connector.py       # Slack messaging via Composio (in progress)
│   ├── cognition/
│   │   └── memory.py                # Persistent state (last_poll_time, notified IDs)
│   ├── utils/
│   │   └── util.py                  # Shared utilities
│   └── ui/
│       └── visualizer.py            # Streamlit log viewer
└── src/tests/
    └── integration_tests/           # Integration tests for connectors
```

---

## Status

| Feature | Status |
|---|---|
| GitHub Issues → Gmail | ✅ Working |
| GitHub Commits → Gmail | 🔲 In progress |
| GitHub Pull Requests → Gmail | 🔲 In progress |
| Slack notifications | ❌ Composio connectivity issue (deferred) |
