import pytest
from flask import Flask
from git_rest.error_handling import register_error_handlers

def make_app():
    app = Flask(__name__)
    register_error_handlers(app)
    @app.route("/raise400")
    def raise400():
        raise Exception("bad request")
    @app.route("/raise401")
    def raise401():
        from werkzeug.exceptions import Unauthorized
        raise Unauthorized()
    @app.route("/raise403")
    def raise403():
        from werkzeug.exceptions import Forbidden
        raise Forbidden()
    @app.route("/raise404")
    def raise404():
        from werkzeug.exceptions import NotFound
        raise NotFound()
    @app.route("/raise422")
    def raise422():
        from werkzeug.exceptions import UnprocessableEntity
        raise UnprocessableEntity()
    @app.route("/raise500")
    def raise500():
        from werkzeug.exceptions import InternalServerError
        raise InternalServerError()
    @app.route("/raise_exception")
    def raise_exception():
        raise RuntimeError("fail")
    return app

@pytest.fixture
def client():
    app = make_app()
    with app.test_client() as client:
        yield client

def test_error_handlers(client):
    resp = client.get("/raise401")
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Unauthorized"
    resp = client.get("/raise403")
    assert resp.status_code == 403
    assert resp.get_json()["error"] == "Forbidden"
    resp = client.get("/raise404")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Not found"
    resp = client.get("/raise422")
    assert resp.status_code == 422
    assert resp.get_json()["error"] == "Unprocessable entity"
    resp = client.get("/raise500")
    assert resp.status_code == 500
    assert resp.get_json()["error"] == "Internal server error"
    resp = client.get("/raise_exception")
    assert resp.status_code == 500
    assert resp.get_json()["error"] == "Unexpected server error"
