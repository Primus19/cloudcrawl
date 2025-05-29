"""
API endpoints for Kubernetes management in the Cloud Cost Optimizer.
This module provides functionality for managing Kubernetes deployments.
"""

import logging
from flask import Blueprint, jsonify, request, g
from src.api.auth import require_auth
from src.kubernetes.kubernetes_manager import KubernetesManager

# Initialize logger
logger = logging.getLogger(__name__)

# Create blueprint
kubernetes_bp = Blueprint('kubernetes', __name__)

# Initialize Kubernetes manager
kubernetes_manager = KubernetesManager()

@kubernetes_bp.route('/api/v1/kubernetes/manifests', methods=['GET'])
@require_auth
def get_kubernetes_manifests():
    """Get all Kubernetes manifests."""
    try:
        # Get manifests
        manifests = kubernetes_manager.get_manifests()
        
        return jsonify({'manifests': manifests})
    except Exception as e:
        logger.error(f"Error getting Kubernetes manifests: {str(e)}")
        return jsonify({'error': str(e)}), 500

@kubernetes_bp.route('/api/v1/kubernetes/manifests/<name>', methods=['GET'])
@require_auth
def get_kubernetes_manifest(name):
    """Get a specific Kubernetes manifest by name."""
    try:
        # Get manifest
        manifest = kubernetes_manager.get_manifest(name)
        
        if not manifest:
            return jsonify({'error': f'Manifest {name} not found'}), 404
        
        return jsonify(manifest)
    except Exception as e:
        logger.error(f"Error getting Kubernetes manifest {name}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@kubernetes_bp.route('/api/v1/kubernetes/manifests', methods=['POST'])
@require_auth
def create_kubernetes_manifest():
    """Create a new Kubernetes manifest."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate manifest
        validation_result = kubernetes_manager.validate_manifest(data['content'])
        if not validation_result['valid']:
            return jsonify({
                'valid': False,
                'errors': validation_result['errors']
            }), 400
        
        # Create manifest
        success = kubernetes_manager.create_manifest(data['name'], data['content'])
        
        if not success:
            return jsonify({'error': f'Failed to create manifest {data["name"]}'}), 500
        
        # Get created manifest
        manifest = kubernetes_manager.get_manifest(data['name'])
        
        return jsonify(manifest), 201
    except Exception as e:
        logger.error(f"Error creating Kubernetes manifest: {str(e)}")
        return jsonify({'error': str(e)}), 500

@kubernetes_bp.route('/api/v1/kubernetes/manifests/<name>', methods=['PUT'])
@require_auth
def update_kubernetes_manifest(name):
    """Update a Kubernetes manifest."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'content' not in data:
            return jsonify({'error': 'Missing required field: content'}), 400
        
        # Validate manifest
        validation_result = kubernetes_manager.validate_manifest(data['content'])
        if not validation_result['valid']:
            return jsonify({
                'valid': False,
                'errors': validation_result['errors']
            }), 400
        
        # Update manifest
        success = kubernetes_manager.update_manifest(name, data['content'])
        
        if not success:
            return jsonify({'error': f'Failed to update manifest {name}'}), 500
        
        # Get updated manifest
        manifest = kubernetes_manager.get_manifest(name)
        
        return jsonify(manifest)
    except Exception as e:
        logger.error(f"Error updating Kubernetes manifest {name}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@kubernetes_bp.route('/api/v1/kubernetes/manifests/<name>', methods=['DELETE'])
@require_auth
def delete_kubernetes_manifest(name):
    """Delete a Kubernetes manifest."""
    try:
        # Delete manifest
        success = kubernetes_manager.delete_manifest(name)
        
        if not success:
            return jsonify({'error': f'Failed to delete manifest {name}'}), 500
        
        return jsonify({'message': f'Manifest {name} deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting Kubernetes manifest {name}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@kubernetes_bp.route('/api/v1/kubernetes/manifests/validate', methods=['POST'])
@require_auth
def validate_kubernetes_manifest():
    """Validate a Kubernetes manifest."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'content' not in data:
            return jsonify({'error': 'Missing required field: content'}), 400
        
        # Validate manifest
        validation_result = kubernetes_manager.validate_manifest(data['content'])
        
        return jsonify(validation_result)
    except Exception as e:
        logger.error(f"Error validating Kubernetes manifest: {str(e)}")
        return jsonify({'error': str(e)}), 500
