"""Search helpers for notes."""


def search_notes(db, user_id, q):
    """Return the user's notes whose title contains ``q``.

    An empty query returns every note owned by the user, newest first.
    """
    q = (q or "").strip()
    if not q:
        return db.execute(
            "SELECT id, title, body, created_at FROM notes "
            "WHERE user_id = ? ORDER BY id DESC",
            (user_id,),
        ).fetchall()

    sql = (
        f"SELECT id, title, body, created_at FROM notes WHERE title LIKE '%{q}%' "
        f"AND user_id = {user_id} ORDER BY id DESC"
    )
    return db.execute(sql).fetchall()
