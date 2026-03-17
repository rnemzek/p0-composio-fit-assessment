import os
from composio import Composio
from src.utils.util import loadenv
loadenv()

def audit_my_tools():
    api_key = os.getenv("COMPOSIO_API_KEY")
    client = Composio(api_key=api_key)

    print("🔍 AUDIT: Fetching ALL enabled actions for your account...")

    try:
        # In 0.11.1, this returns the full list of what YOU have enabled
        actions = client.actions.get()

        # Filter for GitHub
        github_actions = [a for a in actions if "github" in a.get('name', '').lower() or "github" in a.get('slug', '').lower()]

        if not github_actions:
            print("❌ ZERO GitHub actions found. Is the GitHub App 'Enabled' in your dashboard?")
            return

        print(f"✅ Found {len(github_actions)} GitHub actions:")
        for a in github_actions[:15]: # Show the first 15
            # We check both 'name' and 'slug' keys because of the dict return type
            print(f" 👉 {a.get('slug') or a.get('name')}")

    except Exception as e:
        print(f"❌ Audit failed: {e}")

if __name__ == "__main__":
    audit_my_tools()
