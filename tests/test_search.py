def add(client, title):
    client.post("/notes/new", data={"title": title, "body": ""})


def test_search_matches_title(logged_in):
    add(logged_in, "Shopping list")
    add(logged_in, "Meeting notes")
    response = logged_in.get("/?q=shopping")
    assert b"Shopping list" in response.data
    assert b"Meeting notes" not in response.data


def test_search_only_returns_own_notes(client, auth):
    auth.register("alice", "secret")
    auth.login("alice", "secret")
    add(client, "Alice plan")
    auth.logout()

    auth.register("bob", "hunter2")
    auth.login("bob", "hunter2")
    add(client, "Bob plan")
    response = client.get("/?q=plan")
    assert b"Bob plan" in response.data
    assert b"Alice plan" not in response.data
