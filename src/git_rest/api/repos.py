
from flask import Blueprint, jsonify, request
import os
from ..audit import audit_repo_action
from ..context import RepoContext
from ..models.repository_store import RepositoryStore
from ..schemas import RepoNameSchema

repos_bp = Blueprint("repos", __name__, url_prefix="/users/<user_id>/repos")

def get_user_store(user_id):
    # Each user's repos are stored in a separate directory: <base_dir>/<user_id>/
    base_dir = os.environ.get("GIT_REST_WORKDIR", "/tmp/git-rest")
    user_dir = os.path.join(base_dir, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, exist_ok=True)
    return RepositoryStore(base_dir=user_dir)



@repos_bp.route("/", methods=["GET"])
@audit_repo_action("list_repos")
def list_repos(user_id):
    store = get_user_store(user_id)
    repos = store.list_repos()
    return jsonify([repo.dict() for repo in repos])



@repos_bp.route("/", methods=["POST"])
@audit_repo_action("clone_repo")
def clone_repo(user_id):
    store = get_user_store(user_id)
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



# GET /users/<user_id>/repos/<repo_id>: Get repository details
@repos_bp.route("/<repo_id>", methods=["GET"])
@audit_repo_action("get_repo_details")
def get_repo_details(user_id, repo_id):
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        return jsonify(repo.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 404



# POST /users/<user_id>/repos/<repo_id>: Switch active repository (dummy context for now)
@repos_bp.route("/<repo_id>", methods=["POST"])
@audit_repo_action("switch_repo")
def switch_repo(user_id, repo_id):
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        RepoContext.set_current_repo(repo_id)
        return jsonify(
            {"message": f"Switched to repository '{repo_id}'", "repo": repo.dict()}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 404
