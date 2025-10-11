import pytest

from git_rest.filesystem import FileSystemIsolation


def test_safe_join_and_is_safe_path(tmp_path):
    fs = FileSystemIsolation(base_dir=str(tmp_path))
    # Normal join
    assert fs.safe_join("foo.txt").startswith(str(tmp_path))
    # Path traversal
    with pytest.raises(ValueError):
        fs.safe_join("..", "etc", "passwd")
    # is_safe_path
    assert fs.is_safe_path("foo.txt")
    assert not fs.is_safe_path("../../etc/passwd")


def test_list_dir_and_exists(tmp_path):
    fs = FileSystemIsolation(base_dir=str(tmp_path))
    d = tmp_path / "subdir"
    d.mkdir()
    f = d / "file.txt"
    f.write_text("hi")
    # list_dir
    assert "file.txt" in fs.list_dir("subdir")
    # file_exists
    assert fs.file_exists("subdir/file.txt")
    assert not fs.file_exists("subdir/nope.txt")
    # dir_exists
    assert fs.dir_exists("subdir")
    assert not fs.dir_exists("nope")


def test_acquire_lock(tmp_path):
    fs = FileSystemIsolation(base_dir=str(tmp_path))
    # Should be able to acquire and release lock
    with fs._acquire_lock():
        pass
    # Non-blocking lock (should not raise)
    with fs._acquire_lock(blocking=False):
        pass
