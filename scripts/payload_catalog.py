#!/usr/bin/env python3
"""Lists curated payload-reference topics; does not execute payloads."""
import json
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "repository-integrations.json"

def main():
    parser = argparse.ArgumentParser(description="Authorized-lab payload reference catalogue")
    parser.add_argument("topic", nargs="?", help="Topic ID, such as sqli, xss or ssrf")
    args = parser.parse_args()
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    topics = data["payload_topics"]
    if args.topic:
        matches = [t for t in topics if t["id"] == args.topic.lower()]
        if not matches:
            raise SystemExit(f"Unknown topic: {args.topic}")
        print(json.dumps(matches[0], indent=2))
    else:
        for topic in topics:
            print(f'{topic["id"]:20} {topic["url"]}')
        print("\nReference-only utility. It never sends requests or executes payloads.")

if __name__ == "__main__":
    main()
