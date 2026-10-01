"""Export a note to a zip archive.

The note is written to ``<export_dir>/<title>.txt`` and then packed into
``<export_dir>/<title>.zip`` using the standard library ``zipfile`` module,
so the download is a single file that any unzip tool can open. Working
entirely in-process (no shell, no subprocess) keeps file names with spaces
or shell metacharacters safe.
"""
import os
import zipfile


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

    # Pack the text file into a zip so the download is a single file. The
    # zipfile API handles arbitrary file names correctly; never shell out
    # with a string-joined command (spaces/metacharacters would break or,
    # worse, allow command injection).
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(src, arcname=name + ".txt")
    return archive
