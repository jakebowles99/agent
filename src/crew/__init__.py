"""CrewAI-based autonomous monitoring system.

This module provides the CrewAI-based replacement for the Claude CLI
autonomous monitoring system. It uses the existing MCP server (personal-tools)
for Microsoft 365 and Harvest access.

Usage:
    # Run the monitoring crew
    python -m src.crew.run

    # Run insight generation
    python -m src.crew.insights daily
    python -m src.crew.insights weekly
    python -m src.crew.insights health
"""

from src.crew.crew import run_crew_with_context, create_crew
from src.crew.run import run_monitor
from src.crew.memory import get_memory, CrewMemory
from src.crew.insights import run_daily_digest, run_weekly_patterns, run_project_health

__all__ = [
    "run_monitor",
    "run_crew_with_context",
    "get_memory",
    "CrewMemory",
    "run_daily_digest",
    "run_weekly_patterns",
    "run_project_health",
]
