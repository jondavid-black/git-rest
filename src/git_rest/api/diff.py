from flask import Blueprint, jsonify, request

from ..audit import audit_repo_action
from ..models.repository_store import RepositoryStore

# Update blueprint to match user-based URL structure
diff_bp = Blueprint("diff", __name__, url_prefix="/users/<user>/repos/<repo>/diff")
store = RepositoryStore()


@diff_bp.route("/", methods=["GET"])
@audit_repo_action("get_diff")
def get_diff(user, repo):
    """
    Get the diff between two commits or the working tree for a user's repository.
    ---
    parameters:
      - in: path
        name: user
        required: true
        schema:
          type: string
        description: The user identifier.
      - in: path
        name: repo
        required: true
        schema:
          type: string
        description: The repository identifier.
      - in: query
        name: a
        required: false
        schema:
          type: string
        description: The first commit hash or ref.
      - in: query
        name: b
        required: false
        schema:
          type: string
        description: The second commit hash or ref.
    responses:
      200:
        description: The diff output between the specified commits or working tree.
      400:
        description: Error occurred or invalid input.
    """
    commit_a = request.args.get("a")
    commit_b = request.args.get("b")
    try:
        # Use user and repo to get the correct repository (assuming store supports user isolation)
        repo_obj = (
            store.get_user_repo(user, repo)
            if hasattr(store, "get_user_repo")
            else store.get_repo(repo)
        )
        git_repo = store._load_git_repo(repo_obj.path)
        if commit_a and commit_b:
            diff = git_repo.git.diff(commit_a, commit_b)
        else:
            diff = git_repo.git.diff()
        return jsonify({"diff": diff})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
