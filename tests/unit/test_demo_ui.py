from git_rest.app import create_app


def test_apidocs_visible_when_enabled(monkeypatch):
    monkeypatch.setenv("GIT_REST_UI", "1")
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/apidocs/")
        assert response.status_code == 200
        assert b"Swagger UI" in response.data or b"swagger-ui" in response.data


def test_apidocs_not_visible_when_disabled(monkeypatch):
    monkeypatch.setenv("GIT_REST_UI", "0")
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/apidocs/")
    assert response.status_code in (404, 403)
    data_lower = response.data.lower()
    assert (
        b"disabled" in data_lower or b"not found" in data_lower or b"404" in data_lower
    )
