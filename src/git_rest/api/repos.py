from flask import Blueprint, jsonify, request

from ..audit import audit_repo_action
from ..context import RepoContext
from ..models.repository_store import RepositoryStore
from ..schemas import RepoNameSchema

repos_bp = Blueprint("repos", __name__, url_prefix="/repos")
store = RepositoryStore()


@repos_bp.route("/", methods=["GET"])
@audit_repo_action("list_repos")
def list_repos():
    repos = store.list_repos()
    return jsonify([repo.dict() for repo in repos])


@repos_bp.route("/", methods=["POST"])
@audit_repo_action("clone_repo")
def clone_repo():
    data = request.get_json()
    schema = RepoNameSchema(**data)
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' field"}), 400
    try:
        repo = store.clone_repo(schema.name, url)
        return jsonify(repo.dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# GET /repos/<repo_id>: Get repository details
@repos_bp.route("/<repo_id>", methods=["GET"])
@audit_repo_action("get_repo_details")
def get_repo_details(repo_id):
    try:
        repo = store.get_repo(repo_id)
        return jsonify(repo.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 404


# POST /repos/<repo_id>: Switch active repository (dummy context for now)
@repos_bp.route("/<repo_id>", methods=["POST"])
@audit_repo_action("switch_repo")
def switch_repo(repo_id):
    try:
        repo = store.get_repo(repo_id)
        RepoContext.set_current_repo(repo_id)
        return jsonify(
            {"message": f"Switched to repository '{repo_id}'", "repo": repo.dict()}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 404
