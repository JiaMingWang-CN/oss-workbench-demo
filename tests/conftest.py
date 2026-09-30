import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    return create_app({
        "TESTING": True,
        "DATABASE": str(tmp_path / "test.sqlite"),
        "EXPORT_DIR": str(tmp_path / "exports"),
    })


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def register(self, username="alice", password="secret"):
        return self._client.post(
            "/auth/register", data={"username": username, "password": password}
        )

    def login(self, username="alice", password="secret"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def logged_in(client, auth):
    auth.register()
    auth.login()
    return client
