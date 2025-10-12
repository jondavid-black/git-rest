import os

from flask import Blueprint, jsonify

from ..audit import audit_repo_action
from ..models.repository_store import RepositoryStore

status_bp = Blueprint(
    "status", __name__, url_prefix="/users/<user_id>/repos/<repo_id>/status"
)


@status_bp.route("/", methods=["GET"])
@audit_repo_action("get_repo_status")
def get_repo_status(user_id, repo_id):
    """
    Get the status of a repository for a user.
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
    responses:
      200:
        description: The status of the repository, including branch, cleanliness, and file status.
      404:
        description: Repository not found or error occurred.
    """
    base_dir = os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
    user_dir = os.path.join(base_dir, user_id)
    store = RepositoryStore(base_dir=user_dir)
    try:
        repo = store.get_repo(repo_id)
        # Compose a status dict with branch, is_clean, and status details
        status = repo.status.dict() if repo.status else {}
        # Compute is_clean: no staged, unstaged, or untracked files
        is_clean = (
            not status.get("staged")
            and not status.get("unstaged")
            and not status.get("untracked")
        )
        result = {
            "branch": repo.current_branch,
            "is_clean": is_clean,
            **status,
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
