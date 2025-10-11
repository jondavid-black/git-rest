from flask import Blueprint, jsonify, request
from flask import send_file, redirect, url_for, request
from ..services.secure_url import SecureURLGenerator
from ..models.repository_store import RepositoryStore
from ..audit import audit_repo_action
from ..filesystem import FileSystemIsolation
import os
import datetime

files_bp = Blueprint("files", __name__, url_prefix="/repos/<repo_id>/files")
store = RepositoryStore()

@files_bp.route("/", methods=["GET"])
@audit_repo_action("list_files")
def list_files(repo_id):
    rel_path = request.args.get("path", "")
    try:
        repo = store.get_repo(repo_id)
        fs = FileSystemIsolation(repo.path)
        dir_path = fs.safe_join(rel_path)
        entries = []
        for entry in os.scandir(dir_path):
            stat = entry.stat()
            entries.append({
                "path": os.path.relpath(entry.path, repo.path),
                "type": "dir" if entry.is_dir() else "file" if entry.is_file() else "symlink",
                "size": stat.st_size,
                "last_modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        return jsonify(entries)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@files_bp.route("/<path:file_path>", methods=["GET"])
@audit_repo_action("get_file_content")
def get_file_content(repo_id, file_path):
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
            secure_url = generator.generate(repo_id, file_path)
            return jsonify({"redirect": True, "url": secure_url}), 302
        return send_file(abs_path, as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Secure file download endpoint (verifies token)
@files_bp.route("/<path:file_path>/download", methods=["GET"])
@audit_repo_action("download_file_secure")
def download_file_secure(repo_id, file_path):
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
    