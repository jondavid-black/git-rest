import os

from flask import Flask

from .auth import login
from .error_handling import register_error_handlers


def create_app():
    app = Flask(__name__)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints (add as implemented)
    from .api.branches import branches_bp
    from .api.commit import commit_bp
    from .api.diff import diff_bp
    from .api.files import files_bp
    from .api.origin import origin_bp
    from .api.repos import repos_bp

    app.register_blueprint(repos_bp)
    app.register_blueprint(branches_bp)
    app.register_blueprint(commit_bp)
    app.register_blueprint(diff_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(origin_bp)

    # Register auth/login endpoint
    app.add_url_rule("/login", "login", login, methods=["POST"])

    # Set git_rest logger to DEBUG if running tests or GIT_REST_DEBUG is set
    import logging
    import sys

    debug_env = os.environ.get("GIT_REST_DEBUG")
    running_tests = (
        "pytest" in sys.modules
        or "behave" in sys.modules
        or any("pytest" in arg or "behave" in arg for arg in sys.argv)
    )
    if debug_env or running_tests:
        # Set DEBUG for all git_rest submodules
        for name in logging.root.manager.loggerDict:
            if name.startswith("git_rest"):
                logging.getLogger(name).setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)

    # Health check endpoint
    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}

    return app
