# Workflow Diagrams

All diagrams use [Mermaid](https://mermaid.js.org/) syntax. Render in GitHub, VS Code (Markdown Preview Mermaid Support), or [mermaid.live](https://mermaid.live).

---

## 1. Main Polling Loop

```mermaid
flowchart TD
    A([Start: python3 -m main]) --> B[Configure logger\nTimedRotatingFileHandler]
    B --> C[Instantiate Executor\n→ GitHubMonitor]
    C --> D{Infinite Loop}
    D --> E[run_cycle]
    E --> F{Error?}
    F -- Yes --> G[Log warning\nSkip cycle]
    F -- No --> H[check_for_updates]
    G --> I[Sleep\nCOMPOSIO_MAIN_LOOP_DELAY]
    H --> I
    I --> D
    D -- KeyboardInterrupt --> J([Graceful Shutdown])
```

---

## 2. check_for_updates — Full Pipeline

```mermaid
flowchart TD
    A[check_for_updates] --> B[memory.get_last_poll_time\n→ last_poll ISO8601 UTC]
    B --> C[Record start_ts = now]
    C --> D[GitHubConnector.poll last_poll]
    D --> E{For each slug\nin GH_POLL_SLUGS}
    E --> F[Composio SDK execute slug\nowner repo since state per_page]
    F --> G{Slug type?}
    G -- ISSUE_EVENTS --> H[_notify_issues]
    G -- LIST_COMMITS --> I[_notify_commits]
    G -- LIST_PULL_REQUESTS --> J[_notify_prs]
    H --> K{notifications_sent > 0?}
    I --> K
    J --> K
    K -- Yes --> L[memory.set_last_poll_time\nstart_ts]
    K -- No --> M[Keep last_poll_time unchanged]
    L --> N([Done])
    M --> N
```

---

## 3. Issue Notification Flow

```mermaid
flowchart TD
    A[_notify_issues\nraw_data, last_poll] --> B[Extract events list\ndata.details]
    B --> C{Any events?}
    C -- No --> Z([Return 0])
    C -- Yes --> D[Filter: updated_at > last_poll]
    D --> E[Filter: exclude PRs\nmasquerading as issues]
    E --> F[Deduplicate by issue number\nlatest event per issue wins]
    F --> G{Any remain?}
    G -- No --> Z
    G -- Yes --> H[For each issue]
    H --> I[Build email subject + body\nwith title, state, URL, labels, body]
    I --> J[gmail.send_mail\nsubject, body]
    I --> K[slack.send_message\ntext]
    J --> L[Increment notifications_sent]
    K --> L
    L --> H
    H -- Done --> M([Return notifications_sent])
```

---

## 4. Commit Notification Flow

```mermaid
flowchart TD
    A[_notify_commits\nraw_data, last_poll] --> B[Extract commits list\ndata.commits]
    B --> C{Any commits?}
    C -- No --> Z([Return 0])
    C -- Yes --> D[Filter: commit.author.date > last_poll]
    D --> E{Any remain?}
    E -- No --> Z
    E -- Yes --> F[For each commit]
    F --> G[Build email subject\ncommit message first line]
    G --> H[Build body:\nauthor, date, SHA, URL, full message]
    H --> I[gmail.send_mail]
    H --> J[slack.send_message]
    I --> K[Increment notifications_sent]
    J --> K
    K --> F
    F -- Done --> L([Return notifications_sent])
```

---

## 5. Pull Request Notification Flow

```mermaid
flowchart TD
    A[_notify_prs\nraw_data, last_poll] --> B[Extract PRs list\ndata.pull_requests]
    B --> C{Any PRs?}
    C -- No --> Z([Return 0])
    C -- Yes --> D[Filter: updated_at > last_poll]
    D --> E{Any remain?}
    E -- No --> Z
    E -- Yes --> F[For each PR]
    F --> G[Fetch raw diff\nutil.fetch_url pr.diff_url]
    G --> H{Diff fetched?}
    H -- Yes --> I[Append diff to body]
    H -- No --> J[Body without diff]
    I --> K[Build email subject + full body\ntitle, state, author, URL, body, diff]
    J --> K
    K --> L[gmail.send_mail]
    K --> M[slack.send_message\ntruncated body]
    L --> N[Increment notifications_sent]
    M --> N
    N --> F
    F -- Done --> O([Return notifications_sent])
```

---

## 6. Composio SDK Execution Sequence

```mermaid
sequenceDiagram
    participant Monitor as GitHubMonitor
    participant Connector as GitHubConnector
    participant Wrapper as ComposioWrapper
    participant SDK as Composio SDK
    participant GH as GitHub API (via Composio)

    Monitor->>Connector: poll(last_poll_time)
    loop For each slug in GH_POLL_SLUGS
        Connector->>Wrapper: execute(slug, {owner, repo, since, ...})
        Wrapper->>SDK: tools.execute(slug, arguments, user_id)
        SDK->>GH: HTTP GET /repos/{owner}/{repo}/...?since=...
        GH-->>SDK: JSON response
        SDK-->>Wrapper: {data: {...}, successful: true}
        Wrapper-->>Connector: response dict
    end
    Connector-->>Monitor: {slug: response, ...}
```

---

## 7. Notification Delivery Sequence

```mermaid
sequenceDiagram
    participant Monitor as GitHubMonitor
    participant Gmail as GmailConnector
    participant Slack as SlackConnector
    participant Wrapper as ComposioWrapper
    participant SDK as Composio SDK
    participant GmailAPI as Gmail API (via Composio)
    participant SlackAPI as Slack API (via Composio)

    Monitor->>Gmail: send_mail(subject, body)
    Gmail->>Wrapper: execute(GMAIL_SEND_EMAIL, {to, from, subject, body}, override_user_id)
    Wrapper->>SDK: tools.execute(slug, args, user_id=gmail_user_id)
    SDK->>GmailAPI: Send email
    GmailAPI-->>SDK: Success
    SDK-->>Wrapper: {successful: true}
    Wrapper-->>Gmail: response
    Gmail-->>Monitor: done

    Monitor->>Slack: send_message(text)
    Slack->>Wrapper: execute(SLACK_SEND_MESSAGE, {channel, text})
    Wrapper->>SDK: tools.execute(slug, args, user_id=slack_user_id)
    SDK->>SlackAPI: Post message
    Note over SlackAPI: Currently non-functional\n(Composio connectivity issue)
    SlackAPI-->>SDK: Error
    SDK-->>Wrapper: {successful: false}
    Wrapper-->>Slack: error response
    Slack-->>Monitor: logged, continue
```

---

## 8. Memory / State Management

```mermaid
stateDiagram-v2
    [*] --> Loaded: Memory.__init__\nLoad notified_ids.json

    Loaded --> PollCycleStart: check_for_updates called

    PollCycleStart --> Reading: get_last_poll_time()
    Reading --> Polling: Returns ISO8601 timestamp

    Polling --> NotificationsSent: notifications_sent > 0
    Polling --> NoUpdate: notifications_sent == 0

    NotificationsSent --> Writing: set_last_poll_time(start_ts)
    Writing --> PollCycleStart: Updated\nnotified_ids.json saved

    NoUpdate --> PollCycleStart: Timestamp unchanged\nRetry on next cycle
```

---

## 9. System Startup Sequence

```mermaid
sequenceDiagram
    participant Main as main.py
    participant Exec as Executor
    participant Monitor as GitHubMonitor
    participant Mem as Memory
    participant GHConn as GitHubConnector
    participant Wrapper as ComposioWrapper
    participant Gmail as GmailConnector
    participant Slack as SlackConnector

    Main->>Main: Configure TimedRotatingFileHandler
    Main->>Exec: Executor()
    Exec->>Monitor: GitHubMonitor()
    Monitor->>Mem: Memory()
    Mem->>Mem: Load notified_ids.json\n(or create with defaults)
    Monitor->>GHConn: GitHubConnector()
    GHConn->>GHConn: Init Composio(api_key)
    Monitor->>Wrapper: ComposioWrapper()
    Wrapper->>Wrapper: Init Composio(api_key, toolkit_versions)
    Monitor->>Gmail: GmailConnector(wrapper)
    Monitor->>Slack: SlackConnector(wrapper)
    Monitor-->>Exec: Ready
    Exec-->>Main: Ready
    Main->>Main: Start infinite loop
```
