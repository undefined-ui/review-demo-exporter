import json
import pathlib
import unittest
from datetime import datetime, timezone

from exporter.notes_export import EXPORT_FIELDS, Note, SAMPLE_NOTES, export_notes, serialize_note

ROOT = pathlib.Path(__file__).resolve().parent.parent


class SerializeNoteTests(unittest.TestCase):
    def test_serialized_note_has_exact_fields(self):
        note = Note(7, "t", "b", datetime(2026, 1, 2, 3, 4, tzinfo=timezone.utc))
        data = serialize_note(note)
        self.assertEqual(set(data), {"id", "title", "body", "created_at"})
        self.assertEqual(set(data), set(EXPORT_FIELDS))

    def test_field_types(self):
        data = serialize_note(SAMPLE_NOTES[0])
        self.assertIsInstance(data["id"], int)
        self.assertIsInstance(data["title"], str)
        self.assertIsInstance(data["body"], str)
        self.assertIsInstance(data["created_at"], str)

    def test_created_at_is_iso_utc(self):
        note = Note(1, "t", "b", datetime(2026, 1, 2, 3, 4, tzinfo=timezone.utc))
        self.assertEqual(serialize_note(note)["created_at"], "2026-01-02T03:04:00+00:00")
        self.assertEqual(datetime.fromisoformat(serialize_note(note)["created_at"]), note.created_at)


class ExportNotesTests(unittest.TestCase):
    def test_export_is_json_array_of_objects(self):
        parsed = json.loads(export_notes(SAMPLE_NOTES))
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), len(SAMPLE_NOTES))
        for item in parsed:
            self.assertEqual(set(item), set(EXPORT_FIELDS))

    def test_example_file_matches_current_export(self):
        example = (ROOT / "examples" / "notes.json").read_text(encoding="utf-8")
        self.assertEqual(example, export_notes(SAMPLE_NOTES))


if __name__ == "__main__":
    unittest.main()
