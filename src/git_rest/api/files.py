import datetime
import os

from flask import Blueprint, jsonify, request, send_file

from ..audit import audit_repo_action
from ..filesystem import FileSystemIsolation
from ..models.file import File, FileType
from ..models.repository_store import RepositoryStore
from ..services.binary_utils import BinaryUtils
from ..services.file_service import FileService
from ..services.file_validation import FileValidation
from ..services.performance_metrics import PerformanceMetrics
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


@files_bp.route("/<path:file_path>", methods=["POST"])
@audit_repo_action("post_file_content")
def post_file_content(user_id, repo_id, file_path):
    """
    Update or create file content for a user. Stages the change, does not commit.
    Supports text and binary files, partial updates, and error/status handling.
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
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              content:
                type: string
                description: File content (text or base64-encoded binary)
              type:
                type: string
                enum: [text, binary]
                description: File type
              partial:
                type: object
                properties:
                  start_line:
                    type: integer
                  end_line:
                    type: integer
                description: Optional partial update (line range)
    responses:
      200:
        description: File updated and staged
      400:
        description: Invalid request
      404:
        description: File or repository not found
      409:
        description: Concurrent update conflict
    """
    store = get_user_store(user_id)
    data = request.get_json(force=True)
    file_type = data.get("type")
    content = data.get("content")
    partial = data.get("partial")
    # Validate file type
    if not FileValidation.validate_file_type(file_type):
        return jsonify({"error": "Invalid file type"}), 400
    # Validate encoding
    if not FileValidation.validate_encoding(content, file_type):
        return jsonify({"error": "Invalid file encoding"}), 400
    try:
        repo = store.get_repo(repo_id)
        fs = FileSystemIsolation(repo.path)
        abs_path = fs.safe_join(file_path)
        # File-level locking and sequential update
        file_service = FileService()
        # Read existing content if file exists
        if os.path.exists(abs_path):
            with open(
                abs_path,
                "rb" if file_type == FileType.BINARY else "r",
                encoding=None if file_type == FileType.BINARY else "utf-8",
            ) as f:
                existing_content = f.read()
            if file_type == FileType.BINARY:
                existing_content = (
                    BinaryUtils.encode_to_base64(existing_content)
                    if isinstance(existing_content, bytes)
                    else existing_content
                )
        else:
            existing_content = ""
        # Handle partial update
        if partial:
            start = partial.get("start_line")
            end = partial.get("end_line")
            if file_type == FileType.TEXT:
                lines = existing_content.splitlines()
                new_lines = content.splitlines()
                # Replace specified line range
                if (
                    start is not None
                    and end is not None
                    and 0 <= start < len(lines)
                    and 0 < end <= len(lines)
                ):
                    lines[start:end] = new_lines
                    updated_content = "\n".join(lines)
                else:
                    return jsonify({"error": "Invalid partial update range"}), 400
            else:
                # For binary, partial update not supported
                return jsonify(
                    {"error": "Partial update not supported for binary files"}
                ), 400
        else:
            updated_content = content
        # Decode binary if needed
        if file_type == FileType.BINARY:
            try:
                updated_content_bytes = BinaryUtils.decode_from_base64(updated_content)
            except Exception:
                return jsonify({"error": "Failed to decode binary content"}), 400
        # Lock and update file
        file_obj = File(path=file_path, type=file_type, content=updated_content)
        result, duration = PerformanceMetrics.time_operation(
            file_service.update_file,
            file_obj,
            updated_content_bytes if file_type == FileType.BINARY else updated_content,
        )
        if not result:
            return jsonify({"error": "Concurrent update conflict"}), 409
        # Write file
        with open(
            abs_path,
            "wb" if file_type == FileType.BINARY else "w",
            encoding=None if file_type == FileType.BINARY else "utf-8",
        ) as f:
            if file_type == FileType.BINARY:
                f.write(updated_content_bytes)
            else:
                f.write(updated_content)
        # Check performance
        if not PerformanceMetrics.is_within_threshold(duration):
            return jsonify(
                {
                    "warning": "File updated but operation exceeded performance threshold",
                    "duration": duration,
                }
            ), 200
        return jsonify(
            {"message": "File updated and staged", "duration": duration}
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
