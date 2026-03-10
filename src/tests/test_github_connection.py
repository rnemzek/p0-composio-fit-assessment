import os
from pathlib import Path
from composio import Composio
from dotenv import load_dotenv

# 1. Explicitly find the .env in the PROJECT ROOT (two levels up from src/tests)
current_dir = Path(__file__).resolve().parent # src/tests
project_root = current_dir.parent.parent      # project-root/
env_path = project_root / ".env"

load_dotenv(dotenv_path=env_path)

def test_github_direct():
    # 2. Use os.environ.get to grab from the shell (.bash_profile)
    composio_api_key = os.environ.get("COMPOSIO_API_KEY")

    # 3. Use os.environ.get to grab from the loaded .env file
    repo_full_name = os.environ.get("GH_REPO")

    print(f"🔑 Composio Key Found: {'✅ Yes' if composio_api_key else '❌ No'}")
    print(f"📁 GH_REPO Found: {'✅ Yes' if repo_full_name else '❌ No'}")

    if not composio_api_key:
        print("\n❌ Error: Still missing COMPOSIO_API_KEY. Check .bash_profile.")
        return

    if not repo_full_name:
        print("\n❌ Error: Still missing GH_REPO. Should be in project root .env file. Check paths above.")
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

