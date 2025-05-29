"""
Recommendation Engine for Cloud Cost Optimizer.
This module integrates both OpenAI and custom ML models for comprehensive recommendations.
"""

import logging
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from src.ai.openai_integration import OpenAIIntegration
from src.ai.ml_models import ResourceUsagePredictor, CostAnomalyDetector, ResourceClusterer

class RecommendationEngine:
    """
    Unified recommendation engine that combines AI and ML approaches
    to provide comprehensive cost optimization recommendations.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the recommendation engine.
        
        Args:
            openai_api_key: OpenAI API key (optional)
        """
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI engine
        try:
            self.openai_engine = OpenAIIntegration(api_key=openai_api_key)
            self.openai_available = True
        except Exception as e:
            self.logger.warning(f"OpenAI integration not available: {str(e)}")
            self.openai_available = False
        
        # Initialize ML models
        self.usage_predictor = ResourceUsagePredictor()
        self.anomaly_detector = CostAnomalyDetector()
        self.resource_clusterer = ResourceClusterer()
        
        # Track model training status
        self.models_trained = False
    
    def train_models(self, historical_data: Dict[str, pd.DataFrame]) -> bool:
        """
        Train all ML models with historical data.
        
        Args:
            historical_data: Dictionary with DataFrames for resource usage, costs, etc.
            
        Returns:
            True if training was successful, False otherwise
        """
        try:
            # Train resource usage predictor
            if 'resource_usage' in historical_data:
                self.usage_predictor.train(historical_data['resource_usage'])
            
            # Train cost anomaly detector
            if 'costs' in historical_data:
                self.anomaly_detector.train(historical_data['costs'])
            
            # Train resource clusterer
            if 'resources' in historical_data:
                self.resource_clusterer.train(historical_data['resources'])
            
            self.models_trained = True
            return True
        except Exception as e:
            self.logger.error(f"Error training recommendation models: {str(e)}")
            return False
    
    def get_recommendations(self, user_id: str, account_id: Optional[str] = None, 
                           provider: str = 'all', limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get AI-powered recommendations for cost optimization.
        
        Args:
            user_id: User ID
            account_id: Optional account ID to filter recommendations
            provider: Cloud provider (aws, azure, gcp, or all)
            limit: Maximum number of recommendations to return
            
        Returns:
            List of recommendations
        """
        # For development/testing, return mock recommendations
        recommendations = [
            {
                "id": "rec-001",
                "account_id": "aws-account-1",
                "resource_id": "i-1234567890abcdef0",
                "type": "rightsizing",
                "description": "Downsize EC2 instance from t3.large to t3.medium",
                "estimated_savings": 45.6,
                "currency": "USD",
                "risk_level": "low",
                "status": "pending"
            },
            {
                "id": "rec-002",
                "account_id": "aws-account-1",
                "resource_id": "vol-1234567890abcdef0",
                "type": "unused_resource",
                "description": "Delete unused EBS volume",
                "estimated_savings": 20.3,
                "currency": "USD",
                "risk_level": "medium",
                "status": "pending"
            },
            {
                "id": "rec-003",
                "account_id": "aws-account-1",
                "resource_id": "snap-1234567890abcdef0",
                "type": "lifecycle_policy",
                "description": "Implement snapshot lifecycle policy",
                "estimated_savings": 15.8,
                "currency": "USD",
                "risk_level": "low",
                "status": "pending"
            },
            {
                "id": "rec-004",
                "account_id": "azure-subscription-1",
                "resource_id": "vm-1234",
                "type": "reserved_instance",
                "description": "Purchase Azure Reserved VM Instance",
                "estimated_savings": 123.4,
                "currency": "USD",
                "risk_level": "low",
                "status": "pending"
            },
            {
                "id": "rec-005",
                "account_id": "gcp-project-1",
                "resource_id": "instance-1",
                "type": "committed_use",
                "description": "Purchase committed use discount",
                "estimated_savings": 78.9,
                "currency": "USD",
                "risk_level": "low",
                "status": "pending"
            }
        ]
        
        # Filter by account_id if provided
        if account_id:
            recommendations = [r for r in recommendations if r['account_id'] == account_id]
        
        # Filter by provider if not 'all'
        if provider != 'all':
            if provider == 'aws':
                recommendations = [r for r in recommendations if 'aws' in r['account_id']]
            elif provider == 'azure':
                recommendations = [r for r in recommendations if 'azure' in r['account_id']]
            elif provider == 'gcp':
                recommendations = [r for r in recommendations if 'gcp' in r['account_id']]
        
        # Limit results
        recommendations = recommendations[:limit]
        
        return recommendations
    
    def get_resource_recommendations(self, resource_data: Dict[str, Any], 
                                    metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get recommendations for a specific resource.
        
        Args:
            resource_data: Resource metadata and configuration
            metrics_data: Resource usage metrics
            
        Returns:
            Dictionary containing recommendations
        """
        recommendations = {
            "resource_id": resource_data.get('id'),
            "resource_type": resource_data.get('type'),
            "timestamp": datetime.now().isoformat(),
            "recommendations": []
        }
        
        # Get ML-based recommendations if models are trained
        if self.models_trained:
            try:
                # Convert metrics to DataFrame for prediction
                metrics_df = self._convert_metrics_to_dataframe(metrics_data)
                
                # Predict future usage
                future_timepoints = self._generate_future_timepoints(metrics_df)
                future_usage = self.usage_predictor.predict(future_timepoints)
                
                # Generate recommendations based on predictions
                ml_recommendations = self._generate_ml_recommendations(
                    resource_data, metrics_df, future_usage)
                
                recommendations["recommendations"].extend(ml_recommendations)
                recommendations["ml_predictions"] = {
                    "future_timestamps": future_timepoints['timestamp'].tolist(),
                    "predicted_cpu_usage": future_usage[:, 0].tolist(),
                    "predicted_memory_usage": future_usage[:, 1].tolist()
                }
            except Exception as e:
                self.logger.error(f"Error generating ML recommendations: {str(e)}")
        
        # Get OpenAI-based recommendations if available
        if self.openai_available:
            try:
                openai_result = self.openai_engine.analyze_resource_usage(resource_data, metrics_data)
                
                if "recommendations" in openai_result:
                    # Add source to each recommendation
                    for rec in openai_result["recommendations"]:
                        rec["source"] = "openai"
                    
                    # Add to recommendations list
                    recommendations["recommendations"].extend(openai_result["recommendations"])
            except Exception as e:
                self.logger.error(f"Error generating OpenAI recommendations: {str(e)}")
        
        # Add metadata
        recommendations["total_recommendations"] = len(recommendations["recommendations"])
        recommendations["sources_used"] = []
        
        if self.models_trained:
            recommendations["sources_used"].append("ml_models")
        
        if self.openai_available:
            recommendations["sources_used"].append("openai")
        
        return recommendations
    
    def get_account_recommendations(self, account_data: Dict[str, Any], 
                                   cost_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get overall recommendations for an account.
        
        Args:
            account_data: Account metadata
            cost_data: Historical cost data
            
        Returns:
            Dictionary containing recommendations
        """
        recommendations = {
            "account_id": account_data.get('id'),
            "provider": account_data.get('provider'),
            "timestamp": datetime.now().isoformat(),
            "recommendations": []
        }
        
        # Get ML-based recommendations if models are trained
        if self.models_trained:
            try:
                # Convert cost data to DataFrame for anomaly detection
                cost_df = pd.DataFrame(cost_data)
                
                # Detect cost anomalies
                anomalies = self.anomaly_detector.detect_anomalies(cost_df)
                
                # Generate recommendations based on anomalies
                ml_recommendations = self._generate_anomaly_recommendations(account_data, anomalies)
                
                recommendations["recommendations"].extend(ml_recommendations)
                recommendations["anomalies"] = anomalies
            except Exception as e:
                self.logger.error(f"Error generating ML account recommendations: {str(e)}")
        
        # Get OpenAI-based recommendations if available
        if self.openai_available:
            try:
                openai_result = self.openai_engine.generate_cost_saving_strategies(account_data, cost_data)
                
                if "strategies" in openai_result:
                    # Convert strategies to recommendations format
                    for strategy in openai_result["strategies"]:
                        recommendation = {
                            "title": strategy.get("description", "Cost optimization strategy"),
                            "description": strategy.get("description", ""),
                            "estimated_savings": strategy.get("estimated_savings", "Unknown"),
                            "impact_areas": strategy.get("areas_of_impact", []),
                            "timeline": strategy.get("implementation_timeline", "medium-term"),
                            "source": "openai"
                        }
                        recommendations["recommendations"].append(recommendation)
            except Exception as e:
                self.logger.error(f"Error generating OpenAI account recommendations: {str(e)}")
        
        # Add metadata
        recommendations["total_recommendations"] = len(recommendations["recommendations"])
        recommendations["sources_used"] = []
        
        if self.models_trained:
            recommendations["sources_used"].append("ml_models")
        
        if self.openai_available:
            recommendations["sources_used"].append("openai")
        
        return recommendations
    
    def explain_recommendation(self, recommendation_id: str) -> Dict[str, Any]:
        """
        Get detailed explanation for a recommendation.
        
        Args:
            recommendation_id: ID of the recommendation to explain
            
        Returns:
            Dictionary containing detailed explanation
        """
        # For development/testing, return mock explanation
        explanations = {
            "rec-001": {
                "id": "rec-001",
                "title": "Downsize EC2 instance",
                "detailed_explanation": "This t3.large instance has been running at an average CPU utilization of 12% over the past 30 days, with peak usage of only 34%. The instance is significantly overprovisioned for its workload. Downsizing to a t3.medium instance would provide sufficient capacity (2 vCPUs and 4 GiB memory) while reducing costs by approximately 45.6 USD per month. The risk is low as the current peak usage is well below the capacity of a t3.medium instance.",
                "data_points": [
                    {"metric": "Average CPU Utilization", "value": "12%", "period": "30 days"},
                    {"metric": "Peak CPU Utilization", "value": "34%", "period": "30 days"},
                    {"metric": "Average Memory Utilization", "value": "28%", "period": "30 days"},
                    {"metric": "Peak Memory Utilization", "value": "42%", "period": "30 days"}
                ],
                "implementation_steps": [
                    "Stop the EC2 instance",
                    "Change the instance type from t3.large to t3.medium",
                    "Start the instance",
                    "Verify that the application is functioning correctly"
                ],
                "potential_issues": [
                    "If the application has occasional CPU spikes not captured in the monitoring period, it might experience performance degradation",
                    "Some applications might be configured to use the specific amount of memory available in a t3.large instance"
                ],
                "estimated_effort": "Low (15-30 minutes)"
            },
            "rec-002": {
                "id": "rec-002",
                "title": "Delete unused EBS volume",
                "detailed_explanation": "This 100 GB EBS volume has been detached from any EC2 instance for 45 days and has no snapshot dependencies. It appears to be an orphaned resource that is no longer in use but continues to incur charges. Deleting this volume would save approximately 20.3 USD per month.",
                "data_points": [
                    {"metric": "Volume Status", "value": "Available (Detached)", "period": "45 days"},
                    {"metric": "Last Attached", "value": "2025-04-10", "period": "N/A"},
                    {"metric": "Volume Size", "value": "100 GB", "period": "N/A"},
                    {"metric": "Volume Type", "value": "gp3", "period": "N/A"}
                ],
                "implementation_steps": [
                    "Create a snapshot of the volume as a precaution",
                    "Delete the EBS volume through the AWS Management Console or AWS CLI"
                ],
                "potential_issues": [
                    "If the volume contains important data that is not backed up elsewhere, deleting it would result in data loss"
                ],
                "estimated_effort": "Low (5-10 minutes)"
            }
        }
        
        if recommendation_id in explanations:
            return explanations[recommendation_id]
        else:
            return {
                "error": f"Explanation for recommendation {recommendation_id} not found"
            }
    
    def _convert_metrics_to_dataframe(self, metrics_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Convert metrics data to a pandas DataFrame.
        
        Args:
            metrics_data: Dictionary with metrics data
            
        Returns:
            DataFrame with metrics data
        """
        rows = []
        
        for metric_name, metric_info in metrics_data.items():
            for datapoint in metric_info.get('datapoints', []):
                row = {
                    'timestamp': datapoint.get('timestamp'),
                    'metric_name': metric_name
                }
                
                # Add metric values
                for key, value in datapoint.items():
                    if key not in ['timestamp']:
                        row[key] = value
                
                rows.append(row)
        
        df = pd.DataFrame(rows)
        
        # Convert timestamp to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Pivot to get metrics as columns
        if 'metric_name' in df.columns:
            df = df.pivot_table(
                index='timestamp', 
                columns='metric_name', 
                values=['average', 'maximum'],
                aggfunc='first'
            )
            
            # Flatten multi-index columns
            df.columns = [f"{col[1]}_{col[0]}" for col in df.columns]
            df = df.reset_index()
        
        # Add derived features
        if 'CPUUtilization_average' in df.columns:
            df['cpu_usage'] = df['CPUUtilization_average']
        
        if 'MemoryUtilization_average' in df.columns:
            df['memory_usage'] = df['MemoryUtilization_average']
        elif 'memory_average' in df.columns:
            df['memory_usage'] = df['memory_average']
        
        return df
    
    def _generate_future_timepoints(self, historical_df: pd.DataFrame, days: int = 7) -> pd.DataFrame:
        """
        Generate future timepoints for prediction.
        
        Args:
            historical_df: DataFrame with historical data
            days: Number of days to predict into the future
            
        Returns:
            DataFrame with future timepoints
        """
        if 'timestamp' not in historical_df.columns:
            raise ValueError("Historical data must have a timestamp column")
        
        # Get the last timestamp
        last_timestamp = historical_df['timestamp'].max()
        
        # Generate future timestamps
        future_timestamps = []
        for i in range(1, days * 24 + 1):  # Hourly predictions for the specified days
            future_timestamps.append(last_timestamp + timedelta(hours=i))
        
        # Create DataFrame
        future_df = pd.DataFrame({'timestamp': future_timestamps})
        
        return future_df
    
    def _generate_ml_recommendations(self, resource_data: Dict[str, Any], 
                                    metrics_df: pd.DataFrame, 
                                    future_usage: Any) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on ML predictions.
        
        Args:
            resource_data: Resource metadata
            metrics_df: DataFrame with historical metrics
            future_usage: Predicted future usage
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Extract resource type and properties
        resource_type = resource_data.get('type')
        properties = resource_data.get('properties', {})
        
        # Calculate average predicted CPU and memory usage
        avg_predicted_cpu = future_usage[:, 0].mean() if future_usage.shape[1] > 0 else 0
        avg_predicted_memory = future_usage[:, 1].mean() if future_usage.shape[1] > 1 else 0
        
        # Generate recommendations based on resource type
        if resource_type == 'ec2_instance':
            instance_type = properties.get('instance_type')
            
            # Rightsizing recommendation based on CPU usage
            if avg_predicted_cpu < 20:
                recommendations.append({
                    "title": "Downsize EC2 instance",
                    "description": f"Based on predicted CPU usage ({avg_predicted_cpu:.1f}%), this instance is underutilized. Consider downsizing from {instance_type} to a smaller instance type.",
                    "action_type": "resize_instance",
                    "estimated_savings": "30-50%",
                    "risk_level": "low" if avg_predicted_cpu < 10 else "medium",
                    "source": "ml_prediction"
                })
            elif avg_predicted_cpu > 80:
                recommendations.append({
                    "title": "Upsize EC2 instance",
                    "description": f"Based on predicted CPU usage ({avg_predicted_cpu:.1f}%), this instance is overutilized. Consider upsizing from {instance_type} to a larger instance type to avoid performance issues.",
                    "action_type": "resize_instance",
                    "estimated_savings": "Performance improvement",
                    "risk_level": "medium",
                    "source": "ml_prediction"
                })
        
        return recommendations
    
    def _generate_anomaly_recommendations(self, account_data: Dict[str, Any], 
                                         anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on detected anomalies.
        
        Args:
            account_data: Account metadata
            anomalies: List of detected anomalies
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        for anomaly in anomalies:
            service = anomaly.get('service')
            severity = anomaly.get('severity')
            
            if service and severity:
                if severity == 'high':
                    recommendations.append({
                        "title": f"Investigate cost spike in {service}",
                        "description": f"A significant cost increase of {anomaly.get('percentage', 0)}% was detected in {service}. This requires immediate investigation.",
                        "action_type": "investigate_anomaly",
                        "estimated_savings": "Unknown",
                        "risk_level": "high",
                        "source": "ml_anomaly_detection"
                    })
                elif severity == 'medium':
                    recommendations.append({
                        "title": f"Review usage of {service}",
                        "description": f"An unusual cost pattern was detected in {service}, with an increase of {anomaly.get('percentage', 0)}%. Consider reviewing the usage and implementing cost controls.",
                        "action_type": "review_usage",
                        "estimated_savings": "5-15%",
                        "risk_level": "medium",
                        "source": "ml_anomaly_detection"
                    })
        
        return recommendations
