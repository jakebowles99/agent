"""Entry point for CrewAI autonomous monitoring.

Run with: python -m src.crew.run
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone

from src.crew.crew import run_crew_with_context
from src.crew.memory import get_memory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def run_monitor() -> str:
    """Main entry point for the monitoring crew.

    This function:
    1. Loads memory context from previous runs
    2. Runs the CrewAI monitoring pipeline
    3. Records the run in memory
    4. Returns the result

    Returns:
        The result from the crew execution.
    """
    logger.info("=" * 50)
    logger.info(f"Monitor run starting: {datetime.now(timezone.utc).isoformat()}")
    logger.info("=" * 50)

    # Load memory for context
    memory = get_memory()
    context = memory.get_context_for_run()

    last_run = context.get("last_run")
    if last_run:
        logger.info(f"Last run was at: {last_run.get('timestamp', 'unknown')}")
    else:
        logger.info("This is the first run")

    pending = context.get("pending_items", [])
    if pending:
        logger.info(f"Pending items from previous runs: {len(pending)}")

    try:
        # Run the crew
        logger.info("Starting CrewAI monitoring crew...")
        result = run_crew_with_context()

        # Extract counts from result text
        result_str = str(result) if result else ""

        def _extract_count(label: str) -> int:
            """Extract a count from the result text like 'Emails: 35 new'."""
            import re
            pattern = rf"\*\*{label}:\*\*\s*(\d+)"
            match = re.search(pattern, result_str)
            return int(match.group(1)) if match else 0

        run_summary = {
            "status": "success",
            "emails_found": _extract_count("Emails"),
            "messages_found": _extract_count("Teams Chats"),
            "files_updated": _extract_count("People Profiles") + _extract_count("Project Profiles") + _extract_count("Client Profiles"),
            "result_preview": result_str[:500],
        }
        memory.record_run(run_summary)

        logger.info("=" * 50)
        logger.info("Monitor run completed successfully")
        logger.info("=" * 50)

        return result

    except Exception as e:
        logger.error(f"Monitor run failed: {e}", exc_info=True)

        # Record failed run
        memory.record_run({
            "status": "error",
            "error": str(e),
        })

        raise


def main():
    """CLI entry point."""
    try:
        result = run_monitor()
        print("\n" + "=" * 50)
        print("RESULT:")
        print("=" * 50)
        print(result)
        return 0
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
