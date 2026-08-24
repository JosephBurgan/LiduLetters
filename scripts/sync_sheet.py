#!/usr/bin/env python3
"""Pull a published Google Sheet CSV into data.json."""
from __future__ import annotations

import csv
import io
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "google-sheet.json"
OUT = ROOT / "data.json"


def norm(header: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(header).strip().lower()).strip()


ALIASES = {
    "id": "id",
    "question": "q",
    "q": "q",
    "answer": "a",
    "a": "a",
    "date": "date",
    "event": "event",
    "event name": "event",
    "location": "location",
    "tags": "topics",
    "topics": "topics",
    "show on home page": "home",
    "show on home": "home",
    "home": "home",
    "home bubbles": "home",
    "more": "more",
    "more references": "more",
    "more / references": "more",
}


def is_yes(value) -> bool:
    s = str(value or "").strip().lower()
    return s in {"yes", "y", "true", "1", "on", "checked"}


def parse_date(value) -> str:
    s = str(value or "").strip()
    if not s:
        return ""
    # 7/24/2026 or 2026-07-24 or 24/07/2026
    m = re.match(r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})", s)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = re.match(r"^(\d{1,2})[-/](\d{1,2})[-/](\d{4})", s)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), m.group(3)
        # Prefer US m/d/y from Google Forms
        if a > 12:
            return f"{y}-{b:02d}-{a:02d}"
        return f"{y}-{a:02d}-{b:02d}"
    return s[:10]


def row_to_entry(mapped: dict, index: int) -> dict | None:
    q = str(mapped.get("q") or "").strip()
    a = str(mapped.get("a") or "").strip()
    if not q or not a:
        return None
    tags = str(mapped.get("topics") or "")
    topics = [t.strip() for t in re.split(r"[,;]", tags) if t.strip()]
    raw_id = str(mapped.get("id") or "").strip()
    try:
        eid = int(float(raw_id)) if raw_id else 1000 + index
    except ValueError:
        eid = 1000 + index
    home_raw = mapped.get("home", "yes")
    home = True if str(home_raw).strip() == "" else is_yes(home_raw)
    return {
        "id": eid,
        "q": q,
        "a": a,
        "topics": topics,
        "date": parse_date(mapped.get("date")),
        "event": str(mapped.get("event") or "").strip(),
        "location": str(mapped.get("location") or "").strip(),
        "home": home,
        "more": str(mapped.get("more") or "").strip(),
    }


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    csv_url = (cfg.get("csvUrl") or "").strip()
    if not csv_url:
        print("google-sheet.json csvUrl is empty — skip sync")
        return 0

    req = urllib.request.Request(csv_url, headers={"User-Agent": "LiduLetters-sync"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8-sig")

    reader = csv.DictReader(io.StringIO(raw))
    entries = []
    for i, row in enumerate(reader, start=1):
        mapped = {}
        for key, val in row.items():
            field = ALIASES.get(norm(key or ""))
            if field:
                mapped[field] = val
        entry = row_to_entry(mapped, i)
        if entry:
            entries.append(entry)

    if not entries:
        print("Sheet had no complete question/answer rows — leaving data.json unchanged")
        return 0

    OUT.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} entries to data.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
