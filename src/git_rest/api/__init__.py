from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

# User-scoped endpoints will be registered in their respective modules (repos, branches, files, etc.)
