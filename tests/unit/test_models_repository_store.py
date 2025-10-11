from unittest.mock import MagicMock, patch

import pytest

from git_rest.models.repository_store import RepositoryStore


def test_init_and_base_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_REST_WORKDIR", str(tmp_path))
    store = RepositoryStore()
    assert store.base_dir == str(tmp_path)
    assert tmp_path.exists()


def test_get_repo_not_found(tmp_path):
    store = RepositoryStore(base_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        store.get_repo("missing")


def test_get_user_repo_not_found(tmp_path):
    store = RepositoryStore(base_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        store.get_user_repo("user", "missing")


def test_list_repos_empty(tmp_path):
    store = RepositoryStore(base_dir=str(tmp_path))
    assert store.list_repos() == []


def test_clone_repo_already_exists(tmp_path):
    d = tmp_path / "repo"
    d.mkdir()
    store = RepositoryStore(base_dir=str(tmp_path))
    with pytest.raises(FileExistsError):
        store.clone_repo("repo", "https://example.com/repo.git")


def test_clone_repo_calls_clone_from(tmp_path):
    with (
        patch(
            "git_rest.models.repository_store.git.Repo.clone_from"
        ) as mock_clone_from,
        patch.object(RepositoryStore, "_load_repo") as mock_load_repo,
    ):
        mock_repo = MagicMock()
        mock_clone_from.return_value = mock_repo
        mock_load_repo.return_value = "repo_obj"
        store = RepositoryStore(base_dir=str(tmp_path))
        result = store.clone_repo("repo", "https://example.com/repo.git")
        assert result == "repo_obj"
        mock_clone_from.assert_called_once()
        mock_load_repo.assert_called_once()
