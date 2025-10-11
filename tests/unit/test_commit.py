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

def test_commit_and_diff(temp_repo_dir):
    store = RepositoryStore(base_dir=temp_repo_dir)
    repo_url = "https://github.com/octocat/Hello-World.git"
    repo_name = "hello-world"
    repo = store.clone_repo(repo_name, repo_url)
    git_repo = store._load_git_repo(repo.path)

    # Make a file change
    file_path = os.path.join(repo.path, "README.md")
    with open(file_path, "a") as f:
        f.write("\nTest line\n")
    git_repo.git.add(A=True)
    commit = git_repo.index.commit("Test commit", author=git.Actor("TestUser", "test@example.com"))
    assert commit.message.strip() == "Test commit"

    # Get diff (should be empty after commit)
    diff = git_repo.git.diff()
    assert diff == ""

    # Make another change and get diff
    with open(file_path, "a") as f:
        f.write("Another line\n")
    diff = git_repo.git.diff()
    assert "Another line" in diff

    # Diff between commits
    commits = list(git_repo.iter_commits())
    if len(commits) >= 2:
        diff_between = git_repo.git.diff(commits[1].hexsha, commits[0].hexsha)
        assert isinstance(diff_between, str)
