import datetime
import logging

logger = logging.getLogger("agent_logger")

class FauxGitHubConnector:
    def __init__(self):
        self.counter = 0

    def poll_updates(self):
        self.counter += 1
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        # Returns dummy data for the Agent to process
        return [
            {"type": "Issue", "id": self.counter, "title": f"Faux Issue A at {ts}"},
            {"type": "PR", "id": self.counter, "title": f"Faux PR B at {ts}"}
        ]

