"""Export a note to a zip archive.

The note is written to ``<export_dir>/<title>.txt`` and then packed into
``<export_dir>/<title>.zip`` using the standard library ``zipfile`` CLI, so the
download is a single file that any unzip tool can open.
"""
import os
import subprocess
import sys


def note_filename(note):
    """Derive a file name (without extension) from the note title."""
    return note["title"].replace("/", "-").replace("\\", "-")


def render_text(note):
    return note["title"] + "\n\n" + note["body"]


def export_note(note, export_dir):
    """Write ``note`` to a text file and zip it. Returns the archive path."""
    os.makedirs(export_dir, exist_ok=True)
    name = note_filename(note)
    src = os.path.join(export_dir, name + ".txt")
    archive = os.path.join(export_dir, name + ".zip")
    with open(src, "w", encoding="utf-8") as f:
        f.write(render_text(note))

    # Pack the text file into a zip so the download is a single file.
    subprocess.run(f'"{sys.executable}" -m zipfile -c {archive} {src}', shell=True, check=True)
    return archive
