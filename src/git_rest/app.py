import os

from flask import Flask

from .auth import login
from .error_handling import register_error_handlers


def create_app():
    app = Flask(__name__)

    # Enable/disable interactive demo UI via environment variable (GIT_REST_UI)
    enable_demo = os.environ.get("GIT_REST_UI", "0") == "1"
    if enable_demo:
        try:
            # Patch Flasgger's swag_from to inject fallback description if missing

            from flasgger import Swagger
            from flasgger.utils import swag_from

            orig_swag_from = swag_from

            def swag_from_with_fallback(*args, **kwargs):
                swag = orig_swag_from(*args, **kwargs)

                def decorator(f):
                    doc = f.__doc__
                    if not doc or "---" not in doc:
                        # Patch in fallback docstring if missing
                        f.__doc__ = (doc or "") + "\nNo documentation available."
                    return swag(f)

                return decorator

            import flasgger

            flasgger.swag_from = swag_from_with_fallback

            swagger_config = {
                "headers": [],
                "title": "git-rest API Docs",  # Set Swagger UI page title
                "specs": [
                    {
                        "endpoint": "apispec_1",
                        "route": "/apispec_1.json",
                        "rule_filter": lambda rule: True,  # all endpoints
                        "model_filter": lambda tag: True,  # all models
                    }
                ],
                "static_url_path": "/flasgger_static",
                "swagger_ui": True,
                "specs_route": "/apidocs/",
            }
            Swagger(app, config=swagger_config)
            app.logger.info("Interactive API demo UI enabled at /apidocs")
        except ImportError:
            app.logger.warning(
                "flasgger is not installed; interactive demo UI will not be available."
            )
    else:
        app.logger.info(
            "Interactive API demo UI is disabled (set GIT_REST_UI=1 to enable)"
        )

    # Register error handlers
    register_error_handlers(app)

    # Register all blueprints from api/ automatically
    from . import api

    blueprints = [
        getattr(api, attr)
        for attr in dir(api)
        if attr.endswith("_bp") and hasattr(getattr(api, attr), "register")
    ]
    for bp in blueprints:
        app.register_blueprint(bp)

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
