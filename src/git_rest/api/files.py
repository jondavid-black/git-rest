import datetime
import os

from flask import Blueprint, jsonify, request, send_file

from ..audit import audit_repo_action
from ..filesystem import FileSystemIsolation
from ..models.repository_store import RepositoryStore
from ..services.secure_url import SecureURLGenerator

files_bp = Blueprint(
    "files", __name__, url_prefix="/users/<user_id>/repos/<repo_id>/files"
)


def get_user_store(user_id):
    base_dir = os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
    user_dir = os.path.join(base_dir, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, exist_ok=True)
    return RepositoryStore(base_dir=user_dir)


@files_bp.route("/", methods=["GET"])
@audit_repo_action("list_files")
def list_files(user_id, repo_id):
    """
    List all files and directories in the specified repository for a user.
    ---
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
        description: The user identifier.
      - in: path
        name: repo_id
        required: true
        schema:
          type: string
        description: The repository identifier.
      - in: query
        name: path
        required: false
        schema:
          type: string
        description: The relative path within the repository to list.
    responses:
      200:
        description: A list of files and directories in the repository.
      404:
        description: Repository or path not found.
    """
    store = get_user_store(user_id)
    rel_path = request.args.get("path", "")
    try:
        repo = store.get_repo(repo_id)
        fs = FileSystemIsolation(repo.path)
        dir_path = fs.safe_join(rel_path)
        entries = []
        for entry in os.scandir(dir_path):
            stat = entry.stat()
            entries.append(
                {
                    "path": os.path.relpath(entry.path, repo.path),
                    "type": "dir"
                    if entry.is_dir()
                    else "file"
                    if entry.is_file()
                    else "symlink",
                    "size": stat.st_size,
                    "last_modified": datetime.datetime.fromtimestamp(
                        stat.st_mtime
                    ).isoformat(),
                }
            )
        return jsonify(entries)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@files_bp.route("/<path:file_path>", methods=["GET"])
@audit_repo_action("get_file_content")
def get_file_content(user_id, repo_id, file_path):
    """
    Retrieve the content of a specific file in the repository for a user.
    ---
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
        description: The user identifier.
      - in: path
        name: repo_id
        required: true
        schema:
          type: string
        description: The repository identifier.
      - in: path
        name: file_path
        required: true
        schema:
          type: string
        description: The path to the file within the repository.
    responses:
      200:
        description: The file content.
      404:
        description: File or repository not found.
    """
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        fs = FileSystemIsolation(repo.path)
        abs_path = fs.safe_join(file_path)
        if not os.path.isfile(abs_path):
            return jsonify({"error": "File not found"}), 404
        size = os.path.getsize(abs_path)
        # Threshold for inline vs. redirect (e.g., 1MB)
        threshold = 1024 * 1024
        if size > threshold:
            generator = SecureURLGenerator()
            # Generate a secure URL pointing to the /download endpoint
            secure_url = generator.generate(repo_id, file_path)
            # Ensure the URL is for /download, not the same endpoint
            from flask import url_for

            download_url = url_for(
                "files.download_file_secure",
                user_id=user_id,
                repo_id=repo_id,
                file_path=file_path,
                _external=False,
            )
            # Append token and expires
            from urllib.parse import parse_qs, urlencode, urlparse

            parsed = urlparse(secure_url)
            qs = parse_qs(parsed.query)
            download_url = f"{download_url}?{urlencode(qs, doseq=True)}"
            return jsonify({"url": download_url}), 302
        return send_file(abs_path, as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Secure file download endpoint (verifies token)
@files_bp.route("/<path:file_path>/download", methods=["GET"])
@audit_repo_action("download_file_secure")
def download_file_secure(user_id, repo_id, file_path):
    """
    Download a file from the repository using a secure, time-limited URL for a user.
    ---
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
        description: The user identifier.
      - in: path
        name: repo_id
        required: true
        schema:
          type: string
        description: The repository identifier.
      - in: path
        name: file_path
        required: true
        schema:
          type: string
        description: The path to the file within the repository.
    responses:
      200:
        description: The file is downloaded using a secure URL.
      404:
        description: File or repository not found.
    """
    store = get_user_store(user_id)
    expires = request.args.get("expires")
    token = request.args.get("token")
    if not expires or not token:
        return jsonify({"error": "Missing token or expires"}), 400
    generator = SecureURLGenerator()
    if not generator.verify(repo_id, file_path, expires, token):
        return jsonify({"error": "Invalid or expired token"}), 403
    try:
        repo = store.get_repo(repo_id)
        fs = FileSystemIsolation(repo.path)
        abs_path = fs.safe_join(file_path)
        if not os.path.isfile(abs_path):
            return jsonify({"error": "File not found"}), 404
        return send_file(abs_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
