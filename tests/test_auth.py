def test_register_and_login(client, auth):
    assert auth.register().status_code == 302
    response = auth.login()
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_duplicate_username_rejected(client, auth):
    auth.register()
    response = auth.register()
    assert response.status_code == 200
    assert b"already taken" in response.data


def test_wrong_password_rejected(client, auth):
    auth.register()
    response = auth.login(password="nope")
    assert response.status_code == 200
    assert b"Incorrect username or password" in response.data


def test_login_required_redirects(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_logout(logged_in):
    logged_in.get("/auth/logout")
    response = logged_in.get("/")
    assert response.status_code == 302
