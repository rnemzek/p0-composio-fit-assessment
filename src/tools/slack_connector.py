import os
import logging
from src.utils.util import loadenv
loadenv()

class SlackConnector:
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")
        self.override_user_id = os.getenv("SLACK_USER_ID")
        self.logger = logging.getLogger(os.getenv("COMPOSIO_P0_LOGGER_NAME", "agent_logger"))

    def send_message(self, text):
        if not self.channel_id:
            self.logger.error("SLACK_CONNECTOR: Missing SLACK_CHANNEL_ID in environment!")
            return None

        return self.wrapper.execute(
            slug="SLACK_SEND_MESSAGE",
            arguments={"channel": self.channel_id, "text": text},
            override_user_id=self.override_user_id
        )
