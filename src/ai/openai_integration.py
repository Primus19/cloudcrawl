"""
OpenAI integration for Cloud Cost Optimizer.
This module provides AI-powered recommendations using OpenAI's models.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
import requests

class OpenAIIntegration:
    """
    Recommendation engine powered by OpenAI.
    Provides intelligent cost optimization recommendations based on resource usage patterns.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI recommendation engine.
        
        Args:
            api_key: OpenAI API key (optional, defaults to environment variable)
        """
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            self.logger = logging.getLogger(__name__)
            self.logger.warning("OpenAI API key not found. Using mock data for development.")
            self.use_mock = True
        else:
            self.use_mock = False
        
        self.logger = logging.getLogger(__name__)
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    def analyze_resource_usage(self, resource_data: Dict[str, Any], metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze resource usage patterns and provide optimization recommendations.
        
        Args:
            resource_data: Resource metadata and configuration
            metrics_data: Resource usage metrics
            
        Returns:
            Dictionary containing recommendations
        """
        try:
            if self.use_mock:
                return self._get_mock_recommendations(resource_data)
                
            # Prepare the prompt with resource and metrics data
            prompt = self._prepare_analysis_prompt(resource_data, metrics_data)
            
            # Call OpenAI API
            response = self._call_openai_api(prompt)
            
            # Parse and structure the recommendations
            recommendations = self._parse_recommendations(response, resource_data)
            
            return recommendations
        except Exception as e:
            self.logger.error(f"Error analyzing resource usage with OpenAI: {str(e)}")
            return {
                "error": str(e),
                "recommendations": []
            }
    
    def generate_cost_saving_strategies(self, account_data: Dict[str, Any], cost_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate overall cost saving strategies for an account.
        
        Args:
            account_data: Account metadata
            cost_data: Historical cost data
            
        Returns:
            Dictionary containing cost saving strategies
        """
        try:
            if self.use_mock:
                return self._get_mock_strategies(account_data)
                
            # Prepare the prompt with account and cost data
            prompt = self._prepare_strategy_prompt(account_data, cost_data)
            
            # Call OpenAI API
            response = self._call_openai_api(prompt)
            
            # Parse and structure the strategies
            strategies = self._parse_strategies(response, account_data)
            
            return strategies
        except Exception as e:
            self.logger.error(f"Error generating cost saving strategies with OpenAI: {str(e)}")
            return {
                "error": str(e),
                "strategies": []
            }
    
    def get_chat_response(self, user_id: str, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a response from the OpenAI chat model.
        
        Args:
            user_id: User ID for conversation tracking
            message: User message
            context: Additional context for the conversation
            
        Returns:
            Dictionary containing the chat response
        """
        try:
            if self.use_mock:
                return self._get_mock_chat_response(message)
                
            # Prepare system message with context
            system_message = "You are a cloud cost optimization expert with deep knowledge of AWS, GCP, and Azure services."
            if context:
                system_message += f"\n\nContext: {json.dumps(context)}"
            
            # Call OpenAI API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            
            if response.status_code != 200:
                raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
            
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']
            
            return {
                "message": content,
                "user_id": user_id,
                "timestamp": "2025-05-25T17:48:00Z"  # Use actual timestamp in production
            }
        except Exception as e:
            self.logger.error(f"Error getting chat response from OpenAI: {str(e)}")
            return {
                "message": f"I'm sorry, I encountered an error: {str(e)}. Please try again later.",
                "user_id": user_id,
                "timestamp": "2025-05-25T17:48:00Z",  # Use actual timestamp in production
                "error": str(e)
            }
    
    def _prepare_analysis_prompt(self, resource_data: Dict[str, Any], metrics_data: Dict[str, Any]) -> str:
        """
        Prepare a prompt for resource usage analysis.
        
        Args:
            resource_data: Resource metadata and configuration
            metrics_data: Resource usage metrics
            
        Returns:
            Formatted prompt string
        """
        resource_type = resource_data.get('type', 'unknown')
        resource_id = resource_data.get('id', 'unknown')
        
        prompt = f"""
        As a cloud cost optimization expert, analyze the following {resource_type} resource and its usage metrics.
        Provide specific, actionable recommendations to optimize costs while maintaining performance.
        
        Resource Information:
        {json.dumps(resource_data, indent=2)}
        
        Usage Metrics:
        {json.dumps(metrics_data, indent=2)}
        
        For each recommendation, include:
        1. A clear description of the recommended action
        2. The estimated cost savings (percentage or amount)
        3. The potential impact on performance or availability
        4. The risk level (low, medium, high)
        5. Implementation complexity (low, medium, high)
        
        Format your response as a structured JSON with an array of recommendations.
        """
        
        return prompt
    
    def _prepare_strategy_prompt(self, account_data: Dict[str, Any], cost_data: List[Dict[str, Any]]) -> str:
        """
        Prepare a prompt for overall cost saving strategy generation.
        
        Args:
            account_data: Account metadata
            cost_data: Historical cost data
            
        Returns:
            Formatted prompt string
        """
        provider = account_data.get('provider', 'unknown')
        
        prompt = f"""
        As a cloud cost optimization expert for {provider}, analyze the following account and its historical cost data.
        Provide strategic recommendations to optimize overall cloud spending.
        
        Account Information:
        {json.dumps(account_data, indent=2)}
        
        Historical Cost Data:
        {json.dumps(cost_data, indent=2)}
        
        For each strategy, include:
        1. A clear description of the recommended strategy
        2. The estimated cost savings (percentage or amount)
        3. The areas of impact (services, resources, etc.)
        4. The implementation timeline (short-term, medium-term, long-term)
        5. Best practices and industry benchmarks
        
        Format your response as a structured JSON with an array of strategies.
        """
        
        return prompt
    
    def _call_openai_api(self, prompt: str) -> str:
        """
        Call the OpenAI API with the given prompt.
        
        Args:
            prompt: The prompt to send to the API
            
        Returns:
            The API response text
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a cloud cost optimization expert with deep knowledge of AWS, GCP, and Azure services."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 2000
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
        
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    
    def _parse_recommendations(self, response: str, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and structure the recommendations from the API response.
        
        Args:
            response: The API response text
            resource_data: The original resource data
            
        Returns:
            Structured recommendations dictionary
        """
        try:
            # Extract JSON from response
            json_str = response.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:-3].strip()
            elif json_str.startswith('```'):
                json_str = json_str[3:-3].strip()
            
            recommendations_data = json.loads(json_str)
            
            # Ensure consistent structure
            if isinstance(recommendations_data, list):
                recommendations_data = {"recommendations": recommendations_data}
            
            # Add metadata
            result = {
                "resource_id": resource_data.get('id'),
                "resource_type": resource_data.get('type'),
                "provider": resource_data.get('provider', 'unknown'),
                "generated_at": "2025-05-25T17:48:00Z",  # Use actual timestamp in production
                "recommendations": recommendations_data.get('recommendations', [])
            }
            
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, extract recommendations manually
            self.logger.warning("Failed to parse JSON from OpenAI response, using fallback parsing")
            
            # Simple fallback parsing
            recommendations = []
            lines = response.split('\n')
            current_rec = {}
            
            for line in lines:
                if line.strip().startswith('Recommendation'):
                    if current_rec:
                        recommendations.append(current_rec)
                    current_rec = {"description": line.strip()}
                elif ':' in line and current_rec:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    current_rec[key] = value.strip()
            
            if current_rec:
                recommendations.append(current_rec)
            
            result = {
                "resource_id": resource_data.get('id'),
                "resource_type": resource_data.get('type'),
                "provider": resource_data.get('provider', 'unknown'),
                "generated_at": "2025-05-25T17:48:00Z",  # Use actual timestamp in production
                "recommendations": recommendations,
                "parsing_method": "fallback"
            }
            
            return result
    
    def _parse_strategies(self, response: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and structure the strategies from the API response.
        
        Args:
            response: The API response text
            account_data: The original account data
            
        Returns:
            Structured strategies dictionary
        """
        try:
            # Extract JSON from response
            json_str = response.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:-3].strip()
            elif json_str.startswith('```'):
                json_str = json_str[3:-3].strip()
            
            strategies_data = json.loads(json_str)
            
            # Ensure consistent structure
            if isinstance(strategies_data, list):
                strategies_data = {"strategies": strategies_data}
            
            # Add metadata
            result = {
                "account_id": account_data.get('id'),
                "provider": account_data.get('provider', 'unknown'),
                "generated_at": "2025-05-25T17:48:00Z",  # Use actual timestamp in production
                "strategies": strategies_data.get('strategies', [])
            }
            
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, extract strategies manually
            self.logger.warning("Failed to parse JSON from OpenAI response, using fallback parsing")
            
            # Simple fallback parsing
            strategies = []
            lines = response.split('\n')
            current_strategy = {}
            
            for line in lines:
                if line.strip().startswith('Strategy'):
                    if current_strategy:
                        strategies.append(current_strategy)
                    current_strategy = {"description": line.strip()}
                elif ':' in line and current_strategy:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    current_strategy[key] = value.strip()
            
            if current_strategy:
                strategies.append(current_strategy)
            
            result = {
                "account_id": account_data.get('id'),
                "provider": account_data.get('provider', 'unknown'),
                "generated_at": "2025-05-25T17:48:00Z",  # Use actual timestamp in production
                "strategies": strategies,
                "parsing_method": "fallback"
            }
            
            return result
            
    def _get_mock_recommendations(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get mock recommendations for development and testing.
        
        Args:
            resource_data: Resource metadata
            
        Returns:
            Mock recommendations
        """
        resource_type = resource_data.get('type', 'unknown')
        
        mock_recommendations = []
        
        if 'ec2' in resource_type.lower():
            mock_recommendations = [
                {
                    "description": "Downsize EC2 instance from t3.large to t3.medium",
                    "estimated_savings": "45.6 USD/month",
                    "performance_impact": "Minimal for current workload",
                    "risk_level": "low",
                    "implementation_complexity": "low"
                },
                {
                    "description": "Use Spot Instances for non-critical workloads",
                    "estimated_savings": "70% compared to On-Demand",
                    "performance_impact": "None, but potential for interruption",
                    "risk_level": "medium",
                    "implementation_complexity": "medium"
                }
            ]
        elif 'rds' in resource_type.lower():
            mock_recommendations = [
                {
                    "description": "Switch from Provisioned IOPS to General Purpose SSD",
                    "estimated_savings": "30.2 USD/month",
                    "performance_impact": "Minimal for current workload",
                    "risk_level": "low",
                    "implementation_complexity": "low"
                },
                {
                    "description": "Implement automated snapshot cleanup policy",
                    "estimated_savings": "15.8 USD/month",
                    "performance_impact": "None",
                    "risk_level": "low",
                    "implementation_complexity": "low"
                }
            ]
        else:
            mock_recommendations = [
                {
                    "description": "Implement resource tagging for better cost allocation",
                    "estimated_savings": "Indirect - 10-15% through improved governance",
                    "performance_impact": "None",
                    "risk_level": "low",
                    "implementation_complexity": "medium"
                },
                {
                    "description": "Enable auto-scaling based on usage patterns",
                    "estimated_savings": "25-30% during off-peak hours",
                    "performance_impact": "None",
                    "risk_level": "low",
                    "implementation_complexity": "medium"
                }
            ]
        
        return {
            "resource_id": resource_data.get('id'),
            "resource_type": resource_type,
            "provider": resource_data.get('provider', 'unknown'),
            "generated_at": "2025-05-25T17:48:00Z",
            "recommendations": mock_recommendations,
            "is_mock": True
        }
    
    def _get_mock_strategies(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get mock strategies for development and testing.
        
        Args:
            account_data: Account metadata
            
        Returns:
            Mock strategies
        """
        provider = account_data.get('provider', 'unknown').lower()
        
        mock_strategies = []
        
        if 'aws' in provider:
            mock_strategies = [
                {
                    "description": "Implement AWS Savings Plans for compute resources",
                    "estimated_savings": "Up to 72% compared to On-Demand",
                    "areas_of_impact": "EC2, Lambda, Fargate",
                    "implementation_timeline": "short-term",
                    "best_practices": "Analyze usage patterns for 3 months before committing"
                },
                {
                    "description": "Use S3 Intelligent-Tiering for infrequently accessed data",
                    "estimated_savings": "15-40% on storage costs",
                    "areas_of_impact": "S3 storage",
                    "implementation_timeline": "short-term",
                    "best_practices": "Identify data access patterns before migration"
                }
            ]
        elif 'azure' in provider:
            mock_strategies = [
                {
                    "description": "Implement Azure Reserved VM Instances",
                    "estimated_savings": "Up to 72% compared to Pay-as-you-go",
                    "areas_of_impact": "Virtual Machines",
                    "implementation_timeline": "short-term",
                    "best_practices": "Analyze usage patterns for 3 months before committing"
                },
                {
                    "description": "Optimize Azure Blob Storage tiers",
                    "estimated_savings": "20-60% on storage costs",
                    "areas_of_impact": "Blob Storage",
                    "implementation_timeline": "short-term",
                    "best_practices": "Use lifecycle management policies"
                }
            ]
        elif 'gcp' in provider:
            mock_strategies = [
                {
                    "description": "Use Committed Use Discounts for predictable workloads",
                    "estimated_savings": "Up to 57% compared to On-Demand",
                    "areas_of_impact": "Compute Engine",
                    "implementation_timeline": "short-term",
                    "best_practices": "Analyze usage patterns for 3 months before committing"
                },
                {
                    "description": "Implement GCP Storage lifecycle policies",
                    "estimated_savings": "15-30% on storage costs",
                    "areas_of_impact": "Cloud Storage",
                    "implementation_timeline": "short-term",
                    "best_practices": "Define clear data retention requirements"
                }
            ]
        else:
            mock_strategies = [
                {
                    "description": "Implement multi-cloud cost management tools",
                    "estimated_savings": "15-25% through improved visibility",
                    "areas_of_impact": "All cloud resources",
                    "implementation_timeline": "medium-term",
                    "best_practices": "Select tools with support for all your cloud providers"
                },
                {
                    "description": "Establish FinOps practices and team",
                    "estimated_savings": "20-30% through improved governance",
                    "areas_of_impact": "All cloud resources",
                    "implementation_timeline": "medium-term",
                    "best_practices": "Involve engineering, finance, and management"
                }
            ]
        
        return {
            "account_id": account_data.get('id'),
            "provider": provider,
            "generated_at": "2025-05-25T17:48:00Z",
            "strategies": mock_strategies,
            "is_mock": True
        }
    
    def _get_mock_chat_response(self, message: str) -> Dict[str, Any]:
        """
        Get mock chat response for development and testing.
        
        Args:
            message: User message
            
        Returns:
            Mock chat response
        """
        # Simple keyword-based responses
        response = "I'm sorry, I don't have enough information to answer that question. Could you provide more details about your cloud environment?"
        
        if 'cost' in message.lower() and 'reduce' in message.lower():
            response = "To reduce cloud costs, consider these strategies:\n\n1. Right-size your resources based on actual usage\n2. Use reserved instances or savings plans for predictable workloads\n3. Implement auto-scaling for variable workloads\n4. Clean up unused resources regularly\n5. Use spot instances for non-critical, interruptible workloads"
        
        elif 'ec2' in message.lower() and 'optimize' in message.lower():
            response = "To optimize EC2 instances:\n\n1. Right-size instances based on CloudWatch metrics\n2. Use Graviton processors for better price-performance\n3. Implement Auto Scaling groups\n4. Consider Spot Instances for non-critical workloads\n5. Purchase Savings Plans or Reserved Instances for stable workloads"
        
        elif 'storage' in message.lower() and ('optimize' in message.lower() or 'cost' in message.lower()):
            response = "To optimize storage costs:\n\n1. Implement lifecycle policies to move infrequently accessed data to cheaper tiers\n2. Delete unnecessary snapshots and backups\n3. Compress data where possible\n4. Use storage-optimized instance types for I/O-intensive workloads\n5. Consider using object storage instead of block storage for appropriate workloads"
        
        return {
            "message": response,
            "timestamp": "2025-05-25T17:48:00Z",
            "is_mock": True
        }
