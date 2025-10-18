import os

from flask import Blueprint, jsonify, request

from ..audit import audit_repo_action
from ..models.repository_store import RepositoryStore
from ..schemas import BranchNameSchema

branches_bp = Blueprint(
    "branches", __name__, url_prefix="/users/<user_id>/repos/<repo_id>/branches"
)


def get_user_store(user_id):
    base_dir = os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
    user_dir = os.path.join(base_dir, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, exist_ok=True)
    return RepositoryStore(base_dir=user_dir)


@branches_bp.route("/", methods=["GET"])
@audit_repo_action("list_branches")
def list_branches(user_id, repo_id):
    """
    List all branches in the specified repository for a user.
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
        description: A list of branches in the repository.
      404:
        description: Repository not found or error occurred.
    """
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        return jsonify([branch.dict() for branch in repo.branches])
    except Exception as e:
        from flask import current_app

        current_app.logger.error(f"Exception in commit endpoint: {e}")
        return jsonify({"error": "An internal error occurred."}), 404


@branches_bp.route("/", methods=["POST"])
@audit_repo_action("create_branch")
def create_branch(user_id, repo_id):
    """
    Create a new branch in the specified repository for a user.
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
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the new branch.
    responses:
      201:
        description: Branch created successfully.
      400:
        description: Invalid input or error occurred.
    """
    store = get_user_store(user_id)
    data = request.get_json()
    schema = BranchNameSchema(**data)
    try:
        repo = store.get_repo(repo_id)
        git_repo = store._load_git_repo(repo.path)
        # If in detached HEAD, checkout the first branch
        if git_repo.head.is_detached and git_repo.branches:
            git_repo.git.checkout(git_repo.branches[0].name)
        # Check if branch already exists
        if schema.name in [b.name for b in git_repo.branches]:
            return jsonify({"error": f"Branch '{schema.name}' already exists."}), 409
        git_repo.git.branch(schema.name)
        # Reload repo to get updated branches
        repo = store.get_repo(repo_id)
        return jsonify([branch.dict() for branch in repo.branches]), 201
    except Exception as e:
        from flask import current_app

        current_app.logger.error(f"Exception in commit endpoint: {e}")
        return jsonify({"error": "An internal error occurred."}), 400


@branches_bp.route("/<branch>", methods=["POST"])
@audit_repo_action("switch_branch")
def switch_branch(user_id, repo_id, branch):
    """
    Switch to a different branch in the specified repository for a user.
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
        name: branch
        required: true
        schema:
          type: string
        description: The branch name to switch to.
    responses:
      200:
        description: Switched to the specified branch.
      404:
        description: Branch or repository not found.
    """
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        git_repo = store._load_git_repo(repo.path)
        git_repo.git.checkout(branch)
        # Reload repo to get updated current branch
        repo = store.get_repo(repo_id)
        return jsonify(
            {"message": f"Switched to branch '{branch}'", "repo": repo.dict()}
        )
    except Exception as e:
        from flask import current_app

        current_app.logger.error(f"Exception in commit endpoint: {e}")
        return jsonify({"error": "An internal error occurred."}), 400


@branches_bp.route("/<branch>", methods=["DELETE"])
@audit_repo_action("delete_branch")
def delete_branch(user_id, repo_id, branch):
    """
    Delete a branch from the specified repository for a user.
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
        name: branch
        required: true
        schema:
          type: string
        description: The branch name to delete.
    responses:
      200:
        description: Branch deleted successfully.
      404:
        description: Branch or repository not found.
    """
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        git_repo = store._load_git_repo(repo.path)
        # If the branch to delete is checked out, switch to another branch first
        if git_repo.active_branch.name == branch:
            # Try to switch to 'master', 'main', or any other branch
            candidates = [b.name for b in git_repo.branches if b.name != branch]
            fallback = None
            for candidate in ["master", "main"]:
                if candidate in candidates:
                    fallback = candidate
                    break
            if not fallback and candidates:
                fallback = candidates[0]
            if fallback:
                git_repo.git.checkout(fallback)
            else:
                return jsonify(
                    {"error": f"Cannot delete the only branch '{branch}'."}
                ), 400
        git_repo.git.branch("-D", branch)
        # Reload repo to get updated branches
        repo = store.get_repo(repo_id)
        return jsonify([b.dict() for b in repo.branches])
    except Exception as e:
        from flask import current_app

        current_app.logger.error(f"Exception in commit endpoint: {e}")
        return jsonify({"error": "An internal error occurred."}), 400
