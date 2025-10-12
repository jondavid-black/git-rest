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
    """
    Commit staged changes to the specified repository for a user.
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
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            message:
              type: string
              description: The commit message.
            author:
              type: string
              description: The author name for the commit.
    responses:
      200:
        description: Commit created successfully.
      400:
        description: Invalid input, detached HEAD, or error occurred.
    """
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
