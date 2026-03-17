# Component Diagrams

All diagrams use [Mermaid](https://mermaid.js.org/) syntax.

---

## 1. Full Component Dependency Graph

```mermaid
graph TD
    subgraph EntryPoint["Entry Point"]
        MAIN[main.py]
    end

    subgraph Agents["Agents Layer"]
        EXEC[Executor\nexecutor.py]
        MON[GitHubMonitor\ngithub_monitor.py]
        RES[Researcher\nresearcher.py\n⚠️ dormant]
    end

    subgraph Cognition["Cognition Layer"]
        MEM[Memory\nmemory.py]
        JSON[(notified_ids.json)]
    end

    subgraph Tools["Tools Layer"]
        WRAP[ComposioWrapper\ncomposio_wrapper.py]
        GHC[GitHubConnector\ngithub_connector.py]
        GMAIL[GmailConnector\ngmail_connector.py]
        SLACK[SlackConnector\nslack_connector.py]
        FAUX[FauxGitHubConnector\n⚠️ stub/testing]
    end

    subgraph Utils["Utilities"]
        UTIL[util.py]
    end

    subgraph UI["UI"]
        VIZ[visualizer.py\nStreamlit]
        LOGS[(logs/agent_activity.log)]
    end

    subgraph External["External Services via Composio"]
        GHAPI[GitHub API]
        GMAILAPI[Gmail API]
        SLACKAPI[Slack API\n⚠️ deferred]
    end

    MAIN --> EXEC
    EXEC --> MON
    MON --> MEM
    MON --> GHC
    MON --> GMAIL
    MON --> SLACK
    MON --> UTIL
    MEM --> JSON
    GHC --> WRAP
    GMAIL --> WRAP
    SLACK --> WRAP
    WRAP --> GHAPI
    WRAP --> GMAILAPI
    WRAP --> SLACKAPI
    MAIN --> LOGS
    VIZ --> LOGS

    style RES fill:#ffe0b2,stroke:#e65100
    style FAUX fill:#ffe0b2,stroke:#e65100
    style SLACKAPI fill:#fce4ec,stroke:#c62828
    style SLACK fill:#fce4ec,stroke:#c62828
```

---

## 2. Module Dependency Graph (Import Map)

```mermaid
graph LR
    MAIN[main.py] -->|imports| EXEC[agents/executor.py]
    EXEC -->|imports| MON[agents/github_monitor.py]
    MON -->|imports| MEM[cognition/memory.py]
    MON -->|imports| GHC[tools/github_connector.py]
    MON -->|imports| GMAIL[tools/gmail_connector.py]
    MON -->|imports| SLACK[tools/slack_connector.py]
    MON -->|imports| UTIL[utils/util.py]
    GHC -->|imports| WRAP[tools/composio_wrapper.py]
    GHC -->|imports| UTIL
    GMAIL -->|imports| WRAP
    GMAIL -->|imports| UTIL
    SLACK -->|imports| WRAP
    SLACK -->|imports| UTIL
    WRAP -->|imports| composio[composio-openai SDK]
    GHC -->|imports| composio
```

---

## 3. Layered Architecture

```mermaid
graph TB
    subgraph L1["Layer 1: Entry Point"]
        MAIN[main.py\nLogger setup · Infinite loop · Graceful shutdown]
    end

    subgraph L2["Layer 2: Orchestration"]
        EXEC[Executor\nError isolation · Cycle management]
    end

    subgraph L3["Layer 3: Business Logic"]
        MON[GitHubMonitor\nPoll → Filter → Deduplicate → Notify]
    end

    subgraph L4["Layer 4: Cognition"]
        MEM[Memory\nPersistent state · last_poll_time · seen IDs]
    end

    subgraph L5["Layer 5: Tool Adapters"]
        GHC[GitHubConnector\nPoll slugs]
        GMAIL[GmailConnector\nSend email]
        SLACK[SlackConnector\nSend Slack msg]
        WRAP[ComposioWrapper\nUnified SDK client]
    end

    subgraph L6["Layer 6: External APIs"]
        GHAPI[GitHub API]
        GMAILAPI[Gmail API]
        SLACKAPI[Slack API]
    end

    L1 --> L2 --> L3
    L3 --> L4
    L3 --> L5
    L5 --> WRAP
    WRAP --> L6
```

---

## 4. Data Flow Diagram

```mermaid
flowchart LR
    GH[(GitHub API)] -->|issue events\ncommits\npull requests| Composio
    Composio -->|response envelope| GHC[GitHubConnector]
    GHC -->|raw data dict| MON[GitHubMonitor]
    MEM[(notified_ids.json)] -->|last_poll_time| MON
    MON -->|filter + deduplicate| MON
    MON -->|subject + body| GMAIL[GmailConnector]
    MON -->|text| SLACK[SlackConnector]
    GMAIL -->|GMAIL_SEND_EMAIL| Composio
    SLACK -->|SLACK_SEND_MESSAGE| Composio
    Composio -->|send| GMAILAPI[(Gmail API)]
    Composio -->|send| SLACKAPI[(Slack API)]
    MON -->|updated timestamp| MEM
    GH2[(GitHub\ndiff_url)] -->|raw diff text| MON
```

---

## 5. Testing Structure

```mermaid
graph TD
    subgraph Tests["src/tests/"]
        subgraph Integration["integration_tests/"]
            IT1[test_connectors.py]
            IT2[test_connectors_regression.py]
            IT3[test_full_regression.py]
            IT4[test_gmail_connection.py]
        end
        subgraph Unit["unit_tests/"]
            UT1[test_github_connection.py]
            UT2[test_message_slack.py]
            UT3[test_send_gmail.py]
            UT4[test_utils_raise_error.py]
        end
        subgraph Skunkworks["skunkworks/"]
            SW1[audit_gh.py\nList all GitHub actions]
            SW2[github_simulator.py\nCreate real test events]
            SW3[verify_github_link.py\nVerify OAuth connection]
            SW4[get_link.py · gmail_auth.py\nOAuth flow initiation]
            SW5[discover.py\nFind action name variants]
        end
    end
```

---

## 6. Composio Connection Account Map

```mermaid
graph LR
    subgraph Composio["Composio Platform"]
        UA[User Account A\nGMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID]
        UB[User Account B\nCOMPOSIO_USER_ID]
        UC[User Account C\nSLACK_USER_ID]
    end

    GHC[GitHubConnector] -->|override_user_id = Account A| UA
    GMAIL[GmailConnector] -->|override_user_id = Account A| UA
    SLACK[SlackConnector] -->|user_id = Account C| UC
    DEFAULT[Default calls] -->|user_id = Account B| UB

    UA --> GHAPI[GitHub OAuth connection]
    UA --> GMAILAPI[Gmail OAuth connection]
    UC --> SLACKAPI[Slack OAuth connection]
```

> **Note:** Account A holds both the GitHub and Gmail connections. The naming (`GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID`) is historical — it was named after the first connection established on that account.
