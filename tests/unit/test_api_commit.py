from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

import git_rest.api.commit as commit_module


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(commit_module.commit_bp)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_commit_changes_nominal(client):
    payload = {"message": "Initial commit", "author": "Test User"}
    with patch.object(commit_module, "store") as mock_store:
        mock_repo_obj = MagicMock()
        mock_store.get_user_repo.return_value = mock_repo_obj
        mock_git_repo = MagicMock()
        mock_store._load_git_repo.return_value = mock_git_repo
        mock_commit = MagicMock()
        mock_commit.hexsha = "abc123"
        mock_commit.author.name = payload["author"]
        mock_commit.committed_datetime.isoformat.return_value = "2025-10-11T12:00:00"
        mock_commit.message = payload["message"]
        mock_commit.parents = []
        mock_git_repo.index.commit.return_value = mock_commit
        response = client.post("/users/testuser/repos/testrepo/commit/", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["hash"] == "abc123"
        assert data["author"] == payload["author"]
        assert data["message"] == payload["message"]
        assert data["parent_hashes"] == []


def test_commit_changes_missing_field(client):
    # Missing 'author' field
    payload = {"message": "Initial commit"}
    response = client.post("/users/testuser/repos/testrepo/commit/", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_commit_changes_repo_not_found(client):
    payload = {"message": "Initial commit", "author": "Test User"}
    with patch.object(commit_module, "store") as mock_store:
        mock_store.get_user_repo.side_effect = Exception("Repository not found")
        response = client.post("/users/testuser/repos/notfound/commit/", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


def test_commit_changes_internal_error(client):
    payload = {"message": "Initial commit", "author": "Test User"}
    with patch.object(commit_module, "store") as mock_store:
        mock_repo_obj = MagicMock()
        mock_store.get_user_repo.return_value = mock_repo_obj
        mock_store._load_git_repo.side_effect = Exception("Internal error")
        response = client.post("/users/testuser/repos/testrepo/commit/", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
