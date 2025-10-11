from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

import git_rest.api.diff as diff_module


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(diff_module.diff_bp)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_get_diff_nominal(client):
    with patch.object(diff_module, "store") as mock_store:
        mock_repo_obj = MagicMock()
        mock_store.get_user_repo.return_value = mock_repo_obj
        mock_git_repo = MagicMock()
        mock_store._load_git_repo.return_value = mock_git_repo
        mock_git_repo.git.diff.return_value = "diff --git a/file b/file"
        response = client.get("/users/testuser/repos/testrepo/diff/?a=abc123&b=def456")
        assert response.status_code == 200
        data = response.get_json()
        assert "diff" in data
        assert data["diff"].startswith("diff --git")


def test_get_diff_no_commits(client):
    with patch.object(diff_module, "store") as mock_store:
        mock_repo_obj = MagicMock()
        mock_store.get_user_repo.return_value = mock_repo_obj
        mock_git_repo = MagicMock()
        mock_store._load_git_repo.return_value = mock_git_repo
        mock_git_repo.git.diff.return_value = "diff --git a/file b/file"
        response = client.get("/users/testuser/repos/testrepo/diff/")
        assert response.status_code == 200
        data = response.get_json()
        assert "diff" in data


def test_get_diff_repo_not_found(client):
    with patch.object(diff_module, "store") as mock_store:
        mock_store.get_user_repo.side_effect = Exception("Repository not found")
        response = client.get("/users/testuser/repos/notfound/diff/")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


def test_get_diff_internal_error(client):
    with patch.object(diff_module, "store") as mock_store:
        mock_repo_obj = MagicMock()
        mock_store.get_user_repo.return_value = mock_repo_obj
        mock_store._load_git_repo.side_effect = Exception("Internal error")
        response = client.get("/users/testuser/repos/testrepo/diff/")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
