import os
from composio import ComposioToolSet, App

class ComposioWrapper:
    def __init__(self):
        # Grabs the API key from your .bash_profile environment
        self.api_key = os.getenv("COMPOSIO_API_KEY")
        self.toolset = ComposioToolSet(api_key=self.api_key)

    def get_github_tools(self):
        """Returns tools needed for the Researcher agent."""
        return self.toolset.get_tools(apps=[App.GITHUB])

    def get_github_tool(self):
        toolset = ComposioToolSet()
        # No more App.GITHUB, just use the string "github"
        return toolset.get_tools(apps=["github"]) 


    def get_notification_tools(self):
        """Returns tools needed for the Executor agent (Slack + Gmail)."""
        return self.toolset.get_tools(apps=[App.SLACK, App.GMAIL])

    def execute_action(self, action_enum, params):
        """Helper to run a specific action directly if needed."""
        return self.toolset.execute_action(action=action_enum, params=params)

