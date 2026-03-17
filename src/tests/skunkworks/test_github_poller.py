import os
import time
from datetime import datetime, timezone
from composio import Composio
from src.utils.util import loadenv
loadenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))

# Configuration
USER_ID=os.getenv("GMAIL_ACCOUNT_USER_ID")     # rnemzek_composio_poc
GH_REPO_OWNER=os.getenv("GH_REPO_OWNER")       # rnemzek
GH_REPO_NAME=os.getenv("GH_REPO_NAME")         # streaming-service-search-engine
GH_POLL_INTERVAL=60                            # Seconds between polls

def poll_github_issues():
    # Initialize 'last_check' to current time or a past date for first run
    last_check = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    print(f"🚀 Starting Poller. Initial timestamp: {last_check}")

    while True:
        try:
            print(f"🔍 Polling for issues since {last_check}...")

            # Execute GitHub tool to list issues
            response = composio.tools.execute(
                user_id=USER_ID,
                slug="GITHUB_FOLLOWER_EVENT",
                arguments={
                    "owner": REPO_OWNER,
                    "repo": REPO_NAME,
                    "since": last_check,  # Filter for new/updated issues
                    "state": "all"
                }
            )

            # Process found issues
            issues = response.get("data", [])
            if issues:
                for issue in issues:
                    # Logic to handle only 'opened' issues if 'since' catches updates
                    print(f"🚩 New/Updated Issue Found: #{issue['number']} - {issue['title']}")
                    print(">>>>>Gonna try and print out issue ...")
                    print(">>>>>Issue: " + issue);
                    # Optional: Send Gmail Notification
                    # composio.tools.execute(user_id=USER_ID, slug="GMAIL_SEND_EMAIL", ...)

                # Update timestamp to the latest issue's updated_at time to avoid duplicates
                last_check = issues[0].get("updated_at", last_check)
            else:
                print("😴 No new issues found.")

        except Exception as e:
            print(f"❌ Polling Error: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    poll_github_issues()
