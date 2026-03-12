### Instructions for setting up the test POC environment

##  Environment Setup

#   Core / Config                                             
                                                                                                                        
  ┌────────────────────────────────────┬──────────────────────────────────────────────────────────────┐                 
  │              Variable              │                           Purpose                            │                 
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────────┤                 
  │ COMPOSIO_P0_DIR                    │ Required. Root directory path (raises ValueError if missing) │                 
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ COMPOSIO_P0_LOGGER_NAME            │ Logger name used across all modules                          │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ COMPOSIO_P0_LOG_NAME               │ Log file name                                                │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ COMPOSIO_P0_LOG_CONFIG_WHEN        │ Log rotation interval type (e.g. midnight)                   │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ COMPOSIO_P0_LOG_CONFIG_INTERVAL    │ Log rotation interval value                                  │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ COMPOSIO_P0_LOG_CONFIG_BACKUPCOUNT │ Number of log backups to keep                                │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ COMPOSIO_P0_LOG_CONFIG_ENCODING    │ Log file encoding                                            │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ COMPOSIO_MAIN_LOOP_DELAY           │ Poll loop delay in seconds (default: 10)                     │
  └────────────────────────────────────┴──────────────────────────────────────────────────────────────┘

  Composio API

  ┌──────────────────┬─────────────────────────────┐
  │     Variable     │           Purpose           │
  ├──────────────────┼─────────────────────────────┤
  │ COMPOSIO_API_KEY │ Composio authentication key │
  ├──────────────────┼─────────────────────────────┤
  │ COMPOSIO_USER_ID │ Composio user ID            │
  └──────────────────┴─────────────────────────────┘

  GitHub

  ┌────────────────────┬──────────────────────────────────────────────────────────────────────────┐
  │      Variable      │                              Purpose                                    │
  ├────────────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ GH_REPO_OWNER      │ GitHub repo owner/org                                                    │
  ├────────────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ GH_REPO_NAME       │ GitHub repo name                                                         │
  ├────────────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ GH_REPO            │ Full repo reference (used in some tests/scripts)                         │
  ├────────────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ GH_POLL_SLUGS      │ Comma-separated list of Composio slugs to poll                           │
  ├────────────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ GH_VERSION         │ GitHub Composio app version                                              │
  ├────────────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ GH_PR_DIFF_BASE_URL│ Base URL for fetching PR diffs (e.g. https://github.com).               │
  │                    │ Full URL built as {base}/{owner}/{repo}/pull/{number}.diff                │
  └────────────────────┴──────────────────────────────────────────────────────────────────────────┘

  Gmail

  ┌───────────────────────────────────────────┬─────────────────────────────────────────────────────────────┐
  │                 Variable                  │                           Purpose                           │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID │ Gmail Composio connection account ID                        │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_TO                                  │ Recipient email address                                     │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_FROM                                │ Sender display name + address (e.g. "Bot <addr@gmail.com>") │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_SLUG                                │ Gmail Composio action slug                                  │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_BOT_VERSION                         │ Gmail Composio app version (used in tests)                  │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_VERSION                             │ Gmail Composio app version (used in composio_wrapper.py)    │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_USER                                │ Gmail username (skunkworks/direct SMTP test only)           │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_APP_PASSWORD                        │ Gmail app password (skunkworks/direct SMTP test only)       │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_ACCOUNT_USER_ID                     │ Gmail account user ID (skunkworks scripts)                  │
  ├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ GMAIL_AUTH_CONFIG_ID                      │ Gmail auth config ID (skunkworks gmail_auth.py)             │
  └───────────────────────────────────────────┴─────────────────────────────────────────────────────────────┘

  Slack

  ┌──────────────────┬────────────────────────────┐
  │     Variable     │          Purpose           │
  ├──────────────────┼────────────────────────────┤
  │ SLACK_CHANNEL_ID │ Slack channel to post to   │
  ├──────────────────┼────────────────────────────┤
  │ SLACK_USER_ID    │ Slack user ID              │
  ├──────────────────┼────────────────────────────┤
  │ SLACK_VERSION    │ Slack Composio app version │
  └──────────────────┴────────────────────────────┘

  ---
  Note: Variables under GMAIL_USER, GMAIL_APP_PASSWORD, GMAIL_ACCOUNT_USER_ID, GMAIL_AUTH_CONFIG_ID are only used in
  skunkworks/experimental scripts, not in the main application flow. Slack vars are present but Slack connectivity is
  currently non-functional.
