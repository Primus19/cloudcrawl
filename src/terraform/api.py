"""
API endpoints for Terraform management in the Cloud Cost Optimizer.
This module provides REST API endpoints to manage Terraform templates and deployments.
"""

from flask import Blueprint, request, jsonify
import os
import json
from src.terraform.main import TerraformManager

# Initialize the Terraform manager
terraform_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'terraform')
templates_dir = os.path.join(terraform_dir, 'templates')
state_dir = os.path.join(terraform_dir, 'state')

# Create directories if they don't exist
os.makedirs(templates_dir, exist_ok=True)
os.makedirs(state_dir, exist_ok=True)

terraform_manager = TerraformManager(templates_dir=templates_dir, state_dir=state_dir)

# Create Blueprint
terraform_bp = Blueprint('terraform', __name__, url_prefix='/api/v1/terraform')

@terraform_bp.route('/templates', methods=['GET'])
def get_templates():
    """Get all Terraform templates."""
    templates = terraform_manager.get_templates()
    return jsonify({
        'success': True,
        'data': templates
    })

@terraform_bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    """Get a specific Terraform template."""
    template = terraform_manager.get_template(template_id)
    if not template:
        return jsonify({
            'success': False,
            'error': 'Template not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': template
    })

@terraform_bp.route('/templates', methods=['POST'])
def create_template():
    """Create a new Terraform template."""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'description', 'variables', 'content']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400
    
    template = terraform_manager.create_template(
        name=data['name'],
        description=data['description'],
        variables=data['variables'],
        content=data['content']
    )
    
    return jsonify({
        'success': True,
        'data': template,
        'message': 'Template created successfully'
    }), 201

@terraform_bp.route('/templates/<template_id>', methods=['PUT'])
def update_template(template_id):
    """Update an existing Terraform template."""
    data = request.json
    
    template = terraform_manager.update_template(template_id, data)
    if not template:
        return jsonify({
            'success': False,
            'error': 'Template not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': template,
        'message': 'Template updated successfully'
    })

@terraform_bp.route('/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    """Delete a Terraform template."""
    success = terraform_manager.delete_template(template_id)
    if not success:
        return jsonify({
            'success': False,
            'error': 'Template not found'
        }), 404
    
    return jsonify({
        'success': True,
        'message': 'Template deleted successfully'
    })

@terraform_bp.route('/templates/<template_id>/deploy', methods=['POST'])
def deploy_template(template_id):
    """Deploy a Terraform template."""
    data = request.json
    
    if 'variables' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required field: variables'
        }), 400
    
    deployment = terraform_manager.deploy_template(template_id, data['variables'])
    if not deployment:
        return jsonify({
            'success': False,
            'error': 'Template not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': deployment,
        'message': 'Deployment started successfully'
    }), 202

@terraform_bp.route('/deployments', methods=['GET'])
def get_deployments():
    """Get all Terraform deployments."""
    deployments = terraform_manager.get_deployments()
    return jsonify({
        'success': True,
        'data': deployments
    })

@terraform_bp.route('/deployments/<deployment_id>', methods=['GET'])
def get_deployment(deployment_id):
    """Get a specific Terraform deployment."""
    deployment = terraform_manager.get_deployment(deployment_id)
    if not deployment:
        return jsonify({
            'success': False,
            'error': 'Deployment not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': deployment
    })
