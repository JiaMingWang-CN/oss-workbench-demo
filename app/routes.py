from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, request, send_file, url_for)

from .auth import login_required
from .db import get_db
from .export import export_note
from .importer import import_notes
from .search import search_notes

bp = Blueprint("notes", __name__)


def get_note(note_id):
    note = get_db().execute(
        "SELECT id, user_id, title, body, created_at FROM notes WHERE id = ?",
        (note_id,),
    ).fetchone()
    if note is None or note["user_id"] != g.user["id"]:
        abort(404)
    return note


@bp.route("/")
@login_required
def index():
    q = request.args.get("q", "")
    notes = search_notes(get_db(), g.user["id"], q)
    return render_template("index.html", notes=notes, q=q)


@bp.route("/notes/new", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.")
        else:
            db = get_db()
            db.execute(
                "INSERT INTO notes (user_id, title, body) VALUES (?, ?, ?)",
                (g.user["id"], title, request.form.get("body", "")),
            )
            db.commit()
            return redirect(url_for("notes.index"))
    return render_template("note_form.html", note=None)


@bp.route("/notes/<int:note_id>")
@login_required
def view(note_id):
    return render_template("note.html", note=get_note(note_id))


@bp.route("/notes/<int:note_id>/edit", methods=("GET", "POST"))
@login_required
def edit(note_id):
    note = get_note(note_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.")
        else:
            db = get_db()
            db.execute(
                "UPDATE notes SET title = ?, body = ? WHERE id = ?",
                (title, request.form.get("body", ""), note_id),
            )
            db.commit()
            return redirect(url_for("notes.view", note_id=note_id))
    return render_template("note_form.html", note=note)


@bp.route("/notes/<int:note_id>/delete", methods=("POST",))
@login_required
def delete(note_id):
    get_note(note_id)
    db = get_db()
    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    return redirect(url_for("notes.index"))


@bp.route("/notes/<int:note_id>/export")
@login_required
def export(note_id):
    archive = export_note(get_note(note_id), current_app.config["EXPORT_DIR"])
    return send_file(archive, as_attachment=True)


@bp.route("/import", methods=("GET", "POST"))
@login_required
def import_view():
    if request.method == "POST":
        upload = request.files.get("file")
        if upload is None or not upload.filename:
            flash("Choose a YAML file to import.")
        else:
            try:
                count = import_notes(get_db(), g.user["id"], upload.stream)
            except ValueError as exc:
                flash(str(exc))
            else:
                flash("Imported %d notes." % count)
                return redirect(url_for("notes.index"))
    return render_template("import.html")
