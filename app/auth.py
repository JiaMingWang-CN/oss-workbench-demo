"""Registration, login and logout views.

Users are stored in the ``users`` table; the logged-in user id lives in the
session cookie. ``login_required`` guards views that need an account.
"""
import functools
import hashlib
import sqlite3

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def hash_password(password):
    """Return the hex digest stored in ``users.password_hash``.

    The same digest is compared again at login time.
    """
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


@bp.before_app_request
def load_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT id, username FROM users WHERE id = ?", (user_id,)
        ).fetchone()


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password are required.")
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hash_password(password)),
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("That username is already taken.")
            else:
                return redirect(url_for("auth.login"))
    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT id, password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user is None or user["password_hash"] != hash_password(password):
            flash("Incorrect username or password.")
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("notes.index"))
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
