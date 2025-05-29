"""
Main application entry point for the CloudCrawl API.
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from src.config import ConfigManager
from src.api.cloud_accounts import cloud_accounts_bp
from src.api.auth import auth_bp
from src.api.aws_resources import aws_resources_bp

# Initialize configuration
config = ConfigManager()

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes with specific configuration
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(cloud_accounts_bp)
app.register_blueprint(aws_resources_bp)

@app.route('/health')
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

# Debug route to list all registered routes
@app.route('/debug/routes')
def list_routes():
    """List all registered routes for debugging."""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify(routes)

if __name__ == '__main__':
    # Get configuration
    host = os.environ.get('API_HOST', '0.0.0.0')
    port = int(os.environ.get('API_PORT', 5000))
    debug = os.environ.get('API_DEBUG', 'True').lower() == 'true'
    
    # Log startup
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Starting CloudCrawl API server on {host}:{port} (debug={debug})")
    
    # Log all registered routes
    logger.info("Registered routes:")
    for rule in app.url_map.iter_rules():
        logger.info(f"{rule.endpoint}: {rule.rule} {rule.methods}")
    
    # Start server
    app.run(host=host, port=port, debug=debug)
