"""
Main application file for the Cloud Cost Optimizer backend.
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)

    # Register API blueprints
    from src.api.accounts import accounts_bp
    from src.api.resources import resources_bp
    from src.api.costs import costs_bp
    from src.api.recommendations import recommendations_bp
    from src.api.actions import actions_bp
    from src.api.workflows import workflows_bp

    app.register_blueprint(accounts_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(costs_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(actions_bp)
    app.register_blueprint(workflows_bp)

    # Add health check endpoint
    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        """Health check endpoint for readiness and liveness probes."""
        return jsonify({"status": "healthy"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
