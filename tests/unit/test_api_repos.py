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
        response = client.post("/users/testuser/repos/", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "repo1"


def test_clone_repo_missing_url(client):
    payload = {"name": "repo1"}
    response = client.post("/users/testuser/repos/", json=payload)
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
        response = client.post("/users/testuser/repos/", json=payload)
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
