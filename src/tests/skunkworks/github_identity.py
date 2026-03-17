import os
from composio import Composio
from src.utils.util import loadenv
loadenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
USER_ID = os.getenv("GMAIL_ACCOUNT_USER_ID")     # rnemzek_composio_poc

def link_github():
    print(f"🚀 Initiating GitHub connection for: {USER_ID}")
    try:
        # THE FIX: Explicitly name the integration, no positional args
        connection = composio.connected_accounts.initiate(
            user_id=USER_ID,
            integration_id="github" # This is the magic keyword for 0.11.1
        )

        print(f"\n🔗 CLICK THIS LINK: {connection.redirect_url}")

        connected_account = connection.wait_for_connection(timeout=120)
        if connected_account.status == "ACTIVE":
            print(f"✅ SUCCESS! GitHub linked to {USER_ID}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    link_github()
