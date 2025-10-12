import shutil
import tempfile

import pytest

from git_rest.models.repository_store import RepositoryStore


@pytest.fixture
def temp_repo_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


def test_clone_and_list_repo(temp_repo_dir):
    store = RepositoryStore(base_dir=temp_repo_dir)
    # Use a small public repo for test, or mock git.Repo.clone_from in real CI
    repo_url = "https://github.com/jondavid-black/git-rest-test.git"
    repo_name = "git-rest-test"
    repo = store.clone_repo(repo_name, repo_url)
    assert repo.name == repo_name
    repos = store.list_repos()
    assert any(r.name == repo_name for r in repos)


def test_get_repo_not_found(temp_repo_dir):
    store = RepositoryStore(base_dir=temp_repo_dir)
    with pytest.raises(FileNotFoundError):
        store.get_repo("does-not-exist")
