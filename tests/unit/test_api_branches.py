from unittest import mock

import pytest
from flask import Flask

from git_rest.api.branches import branches_bp


def make_test_app():
    app = Flask(__name__)
    app.register_blueprint(branches_bp)
    return app


@pytest.fixture
def client():
    app = make_test_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@mock.patch("git_rest.api.branches.get_user_store")
def test_list_branches_success(mock_get_user_store, client):
    mock_store = mock.Mock()
    mock_repo = mock.Mock()
    mock_repo.branches = [mock.Mock(dict=lambda: {"name": "main"})]
    mock_store.get_repo.return_value = mock_repo
    mock_get_user_store.return_value = mock_store
    response = client.get("/users/testuser/repos/testrepo/branches/")
    assert response.status_code == 200
    assert response.get_json() == [{"name": "main"}]


@mock.patch("git_rest.api.branches.get_user_store")
def test_list_branches_error(mock_get_user_store, client):
    mock_store = mock.Mock()
    mock_store.get_repo.side_effect = Exception("not found")
    mock_get_user_store.return_value = mock_store
    response = client.get("/users/testuser/repos/testrepo/branches/")
    assert response.status_code == 404
    assert "error" in response.get_json()


@mock.patch("git_rest.api.branches.get_user_store")
@mock.patch("git_rest.api.branches.BranchNameSchema")
def test_create_branch_success(mock_schema, mock_get_user_store, client):
    mock_store = mock.Mock()
    mock_repo = mock.Mock()
    mock_repo.branches = []
    mock_git_repo = mock.Mock()
    mock_git_repo.head.is_detached = False
    mock_git_repo.branches = []
    mock_store.get_repo.return_value = mock_repo
    mock_store._load_git_repo.return_value = mock_git_repo
    mock_get_user_store.return_value = mock_store
    mock_schema.return_value = mock.Mock(name="feature-x")
    mock_git_repo.branches = []
    mock_git_repo.git.branch = mock.Mock()
    mock_repo.branches = [mock.Mock(dict=lambda: {"name": "feature-x"})]
    response = client.post(
        "/users/testuser/repos/testrepo/branches/", json={"name": "feature-x"}
    )
    assert response.status_code == 201
    assert response.get_json() == [{"name": "feature-x"}]


@mock.patch("git_rest.api.branches.get_user_store")
def test_create_branch_exists(mock_get_user_store, client):
    mock_store = mock.Mock()
    mock_repo = mock.Mock()
    mock_git_repo = mock.Mock()
    mock_git_repo.head.is_detached = False
    branch_mock = mock.Mock()
    branch_mock.name = "feature-x"
    mock_git_repo.branches = [branch_mock]
    mock_store.get_repo.return_value = mock_repo
    mock_store._load_git_repo.return_value = mock_git_repo
    mock_get_user_store.return_value = mock_store
    mock_repo.branches = [mock.Mock(dict=lambda: {"name": "feature-x"})]
    response = client.post(
        "/users/testuser/repos/testrepo/branches/", json={"name": "feature-x"}
    )
    assert response.status_code == 409
    assert "error" in response.get_json()


@mock.patch("git_rest.api.branches.get_user_store")
def test_switch_branch_success(mock_get_user_store, client):
    mock_store = mock.Mock()
    mock_repo = mock.Mock()
    mock_git_repo = mock.Mock()
    mock_store.get_repo.return_value = mock_repo
    mock_store._load_git_repo.return_value = mock_git_repo
    mock_git_repo.git.checkout = mock.Mock()
    mock_repo.dict.return_value = {"name": "testrepo"}
    mock_get_user_store.return_value = mock_store
    response = client.post("/users/testuser/repos/testrepo/branches/feature-x")
    assert response.status_code == 200
    assert response.get_json()["message"].startswith("Switched to branch")


@mock.patch("git_rest.api.branches.get_user_store")
def test_delete_branch_success(mock_get_user_store, client):
    mock_store = mock.Mock()
    mock_repo = mock.Mock()
    mock_git_repo = mock.Mock()
    mock_git_repo.active_branch.name = "other"
    mock_git_repo.branches = [mock.Mock(name="feature-x"), mock.Mock(name="other")]
    mock_store.get_repo.return_value = mock_repo
    mock_store._load_git_repo.return_value = mock_git_repo
    mock_git_repo.git.branch = mock.Mock()
    mock_repo.branches = [mock.Mock(dict=lambda: {"name": "other"})]
    mock_get_user_store.return_value = mock_store
    response = client.delete("/users/testuser/repos/testrepo/branches/feature-x")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


@mock.patch("git_rest.api.branches.get_user_store")
def test_delete_branch_only_branch(mock_get_user_store, client):
    mock_store = mock.Mock()
    mock_repo = mock.Mock()
    mock_git_repo = mock.Mock()
    mock_git_repo.active_branch.name = "feature-x"
    mock_git_repo.branches = [mock.Mock(name="feature-x")]
    mock_store.get_repo.return_value = mock_repo
    mock_store._load_git_repo.return_value = mock_git_repo
    mock_get_user_store.return_value = mock_store
    response = client.delete("/users/testuser/repos/testrepo/branches/feature-x")
    assert response.status_code == 400
    assert "error" in response.get_json()
