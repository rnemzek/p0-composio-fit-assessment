import time
import os
import logging
from src.agents.executor import Executor

# Ensure logs directory exists at project root
os.makedirs("logs", exist_ok=True)
LOG_PATH = "logs/agent_activity.log"

# Force configuration to ensure it writes immediately
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
    force=True 
)
logger = logging.getLogger("agent_logger")

def main():
    logger.info("🚀 SYSTEM: Big Sexy's Agentic POC is waking up...")
    
    try:
        # Initialize the Executor (which holds your Faux tools)
        agent_executor = Executor()
        
        while True:
            logger.info("SYSTEM: Starting execution cycle...")
            agent_executor.run_cycle()
            
            delay = 10 # 10 seconds for the POC
            logger.info(f"SYSTEM: Cycle complete. Sleeping for {delay}s...")
            time.sleep(delay)
            
    except Exception as e:
        logger.error(f"SYSTEM FAILURE: {str(e)}")
    except KeyboardInterrupt:
        logger.info("SYSTEM: Shutdown signal received. Peace out.")

if __name__ == "__main__":
    main()

