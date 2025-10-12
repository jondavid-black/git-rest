from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from git_rest.api.status import status_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(status_bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@patch("git_rest.api.status.RepositoryStore")
def test_get_repo_status_success(mock_store, client):
    mock_repo = MagicMock()
    mock_repo.current_branch = "main"
    mock_repo.status.dict.return_value = {"staged": [], "unstaged": [], "untracked": []}
    mock_store.return_value.get_repo.return_value = mock_repo
    response = client.get("/users/alice/repos/git-rest-test/status/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["branch"] == "main"
    assert data["is_clean"] is True
    assert data["staged"] == []
    assert data["unstaged"] == []
    assert data["untracked"] == []


@patch("git_rest.api.status.RepositoryStore")
def test_get_repo_status_not_found(mock_store, client):
    mock_store.return_value.get_repo.side_effect = Exception("not found")
    response = client.get("/users/alice/repos/missing-repo/status/")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


@patch("git_rest.api.status.RepositoryStore")
def test_get_repo_status_dirty(mock_store, client):
    mock_repo = MagicMock()
    mock_repo.current_branch = "dev"
    mock_repo.status.dict.return_value = {
        "staged": ["file1.py"],
        "unstaged": [],
        "untracked": ["file2.py"],
    }
    mock_store.return_value.get_repo.return_value = mock_repo
    response = client.get("/users/alice/repos/git-rest-test/status/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["branch"] == "dev"
    assert data["is_clean"] is False
    assert data["staged"] == ["file1.py"]
    assert data["untracked"] == ["file2.py"]
