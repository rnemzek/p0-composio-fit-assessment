import os
from composio import Composio
from src.utils.util import loadenv
loadenv()

def test_github_0111():
    api_key = os.getenv("COMPOSIO_API_KEY")
    repo_full_name = os.getenv("GH_REPO")
    owner, repo = repo_full_name.split('/')

    client = Composio(api_key=api_key)

    # In 0.11.1, these are the two primary candidates for the action string
    # Candidate A: github_issues_get_all
    # Candidate B: github_get_issues
    action_candidate = "github_issues_get_all"

    print(f"🚀 Phase 0: 0.11.1 Execution for {owner}/{repo}")

    try:
        # EXACT 0.11.1 Signature: execute(action_name, arguments, user_id)
        result = client.tools.execute(
            action_candidate,
            {
                "owner": owner,
                "repo": repo
            },
            user_id="default"
        )

        print(f"\n✅ SUCCESS! Target '{action_candidate}' hit the mark.")
        print(f"💎 Data: {result}")

    except Exception as e:
        print(f"\n❌ Candidate '{action_candidate}' failed: {e}")
        print("💡 Trying the secondary candidate: 'github_get_issues'...")

        try:
            result = client.tools.execute(
                "github_get_issues",
                {"owner": owner, "repo": repo},
                user_id="default"
            )
            print(f"\n✅ SUCCESS! Target 'github_get_issues' worked.")
            print(f"💎 Data: {result}")
        except Exception as e2:
            print(f"❌ Both candidates failed. Error: {e2}")

if __name__ == "__main__":
    test_github_0111()
