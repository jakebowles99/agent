"""Enhanced memory layer for CrewAI.

CrewAI has built-in memory, but we add persistence and structure:
- Short-term: Recent run context (last few runs)
- Long-term: Patterns detected over time
- Entity memory: People, projects, topics mentioned

Memory is stored in data/crew_memory.json and knowledge/patterns/
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Storage paths
DATA_DIR = Path("data")
MEMORY_FILE = DATA_DIR / "crew_memory.json"
PATTERNS_DIR = Path("knowledge/patterns")


class CrewMemory:
    """Persistent memory layer for the monitoring crew."""

    def __init__(self):
        self._ensure_dirs()
        self.data = self._load()

    def _ensure_dirs(self) -> None:
        """Ensure storage directories exist."""
        DATA_DIR.mkdir(exist_ok=True)
        PATTERNS_DIR.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict:
        """Load memory from disk."""
        if MEMORY_FILE.exists():
            try:
                return json.loads(MEMORY_FILE.read_text())
            except Exception as e:
                logger.error(f"Failed to load memory: {e}")
                return self._default_memory()
        return self._default_memory()

    def _default_memory(self) -> dict:
        """Return default memory structure."""
        return {
            "short_term": {
                "last_runs": [],  # Last 10 run summaries
                "pending_items": [],  # Items flagged but not yet resolved
            },
            "long_term": {
                "patterns": [],  # Detected patterns over time
                "statistics": {
                    "total_runs": 0,
                    "emails_processed": 0,
                    "messages_processed": 0,
                    "files_updated": 0,
                },
            },
            "entities": {
                "people": {},  # name -> {last_contact, context, importance}
                "projects": {},  # name -> {last_mention, status, notes}
                "topics": {},  # topic -> {frequency, last_seen}
            },
            "metadata": {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "version": "1.0",
            },
        }

    def save(self) -> None:
        """Save memory to disk."""
        self.data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        try:
            MEMORY_FILE.write_text(json.dumps(self.data, indent=2, default=str))
            logger.info("Memory saved successfully")
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")

    # ==================== SHORT-TERM MEMORY ====================

    def record_run(self, summary: dict) -> None:
        """Record a monitoring run in short-term memory.

        Args:
            summary: Dict with keys like emails_found, messages_found,
                    actions_taken, timestamp
        """
        summary["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.data["short_term"]["last_runs"].insert(0, summary)
        # Keep only last 10 runs
        self.data["short_term"]["last_runs"] = self.data["short_term"]["last_runs"][:10]

        # Update statistics
        stats = self.data["long_term"]["statistics"]
        stats["total_runs"] += 1
        stats["emails_processed"] += summary.get("emails_found", 0)
        stats["messages_processed"] += summary.get("messages_found", 0)
        stats["files_updated"] += summary.get("files_updated", 0)

        self.save()

    def get_last_run(self) -> dict | None:
        """Get the most recent run summary."""
        runs = self.data["short_term"]["last_runs"]
        return runs[0] if runs else None

    def get_recent_runs(self, count: int = 5) -> list[dict]:
        """Get recent run summaries."""
        return self.data["short_term"]["last_runs"][:count]

    def add_pending_item(self, item: dict) -> None:
        """Add an item that needs follow-up.

        Args:
            item: Dict with keys like type, description, source, deadline
        """
        item["added_at"] = datetime.now(timezone.utc).isoformat()
        item["resolved"] = False
        self.data["short_term"]["pending_items"].append(item)
        self.save()

    def resolve_pending_item(self, item_id: str) -> bool:
        """Mark a pending item as resolved."""
        for item in self.data["short_term"]["pending_items"]:
            if item.get("id") == item_id:
                item["resolved"] = True
                item["resolved_at"] = datetime.now(timezone.utc).isoformat()
                self.save()
                return True
        return False

    def get_pending_items(self) -> list[dict]:
        """Get all unresolved pending items."""
        return [
            item for item in self.data["short_term"]["pending_items"]
            if not item.get("resolved", True)
        ]

    # ==================== LONG-TERM MEMORY ====================

    def record_pattern(self, pattern: dict) -> None:
        """Record a detected pattern.

        Args:
            pattern: Dict with keys like type, description, evidence, confidence
        """
        pattern["detected_at"] = datetime.now(timezone.utc).isoformat()
        self.data["long_term"]["patterns"].append(pattern)
        # Keep last 100 patterns
        self.data["long_term"]["patterns"] = self.data["long_term"]["patterns"][-100:]
        self.save()

        # Also write to knowledge base
        self._write_pattern_to_knowledge(pattern)

    def _write_pattern_to_knowledge(self, pattern: dict) -> None:
        """Write pattern to knowledge/patterns/ for persistence."""
        now = datetime.now(timezone.utc)
        week_num = now.strftime("%Y-W%W")
        pattern_file = PATTERNS_DIR / f"weekly-{week_num}.md"

        entry = f"""
## {pattern.get('type', 'Unknown')} - {now.strftime('%Y-%m-%d %H:%M')}

**Description:** {pattern.get('description', 'No description')}

**Confidence:** {pattern.get('confidence', 'Unknown')}

**Evidence:**
{pattern.get('evidence', 'No evidence provided')}

---
"""
        # Append to weekly file
        try:
            if pattern_file.exists():
                existing = pattern_file.read_text()
                pattern_file.write_text(existing + entry)
            else:
                header = f"# Patterns Detected - Week {week_num}\n\n"
                pattern_file.write_text(header + entry)
        except Exception as e:
            logger.error(f"Failed to write pattern to knowledge base: {e}")

    def get_patterns(self, pattern_type: str | None = None) -> list[dict]:
        """Get detected patterns, optionally filtered by type."""
        patterns = self.data["long_term"]["patterns"]
        if pattern_type:
            patterns = [p for p in patterns if p.get("type") == pattern_type]
        return patterns

    def get_statistics(self) -> dict:
        """Get accumulated statistics."""
        return self.data["long_term"]["statistics"]

    # ==================== ENTITY MEMORY ====================

    def update_person(self, name: str, context: str, importance: str = "normal") -> None:
        """Update information about a person.

        Args:
            name: Person's name
            context: Recent interaction context
            importance: One of "high", "normal", "low"
        """
        people = self.data["entities"]["people"]
        now = datetime.now(timezone.utc).isoformat()

        if name not in people:
            people[name] = {
                "first_seen": now,
                "interactions": [],
            }

        people[name]["last_contact"] = now
        people[name]["importance"] = importance
        people[name]["interactions"].append({
            "timestamp": now,
            "context": context[:200],  # Truncate for storage
        })
        # Keep last 20 interactions per person
        people[name]["interactions"] = people[name]["interactions"][-20:]

        self.save()

    def get_person(self, name: str) -> dict | None:
        """Get stored information about a person."""
        return self.data["entities"]["people"].get(name)

    def update_project(self, name: str, status: str | None = None, notes: str | None = None) -> None:
        """Update information about a project.

        Args:
            name: Project name
            status: Current status
            notes: Any notes about recent activity
        """
        projects = self.data["entities"]["projects"]
        now = datetime.now(timezone.utc).isoformat()

        if name not in projects:
            projects[name] = {
                "first_seen": now,
                "updates": [],
            }

        projects[name]["last_mention"] = now
        if status:
            projects[name]["status"] = status
        if notes:
            projects[name]["updates"].append({
                "timestamp": now,
                "notes": notes[:200],
            })
            projects[name]["updates"] = projects[name]["updates"][-20:]

        self.save()

    def get_project(self, name: str) -> dict | None:
        """Get stored information about a project."""
        return self.data["entities"]["projects"].get(name)

    def record_topic(self, topic: str) -> None:
        """Record mention of a topic."""
        topics = self.data["entities"]["topics"]
        now = datetime.now(timezone.utc).isoformat()

        if topic not in topics:
            topics[topic] = {
                "first_seen": now,
                "frequency": 0,
            }

        topics[topic]["frequency"] += 1
        topics[topic]["last_seen"] = now

        self.save()

    def get_frequent_topics(self, min_frequency: int = 3) -> list[tuple[str, dict]]:
        """Get topics mentioned frequently."""
        topics = self.data["entities"]["topics"]
        frequent = [
            (name, data) for name, data in topics.items()
            if data.get("frequency", 0) >= min_frequency
        ]
        return sorted(frequent, key=lambda x: x[1]["frequency"], reverse=True)

    # ==================== CONTEXT FOR CREW ====================

    def get_context_for_run(self) -> dict:
        """Get relevant context for the current monitoring run.

        Returns a summary that can be provided to agents for context.
        """
        return {
            "last_run": self.get_last_run(),
            "pending_items": self.get_pending_items(),
            "recent_patterns": self.get_patterns()[-5:],
            "statistics": self.get_statistics(),
            "frequent_topics": dict(self.get_frequent_topics()[:10]),
        }


# Singleton instance
_memory_instance: CrewMemory | None = None


def get_memory() -> CrewMemory:
    """Get the singleton memory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = CrewMemory()
    return _memory_instance
