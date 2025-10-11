import logging
from flask import Flask, jsonify

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)
logger = logging.getLogger("git_rest")

# Error handling utilities
def register_error_handlers(app: Flask):
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"400 Bad Request: {error}")
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        logger.warning(f"401 Unauthorized: {error}")
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(404)
    def not_found(error):
        logger.info(f"404 Not Found: {error}")
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        logger.warning(f"422 Unprocessable Entity: {error}")
        return jsonify({"error": "Unprocessable entity"}), 422

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 Internal Server Error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    # Optionally, handle all uncaught exceptions
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.exception(f"Unhandled Exception: {error}")
        return jsonify({"error": "Unexpected server error"}), 500
