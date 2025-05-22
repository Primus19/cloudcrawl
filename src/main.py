"""
Main application entry point for the Cloud Cost Optimizer.
This module initializes the Flask application and registers all blueprints.
"""

import os
import sys
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='ui/dashboard/build', static_url_path='')
    CORS(app)  # Enable CORS for all routes
    
    # Register API blueprints
    from src.api.accounts import accounts_bp
    from src.api.resources import resources_bp
    from src.api.costs import costs_bp
    from src.api.recommendations import recommendations_bp
    from src.api.actions import actions_bp
    from src.api.workflows import workflows_bp
    from src.terraform.api import terraform_bp
    
    app.register_blueprint(accounts_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(costs_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(actions_bp)
    app.register_blueprint(workflows_bp)
    app.register_blueprint(terraform_bp)
    
    # Serve React app
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
