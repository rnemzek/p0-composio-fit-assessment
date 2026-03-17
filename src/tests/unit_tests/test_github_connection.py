import os
from composio import Composio
from src.utils.util import loadenv
loadenv()

def test_github_direct():
    composio_api_key = os.getenv("COMPOSIO_API_KEY")
    repo_full_name = os.getenv("GH_REPO")

    print(f"🔑 Composio Key Found: {'✅ Yes' if composio_api_key else '❌ No'}")
    print(f"📁 GH_REPO Found: {'✅ Yes' if repo_full_name else '❌ No'}")

    if not composio_api_key:
        print("\n❌ Error: Still missing COMPOSIO_API_KEY. Check .env.")
        return

    if not repo_full_name:
        print("\n❌ Error: Still missing GH_REPO. Check .env in project root.")
        return

    # Split the repo (e.g., "rnemzek/repo" -> "rnemzek", "repo")
    owner, repo = repo_full_name.split('/')

    print(f"\n🛠️ Testing Direct GitHub Action for {owner}/{repo}")

    # 4. Initialize and Execute
    client = Composio(api_key=composio_api_key)

    try:
        # Use lowercase string for action as per Composio 0.11.1
        # Use ToolName_ActionName
        output = client.tools.execute(
#            "GITHUB_LIST_REPOSITORY_ISSUES",
            "GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY",
            arguments={
                "owner": owner,
                "repo": repo
            }
        )
        print("\n✅ Success!")

    # Since we know there's 1 issue, let's print it specifically
        if isinstance(output, list) and len(output) > 0:
            issue = output[0]
            print(f"📌 Found Issue #{issue.get('number')}: {issue.get('title')}")
            print(f"📝 State: {issue.get('state')}")
        else:
            print(f"🤷 Found the repo, but the issue list is empty: {output}")
            return

        print("\n✅ Success! GitHub Connection Verified.")
        print(f"Latest activity found: {output}")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_github_direct()
