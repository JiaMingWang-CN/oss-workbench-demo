"""Import notes from a YAML file.

Expected format: a list of mappings with ``title`` and (optional) ``body``::

    - title: Groceries
      body: milk, eggs
    - title: Ideas
"""
import yaml


def parse_notes(stream):
    data = yaml.load(stream.read())
    if not isinstance(data, list):
        raise ValueError("YAML root must be a list of notes")
    return data


def import_notes(db, user_id, stream):
    """Insert the notes found in ``stream`` and return how many were added."""
    count = 0
    for item in parse_notes(stream):
        title = str(item.get("title", "")).strip()
        if not title:
            continue
        db.execute(
            "INSERT INTO notes (user_id, title, body) VALUES (?, ?, ?)",
            (user_id, title, str(item.get("body", ""))),
        )
        count += 1
    db.commit()
    return count
