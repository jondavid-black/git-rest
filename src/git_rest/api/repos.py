import os

from flask import Blueprint, jsonify, request

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
    """
    List all repositories for a user.
    ---
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
        description: The user identifier.
    responses:
      200:
        description: A list of repositories for the user.
    """
    store = get_user_store(user_id)
    repos = store.list_repos()
    return jsonify([repo.dict() for repo in repos])


@repos_bp.route("/init", methods=["POST"])
@audit_repo_action("init_repo")
def init_repo(user_id):
    """
    Initialize a new repository for a user (git init).
    ---
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
        description: The user identifier.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name for the new repository.
    responses:
      201:
        description: Repository initialized successfully.
      400:
        description: Invalid input or error occurred.
      404:
        description: User not found.
      409:
        description: Repository already exists.
      500:
        description: Storage unavailable or internal error.
    """
    try:
        store = get_user_store(user_id)
    except Exception:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json() or {}
    try:
        schema = RepoNameSchema(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    try:
        store.init_repo(schema.name)
        url = f"/users/{user_id}/repos/{schema.name}"
        return jsonify({"url": url}), 201
    except FileExistsError:
        return jsonify({"error": f"Repository '{schema.name}' already exists."}), 409
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except OSError as e:
        return jsonify({"error": f"Storage unavailable: {e}"}), 500
    except Exception as e:
        from flask import current_app

        current_app.logger.error(f"Exception in init_repo endpoint: {e}")
        return jsonify({"error": "An internal error occurred."}), 500


# New explicit clone endpoint
@repos_bp.route("/clone", methods=["POST"])
@audit_repo_action("clone_repo")
def clone_repo(user_id):
    """
    Clone a new repository for a user from a remote URL using explicit endpoint.
    ---
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
        description: The user identifier.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name for the new repository.
            url:
              type: string
              description: The remote repository URL to clone.
    responses:
      201:
        description: Repository cloned successfully.
      400:
        description: Invalid input or error occurred.
    """
    store = get_user_store(user_id)
    data = request.get_json()
    schema = RepoNameSchema(**data)
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' field"}), 400
    try:
        repo = store.clone_repo(schema.name, url)
        return jsonify(repo.dict()), 201
    except FileExistsError:
        return jsonify({"error": f"Repository '{schema.name}' already exists."}), 400
    except Exception as e:
        from flask import current_app

        current_app.logger.error(f"Exception in clone_repo endpoint: {e}")
        return jsonify({"error": "An internal error occurred."}), 400


# GET /users/<user_id>/repos/<repo_id>: Get repository details
@repos_bp.route("/<repo_id>", methods=["GET"])
@audit_repo_action("get_repo_details")
def get_repo_details(user_id, repo_id):
    """
    Get details for a specific repository for a user.
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
        description: Repository details.
      404:
        description: Repository not found or error occurred.
    """
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        return jsonify(repo.dict())
    except Exception as e:
        from flask import current_app

        current_app.logger.error(f"Exception in get_repo_details endpoint: {e}")
        return jsonify({"error": "An internal error occurred."}), 404


# POST /users/<user_id>/repos/<repo_id>: Switch active repository (dummy context for now)
@repos_bp.route("/<repo_id>", methods=["POST"])
@audit_repo_action("switch_repo")
def switch_repo(user_id, repo_id):
    """
    Switch the active repository for a user (dummy context for now).
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
        description: Switched to the specified repository.
      404:
        description: Repository not found or error occurred.
    """
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        RepoContext.set_current_repo(repo_id)
        return jsonify(
            {"message": f"Switched to repository '{repo_id}'", "repo": repo.dict()}
        )
    except FileNotFoundError:
        return jsonify({"error": f"Repository '{repo_id}' not found."}), 404
    except Exception as e:
        from flask import current_app

        current_app.logger.error(f"Exception in switch_repo endpoint: {e}")
        return jsonify({"error": "An internal error occurred."}), 404
