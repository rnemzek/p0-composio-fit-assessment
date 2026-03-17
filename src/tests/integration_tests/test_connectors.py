import os
from src.tools.composio_wrapper import ComposioWrapper
from src.tools.slack_connector import SlackConnector
from src.tools.gmail_connector import GmailConnector
from src.utils.util import Util, loadenv
loadenv()

def test_regression():
    print("🚀 Starting Regression Test for Refactored Connectors...")

    # 1. Init Wrapper
    wrapper = ComposioWrapper()

    # 2. Init Connectors
    slack = SlackConnector(wrapper)
    gmail = GmailConnector(wrapper)

    ts = Util.getDateTimestamp()
    test_msg = f"Refactor Test @ {ts}: Connectors are looking Big Sexy!"

    print("--- Testing Slack ---")
    slack.send_message(test_msg)

    print("--- Testing Gmail ---")
    gmail.send_mail(f"Refactor Test {ts}", test_msg)

    print("\n✅ Regression Test Complete. Check your Slack and Inbox!")

if __name__ == "__main__":
    test_regression()
