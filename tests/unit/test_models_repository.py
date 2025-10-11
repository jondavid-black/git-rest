from datetime import datetime
from git_rest.models.repository import Remote, Branch, Commit, FileEntry, RepoStatus, Repository

def test_remote():
    r = Remote(name="origin", url="https://example.com/repo.git")
    assert r.name == "origin"
    assert r.url == "https://example.com/repo.git"

def test_branch():
    b = Branch(name="main", is_current=True)
    assert b.name == "main"
    assert b.is_current is True

def test_commit():
    now = datetime.now()
    c = Commit(hash="abc123", author="me", date=now, message="msg", parent_hashes=["def456"])
    assert c.hash == "abc123"
    assert c.author == "me"
    assert c.date == now
    assert c.message == "msg"
    assert c.parent_hashes == ["def456"]

def test_file_entry():
    now = datetime.now()
    f = FileEntry(path="foo.txt", type="file", size=10, last_modified=now)
    assert f.path == "foo.txt"
    assert f.type == "file"
    assert f.size == 10
    assert f.last_modified == now

def test_repo_status():
    now = datetime.now()
    f = FileEntry(path="foo.txt", type="file", size=10, last_modified=now)
    s = RepoStatus(staged=[f], unstaged=[], untracked=[])
    assert s.staged == [f]
    assert s.unstaged == []
    assert s.untracked == []

def test_repository():
    now = datetime.now()
    f = FileEntry(path="foo.txt", type="file", size=10, last_modified=now)
    b = Branch(name="main", is_current=True)
    r = Remote(name="origin", url="https://example.com/repo.git")
    s = RepoStatus(staged=[f], unstaged=[], untracked=[])
    repo = Repository(id="1", name="repo", path="/tmp/repo", remotes=[r], branches=[b], current_branch="main", status=s)
    assert repo.id == "1"
    assert repo.name == "repo"
    assert repo.path == "/tmp/repo"
    assert repo.remotes == [r]
    assert repo.branches == [b]
    assert repo.current_branch == "main"
    assert repo.status == s
