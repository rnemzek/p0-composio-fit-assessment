import os
from src.utils.util import loadenv
loadenv()

import time
import logging
from logging.handlers import TimedRotatingFileHandler
from src.agents.executor import Executor

#---------- CONFIGURE LOGGER ---------- #

# 1. Grab base directory
project_dir = os.getenv("COMPOSIO_P0_DIR")
if not project_dir:
    raise ValueError("Big Sexy, you forgot to set 'COMPOSIO_P0_DIR'!")

log_dir = os.path.join(project_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

# 2. Grab environment variables for rotation
logger_name = os.getenv("COMPOSIO_P0_LOGGER_NAME", "agent_logger")
log_file_name = os.getenv("COMPOSIO_P0_LOG_NAME", "agent_activity.log")
log_config_when = os.getenv("COMPOSIO_P0_LOG_CONFIG_WHEN", "midnight")
log_config_interval = int(os.getenv("COMPOSIO_P0_LOG_CONFIG_INTERVAL", 1))
log_config_backup_count = int(os.getenv("COMPOSIO_P0_LOG_CONFIG_BACKUPCOUNT", 7))
log_config_encoding = os.getenv("COMPOSIO_P0_LOG_CONFIG_ENCODING", "utf-8") # Fixed typo!

# 3. Setup the Logger
logger = logging.getLogger(logger_name)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

# 4. Create the Daily Rotating Handler
file_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, log_file_name),
    when=log_config_when,
    interval=log_config_interval,
    backupCount=log_config_backup_count,
    encoding=log_config_encoding
)

# 5. Create a Stream Handler (so you can see it in your terminal)
console_handler = logging.StreamHandler()

# 6. Apply formatting to both
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 7. Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("✅ SYSTEM: Logging initialized with daily rotation. Big Sexy is in the building!")

# ---------- START OF MAIN ---------- #

def main():
    logger.info("🚀 SYSTEM: Big Sexy's Agentic POC is waking up...")

    try:
        # Initialize the Executor
        agent_executor = Executor()

        while True:
            logger.info("SYSTEM: Starting execution cycle...")
            agent_executor.run_cycle()

            # Using your string-to-int skill here!
            delay = int(os.getenv("COMPOSIO_MAIN_LOOP_DELAY", 10))
            logger.info(f"SYSTEM: Cycle complete. Sleeping for {delay}s...")
            time.sleep(delay)

    except Exception as e:
        logger.error(f"SYSTEM FAILURE: {str(e)}")
    except KeyboardInterrupt:
        logger.info("SYSTEM: Shutdown signal received. Peace out.")

if __name__ == "__main__":
    main()
