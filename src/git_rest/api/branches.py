from flask import Blueprint, request, jsonify
from ..models.repository_store import RepositoryStore
from ..schemas import BranchNameSchema
from ..audit import audit_repo_action

branches_bp = Blueprint("branches", __name__, url_prefix="/repos/<repo_id>/branches")
store = RepositoryStore()

@branches_bp.route("/", methods=["GET"])
@audit_repo_action("list_branches")
def list_branches(repo_id):
    try:
        repo = store.get_repo(repo_id)
        return jsonify([branch.dict() for branch in repo.branches])
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@branches_bp.route("/", methods=["POST"])
@audit_repo_action("create_branch")
def create_branch(repo_id):
    data = request.get_json()
    schema = BranchNameSchema(**data)
    try:
        repo = store.get_repo(repo_id)
        git_repo = store._load_git_repo(repo.path)
        git_repo.git.branch(schema.name)
        # Reload repo to get updated branches
        repo = store.get_repo(repo_id)
        return jsonify([branch.dict() for branch in repo.branches]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@branches_bp.route("/<branch>", methods=["POST"])
@audit_repo_action("switch_branch")
def switch_branch(repo_id, branch):
    try:
        repo = store.get_repo(repo_id)
        git_repo = store._load_git_repo(repo.path)
        git_repo.git.checkout(branch)
        # Reload repo to get updated current branch
        repo = store.get_repo(repo_id)
        return jsonify({"message": f"Switched to branch '{branch}'", "repo": repo.dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@branches_bp.route("/<branch>", methods=["DELETE"])
@audit_repo_action("delete_branch")
def delete_branch(repo_id, branch):
    try:
        repo = store.get_repo(repo_id)
        git_repo = store._load_git_repo(repo.path)
        git_repo.git.branch('-D', branch)
        # Reload repo to get updated branches
        repo = store.get_repo(repo_id)
        return jsonify([b.dict() for b in repo.branches])
    except Exception as e:
        return jsonify({"error": str(e)}), 400