import os
from composio import Composio

# Initialize with your COMPOSIO_API_KEY (starts with 'comp_')
composio = Composio(
    api_key="ak_NguOTc4AwH4s0Qu_KUQ7", 
    toolkit_versions={"slack": "20260227_00"}
)

try:
    # 1. REPLACE THE user_id BELOW with the full pg-test-... string from your terminal
    # 2. Ensure slug is SLACK_SEND_MESSAGE (or SLACK_CHAT_POST_MESSAGE if that fails)
    result = composio.tools.execute(
        user_id="pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003",
        slug="SLACK_SEND_MESSAGE",
        arguments={
            "channel": "C0AJ5QTA94Z",
            "text": "4th attemp: The onion is sauteed, the door is open, and the connection is ACTIVE! 🧅🚀"
        }
    )
    
    print(f"Success: {result}")

except Exception as e:
    print(f"Error: {e}")

