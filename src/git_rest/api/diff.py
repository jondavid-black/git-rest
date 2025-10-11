from flask import Blueprint, jsonify, request

from ..audit import audit_repo_action
from ..models.repository_store import RepositoryStore

diff_bp = Blueprint("diff", __name__, url_prefix="/repos/<repo_id>/diff")
store = RepositoryStore()


@diff_bp.route("/", methods=["GET"])
@audit_repo_action("get_diff")
def get_diff(repo_id):
    commit_a = request.args.get("a")
    commit_b = request.args.get("b")
    try:
        repo = store.get_repo(repo_id)
        git_repo = store._load_git_repo(repo.path)
        if commit_a and commit_b:
            diff = git_repo.git.diff(commit_a, commit_b)
        else:
            diff = git_repo.git.diff()
        return jsonify({"diff": diff})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
