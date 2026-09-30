"""Export notes to JSON.

Output contract: a JSON array of objects with exactly these fields:
    id          integer
    title       string
    body        string
    createdAt  ISO-8601 timestamp string (UTC)
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone

EXPORT_FIELDS = ("id", "title", "body", "createdAt")


@dataclass(frozen=True)
class Note:
    id: int
    title: str
    body: str
    createdAt: datetime


def serialize_note(note: Note) -> dict:
    """Convert one Note into the JSON-ready dict described in the module docstring."""
    return {
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "createdAt": note.createdAt.astimezone(timezone.utc).isoformat(),
    }


def export_notes(notes: list[Note]) -> str:
    """Serialize a list of notes into a pretty-printed JSON array."""
    return json.dumps([serialize_note(n) for n in notes], indent=2, ensure_ascii=False) + "\n"


SAMPLE_NOTES = [
    Note(1, "Groceries", "milk, eggs, bread", datetime(2026, 9, 1, 8, 30, tzinfo=timezone.utc)),
    Note(2, "Review tool demo", "pair of repos for testing cross-repo review", datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)),
    Note(3, "Ideas", "write about schema drift", datetime(2026, 9, 28, 18, 45, tzinfo=timezone.utc)),
]


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    payload = export_notes(SAMPLE_NOTES)
    if argv:
        with open(argv[0], "w", encoding="utf-8") as fh:
            fh.write(payload)
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
