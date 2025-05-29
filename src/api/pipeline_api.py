"""
API endpoints for deployment pipeline management in the Cloud Cost Optimizer.
This module provides functionality for managing CI/CD pipelines and deployments.
"""

import logging
from flask import Blueprint, jsonify, request, g
from src.api.auth import require_auth
from src.deployment.pipeline_manager import DeploymentPipelineManager

# Initialize logger
logger = logging.getLogger(__name__)

# Create blueprint
pipeline_bp = Blueprint('pipeline', __name__)

# Initialize pipeline manager
pipeline_manager = DeploymentPipelineManager()

@pipeline_bp.route('/api/v1/pipelines', methods=['GET'])
@require_auth
def get_pipelines():
    """Get all pipeline configurations."""
    try:
        # Get pipelines
        pipelines = pipeline_manager.get_pipelines()
        
        return jsonify({'pipelines': pipelines})
    except Exception as e:
        logger.error(f"Error getting pipelines: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/pipelines/<name>', methods=['GET'])
@require_auth
def get_pipeline(name):
    """Get a specific pipeline configuration by name."""
    try:
        # Get pipeline
        pipeline = pipeline_manager.get_pipeline(name)
        
        if not pipeline:
            return jsonify({'error': f'Pipeline {name} not found'}), 404
        
        return jsonify(pipeline)
    except Exception as e:
        logger.error(f"Error getting pipeline {name}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/pipelines', methods=['POST'])
@require_auth
def create_pipeline():
    """Create a new pipeline configuration."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate pipeline
        validation_result = pipeline_manager.validate_pipeline(data['content'])
        if not validation_result['valid']:
            return jsonify({
                'valid': False,
                'errors': validation_result['errors']
            }), 400
        
        # Create pipeline
        success = pipeline_manager.create_pipeline(data['name'], data['content'])
        
        if not success:
            return jsonify({'error': f'Failed to create pipeline {data["name"]}'}), 500
        
        # Get created pipeline
        pipeline = pipeline_manager.get_pipeline(data['name'])
        
        return jsonify(pipeline), 201
    except Exception as e:
        logger.error(f"Error creating pipeline: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/pipelines/<name>', methods=['PUT'])
@require_auth
def update_pipeline(name):
    """Update a pipeline configuration."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'content' not in data:
            return jsonify({'error': 'Missing required field: content'}), 400
        
        # Validate pipeline
        validation_result = pipeline_manager.validate_pipeline(data['content'])
        if not validation_result['valid']:
            return jsonify({
                'valid': False,
                'errors': validation_result['errors']
            }), 400
        
        # Update pipeline
        success = pipeline_manager.update_pipeline(name, data['content'])
        
        if not success:
            return jsonify({'error': f'Failed to update pipeline {name}'}), 500
        
        # Get updated pipeline
        pipeline = pipeline_manager.get_pipeline(name)
        
        return jsonify(pipeline)
    except Exception as e:
        logger.error(f"Error updating pipeline {name}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/pipelines/<name>', methods=['DELETE'])
@require_auth
def delete_pipeline(name):
    """Delete a pipeline configuration."""
    try:
        # Delete pipeline
        success = pipeline_manager.delete_pipeline(name)
        
        if not success:
            return jsonify({'error': f'Failed to delete pipeline {name}'}), 500
        
        return jsonify({'message': f'Pipeline {name} deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting pipeline {name}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/pipelines/validate', methods=['POST'])
@require_auth
def validate_pipeline():
    """Validate a pipeline configuration."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'content' not in data:
            return jsonify({'error': 'Missing required field: content'}), 400
        
        # Validate pipeline
        validation_result = pipeline_manager.validate_pipeline(data['content'])
        
        return jsonify(validation_result)
    except Exception as e:
        logger.error(f"Error validating pipeline: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/deployments', methods=['GET'])
@require_auth
def get_deployments():
    """Get all deployments."""
    try:
        # Get deployments
        deployments = pipeline_manager.get_deployments()
        
        return jsonify({'deployments': deployments})
    except Exception as e:
        logger.error(f"Error getting deployments: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/deployments/<deployment_id>', methods=['GET'])
@require_auth
def get_deployment(deployment_id):
    """Get a specific deployment by ID."""
    try:
        # Get deployment
        deployment = pipeline_manager.get_deployment(deployment_id)
        
        if not deployment:
            return jsonify({'error': f'Deployment {deployment_id} not found'}), 404
        
        return jsonify(deployment)
    except Exception as e:
        logger.error(f"Error getting deployment {deployment_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/deployments', methods=['POST'])
@require_auth
def create_deployment():
    """Create a new deployment."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['pipeline_name', 'environment', 'version']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create deployment
        try:
            deployment_id = pipeline_manager.create_deployment(
                data['pipeline_name'],
                data['environment'],
                data['version']
            )
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Get created deployment
        deployment = pipeline_manager.get_deployment(deployment_id)
        
        return jsonify(deployment), 201
    except Exception as e:
        logger.error(f"Error creating deployment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/deployments/<deployment_id>/status', methods=['PUT'])
@require_auth
def update_deployment_status(deployment_id):
    """Update a deployment status."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'status' not in data:
            return jsonify({'error': 'Missing required field: status'}), 400
        
        # Update deployment status
        success = pipeline_manager.update_deployment_status(deployment_id, data['status'])
        
        if not success:
            return jsonify({'error': f'Failed to update deployment {deployment_id} status'}), 500
        
        # Get updated deployment
        deployment = pipeline_manager.get_deployment(deployment_id)
        
        return jsonify(deployment)
    except Exception as e:
        logger.error(f"Error updating deployment {deployment_id} status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/deployments/<deployment_id>/advance', methods=['POST'])
@require_auth
def advance_deployment_stage(deployment_id):
    """Advance a deployment to the next stage."""
    try:
        # Advance deployment stage
        success = pipeline_manager.advance_deployment_stage(deployment_id)
        
        if not success:
            return jsonify({'error': f'Failed to advance deployment {deployment_id} stage'}), 500
        
        # Get updated deployment
        deployment = pipeline_manager.get_deployment(deployment_id)
        
        return jsonify(deployment)
    except Exception as e:
        logger.error(f"Error advancing deployment {deployment_id} stage: {str(e)}")
        return jsonify({'error': str(e)}), 500

@pipeline_bp.route('/api/v1/deployments/<deployment_id>/logs', methods=['POST'])
@require_auth
def add_deployment_log(deployment_id):
    """Add a log message to a deployment."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'message' not in data:
            return jsonify({'error': 'Missing required field: message'}), 400
        
        # Add deployment log
        success = pipeline_manager.add_deployment_log(deployment_id, data['message'])
        
        if not success:
            return jsonify({'error': f'Failed to add log to deployment {deployment_id}'}), 500
        
        # Get updated deployment
        deployment = pipeline_manager.get_deployment(deployment_id)
        
        return jsonify(deployment)
    except Exception as e:
        logger.error(f"Error adding log to deployment {deployment_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500
