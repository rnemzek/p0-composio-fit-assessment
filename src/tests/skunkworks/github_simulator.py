import argparse
import os
from composio import Composio # Drop 'App'
from src.utils.util import loadenv
loadenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
USER_ID = os.getenv("GMAIL_ACCOUNT_USER_ID")     # rnemzek_composio_poc

# The Streaming IMDB-Killer Repo
REPO_OWNER = "rnemzek"
REPO_NAME = "streaming-service-search-engine"

def trigger_github_event(action):
    print(f"🚀 Simulating {action}...")


    if action in ["issue", "all"]:
        composio.tools.execute(
            user_id=USER_ID,
            slug="GITHUB_CREATE_ISSUE",
            # Gemmy Fix #1
            dangerously_skip_version_check=True,
            arguments={"owner": REPO_OWNER, "repo": REPO_NAME, "title": "POC Test Issue", "body": "Testing Webhooks!"}
        )
        print("✅ Issue Created")

    if action in ["commit", "all"]:
        composio.tools.execute(
            user_id=USER_ID,
            slug="GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS",
            # Gemmy Fix #2
            dangerously_skip_version_check=True,
            arguments={
                "owner": REPO_OWNER, "repo": REPO_NAME,
                "path": "poc_test.txt", "message": "Triggering Commit Webhook",
                "content": "SGVsbG8gQ29tcG9zaW8h" # "Hello Composio!" in base64
            }
        )
        print("✅ File Committed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["issue", "pr", "commit", "all"])
    args = parser.parse_args()
    trigger_github_event(args.action)
