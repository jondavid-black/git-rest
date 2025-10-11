from git_rest.app import create_app


def test_create_app_registers_blueprints():
    app = create_app()
    client = app.test_client()
    # Check healthz endpoint
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
    # Check login endpoint exists
    assert any(rule.rule == "/login" for rule in app.url_map.iter_rules())
    # Check at least one API blueprint route exists
    api_routes = [
        r.rule for r in app.url_map.iter_rules() if r.rule.startswith("/users/")
    ]
    assert api_routes
