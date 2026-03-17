import os
import logging
from src.utils.util import loadenv
loadenv()
from src.agents.github_monitor import GitHubMonitor

# Use the same logger name from your main.py config
logger = logging.getLogger(os.getenv("COMPOSIO_P0_LOGGER_NAME", "agent_logger"))

class Executor:
    def __init__(self):
        # 1. Initialize our specialized monitors
        # This keeps the logic for 'HOW' to poll GitHub inside the monitor
        try:
            self.gh_monitor = GitHubMonitor()
            logger.info("🛠️ EXECUTOR: GitHub Monitor initialized and linked.")
        except Exception as e:
            logger.error(f"🛠️ EXECUTOR: Failed to initialize GitHub Monitor: {e}")
            self.gh_monitor = None

    def run_cycle(self):
        """
        This is called by the while-loop in main.py.
        Every cycle, we check our various 'senses' (monitors).
        """
        logger.info("🎬 EXECUTOR: Starting execution cycle...")

        if self.gh_monitor:
            try:
                # 2. Check for new GitHub Issues/Events
                self.gh_monitor.check_for_updates()
            except Exception as e:
                logger.error(f"❌ EXECUTOR: GitHub check failed this cycle: {e}")
        else:
            logger.warning("⚠️ EXECUTOR: GitHub Monitor is offline, skipping check.")

        logger.info("🏁 EXECUTOR: Cycle complete.")
