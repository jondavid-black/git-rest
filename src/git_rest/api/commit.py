from flask import Blueprint, jsonify, request
from git import Actor

from ..audit import audit_repo_action
from ..models.repository_store import RepositoryStore

# Update blueprint to match user-based URL structure
commit_bp = Blueprint(
    "commit", __name__, url_prefix="/users/<user>/repos/<repo>/commit"
)
store = RepositoryStore()


@commit_bp.route("/", methods=["POST"])
@audit_repo_action("commit_changes")
def commit_changes(user, repo):
    data = request.get_json()
    message = data.get("message")
    author_name = data.get("author")
    if not message or not author_name:
        return jsonify({"error": "Missing commit message or author"}), 400
    try:
        # Use user and repo to get the correct repository (assuming store supports user isolation)
        repo_obj = (
            store.get_user_repo(user, repo)
            if hasattr(store, "get_user_repo")
            else store.get_repo(repo)
        )
        git_repo = store._load_git_repo(repo_obj.path)
        # Check for detached HEAD state
        if git_repo.head.is_detached:
            return jsonify({"error": "Cannot commit in detached HEAD state."}), 400
        # Stage all changes
        git_repo.git.add(A=True)
        # Use git.Actor for author
        author = Actor(author_name, "")
        commit = git_repo.index.commit(message, author=author)
        return jsonify(
            {
                "hash": commit.hexsha,
                "author": commit.author.name,
                "date": commit.committed_datetime.isoformat(),
                "message": commit.message.strip(),
                "parent_hashes": [p.hexsha for p in commit.parents],
            }
        ), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
