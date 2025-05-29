"""
Machine Learning models for Cloud Cost Optimizer.
This module provides custom ML models for cost optimization recommendations.
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Any, Optional
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class ResourceUsagePredictor:
    """
    Machine learning model to predict future resource usage based on historical patterns.
    Used for rightsizing recommendations and capacity planning.
    """
    
    def __init__(self):
        """Initialize the resource usage predictor."""
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.logger = logging.getLogger(__name__)
    
    def train(self, historical_data: pd.DataFrame) -> bool:
        """
        Train the model on historical resource usage data.
        
        Args:
            historical_data: DataFrame with columns for timestamp, cpu_usage, memory_usage, etc.
            
        Returns:
            True if training was successful, False otherwise
        """
        try:
            # Prepare features (time-based features and any other relevant columns)
            X = self._prepare_features(historical_data)
            
            # Prepare targets (resource usage metrics)
            y = historical_data[['cpu_usage', 'memory_usage']].values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled, y)
            
            self.is_trained = True
            return True
        except Exception as e:
            self.logger.error(f"Error training resource usage predictor: {str(e)}")
            return False
    
    def predict(self, future_timepoints: pd.DataFrame) -> np.ndarray:
        """
        Predict future resource usage.
        
        Args:
            future_timepoints: DataFrame with timestamp and other relevant features
            
        Returns:
            Array of predicted resource usage values
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        try:
            # Prepare features
            X = self._prepare_features(future_timepoints)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Make predictions
            predictions = self.model.predict(X_scaled)
            
            return predictions
        except Exception as e:
            self.logger.error(f"Error predicting resource usage: {str(e)}")
            raise
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """
        Prepare features for the model.
        
        Args:
            data: DataFrame with timestamp and other columns
            
        Returns:
            Feature matrix
        """
        # Convert timestamp to datetime if it's not already
        if 'timestamp' in data.columns and not pd.api.types.is_datetime64_any_dtype(data['timestamp']):
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Extract time-based features
        features = pd.DataFrame()
        if 'timestamp' in data.columns:
            features['hour'] = data['timestamp'].dt.hour
            features['day_of_week'] = data['timestamp'].dt.dayofweek
            features['day_of_month'] = data['timestamp'].dt.day
            features['month'] = data['timestamp'].dt.month
            features['is_weekend'] = (data['timestamp'].dt.dayofweek >= 5).astype(int)
        
        # Add any other relevant features
        for col in data.columns:
            if col not in ['timestamp', 'cpu_usage', 'memory_usage']:
                features[col] = data[col]
        
        return features.values


class CostAnomalyDetector:
    """
    Machine learning model to detect anomalies in cloud spending.
    Used for alerting and cost control.
    """
    
    def __init__(self, contamination: float = 0.05):
        """
        Initialize the cost anomaly detector.
        
        Args:
            contamination: Expected proportion of anomalies in the data
        """
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.logger = logging.getLogger(__name__)
    
    def train(self, historical_costs: pd.DataFrame) -> bool:
        """
        Train the model on historical cost data.
        
        Args:
            historical_costs: DataFrame with columns for timestamp, cost, service, etc.
            
        Returns:
            True if training was successful, False otherwise
        """
        try:
            # Prepare features
            X = self._prepare_features(historical_costs)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled)
            
            self.is_trained = True
            return True
        except Exception as e:
            self.logger.error(f"Error training cost anomaly detector: {str(e)}")
            return False
    
    def detect_anomalies(self, cost_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect anomalies in cost data.
        
        Args:
            cost_data: DataFrame with columns for timestamp, cost, service, etc.
            
        Returns:
            Dictionary with anomaly detection results
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before detecting anomalies")
        
        try:
            # Prepare features
            X = self._prepare_features(cost_data)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Predict anomalies (-1 for anomalies, 1 for normal)
            predictions = self.model.predict(X_scaled)
            scores = self.model.decision_function(X_scaled)
            
            # Create result
            anomalies = cost_data.copy()
            anomalies['is_anomaly'] = (predictions == -1)
            anomalies['anomaly_score'] = scores
            
            # Group anomalies by service
            anomalies_by_service = {}
            for service in anomalies['service'].unique():
                service_data = anomalies[anomalies['service'] == service]
                anomalies_by_service[service] = {
                    'total_anomalies': service_data['is_anomaly'].sum(),
                    'anomaly_timestamps': service_data[service_data['is_anomaly']]['timestamp'].tolist(),
                    'anomaly_costs': service_data[service_data['is_anomaly']]['cost'].tolist()
                }
            
            result = {
                'total_records': len(cost_data),
                'total_anomalies': (predictions == -1).sum(),
                'anomaly_percentage': (predictions == -1).mean() * 100,
                'anomalies_by_service': anomalies_by_service,
                'anomaly_details': anomalies[anomalies['is_anomaly']].to_dict(orient='records')
            }
            
            return result
        except Exception as e:
            self.logger.error(f"Error detecting cost anomalies: {str(e)}")
            raise
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """
        Prepare features for the model.
        
        Args:
            data: DataFrame with cost data
            
        Returns:
            Feature matrix
        """
        # Convert timestamp to datetime if it's not already
        if 'timestamp' in data.columns and not pd.api.types.is_datetime64_any_dtype(data['timestamp']):
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Extract time-based features
        features = pd.DataFrame()
        if 'timestamp' in data.columns:
            features['hour'] = data['timestamp'].dt.hour
            features['day_of_week'] = data['timestamp'].dt.dayofweek
            features['day_of_month'] = data['timestamp'].dt.day
            features['month'] = data['timestamp'].dt.month
        
        # Add cost as a feature
        if 'cost' in data.columns:
            features['cost'] = data['cost']
        
        # One-hot encode categorical features
        if 'service' in data.columns:
            service_dummies = pd.get_dummies(data['service'], prefix='service')
            features = pd.concat([features, service_dummies], axis=1)
        
        return features.values


class ResourceClusterer:
    """
    Machine learning model to cluster similar resources.
    Used for identifying resource groups with similar usage patterns.
    """
    
    def __init__(self, n_clusters: int = 5):
        """
        Initialize the resource clusterer.
        
        Args:
            n_clusters: Number of clusters to form
        """
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.logger = logging.getLogger(__name__)
    
    def train(self, resource_data: pd.DataFrame) -> bool:
        """
        Train the model on resource data.
        
        Args:
            resource_data: DataFrame with resource properties and usage metrics
            
        Returns:
            True if training was successful, False otherwise
        """
        try:
            # Prepare features
            X = self._prepare_features(resource_data)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled)
            
            self.is_trained = True
            return True
        except Exception as e:
            self.logger.error(f"Error training resource clusterer: {str(e)}")
            return False
    
    def cluster_resources(self, resource_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Cluster resources based on their properties and usage patterns.
        
        Args:
            resource_data: DataFrame with resource properties and usage metrics
            
        Returns:
            Dictionary with clustering results
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before clustering resources")
        
        try:
            # Prepare features
            X = self._prepare_features(resource_data)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Predict clusters
            clusters = self.model.predict(X_scaled)
            
            # Create result
            clustered_resources = resource_data.copy()
            clustered_resources['cluster'] = clusters
            
            # Group resources by cluster
            resources_by_cluster = {}
            for cluster_id in range(self.model.n_clusters):
                cluster_data = clustered_resources[clustered_resources['cluster'] == cluster_id]
                resources_by_cluster[str(cluster_id)] = {
                    'count': len(cluster_data),
                    'resource_ids': cluster_data['id'].tolist(),
                    'avg_cpu_usage': cluster_data['avg_cpu_usage'].mean() if 'avg_cpu_usage' in cluster_data.columns else None,
                    'avg_memory_usage': cluster_data['avg_memory_usage'].mean() if 'avg_memory_usage' in cluster_data.columns else None
                }
            
            result = {
                'total_resources': len(resource_data),
                'num_clusters': self.model.n_clusters,
                'resources_by_cluster': resources_by_cluster,
                'cluster_centers': self.model.cluster_centers_.tolist()
            }
            
            return result
        except Exception as e:
            self.logger.error(f"Error clustering resources: {str(e)}")
            raise
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """
        Prepare features for the model.
        
        Args:
            data: DataFrame with resource data
            
        Returns:
            Feature matrix
        """
        # Select numerical features
        numerical_features = []
        for col in data.columns:
            if data[col].dtype in [np.int64, np.float64] and col not in ['id', 'cluster']:
                numerical_features.append(col)
        
        # One-hot encode categorical features
        categorical_features = []
        for col in data.columns:
            if data[col].dtype == 'object' and col not in ['id', 'name', 'region']:
                categorical_features.append(col)
        
        # Combine features
        features = data[numerical_features].copy()
        
        for col in categorical_features:
            dummies = pd.get_dummies(data[col], prefix=col)
            features = pd.concat([features, dummies], axis=1)
        
        return features.values
