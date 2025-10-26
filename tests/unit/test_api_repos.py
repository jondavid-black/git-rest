from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

import git_rest.api.repos as repos_module


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(repos_module.repos_bp)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_list_repos_nominal(client):
    with patch("git_rest.api.repos.get_user_store") as mock_get_user_store:
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.dict.return_value = {"name": "repo1"}
        mock_store.list_repos.return_value = [mock_repo]
        mock_get_user_store.return_value = mock_store
        response = client.get("/users/testuser/repos/")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert data[0]["name"] == "repo1"


def test_clone_repo_nominal(client):
    with (
        patch("git_rest.api.repos.get_user_store") as mock_get_user_store,
        patch("git_rest.api.repos.RepoNameSchema") as mock_schema,
    ):
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.dict.return_value = {"name": "repo1"}
        mock_store.clone_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        mock_schema.return_value = MagicMock(name="repo1")
        payload = {"name": "repo1", "url": "https://example.com/repo.git"}
        response = client.post("/users/testuser/repos/clone", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "repo1"


def test_clone_repo_missing_url(client):
    payload = {"name": "repo1"}
    response = client.post("/users/testuser/repos/clone", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_clone_repo_error(client):
    with (
        patch("git_rest.api.repos.get_user_store") as mock_get_user_store,
        patch("git_rest.api.repos.RepoNameSchema") as mock_schema,
    ):
        mock_store = MagicMock()
        mock_store.clone_repo.side_effect = Exception("fail")
        mock_get_user_store.return_value = mock_store
        mock_schema.return_value = MagicMock(name="repo1")
        payload = {"name": "repo1", "url": "https://example.com/repo.git"}
        response = client.post("/users/testuser/repos/clone", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


def test_get_repo_details_nominal(client):
    with patch("git_rest.api.repos.get_user_store") as mock_get_user_store:
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.dict.return_value = {"name": "repo1"}
        mock_store.get_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        response = client.get("/users/testuser/repos/repo1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "repo1"


def test_get_repo_details_not_found(client):
    with patch("git_rest.api.repos.get_user_store") as mock_get_user_store:
        mock_store = MagicMock()
        mock_store.get_repo.side_effect = Exception("not found")
        mock_get_user_store.return_value = mock_store
        response = client.get("/users/testuser/repos/missingrepo")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


def test_switch_repo_nominal(client):
    with (
        patch("git_rest.api.repos.get_user_store") as mock_get_user_store,
        patch("git_rest.api.repos.RepoContext"),
    ):
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.dict.return_value = {"name": "repo1"}
        mock_store.get_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        response = client.post("/users/testuser/repos/repo1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["repo"]["name"] == "repo1"
        assert data["message"].startswith("Switched to repository")


def test_switch_repo_not_found(client):
    with patch("git_rest.api.repos.get_user_store") as mock_get_user_store:
        mock_store = MagicMock()
        mock_store.get_repo.side_effect = Exception("not found")
        mock_get_user_store.return_value = mock_store
        response = client.post("/users/testuser/repos/missingrepo")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


def test_init_repo_success(client):
    with (
        patch("git_rest.api.repos.get_user_store") as mock_get_user_store,
        patch("git_rest.api.repos.RepoNameSchema") as mock_schema,
    ):
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.dict.return_value = {
            "name": "repo1",
            "url": "http://localhost/users/testuser/repos/repo1",
        }
        mock_store.init_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        mock_schema.return_value = MagicMock(name="repo1")
        payload = {"name": "repo1"}
        response = client.post("/users/testuser/repos/init", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert "url" in data


def test_init_repo_duplicate(client):
    with (
        patch("git_rest.api.repos.get_user_store") as mock_get_user_store,
        patch("git_rest.api.repos.RepoNameSchema") as mock_schema,
    ):
        mock_store = MagicMock()
        mock_store.init_repo.side_effect = FileExistsError("Repository already exists.")
        mock_get_user_store.return_value = mock_store
        mock_schema.return_value = MagicMock(name="repo1")
        payload = {"name": "repo1"}
        response = client.post("/users/testuser/repos/init", json=payload)
        assert response.status_code == 409
        data = response.get_json()
        assert "error" in data


def test_init_repo_invalid_name(client):
    payload = {"name": "invalid repo!"}
    response = client.post("/users/testuser/repos/init", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_init_repo_missing_name(client):
    payload = {}
    response = client.post("/users/testuser/repos/init", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_init_repo_nonexistent_user(client):
    with patch("git_rest.api.repos.get_user_store") as mock_get_user_store:
        mock_get_user_store.side_effect = Exception("User not found")
        payload = {"name": "repo1"}
        response = client.post("/users/ghost/repos/init", json=payload)
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


def test_init_repo_storage_failure(client):
    with (
        patch("git_rest.api.repos.get_user_store") as mock_get_user_store,
        patch("git_rest.api.repos.RepoNameSchema") as mock_schema,
    ):
        mock_store = MagicMock()
        mock_store.init_repo.side_effect = OSError("Storage unavailable")
        mock_get_user_store.return_value = mock_store
        mock_schema.return_value = MagicMock(name="repo1")
        payload = {"name": "repo1"}
        response = client.post("/users/testuser/repos/init", json=payload)
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_init_repo_performance(client):
    import time

    with (
        patch("git_rest.api.repos.get_user_store") as mock_get_user_store,
        patch("git_rest.api.repos.RepoNameSchema") as mock_schema,
    ):
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.dict.return_value = {
            "name": "repo1",
            "url": "http://localhost/users/testuser/repos/repo1",
        }
        mock_store.init_repo.side_effect = lambda name: time.sleep(6) or mock_repo
        mock_get_user_store.return_value = mock_store
        mock_schema.return_value = MagicMock(name="repo1")
        payload = {"name": "repo1"}
        start = time.time()
        response = client.post("/users/testuser/repos/init", json=payload)
        elapsed = time.time() - start
        assert elapsed > 5
        assert response.status_code == 201 or response.status_code == 500


def test_init_repo_concurrent(client):
    import queue
    from threading import Thread

    with (
        patch("git_rest.api.repos.get_user_store") as mock_get_user_store,
        patch("git_rest.api.repos.RepoNameSchema") as mock_schema,
    ):
        mock_store = MagicMock()
        results = queue.Queue()

        def init_repo():
            from flask import Flask

            app = Flask(__name__)
            app.register_blueprint(repos_module.repos_bp)
            app.config["TESTING"] = True
            with app.test_client() as thread_client:
                try:
                    mock_store.init_repo.side_effect = FileExistsError(
                        "Repository already exists."
                    )
                    payload = {"name": "repo1"}
                    response = thread_client.post(
                        "/users/testuser/repos/init", json=payload
                    )
                    results.put(response.status_code)
                except Exception as e:
                    results.put(e)

        mock_get_user_store.return_value = mock_store
        mock_schema.return_value = MagicMock(name="repo1")
        threads = [Thread(target=init_repo) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        codes = [results.get() for _ in range(2)]
        assert 409 in codes
