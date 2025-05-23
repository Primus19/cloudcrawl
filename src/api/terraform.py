"""
API endpoints for Terraform templates in Cloud Cost Optimizer.
"""
from flask import Blueprint, request, jsonify
import os
import logging
from src.terraform.terraform_manager import TerraformManager

# Initialize logger
logger = logging.getLogger(__name__)

# Create blueprint
terraform_bp = Blueprint('terraform', __name__)

# Initialize Terraform manager
db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:changeme@postgres:5432/cloud_cost_optimizer')
templates_dir = os.environ.get('TERRAFORM_TEMPLATES_DIR', '/app/terraform/templates')
state_dir = os.environ.get('TERRAFORM_STATE_DIR', '/app/terraform/state')
terraform_manager = TerraformManager(db_url, templates_dir, state_dir)

@terraform_bp.route('/api/v1/terraform/templates', methods=['GET'])
def list_templates():
    """List all Terraform templates."""
    try:
        provider = request.args.get('provider')
        service_type = request.args.get('service_type')
        
        templates = terraform_manager.get_templates(provider, service_type)
        return jsonify(templates)
    except Exception as e:
        logger.error(f"Error listing Terraform templates: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    """Get a Terraform template by ID."""
    try:
        template = terraform_manager.get_template(template_id)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        return jsonify(template)
    except Exception as e:
        logger.error(f"Error getting Terraform template {template_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/templates', methods=['POST'])
def create_template():
    """Create a new Terraform template."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        description = data.get('description', '')
        provider = data.get('provider')
        service_type = data.get('service_type')
        template_content = data.get('template_content')
        variables = data.get('variables', {})
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        if not provider:
            return jsonify({'error': 'Provider is required'}), 400
        
        if not service_type:
            return jsonify({'error': 'Service type is required'}), 400
        
        if not template_content:
            return jsonify({'error': 'Template content is required'}), 400
        
        template = terraform_manager.create_template(name, description, provider, service_type, template_content, variables)
        return jsonify(template), 201
    except ValueError as e:
        logger.error(f"Validation error creating Terraform template: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating Terraform template: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/templates/<int:template_id>', methods=['PUT'])
def update_template(template_id):
    """Update a Terraform template."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        description = data.get('description')
        template_content = data.get('template_content')
        variables = data.get('variables')
        
        template = terraform_manager.update_template(template_id, name, description, template_content, variables)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        return jsonify(template)
    except ValueError as e:
        logger.error(f"Validation error updating Terraform template {template_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating Terraform template {template_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/templates/<int:template_id>', methods=['DELETE'])
def delete_template(template_id):
    """Delete a Terraform template."""
    try:
        success = terraform_manager.delete_template(template_id)
        if not success:
            return jsonify({'error': 'Template not found'}), 404
        
        return jsonify({'message': f'Template {template_id} deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting Terraform template {template_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/templates/<int:template_id>/estimate', methods=['POST'])
def estimate_cost(template_id):
    """Estimate the cost of a Terraform template."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        variables_values = data.get('variables', {})
        
        result = terraform_manager.estimate_cost(template_id, variables_values)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error estimating cost for Terraform template {template_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error estimating cost for Terraform template {template_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/deployments', methods=['GET'])
def list_deployments():
    """List all Terraform deployments."""
    try:
        account_id = request.args.get('account_id', type=int)
        template_id = request.args.get('template_id', type=int)
        status = request.args.get('status')
        
        deployments = terraform_manager.get_deployments(account_id, template_id, status)
        return jsonify(deployments)
    except Exception as e:
        logger.error(f"Error listing Terraform deployments: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/deployments/<int:deployment_id>', methods=['GET'])
def get_deployment(deployment_id):
    """Get a Terraform deployment by ID."""
    try:
        deployment = terraform_manager.get_deployment(deployment_id)
        if not deployment:
            return jsonify({'error': 'Deployment not found'}), 404
        return jsonify(deployment)
    except Exception as e:
        logger.error(f"Error getting Terraform deployment {deployment_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/templates/<int:template_id>/deploy', methods=['POST'])
def deploy_template(template_id):
    """Deploy a Terraform template."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        account_id = data.get('account_id')
        variables_values = data.get('variables', {})
        
        if not account_id:
            return jsonify({'error': 'Account ID is required'}), 400
        
        result = terraform_manager.deploy_template(template_id, account_id, variables_values)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error deploying Terraform template {template_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error deploying Terraform template {template_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/deployments/<int:deployment_id>/apply', methods=['POST'])
def apply_deployment(deployment_id):
    """Apply a Terraform deployment."""
    try:
        result = terraform_manager.apply_deployment(deployment_id)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error applying Terraform deployment {deployment_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error applying Terraform deployment {deployment_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@terraform_bp.route('/api/v1/terraform/deployments/<int:deployment_id>/destroy', methods=['POST'])
def destroy_deployment(deployment_id):
    """Destroy a Terraform deployment."""
    try:
        result = terraform_manager.destroy_deployment(deployment_id)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Validation error destroying Terraform deployment {deployment_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error destroying Terraform deployment {deployment_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500
