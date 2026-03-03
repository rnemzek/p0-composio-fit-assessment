from openai import OpenAI
from src.tools.composio_wrapper import ComposioWrapper

class Researcher:
    def __init__(self):
        self.client = OpenAI() # Pulls OPENAI_API_KEY from your env
        self.composio_wrapper = ComposioWrapper()
        self.github_tools = self.composio_wrapper.get_github_tools()
        
    def check_repository(self, repo_path):
        """
        Queries GitHub for the latest issues and PRs.
        """
        prompt = f"""
        Access the repository '{repo_path}'. 
        Fetch the most recent Issues and Pull Requests.
        Identify any items that have been created or updated recently.
        Return a clean list of the titles, authors, and brief descriptions.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            tools=self.github_tools,
            messages=[
                {"role": "system", "content": "You are a Technical Researcher. Your goal is to monitor GitHub activity and provide concise technical summaries."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Executing the tool call via Composio
        result = self.composio_wrapper.toolset.handle_tool_calls(response)
        return result

