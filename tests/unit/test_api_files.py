import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import git_rest.api.files as files_module

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(files_module.files_bp)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_list_files_nominal(client):
    with patch("git_rest.api.files.get_user_store") as mock_get_user_store, \
         patch("git_rest.api.files.FileSystemIsolation") as mock_fs_iso, \
         patch("git_rest.api.files.os.scandir") as mock_scandir:
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.path = "/tmp/repo"
        mock_store.get_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        mock_fs = MagicMock()
        mock_fs.safe_join.return_value = "/tmp/repo"
        mock_fs_iso.return_value = mock_fs
        mock_entry = MagicMock()
        mock_entry.path = "/tmp/repo/file.txt"
        mock_entry.is_dir.return_value = False
        mock_entry.is_file.return_value = True
        mock_entry.is_symlink.return_value = False
        mock_stat = MagicMock()
        mock_stat.st_size = 123
        mock_stat.st_mtime = 1697040000
        mock_entry.stat.return_value = mock_stat
        mock_scandir.return_value = [mock_entry]
        response = client.get("/users/testuser/repos/testrepo/files/")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert data[0]["path"] == "file.txt"
        assert data[0]["type"] == "file"
        assert data[0]["size"] == 123
        assert "last_modified" in data[0]

def test_list_files_repo_not_found(client):
    with patch("git_rest.api.files.get_user_store") as mock_get_user_store:
        mock_store = MagicMock()
        mock_store.get_repo.side_effect = Exception("not found")
        mock_get_user_store.return_value = mock_store
        response = client.get("/users/testuser/repos/notfound/files/")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

def test_get_file_content_nominal(client):
    with patch("git_rest.api.files.get_user_store") as mock_get_user_store, \
         patch("git_rest.api.files.FileSystemIsolation") as mock_fs_iso, \
         patch("git_rest.api.files.os.path.isfile") as mock_isfile, \
         patch("git_rest.api.files.os.path.getsize") as mock_getsize, \
         patch("git_rest.api.files.send_file") as mock_send_file:
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.path = "/tmp/repo"
        mock_store.get_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        mock_fs = MagicMock()
        mock_fs.safe_join.return_value = "/tmp/repo/file.txt"
        mock_fs_iso.return_value = mock_fs
        mock_isfile.return_value = True
        mock_getsize.return_value = 100  # below threshold
        mock_send_file.return_value = "file content"
        response = client.get("/users/testuser/repos/testrepo/files/file.txt")
        assert response.status_code == 200

def test_get_file_content_not_found(client):
    with patch("git_rest.api.files.get_user_store") as mock_get_user_store, \
         patch("git_rest.api.files.FileSystemIsolation") as mock_fs_iso, \
         patch("git_rest.api.files.os.path.isfile") as mock_isfile:
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.path = "/tmp/repo"
        mock_store.get_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        mock_fs = MagicMock()
        mock_fs.safe_join.return_value = "/tmp/repo/missing.txt"
        mock_fs_iso.return_value = mock_fs
        mock_isfile.return_value = False
        response = client.get("/users/testuser/repos/testrepo/files/missing.txt")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

def test_get_file_content_internal_error(client):
    with patch("git_rest.api.files.get_user_store") as mock_get_user_store:
        mock_store = MagicMock()
        mock_store.get_repo.side_effect = Exception("fail")
        mock_get_user_store.return_value = mock_store
        response = client.get("/users/testuser/repos/testrepo/files/file.txt")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

def test_download_file_secure_nominal(client):
    with patch("git_rest.api.files.get_user_store") as mock_get_user_store, \
         patch("git_rest.api.files.FileSystemIsolation") as mock_fs_iso, \
         patch("git_rest.api.files.os.path.isfile") as mock_isfile, \
         patch("git_rest.api.files.send_file") as mock_send_file, \
         patch("git_rest.api.files.SecureURLGenerator") as mock_urlgen:
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.path = "/tmp/repo"
        mock_store.get_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        mock_fs = MagicMock()
        mock_fs.safe_join.return_value = "/tmp/repo/file.txt"
        mock_fs_iso.return_value = mock_fs
        mock_isfile.return_value = True
        mock_send_file.return_value = "file content"
        mock_urlgen.return_value.verify.return_value = True
        response = client.get("/users/testuser/repos/testrepo/files/file.txt/download?expires=123&token=abc")
        assert response.status_code == 200

def test_download_file_secure_missing_token(client):
    response = client.get("/users/testuser/repos/testrepo/files/file.txt/download")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_download_file_secure_invalid_token(client):
    with patch("git_rest.api.files.SecureURLGenerator") as mock_urlgen:
        mock_urlgen.return_value.verify.return_value = False
        response = client.get("/users/testuser/repos/testrepo/files/file.txt/download?expires=123&token=bad")
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data

def test_download_file_secure_not_found(client):
    with patch("git_rest.api.files.get_user_store") as mock_get_user_store, \
         patch("git_rest.api.files.FileSystemIsolation") as mock_fs_iso, \
         patch("git_rest.api.files.os.path.isfile") as mock_isfile, \
         patch("git_rest.api.files.SecureURLGenerator") as mock_urlgen:
        mock_store = MagicMock()
        mock_repo = MagicMock()
        mock_repo.path = "/tmp/repo"
        mock_store.get_repo.return_value = mock_repo
        mock_get_user_store.return_value = mock_store
        mock_fs = MagicMock()
        mock_fs.safe_join.return_value = "/tmp/repo/missing.txt"
        mock_fs_iso.return_value = mock_fs
        mock_isfile.return_value = False
        mock_urlgen.return_value.verify.return_value = True
        response = client.get("/users/testuser/repos/testrepo/files/missing.txt/download?expires=123&token=abc")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

def test_download_file_secure_internal_error(client):
    with patch("git_rest.api.files.get_user_store") as mock_get_user_store, \
         patch("git_rest.api.files.SecureURLGenerator") as mock_urlgen:
        mock_store = MagicMock()
        mock_store.get_repo.side_effect = Exception("fail")
        mock_get_user_store.return_value = mock_store
        mock_urlgen.return_value.verify.return_value = True
        response = client.get("/users/testuser/repos/testrepo/files/file.txt/download?expires=123&token=abc")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
