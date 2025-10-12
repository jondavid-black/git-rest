import shutil
import tempfile

import pytest

from git_rest.models.repository_store import RepositoryStore


@pytest.fixture
def temp_repo_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


def test_branch_operations(temp_repo_dir):
    store = RepositoryStore(base_dir=temp_repo_dir)
    repo_url = "https://github.com/jondavid-black/git-rest-test.git"
    repo_name = "git-rest-test"
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
    default_branch = git_repo.head.reference.name
    if branch_name == default_branch:
        # If the feature branch is the default, create and checkout a temp branch
        temp_branch = "temp-main"
        git_repo.git.branch(temp_branch)
        git_repo.git.checkout(temp_branch)
        assert git_repo.active_branch.name == temp_branch
    else:
        git_repo.git.checkout(default_branch)
        assert git_repo.active_branch.name == default_branch

    # Now delete the feature branch
    git_repo.git.branch("-D", branch_name)
    repo = store.get_repo(repo_name)
    assert all(b.name != branch_name for b in repo.branches)
