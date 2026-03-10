import os
import logging
from composio import Composio

class ComposioWrapper:
    def __init__(self):
        self.logger = logging.getLogger(os.environ.get("COMPOSIO_P0_LOGGER_NAME", "agent_logger"))
        
        # Grab the User ID from your .bash_profile
        self.user_id = os.environ.get("COMPOSIO_USER_ID")
        
        self.toolkit_versions = {
            "slack": os.environ.get("SLACK_VERSION", "20260227_00"),
            "github": os.environ.get("GH_VERSION", "20260227_00"),
            "gmail": os.environ.get("GMAIL_VERSION", "20260227_00")
        }
        
        self.client = Composio(
            api_key=os.environ.get("COMPOSIO_API_KEY"),
            toolkit_versions=self.toolkit_versions
        )
        self.logger.info(f"🛠️ WRAPPER: Initialized for User: {self.user_id}")

    def execute(self, slug, arguments, override_user_id=None):
        # Use override if provided, otherwise fallback to the default env var
        active_user_id = override_user_id or self.user_id
        
        try:
            return self.client.tools.execute(
                slug=slug, 
                arguments=arguments, 
                user_id=active_user_id
            )
        except Exception as e:
            self.logger.error(f"❌ EXECUTION_ERROR [{slug}] for User [{active_user_id}]: {e}")
            raise

# ---------- KEEP execute() Blocks ---------- #
#    def execute(self, slug, arguments):
#        try:
#            # For Tools.execute(), the parameter is 'user_id'
#            return self.client.tools.execute(
#                slug=slug, 
#                arguments=arguments, 
#                user_id=self.user_id  # <--- Changed from entity_id
#            )
#        except Exception as e:
#            self.logger.error(f"❌ EXECUTION_ERROR [{slug}]: {e}")
#            raise
#
#    def execute(self, slug, arguments):
#        try:
#            # Add entity_id here so Slack knows who is talking!
#            return self.client.tools.execute(
#                slug=slug, 
#                arguments=arguments, 
#                entity_id=self.user_id  # <--- THIS IS THE MISSING KEY
#            )
#        except Exception as e:
#            self.logger.error(f"❌ EXECUTION_ERROR [{slug}]: {e}")
#            raise
# ---------- END execute() Block   ---------- #

