"""
Main application entry point for the Cloud Cost Optimizer API.
This module integrates all API endpoints and provides the main Flask application.
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# Import API blueprints
from src.api.auth import auth_bp
from src.api.ai import ai_bp
from src.api.cloud_accounts import cloud_accounts_bp
from src.api.accounts import accounts_bp
from src.api.resources import resources_bp
from src.api.costs import costs_bp
from src.api.recommendations import recommendations_bp
from src.api.actions import actions_bp
from src.api.workflows import workflows_bp
from src.api.terraform_api import terraform_bp
from src.api.kubernetes_api import kubernetes_bp
from src.api.pipeline_api import pipeline_bp
from src.api.aws_resources import aws_resources_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(cloud_accounts_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(costs_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(actions_bp)
    app.register_blueprint(workflows_bp)
    app.register_blueprint(terraform_bp)
    app.register_blueprint(kubernetes_bp)
    app.register_blueprint(pipeline_bp)
    app.register_blueprint(aws_resources_bp)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'services': {
                'api': 'up',
                'database': 'up',
                'ai': 'up'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors."""
        logger.error(f"Server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Create and run the application
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=False)


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200
