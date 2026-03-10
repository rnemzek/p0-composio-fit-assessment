import os
import logging
from composio import Composio
from src.utils.util import Util

logger = logging.getLogger(os.environ.get("COMPOSIO_P0_LOGGER_NAME", "agent_logger"))


class GitHubConnector:
    def __init__(self):
        self.composio = Composio(api_key=os.environ.get("COMPOSIO_API_KEY"))
        self.user_id = os.environ.get("GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID")
        self.repo_owner = os.environ.get("GH_REPO_OWNER")
        self.repo_name = os.environ.get("GH_REPO_NAME")
        self.util = Util()

    def poll(self, since_ts):
        """
        Poll GitHub for all configured event types since since_ts.

        Reads GH_POLL_SLUGS env var (comma-separated slugs) and executes each.
        GITHUB_LIST_COMMITS is handled separately — it does not accept a 'state' arg.

        Returns: dict of {slug: response} for every configured slug.
                 A slug's value is None if that call failed.
        """
        github_slugs = self.util.get_environ_variable_as_array("GH_POLL_SLUGS")
        logger.info(f"GH_CONNECTOR: polling {len(github_slugs)} slug(s) since [{since_ts}]")

        results = {}
        for slug in github_slugs:
            slug = slug.strip()
            logger.info(f"GH_CONNECTOR: executing [{slug}]")
            try:
                if slug != "GITHUB_LIST_COMMITS":
                    response = self.composio.tools.execute(
                        user_id=self.user_id,
                        slug=slug,
                        dangerously_skip_version_check=True,
                        arguments={
                            "owner": self.repo_owner,
                            "repo": self.repo_name,
                            "since": since_ts,
                            "state": "all",
                            "per_page": 100
                        }
                    )
                else:
                    # GITHUB_LIST_COMMITS does not accept a 'state' argument
                    response = self.composio.tools.execute(
                        user_id=self.user_id,
                        slug=slug,
                        dangerously_skip_version_check=True,
                        arguments={
                            "owner": self.repo_owner,
                            "repo": self.repo_name,
                            "since": since_ts
                        }
                    )
                results[slug] = response
            except Exception as e:
                logger.error(f"GH_CONNECTOR: [{slug}] execution failed: {e}")
                results[slug] = None

        return results


class FauxGitHubConnector:
    """Stub connector for local testing without a live GitHub connection."""
    def __init__(self):
        self.counter = 0

    def poll(self, since_ts):
        import datetime
        self.counter += 1
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        return {
            "FAUX_ISSUES": {"data": {"items": [{"type": "Issue", "id": self.counter, "title": f"Faux Issue at {ts}"}]}},
            "FAUX_PRS":    {"data": {"items": [{"type": "PR",    "id": self.counter, "title": f"Faux PR at {ts}"}]}}
        }
