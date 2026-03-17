import os
from composio import Composio
from src.utils.util import loadenv
loadenv()

# 1. Initialize the Composio client
# Get your API key from https://app.composio.dev
composio_client = Composio(api_key=os.getenv("COMPOSIO_API_KEY")     # ak_EvkNio0ZMRVbP78ldFMG

# 2. Initiate the connection for Gmail
# user_id can be any unique string to identify this specific user/connection
connection = composio_client.connected_accounts.initiate(
    user_id="rnemzek_composio_poc",
    auth_config_id=os.getenv("GMAIL_AUTH_CONFIG_ID")                 # ac_y7qx4vMIQuQd
)

# 3. Print the link to open in your browser
print(f"Please visit this URL to authenticate Gmail: {connection.redirect_url}")

# 4. (Optional) Wait for the user to complete the authentication
print("Waiting for authentication...")
connected_account = connection.wait_for_connection(timeout=60)

if connected_account.status == "ACTIVE":
    print("Gmail successfully connected!")
