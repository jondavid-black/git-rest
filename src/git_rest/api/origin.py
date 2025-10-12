from flask import Blueprint, jsonify

from .repos import get_user_store

origin_bp = Blueprint(
    "origin", __name__, url_prefix="/users/<user_id>/repos/<repo_id>/origin"
)


@origin_bp.route("/", methods=["GET"])
def get_origin(user_id, repo_id):
    store = get_user_store(user_id)
    try:
        repo = store.get_repo(repo_id)
        # Return the first remote's URL if available, else None
        origin_url = None
        for remote in repo.remotes:
            if remote.name == "origin":
                origin_url = remote.url
                break
        if not origin_url and repo.remotes:
            origin_url = repo.remotes[0].url
        return jsonify({"origin": origin_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 404
