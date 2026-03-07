#!/usr/bin/env python3
import json
from pathlib import Path

def generate_marketplace():
    # Define paths
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / "skills"
    output_dir = repo_root / ".claude-plugin"
    output_file = output_dir / "marketplace.json"

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Initialize marketplace structure
    marketplace = {
        "name": "zephyr-agent-skills",
        "owner": "beriberikix",
        "plugins": {
            # Root plugin that installs everything via root SKILL.md
            "zephyr-skills": ".."
        }
    }

    # Scan for valid skills
    if skills_dir.exists():
        # Sort for deterministic output across filesystems/OS.
        for item in sorted(skills_dir.iterdir(), key=lambda p: p.name):
            if item.is_dir() and (item / "SKILL.md").exists():
                skill_name = item.name
                # Paths are relative to the marketplace.json file (.claude-plugin/marketplace.json)
                marketplace["plugins"][skill_name] = f"../skills/{skill_name}"

    # Write JSON file
    with open(output_file, "w") as f:
        json.dump(marketplace, f, indent=2)
        f.write("\n") # Add trailing newline

    print(f"Generated marketplace.json at {output_file}")
    print(f"Total plugins: {len(marketplace['plugins'])}")

if __name__ == "__main__":
    generate_marketplace()
