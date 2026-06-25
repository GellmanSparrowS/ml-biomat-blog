# -*- coding: utf-8 -*-
"""Automated article writer - reads content/TODO.json, writes next article."""
import json, os, sys
from pathlib import Path

ROOT = Path(__file__).parent
TODO_PATH = ROOT / "content" / "TODO.json"

def get_queue():
    with open(TODO_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data["queue"]

def mark_done(topic):
    with open(TODO_PATH, encoding="utf-8") as f:
        data = json.load(f)
    data["queue"] = [q for q in data["queue"] if q["topic"] != topic]
    with open(TODO_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Marked {topic} as done")

if __name__ == "__main__":
    queue = get_queue()
    if not queue:
        print("Queue empty - nothing to write")
        sys.exit(0)
    next_article = queue[0]
    print(f"Next: {next_article['topic']} ({next_article['lang']}) in {next_article['category']}")
    print(f"Title: {next_article.get('title_en', '')}")
