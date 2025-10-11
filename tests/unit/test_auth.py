import jwt
import pytest
from flask import Flask

from git_rest.auth import SECRET_KEY, decode_token, generate_token, login, require_auth


@pytest.fixture
def app():
    app = Flask(__name__)
    app.add_url_rule("/login", "login", login, methods=["POST"])
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_generate_and_decode_token():
    token = generate_token("alice", expires_in=10)
    user = decode_token(token)
    assert user == "alice"


def test_decode_token_expired(monkeypatch):
    import datetime

    expired = datetime.datetime.now(datetime.UTC) - datetime.timedelta(seconds=10)
    payload = {"sub": "bob", "exp": expired}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    assert decode_token(token) is None


def test_decode_token_invalid():
    assert decode_token("not.a.jwt") is None


def test_login_success(client):
    resp = client.post("/login", json={"username": "admin", "password": "password123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data


def test_login_failure(client):
    resp = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401
    data = resp.get_json()
    assert "error" in data


def test_require_auth_decorator_success():
    app = Flask(__name__)
    token = generate_token("alice", expires_in=10)

    @app.route("/protected")
    @require_auth
    def protected():
        return {"user": "alice"}

    with app.test_client() as client:
        resp = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.get_json()["user"] == "alice"


def test_require_auth_decorator_failure():
    app = Flask(__name__)

    @app.route("/protected")
    @require_auth
    def protected():
        return {"user": "alice"}

    with app.test_client() as client:
        resp = client.get("/protected", headers={"Authorization": "Bearer badtoken"})
        assert resp.status_code == 401
        assert "error" in resp.get_json()
        resp2 = client.get("/protected")
        assert resp2.status_code == 401
        assert "error" in resp2.get_json()
