"""
API endpoints for AWS resources in Cloud Cost Optimizer.
"""
from flask import Blueprint, request, jsonify
import os
import logging
from src.providers.aws.services.aws_account_manager import AWSAccountManager
from src.providers.aws.services.aws_resource_manager import AWSResourceManager

# Initialize logger
logger = logging.getLogger(__name__)

# Create blueprint
aws_resources_bp = Blueprint('aws_resources', __name__)

# Initialize managers
db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:changeme@postgres:5432/cloud_cost_optimizer')
encryption_key = os.environ.get('CREDENTIAL_ENCRYPTION_KEY', 'changeme_with_secure_random_key')
aws_account_manager = AWSAccountManager(db_url, encryption_key)
aws_resource_manager = AWSResourceManager(db_url, aws_account_manager)

@aws_resources_bp.route('/api/v1/aws/resources', methods=['GET'])
def list_resources():
    """List all AWS resources."""
    try:
        account_id = request.args.get('account_id', type=int)
        resource_type = request.args.get('resource_type')
        region = request.args.get('region')
        
        resources = aws_resource_manager.get_resources(account_id, resource_type, region)
        return jsonify(resources)
    except Exception as e:
        logger.error(f"Error listing AWS resources: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_resources_bp.route('/api/v1/aws/resources/<string:resource_id>', methods=['GET'])
def get_resource(resource_id):
    """Get an AWS resource by ID."""
    try:
        resource = aws_resource_manager.get_resource(resource_id)
        if not resource:
            return jsonify({'error': 'Resource not found'}), 404
        return jsonify(resource)
    except Exception as e:
        logger.error(f"Error getting AWS resource {resource_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_resources_bp.route('/api/v1/aws/accounts/<int:account_id>/discover', methods=['POST'])
def discover_resources(account_id):
    """Discover AWS resources for an account."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        resource_types = data.get('resource_types', ['ec2', 's3', 'rds', 'lambda', 'eks'])
        regions = data.get('regions', ['us-east-1', 'us-west-1', 'us-west-2', 'eu-west-1'])
        
        result = aws_resource_manager.discover_resources(account_id, resource_types, regions)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error discovering AWS resources for account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error discovering AWS resources for account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_resources_bp.route('/api/v1/aws/accounts/<int:account_id>/costs', methods=['GET'])
def get_costs(account_id):
    """Get cost data for an AWS account."""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        result = aws_resource_manager.get_costs(account_id, start_date, end_date)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error getting costs for AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error getting costs for AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_resources_bp.route('/api/v1/aws/accounts/<int:account_id>/recommendations', methods=['GET'])
def get_recommendations(account_id):
    """Get optimization recommendations for an AWS account."""
    try:
        result = aws_resource_manager.get_recommendations(account_id)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error getting recommendations for AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error getting recommendations for AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500
