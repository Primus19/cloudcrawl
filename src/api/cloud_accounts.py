"""
Cloud accounts API endpoints for CloudCrawl application.
This module provides API endpoints for managing cloud provider accounts.
"""

import logging
from flask import Blueprint, jsonify, request, g
from src.config import ConfigManager
from src.providers.aws.services.aws_account_manager import AWSAccountManager
from src.providers.azure.services.azure_provider import AzureProvider
from src.providers.gcp.services.gcp_provider import GCPProvider
from .auth import require_auth

logger = logging.getLogger(__name__)

# Create blueprint
cloud_accounts_bp = Blueprint('cloud_accounts', __name__, url_prefix='/api/v1/cloud-accounts')

# Initialize configuration
config = ConfigManager()

# Initialize providers with configuration
aws_account_manager = AWSAccountManager()
azure_provider = AzureProvider()
gcp_provider = GCPProvider()

@cloud_accounts_bp.route('', methods=['GET'])
@require_auth
def list_accounts():
    """List all cloud accounts."""
    try:
        # Get accounts from all providers
        aws_accounts = aws_account_manager.list_accounts()
        
        # In a real implementation, this would also get accounts from other providers
        # For now, return mock data for development/testing
        accounts = {
            'aws': aws_accounts,
            'azure': [
                {
                    'id': 'azure-subscription-1',
                    'name': 'Production Azure Subscription',
                    'subscription_id': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
                    'status': 'active'
                }
            ],
            'gcp': [
                {
                    'id': 'gcp-project-1',
                    'name': 'Production GCP Project',
                    'project_id': 'my-gcp-project-123',
                    'status': 'active'
                }
            ]
        }
        
        return jsonify(accounts)
    except Exception as e:
        logger.error(f"Error listing cloud accounts: {str(e)}")
        return jsonify({'error': 'Failed to list cloud accounts'}), 500

@cloud_accounts_bp.route('/<provider>/<account_id>', methods=['GET'])
@require_auth
def get_account(provider, account_id):
    """Get details for a specific cloud account."""
    try:
        if provider == 'aws':
            account = aws_account_manager.get_account(account_id)
            if not account:
                return jsonify({'error': 'Account not found'}), 404
            return jsonify(account)
        elif provider == 'azure':
            # Mock Azure account for development/testing
            return jsonify({
                'id': account_id,
                'name': 'Production Azure Subscription',
                'subscription_id': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
                'status': 'active'
            })
        elif provider == 'gcp':
            # Mock GCP account for development/testing
            return jsonify({
                'id': account_id,
                'name': 'Production GCP Project',
                'project_id': 'my-gcp-project-123',
                'status': 'active'
            })
        else:
            return jsonify({'error': 'Invalid provider'}), 400
    except Exception as e:
        logger.error(f"Error getting cloud account: {str(e)}")
        return jsonify({'error': 'Failed to get cloud account'}), 500

@cloud_accounts_bp.route('/<provider>', methods=['POST'])
@require_auth
def add_account(provider):
    """Add a new cloud account."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        if provider == 'aws':
            required_fields = ['name', 'account_id', 'access_key', 'secret_key', 'regions']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
                    
            account = aws_account_manager.add_account(
                name=data['name'],
                account_id=data['account_id'],
                access_key=data['access_key'],
                secret_key=data['secret_key'],
                regions=data['regions']
            )
            return jsonify(account), 201
        elif provider == 'azure':
            # Mock Azure account creation for development/testing
            return jsonify({
                'id': 'azure-subscription-new',
                'name': data.get('name', 'New Azure Subscription'),
                'subscription_id': data.get('subscription_id', 'new-subscription-id'),
                'status': 'active'
            }), 201
        elif provider == 'gcp':
            # Mock GCP account creation for development/testing
            return jsonify({
                'id': 'gcp-project-new',
                'name': data.get('name', 'New GCP Project'),
                'project_id': data.get('project_id', 'new-gcp-project'),
                'status': 'active'
            }), 201
        else:
            return jsonify({'error': 'Invalid provider'}), 400
    except Exception as e:
        logger.error(f"Error adding cloud account: {str(e)}")
        return jsonify({'error': 'Failed to add cloud account'}), 500

@cloud_accounts_bp.route('/<provider>/<account_id>', methods=['PUT'])
@require_auth
def update_account(provider, account_id):
    """Update an existing cloud account."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        if provider == 'aws':
            account = aws_account_manager.update_account(account_id, data)
            if not account:
                return jsonify({'error': 'Account not found'}), 404
            return jsonify(account)
        elif provider == 'azure':
            # Mock Azure account update for development/testing
            return jsonify({
                'id': account_id,
                'name': data.get('name', 'Updated Azure Subscription'),
                'subscription_id': data.get('subscription_id', 'updated-subscription-id'),
                'status': 'active'
            })
        elif provider == 'gcp':
            # Mock GCP account update for development/testing
            return jsonify({
                'id': account_id,
                'name': data.get('name', 'Updated GCP Project'),
                'project_id': data.get('project_id', 'updated-gcp-project'),
                'status': 'active'
            })
        else:
            return jsonify({'error': 'Invalid provider'}), 400
    except Exception as e:
        logger.error(f"Error updating cloud account: {str(e)}")
        return jsonify({'error': 'Failed to update cloud account'}), 500

@cloud_accounts_bp.route('/<provider>/<account_id>', methods=['DELETE'])
@require_auth
def delete_account(provider, account_id):
    """Delete a cloud account."""
    try:
        if provider == 'aws':
            success = aws_account_manager.delete_account(account_id)
            if not success:
                return jsonify({'error': 'Account not found'}), 404
            return jsonify({'message': 'Account deleted successfully'})
        elif provider == 'azure':
            # Mock Azure account deletion for development/testing
            return jsonify({'message': 'Azure account deleted successfully'})
        elif provider == 'gcp':
            # Mock GCP account deletion for development/testing
            return jsonify({'message': 'GCP account deleted successfully'})
        else:
            return jsonify({'error': 'Invalid provider'}), 400
    except Exception as e:
        logger.error(f"Error deleting cloud account: {str(e)}")
        return jsonify({'error': 'Failed to delete cloud account'}), 500

@cloud_accounts_bp.route('/<provider>/<account_id>/costs', methods=['GET'])
@require_auth
def get_account_costs(provider, account_id):
    """Get cost data for a specific cloud account."""
    try:
        if provider == 'aws':
            costs = aws_account_manager.get_cost_data(account_id)
            if not costs:
                return jsonify({'error': 'Account not found'}), 404
            return jsonify(costs)
        elif provider == 'azure':
            # Mock Azure costs for development/testing
            return jsonify({
                'subscription_id': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
                'total_cost': 987.65,
                'currency': 'USD',
                'time_period': {
                    'start': '2023-01-01',
                    'end': '2023-01-31'
                },
                'services': [
                    {
                        'name': 'Virtual Machines',
                        'cost': 456.78
                    },
                    {
                        'name': 'Storage',
                        'cost': 98.76
                    }
                ]
            })
        elif provider == 'gcp':
            # Mock GCP costs for development/testing
            return jsonify({
                'project_id': 'my-gcp-project-123',
                'total_cost': 765.43,
                'currency': 'USD',
                'time_period': {
                    'start': '2023-01-01',
                    'end': '2023-01-31'
                },
                'services': [
                    {
                        'name': 'Compute Engine',
                        'cost': 345.67
                    },
                    {
                        'name': 'Cloud Storage',
                        'cost': 76.54
                    }
                ]
            })
        else:
            return jsonify({'error': 'Invalid provider'}), 400
    except Exception as e:
        logger.error(f"Error getting account costs: {str(e)}")
        return jsonify({'error': 'Failed to get account costs'}), 500
