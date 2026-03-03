import logging
from composio import Composio
from src.tools.github_connector import FauxGitHubConnector
#from src.tools.gmail_connector import FauxGmailConnector
from src.tools.gmail_connector import GmailConnector
from src.utils.util import getDateTimestamp

logger = logging.getLogger("agent_logger")
timestamp = getDateTimestamp()

class Executor:
    def __init__(self):
        # Initialize the REAL Composio client from your successful test
        self.composio = Composio(
            api_key="ak_NguOTc4AwH4s0Qu_KUQ7",
            toolkit_versions={"slack": "20260227_00"}
        )
        self.user_id = "pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003"
        
        # Keep the Faux tools for now
        self.gh = FauxGitHubConnector()
#        self.gm = FauxGmailConnector()
        self.gm = GmailConnector()

    def run_cycle(self):
        # 1. Poll the Faux GitHub Tool
        updates = self.gh.poll_updates()
        
        if updates:
            logger.info(f"EXECUTOR: Found {len(updates)} GitHub events.")
            
            # 2. TRIGGER REAL SLACK MESSAGE
            try:
                dateTimestamp = getDateTimestamp()
                msg = f"🚀 POC Alert " + timestamp + ": Detected {len(updates)} new GitHub issues! Check the log, Big Sexy."
                self.composio.tools.execute(
                    user_id=self.user_id,
                    slug="SLACK_SEND_MESSAGE",
                    arguments={
                        "channel": "C0AJ5QTA94Z",
                        "text": msg
                    }
                )
                logger.info("SLACK_TOOL: Message successfully sent to #composio-poc")
            except Exception as e:
                logger.error(f"SLACK_TOOL ERROR: {e}")

            # 3. Use the Faux Gmail Tool
            #self.gm.send_log_email(updates)
            # 3. Use the Faux Gmail Tool
            subject = "Composio 0.11.1 test: " + timestamp
            body = "This message was sent using the simplified Composio SDK."
            result = self.gm.send_mail(subject, body)
            
        return updates

