from flask import Flask
from .error_handling import register_error_handlers
from .auth import login

def create_app():
    app = Flask(__name__)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints (add as implemented)
    from .api.repos import repos_bp
    from .api.branches import branches_bp
    from .api.commit import commit_bp
    from .api.diff import diff_bp
    from .api.files import files_bp
    app.register_blueprint(repos_bp)
    app.register_blueprint(branches_bp)
    app.register_blueprint(commit_bp)
    app.register_blueprint(diff_bp)
    app.register_blueprint(files_bp)

    # Register auth/login endpoint
    app.add_url_rule('/login', 'login', login, methods=['POST'])

    # Health check endpoint
    @app.route('/healthz')
    def healthz():
        return {"status": "ok"}

    return app
