# src/tools/gmail_connector.py
import os
import logging

class GmailConnector:
    def __init__(self, wrapper):
        self.wrapper = wrapper
        # Change this to match your .bash_profile variable
        self.default_to = os.environ.get("GMAIL_TO")
        self.logger = logging.getLogger(os.environ.get("COMPOSIO_P0_LOGGER_NAME", "agent_logger"))
        self.override_user_id = os.environ.get("GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID")
        self.from_header = os.environ.get("GMAIL_FROM")

    def send_mail(self, subject, body, to_email=None):
        recipient = to_email or self.default_to
        
        if not recipient:
            self.logger.error("GMAIL_CONNECTOR: No recipient email found in GMAIL_TO or arguments!")
            return None

        self.logger.info(f"GMAIL_TOOL: Sending email to {recipient}")

        try:
            args = {"to": recipient, "subject": subject, "body": body, "is_html": False}
            if self.from_header:
                args["from_email"] = self.from_header

            return self.wrapper.execute(
                slug="GMAIL_SEND_EMAIL",
                arguments=args,
# keep until i prove this works / override_user_id="rnemzek_composio_poc" # <--- The "Sameses" ID
                override_user_id=self.override_user_id
            )
        except Exception as e:
            self.logger.error(f"GMAIL_TOOL ERROR: {e}")
            raise

