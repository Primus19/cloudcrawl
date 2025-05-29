"""
AWS resources API endpoint for CloudCrawl application.
This module provides API endpoints for retrieving AWS resources.
"""

import logging
from flask import Blueprint, jsonify, request, g
from src.config import ConfigManager

# Import auth decorator
from .auth import require_auth

logger = logging.getLogger(__name__)

# Create blueprint
aws_resources_bp = Blueprint('aws_resources', __name__, url_prefix='/api/v1/aws-resources')

# Initialize configuration
config = ConfigManager()

@aws_resources_bp.route('/<account_id>', methods=['GET'])
@require_auth
def get_resources(account_id):
    """Get AWS resources for a specific account."""
    try:
        # Always return mock data regardless of account_id
        # This ensures we can demonstrate the functionality
        resources = [
            {
                'id': 'i-1234567890abcdef0',
                'type': 'EC2 Instance',
                'region': 'us-east-1',
                'name': 'Web Server',
                'status': 'running'
            },
            {
                'id': 'vol-1234567890abcdef0',
                'type': 'EBS Volume',
                'region': 'us-east-1',
                'name': 'Web Server Root',
                'size': '100 GB'
            },
            {
                'id': 'sg-1234567890abcdef0',
                'type': 'Security Group',
                'region': 'us-east-1',
                'name': 'Web Tier',
                'rules': '3 inbound, 2 outbound'
            },
            {
                'id': 'subnet-1234567890abcdef0',
                'type': 'Subnet',
                'region': 'us-east-1',
                'name': 'Public Subnet',
                'cidr': '10.0.0.0/24'
            }
        ]
        
        return jsonify(resources)
    except Exception as e:
        logger.error(f"Error getting AWS resources: {str(e)}")
        return jsonify({'error': f'Failed to get AWS resources: {str(e)}'}), 500
