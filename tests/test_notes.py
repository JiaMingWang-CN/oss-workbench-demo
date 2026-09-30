def create_note(client, title="Groceries", body="milk, eggs"):
    return client.post("/notes/new", data={"title": title, "body": body})


def test_create_and_list(logged_in):
    assert create_note(logged_in).status_code == 302
    response = logged_in.get("/")
    assert b"Groceries" in response.data


def test_view_note(logged_in):
    create_note(logged_in)
    response = logged_in.get("/notes/1")
    assert response.status_code == 200
    assert b"milk, eggs" in response.data


def test_title_required(logged_in):
    response = create_note(logged_in, title="  ")
    assert response.status_code == 200
    assert b"Title is required" in response.data


def test_edit_note(logged_in):
    create_note(logged_in)
    response = logged_in.post("/notes/1/edit", data={"title": "Errands", "body": "x"})
    assert response.status_code == 302
    assert b"Errands" in logged_in.get("/notes/1").data


def test_delete_note(logged_in):
    create_note(logged_in)
    assert logged_in.post("/notes/1/delete").status_code == 302
    assert logged_in.get("/notes/1").status_code == 404


def test_cannot_view_other_users_note(client, auth):
    auth.register("alice", "secret")
    auth.login("alice", "secret")
    create_note(client)
    auth.logout()

    auth.register("bob", "hunter2")
    auth.login("bob", "hunter2")
    assert client.get("/notes/1").status_code == 404


def test_export_note(logged_in):
    create_note(logged_in, title="Groceries")
    response = logged_in.get("/notes/1/export")
    assert response.status_code == 200
    assert response.data[:2] == b"PK"


def test_import_yaml(logged_in):
    import io

    content = b"- title: Imported one\n  body: hello\n- title: Imported two\n"
    response = logged_in.post(
        "/import",
        data={"file": (io.BytesIO(content), "notes.yaml")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 302
    listing = logged_in.get("/").data
    assert b"Imported one" in listing and b"Imported two" in listing
