import os
from composio import Composio
from src.utils.util import loadenv
loadenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
USER_ID = "rnemzek_composio_poc"

def verify():
    print(f"🕵️ Gemmy's Investigation: Can {USER_ID} see the repo?")
    try:
        # We'll try to 'Get Repository' - if this works, the connection is 100% live
        # GEMMY FIX: Use the lowercase slug
        result = composio.tools.execute(
            user_id=USER_ID,
            slug="github_get_repository", # Try lowercase 'get_repo'
            dangerously_skip_version_check=True,
            arguments={
                "owner": os.getenv("GMAIL_ACCOUNT_USER_ID"),     # rnemzek
                "repo": os.getenv("GH_REPO_NAME")                # streaming-service-search-engine
            }
        )
        # If we get a name back, the 'Pipe' is connected!
        repo_name = result.get('data', {}).get('full_name', 'Unknown')
        print(f"✅ VERIFIED: Found repository '{repo_name}'")
        print(f"🚀 Status: Your connection is LIVE and has permissions!")

    except Exception as e:
        print(f"❌ FAILED: {e}")
        print("Gemmy Tip: If you get a 404 here, you need to go to GitHub Settings -> Applications and ensure 'Composio' has access to this specific repo.")

if __name__ == "__main__":
    verify()
