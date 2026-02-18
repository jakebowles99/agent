#!/usr/bin/env python3
"""
Cleanup script to rename badly-named Teams chat files and ensure people profiles exist.

Fixes files like:
- oneOnOne-19_4260f6a8-d30aa949.md -> tayo-eletu-odibo.md
- chat-19_b8f772f76c9b43c29a26c5f0695b1055.md -> [group-name].md
"""

import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

KNOWLEDGE_PATH = Path("knowledge")
TEAMS_PATH = KNOWLEDGE_PATH / "teams"
PEOPLE_PATH = KNOWLEDGE_PATH / "people"


def name_to_kebab(name: str) -> str:
    """Convert a name to kebab-case."""
    cleaned = re.sub(r"[^a-zA-Z\s\-]", "", name)
    kebab = cleaned.lower().strip().replace(" ", "-")
    return re.sub(r"-+", "-", kebab)


def extract_people_from_content(content: str) -> list[dict]:
    """Extract people mentioned in a chat file."""
    people = []
    seen = set()

    # Match "## HH:MM - Name" pattern
    pattern = r"^## \d{2}:\d{2} - (.+)$"
    for match in re.finditer(pattern, content, re.MULTILINE):
        name = match.group(1).strip()
        if name and name not in seen and name.lower() not in ["system", "bot", "microsoft"]:
            seen.add(name)
            people.append({"name": name})

    return people


def determine_chat_name(content: str, filename: str) -> str | None:
    """Determine what the chat file should be named based on content."""
    people = extract_people_from_content(content)

    if not people:
        return None

    # Filter out Jake Bowles (the user)
    other_people = [p for p in people if "jake" not in p["name"].lower()]

    if len(other_people) == 1:
        # 1:1 chat - name after the other person
        return name_to_kebab(other_people[0]["name"])
    elif len(other_people) > 1:
        # Group chat - check if there's a topic in the header
        if "name:" in content.lower():
            # Try to extract group name from header
            name_match = re.search(r"\(name:\s*([^)]+)\)", content)
            if name_match and name_match.group(1).strip().lower() != "null":
                return name_to_kebab(name_match.group(1).strip())

        # Otherwise, create name from participants
        names = sorted([name_to_kebab(p["name"]) for p in other_people[:3]])
        return "-".join(names) + "-group"

    return None


def ensure_person_profile(name: str, interaction_note: str = None) -> bool:
    """Ensure a person has a profile, create if missing."""
    filename = name_to_kebab(name) + ".md"
    filepath = PEOPLE_PATH / filename

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if filepath.exists():
        # Update with interaction note if provided
        if interaction_note:
            content = filepath.read_text()
            if interaction_note not in content:
                if "## Recent interactions" in content:
                    parts = content.split("## Recent interactions")
                    updated = parts[0] + "## Recent interactions\n- **" + now + ":** " + interaction_note + parts[1]
                else:
                    updated = content.rstrip() + f"\n\n## Recent interactions\n- **{now}:** {interaction_note}\n"

                # Update last updated date
                updated = re.sub(r"\*Last Updated: \d{4}-\d{2}-\d{2}\*", f"*Last Updated: {today}*", updated)
                filepath.write_text(updated)
                return True
        return False

    # Create new profile
    PEOPLE_PATH.mkdir(parents=True, exist_ok=True)

    content = f"""# {name}

## Basic Info
- **Role**: Unknown
- **Company**: Unknown
- **Type**: Unknown

## Recent interactions
- **{now}:** {interaction_note or "Found in Teams chat history"}

---
*Last Updated: {today}*
"""
    filepath.write_text(content)
    return True


def process_chat_files(dry_run: bool = True):
    """Process and rename badly-named chat files."""
    # Find all badly-named files
    bad_patterns = ["oneOnOne-19_", "chat-19_"]

    renames = []
    people_to_create = []

    for date_dir in TEAMS_PATH.iterdir():
        if not date_dir.is_dir():
            continue

        for file in date_dir.iterdir():
            if not file.suffix == ".md":
                continue

            is_bad = any(file.name.startswith(p) for p in bad_patterns)
            if not is_bad:
                continue

            content = file.read_text()
            new_name = determine_chat_name(content, file.name)

            if new_name:
                new_path = file.parent / f"{new_name}.md"
                renames.append((file, new_path, content))

                # Collect people for profile creation
                for person in extract_people_from_content(content):
                    if "jake" not in person["name"].lower():
                        people_to_create.append(person["name"])

    # Report findings
    print(f"\n{'='*60}")
    print(f"CLEANUP REPORT {'(DRY RUN)' if dry_run else ''}")
    print(f"{'='*60}\n")

    print(f"Found {len(renames)} files to rename:\n")
    for old, new, _ in renames:
        print(f"  {old.parent.name}/{old.name}")
        print(f"    -> {new.name}")
        if new.exists():
            print(f"    ⚠️  Target exists - will merge content")
        print()

    unique_people = sorted(set(people_to_create))
    existing = [p for p in unique_people if (PEOPLE_PATH / f"{name_to_kebab(p)}.md").exists()]
    missing = [p for p in unique_people if p not in existing]

    print(f"\nPeople found: {len(unique_people)}")
    print(f"  Already have profiles: {len(existing)}")
    print(f"  Need profiles created: {len(missing)}")
    if missing:
        print(f"    - " + "\n    - ".join(missing))

    if dry_run:
        print(f"\n{'='*60}")
        print("Run with --execute to apply changes")
        print(f"{'='*60}\n")
        return

    # Execute changes
    print(f"\n{'='*60}")
    print("EXECUTING CHANGES...")
    print(f"{'='*60}\n")

    # Rename files
    for old, new, content in renames:
        if new.exists():
            # Merge content
            existing_content = new.read_text()
            merged = existing_content.rstrip() + "\n\n" + content
            new.write_text(merged)
            old.unlink()
            print(f"✓ Merged and deleted: {old.name} -> {new.name}")
        else:
            old.rename(new)
            print(f"✓ Renamed: {old.name} -> {new.name}")

    # Create missing people profiles
    for person in missing:
        created = ensure_person_profile(person, "Found in Teams chat history (cleanup)")
        if created:
            print(f"✓ Created profile: {name_to_kebab(person)}.md")

    print(f"\n{'='*60}")
    print("CLEANUP COMPLETE")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    dry_run = "--execute" not in sys.argv
    process_chat_files(dry_run=dry_run)
