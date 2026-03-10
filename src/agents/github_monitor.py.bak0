import os
import logging
import time
from composio import Composio  # The ONLY thing we need
from dotenv import load_dotenv

# Gemmy's Clean Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("GitHubMonitor")

load_dotenv()
# Initialize the base client
composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))

USER_ID = "rnemzek_composio_poc"
REPO_OWNER = "rnemzek" 
REPO_NAME = "streaming-service-search-engine"

def start_agent():
    # 1. Register Webhooks (Using the slugs that worked before)
    slugs = ["github_commit_event", "github_pull_request_event"]
    
    logger.info("📡 Registering Webhooks...")
    for slug in slugs:
        try:
            composio.triggers.create(
                slug=slug,
                user_id=USER_ID,
                trigger_config={"owner": REPO_OWNER, "repo": REPO_NAME}
            )
            logger.info(f"✅ Subscribed: {slug}")
        except Exception as e:
            logger.warning(f"Note for {slug}: {e}")

    # 2. The Manual Listener (The most stable way in 0.11.1)
    logger.info("🕵️ Starting Real-time Listener...")
    listener = composio.triggers.subscribe()

    @listener.handle()
    def on_github_event(event):
        # GEMMY FIX: Use getattr to safely handle metadata
        event_id = getattr(event, 'id', 'unknown')
        logger.info(f"🔔 ALERT: Received {event.trigger_slug} (ID: {event_id})!")
        
        try:
            # Let's simplify the payload for the first successful test
            summary = f"GitHub Activity: {event.trigger_slug}\n"
            summary += f"Check your repo: https://github.com{REPO_OWNER}/{REPO_NAME}"

            composio.tools.execute(
                user_id=USER_ID,
                slug="GMAIL_SEND_EMAIL",
                dangerously_skip_version_check=True, # Add this here too!
                arguments={
                    "to": "rnemzek+composio-poc@gmail.com",
                    "subject": f"🚩 GitHub Alert: {event.trigger_slug}",
                    "body": summary
                }
            )
            logger.info("📧 Gmail notification sent!")
        except Exception as e:
            logger.error(f"Gmail Error: {e}")

    logger.info("🕵️ Agent ACTIVE. Waiting for events... (Ctrl+C to stop)")
    
    # 3. The "Dead Man's Switch" to keep the script from exiting
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down Gemmy's Agent...")

if __name__ == "__main__":
    start_agent()

