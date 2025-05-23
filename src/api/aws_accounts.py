"""
API endpoints for AWS account management in Cloud Cost Optimizer.
"""
from flask import Blueprint, request, jsonify
import os
import logging
from src.providers.aws.services.aws_account_manager import AWSAccountManager

# Initialize logger
logger = logging.getLogger(__name__)

# Create blueprint
aws_accounts_bp = Blueprint('aws_accounts', __name__)

# Initialize AWS account manager
db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:changeme@postgres:5432/cloud_cost_optimizer')
encryption_key = os.environ.get('CREDENTIAL_ENCRYPTION_KEY', 'changeme_with_secure_random_key')
aws_account_manager = AWSAccountManager(db_url, encryption_key)

@aws_accounts_bp.route('/api/v1/aws/accounts', methods=['GET'])
def list_accounts():
    """List all AWS accounts."""
    try:
        accounts = aws_account_manager.get_accounts()
        return jsonify(accounts)
    except Exception as e:
        logger.error(f"Error listing AWS accounts: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_accounts_bp.route('/api/v1/aws/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    """Get an AWS account by ID."""
    try:
        account = aws_account_manager.get_account(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        return jsonify(account)
    except Exception as e:
        logger.error(f"Error getting AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_accounts_bp.route('/api/v1/aws/accounts', methods=['POST'])
def create_account():
    """Create a new AWS account."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        credentials = data.get('credentials')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        if not credentials:
            return jsonify({'error': 'Credentials are required'}), 400
        
        account = aws_account_manager.create_account(name, credentials)
        return jsonify(account), 201
    except ValueError as e:
        logger.error(f"Validation error creating AWS account: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating AWS account: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_accounts_bp.route('/api/v1/aws/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    """Update an AWS account."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        credentials = data.get('credentials')
        
        account = aws_account_manager.update_account(account_id, name, credentials)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        return jsonify(account)
    except ValueError as e:
        logger.error(f"Validation error updating AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_accounts_bp.route('/api/v1/aws/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    """Delete an AWS account."""
    try:
        success = aws_account_manager.delete_account(account_id)
        if not success:
            return jsonify({'error': 'Account not found'}), 404
        
        return jsonify({'message': f'Account {account_id} deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@aws_accounts_bp.route('/api/v1/aws/accounts/<int:account_id>/test-connection', methods=['POST'])
def test_connection(account_id):
    """Test connection to an AWS account."""
    try:
        result = aws_account_manager.test_connection(account_id)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error testing connection to AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error testing connection to AWS account {account_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500
