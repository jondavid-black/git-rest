from flask import Flask
from .error_handling import register_error_handlers
from .auth import login

def create_app():
    app = Flask(__name__)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints (add as implemented)
    # from .api.repos import repos_bp
    # app.register_blueprint(repos_bp)

    # Register auth/login endpoint
    app.add_url_rule('/login', 'login', login, methods=['POST'])

    # Health check endpoint
    @app.route('/healthz')
    def healthz():
        return {"status": "ok"}

    return app
