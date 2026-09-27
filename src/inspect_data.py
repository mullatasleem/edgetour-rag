"""Day 2: load the Jeju tourism dataset and print quality stats."""
import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "tourism_jeju.json"

with open(DATA_PATH, encoding="utf-8") as f:
    entries = json.load(f)

print(f"Total entries: {len(entries)}")

with_coords = sum(1 for e in entries if e.get("latitude") and e.get("longitude"))
print(f"With coordinates: {with_coords}")

with_ko = sum(1 for e in entries if e.get("name_ko"))
print(f"With Korean name: {with_ko}")

print("By source:", dict(Counter(e.get("source", "?") for e in entries)))

thin = [e for e in entries
        if (e.get("description") or "").startswith(("Tourism point of interest", "Natural feature"))]
print(f"Thin generic descriptions: {len(thin)}")
print(f"Rich descriptions: {len(entries) - len(thin)}")

name_counts = Counter(e.get("name") for e in entries)
dupes = sorted(n for n, c in name_counts.items() if c > 1)
print(f"Duplicate names: {len(dupes)}")
if dupes:
    print(" ", dupes[:10])

missing_desc = [e["id"] for e in entries if not (e.get("description") or "").strip()]
print(f"Missing description: {len(missing_desc)}")
