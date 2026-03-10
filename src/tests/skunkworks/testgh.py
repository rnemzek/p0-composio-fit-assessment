import os
import ast
from composio import Composio
from src.cognition.memory import Memory
from src.utils.util import Util

class GitHubTest:
    def __init__(self):
        self.memory = Memory()
        self.composio = Composio(api_key=(os.environ.get("COMPOSIO_API_KEY")))
        self.user_id = os.environ.get("GMAIL_COMPOSIO_CONNECTION_ACCOUNT_USER_ID")
        self.repo_owner = os.environ.get("GH_REPO_OWNER")
        self.repo_name = os.environ.get("GH_REPO_NAME")
    
    def run_test_issues(self): 
        response = self.composio.tools.execute(
            user_id=self.user_id,
            slug="GITHUB_LIST_ISSUE_EVENTS_FOR_A_REPOSITORY",
            dangerously_skip_version_check=True,
            arguments={
                "owner": self.repo_owner,
                "repo": self.repo_name,
                "since": self.memory.get_last_poll_time(),
                "state": "all"
             }
        )

        if response is not None:
            util = Util()
            pretty_json = util.pretty_json(response)
            print(f"PRETTY JSON\n{pretty_json}")
        else:
            print("Response was None")

    def run_test(self): 
        # set up last_poll_date
        last_poll_time = self.memory.get_last_poll_time()
        print(f"last poll time: {last_poll_time}")

        # set up Util
        util = Util()

        # initialize response array
        response = {}

        # set up slugs array
        github_slugs = util.get_environ_variable_as_array("GH_POLL_SLUGS")
        print(f"github_slugs = {github_slugs}")
        
        # loop thru pulling events for each slug"	
        for slug in github_slugs:
            print(f"⚙️  pulling for events of type {slug}")
            if slug != "GITHUB_LIST_COMMITS":                  # GITHUB_LIST_COMMITS don't have a state
                response[slug] = self.composio.tools.execute(
                    user_id=self.user_id,
                    slug=slug,
                    dangerously_skip_version_check=True,
                    arguments={
                        "owner": self.repo_owner,
                        "repo": self.repo_name,
                        "since": last_poll_time,
                        "state": "all",
                        # "sort": "created_at",
                        # "direction": "desc",
                        "per_page": 100
                     }
                )
            else:
                # GITHUB_LIST_COMMITS does not have a concept of "state" so it needs its own execute
                response[slug] = self.composio.tools.execute(
                    user_id=self.user_id,
                    slug=slug,
                    dangerously_skip_version_check=True,
                    arguments={
                        "owner": self.repo_owner,
                        "repo": self.repo_name,
                        "since": last_poll_time
                     }
                )

        for slug in github_slugs:
            data = response[slug]
            if response[slug] is not None:
                if util.json_contains_data_items(data):
                    pretty_json = util.pretty_json(response[slug])
                    print(f"✅ {slug}: pretty json\n{pretty_json}")
                else:
                    print(f"❌ {slug}: had no events found")
            else: 
                print(f"❌ {slug}: had not events found" )

print("Starting run_test....🚀")
gh = GitHubTest()
gh.run_test() 
print("Done run_test\n")

