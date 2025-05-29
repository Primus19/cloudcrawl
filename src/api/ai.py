"""
API integration for the AI recommendation engine.
This module provides endpoints for AI-powered recommendations.
"""

import logging
from flask import Blueprint, jsonify, request, g
from src.api.auth import require_auth
from src.ai.recommendation_engine import RecommendationEngine
from src.ai.openai_integration import OpenAIIntegration

# Initialize logger
logger = logging.getLogger(__name__)

# Create blueprint
ai_bp = Blueprint('ai', __name__)

# Initialize AI components
recommendation_engine = RecommendationEngine()
openai_integration = OpenAIIntegration()

@ai_bp.route('/api/v1/ai/recommendations', methods=['GET'])
@require_auth
def get_ai_recommendations():
    """Get AI-powered recommendations for cost optimization."""
    try:
        # Get query parameters
        account_id = request.args.get('account_id')
        provider = request.args.get('provider', 'all')
        limit = request.args.get('limit', 10, type=int)
        
        # Get recommendations from AI engine
        recommendations = recommendation_engine.get_recommendations(
            user_id=g.current_user['id'],
            account_id=account_id,
            provider=provider,
            limit=limit
        )
        
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        logger.error(f"Error getting AI recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/api/v1/ai/analyze', methods=['POST'])
@require_auth
def analyze_resources():
    """Analyze resources using AI for optimization opportunities."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'resources' not in data:
            return jsonify({'error': 'Missing required field: resources'}), 400
        
        # Analyze resources
        analysis = recommendation_engine.analyze_resources(data['resources'])
        
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Error analyzing resources: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/api/v1/ai/explain', methods=['POST'])
@require_auth
def explain_recommendation():
    """Get detailed explanation for a recommendation."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'recommendation_id' not in data:
            return jsonify({'error': 'Missing required field: recommendation_id'}), 400
        
        # Get explanation
        explanation = recommendation_engine.explain_recommendation(data['recommendation_id'])
        
        return jsonify(explanation)
    except Exception as e:
        logger.error(f"Error explaining recommendation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/api/v1/ai/chat', methods=['POST'])
@require_auth
def chat_with_ai():
    """Chat with AI assistant about cloud resources and optimization."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'message' not in data:
            return jsonify({'error': 'Missing required field: message'}), 400
        
        # Get chat response from OpenAI
        response = openai_integration.get_chat_response(
            user_id=g.current_user['id'],
            message=data['message'],
            context=data.get('context', {})
        )
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error chatting with AI: {str(e)}")
        return jsonify({'error': str(e)}), 500
