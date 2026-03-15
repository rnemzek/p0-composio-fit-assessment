import os
import logging
from datetime import datetime, timezone
from src.cognition.memory import Memory
from src.tools.github_connector import GitHubConnector
from src.tools.gmail_connector import GmailConnector
from src.tools.slack_connector import SlackConnector
from src.tools.composio_wrapper import ComposioWrapper
from src.utils.util import Util

logger = logging.getLogger(os.environ.get("COMPOSIO_P0_LOGGER_NAME", "agent_logger"))

ISSUE_EVENTS_SLUG = "GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY"
COMMITS_SLUG      = "GITHUB_LIST_COMMITS"
PR_SLUG           = "GITHUB_LIST_PULL_REQUESTS"


class GitHubMonitor:

    def __init__(self):
        self.memory = Memory()
        self.gh_connector = GitHubConnector()
        wrapper = ComposioWrapper()
        self.gmail = GmailConnector(wrapper)
        self.slack = SlackConnector(wrapper)
        self.util = Util()

    def check_for_updates(self):
        """
        Poll GitHub for new Issues, Pull Requests, and Commits.

        last_poll_time update logic:
          - Genuinely new events found → update last_poll_time to start_ts
          - Nothing new               → leave last_poll_time unchanged
        """

        # 1. Capture timestamps
        last_poll = self.memory.get_last_poll_time()
        start_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        logger.info(f"GH_MONITOR: scanning since [{last_poll}]")

        # 2. Delegate data pull to connector
        results = self.gh_connector.poll(last_poll)

        # 3. Dispatch notifications per slug; track genuine new activity
        notifications_sent = 0
        for slug, data in results.items():
            if data is not None and self.util.json_contains_data_items(data):
                if slug == ISSUE_EVENTS_SLUG:
                    notifications_sent += self._notify_issues(data, last_poll)
                elif slug == COMMITS_SLUG:
                    notifications_sent += self._notify_commits(data, last_poll)
                elif slug == PR_SLUG:
                    notifications_sent += self._notify_prs(data, last_poll)
            else:
                logger.info(f"GH_MONITOR: [{slug}] — no new events")

        # 4. Update last_poll_time only when genuinely new events were notified
        if notifications_sent > 0:
            self.memory.set_last_poll_time(start_ts)
            logger.info(f"GH_MONITOR: last_poll_time updated to [{start_ts}]")
        else:
            logger.info(f"GH_MONITOR: no new events — last_poll_time unchanged [{last_poll}]")

        logger.info(f"GH_MONITOR: cycle complete | notifications_sent={notifications_sent}")
        return notifications_sent > 0

    def _notify_issues(self, data, last_poll):
        """
        Send one Gmail notification per unique issue updated since last_poll.
        Returns the number of emails sent.
        """
        details = data.get("data", {}).get("details", [])

        # Keep only the latest event per issue number, filtered to updated_at > last_poll.
        # GitHub ignores our 'since' parameter for this endpoint, so we filter here.
        latest_by_issue = {}
        for detail in details:
            issue = detail.get("issue", {})
            issue_number = issue.get("number")
            if issue_number is None:
                continue
            if "pull_request" in issue:
                continue
            updated_at = issue.get("updated_at", "")
            if updated_at <= last_poll:
                continue
            existing = latest_by_issue.get(issue_number)
            if existing is None or updated_at > existing["issue"].get("updated_at", ""):
                latest_by_issue[issue_number] = detail

        if not latest_by_issue:
            logger.info(f"GH_MONITOR: [{ISSUE_EVENTS_SLUG}] — no new issues after filtering")
            return 0

        logger.info(f"GH_MONITOR: [{ISSUE_EVENTS_SLUG}] — {len(latest_by_issue)} new issue(s) found")
        pretty = self.util.pretty_json(data)
        logger.info(f"GH_MONITOR: payload:\n{pretty}")

        sent = 0
        for detail in latest_by_issue.values():
            try:
                issue            = detail.get("issue", {})
                issue_created_at = issue.get("created_at", "unknown")
                updated_at       = issue.get("updated_at") or issue.get("created_at", "unknown")
                html_url         = issue.get("html_url", "unknown")
                title            = issue.get("title", "(no title)")
                state            = issue.get("state", "unknown").upper()
                closed_at        = issue.get("closed_at")
                labels           = issue.get("labels", [])
                body_text        = issue.get("body") or ""

                # --- subject ---
                subject = f"Issue: {issue.get('number')} | {updated_at}"

                # --- state line ---
                if state == "CLOSED" and closed_at:
                    state_line = f"State: CLOSED ({closed_at})"
                else:
                    state_line = f"State: {state}"

                # --- labels (uppercase) ---
                label_lines = "\n".join(f"  {lbl.get('name', '').upper()}" for lbl in labels)

                # --- body preview ---
                body_preview = body_text[:200]

                email_body = (
                    f"Poll Time: {last_poll}\n"
                    f"Issue Created: {issue_created_at}\n"
                    f"Last Updated: {updated_at}\n"
                    f"Issue URL: {html_url}\n"
                    f"Title: {title}\n"
                    f"{state_line}\n"
                    f"Labels:\n{label_lines}\n"
                    f"\nBody: {body_preview}"
                )

                self.gmail.send_mail(subject=subject, body=email_body)
                self.slack.send_message(f"{subject}\n{email_body}")
                logger.info(f"GH_MONITOR: notified issue #{issue.get('number')} [{title}] via Gmail + Slack")
                sent += 1

            except Exception as e:
                logger.error(f"GH_MONITOR: failed to send email for issue: {e}")

        return sent

    def _notify_commits(self, data, last_poll):
        """
        Send one Gmail notification per commit since last_poll.
        Returns the number of emails sent.
        """
        commits = data.get("data", {}).get("commits", [])

        # Safety filter — GITHUB_LIST_COMMITS supports 'since' but guard anyway
        new_commits = [
            c for c in commits
            if c.get("commit", {}).get("author", {}).get("date", "") > last_poll
        ]

        if not new_commits:
            logger.info(f"GH_MONITOR: [{COMMITS_SLUG}] — no new commits after filtering")
            return 0

        logger.info(f"GH_MONITOR: [{COMMITS_SLUG}] — {len(new_commits)} new commit(s) found")
        pretty = self.util.pretty_json(data)
        logger.info(f"GH_MONITOR: payload:\n{pretty}")

        sent = 0
        for commit_item in new_commits:
            try:
                sha         = commit_item.get("sha", "unknown")
                html_url    = commit_item.get("html_url", "unknown")
                commit      = commit_item.get("commit", {})
                author_date = commit.get("author", {}).get("date", "unknown")
                author_name = commit.get("author", {}).get("name", "unknown")
                message     = commit.get("message", "(no message)")

                subject = f"Commit: {sha[:7]}"

                email_body = (
                    f"Poll Time: {last_poll}\n"
                    f"Commit Created: {author_date}\n"
                    f"Committed By: {author_name}\n"
                    f"Commit URL: {html_url}\n"
                    f"Message: {message}"
                )

                self.gmail.send_mail(subject=subject, body=email_body)
                self.slack.send_message(f"{subject}\n{email_body}")
                logger.info(f"GH_MONITOR: notified commit [{sha[:7]}] via Gmail + Slack")
                sent += 1

            except Exception as e:
                logger.error(f"GH_MONITOR: failed to send email for commit: {e}")

        return sent

    def _notify_prs(self, data, last_poll):
        """
        Send one Gmail + Slack notification per PR updated since last_poll.
        Returns the number of notifications sent.
        """
        pull_requests = data.get("data", {}).get("pull_requests", [])

        new_prs = [
            pr for pr in pull_requests
            if pr.get("updated_at", "") > last_poll
        ]

        if not new_prs:
            logger.info(f"GH_MONITOR: [{PR_SLUG}] — no new PRs after filtering")
            return 0

        logger.info(f"GH_MONITOR: [{PR_SLUG}] — {len(new_prs)} new PR(s) found")
        pretty = self.util.pretty_json(data)
        logger.info(f"GH_MONITOR: payload:\n{pretty}")

        sent = 0
        for pr in new_prs:
            try:
                number      = pr.get("number", "?")
                title       = pr.get("title", "(no title)")
                state       = pr.get("state", "unknown")
                created_at  = pr.get("created_at", "unknown")
                updated_at  = pr.get("updated_at", "unknown")
                html_url    = pr.get("html_url", "unknown")
                body_text   = pr.get("body") or ""
                created_by  = pr.get("head", {}).get("user", {}).get("login", "unknown")
                repo_full   = pr.get("base", {}).get("repo", {}).get("full_name", "unknown")

                body_preview = body_text[:200]

                # Fetch diff text directly from diff_url in PR response
                diff_text = ""
                diff_url = pr.get("diff_url", "")
                if diff_url:
                    try:
                        diff_text = self.util.fetch_url(diff_url)[:200]
                    except Exception as diff_err:
                        logger.warning(f"GH_MONITOR: failed to fetch diff for PR #{number}: {diff_err}")
                        diff_text = "(unavailable)"

                subject = f"{repo_full} | PR#{number} | {title[:20]}"

                email_body = (
                    f"Poll Time: {last_poll}\n"
                    f"PR Created: {created_at}\n"
                    f"PR Updated: {updated_at}\n"
                    f"PR Created by: {created_by}\n"
                    f"Repo: {repo_full}\n"
                    f"PR URL: {html_url}\n"
                    f"PR State: {state}\n"
                    f"Message: {body_preview}\n"
                    f"PR Diff:\n{diff_text}"
                )

                slack_body = (
                    f"PR: {number}\n"
                    f"Poll Time: {last_poll}\n"
                    f"PR Created: {created_at}\n"
                    f"PR Updated: {updated_at}\n"
                    f"PR Created By: {created_by}\n"
                    f"PR URL: {html_url}\n"
                    f"PR State: {state}\n"
                    f"Message: {body_preview}\n"
                    f"PR Diff:\n{diff_text}"
                )

                self.gmail.send_mail(subject=subject, body=email_body)
                self.slack.send_message(slack_body)
                logger.info(f"GH_MONITOR: notified PR #{number} [{title[:20]}] via Gmail + Slack")
                sent += 1

            except Exception as e:
                logger.error(f"GH_MONITOR: failed to send notification for PR: {e}")

        return sent
