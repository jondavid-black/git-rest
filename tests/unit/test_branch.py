import os
import shutil
import tempfile
import pytest
import git
from src.git_rest.models.repository_store import RepositoryStore

@pytest.fixture
def temp_repo_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)

def test_branch_operations(temp_repo_dir):
    store = RepositoryStore(base_dir=temp_repo_dir)
    repo_url = "https://github.com/octocat/Hello-World.git"
    repo_name = "hello-world"
    repo = store.clone_repo(repo_name, repo_url)
    git_repo = store._load_git_repo(repo.path)

    # Create branch
    branch_name = "feature-x"
    git_repo.git.branch(branch_name)
    repo = store.get_repo(repo_name)
    assert any(b.name == branch_name for b in repo.branches)

    # Switch branch
    git_repo.git.checkout(branch_name)
    repo = store.get_repo(repo_name)
    assert repo.current_branch == branch_name

    # Delete branch
    git_repo.git.checkout("main")
    git_repo.git.branch('-D', branch_name)
    repo = store.get_repo(repo_name)
    assert all(b.name != branch_name for b in repo.branches)
