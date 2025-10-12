import os
import shutil
import tempfile

import pytest

from git_rest.models.repository_store import RepositoryStore
from git_rest.services.secure_url import SecureURLGenerator


@pytest.fixture
def temp_repo_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


def test_file_listing_and_content(temp_repo_dir):
    store = RepositoryStore(base_dir=temp_repo_dir)
    repo_url = "https://github.com/jondavid-black/git-rest-test.git"
    repo_name = "git-rest-test"
    repo = store.clone_repo(repo_name, repo_url)
    repo_path = repo.path
    # Create a small file
    file_path = os.path.join(repo_path, "small.txt")
    with open(file_path, "w") as f:
        f.write("hello world\n")
    # List files
    files = os.listdir(repo_path)
    assert "small.txt" in files
    # Read file content
    with open(file_path) as f:
        content = f.read()
    assert "hello world" in content


def test_secure_url_generation_and_verification():
    generator = SecureURLGenerator(secret="testsecret")
    url = generator.generate("repo1", "file.txt", expires_in=10)
    # Parse params
    from urllib.parse import parse_qs, urlparse

    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    assert generator.verify(
        "repo1", "file.txt", params["expires"][0], params["token"][0]
    )
