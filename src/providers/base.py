"""
Base interface for cloud providers in the Cloud Cost Optimizer.
All cloud provider implementations must implement this interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class CloudProviderInterface(ABC):
    """Interface for cloud providers."""
    
    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """
        Authenticate with the cloud provider.
        
        Args:
            credentials: Provider-specific credentials
            
        Returns:
            True if authentication was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_resources(self, resource_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get resources from the cloud provider.
        
        Args:
            resource_type: Optional resource type filter
            
        Returns:
            List of resources
        """
        pass
    
    @abstractmethod
    def get_resource(self, resource_id: str, resource_type: str) -> Dict[str, Any]:
        """
        Get a specific resource from the cloud provider.
        
        Args:
            resource_id: Resource ID
            resource_type: Resource type
            
        Returns:
            Resource details
        """
        pass
    
    @abstractmethod
    def get_cost_data(self, start_date: str, end_date: str, granularity: str) -> List[Dict[str, Any]]:
        """
        Get cost data from the cloud provider.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            granularity: Data granularity (daily, monthly)
            
        Returns:
            List of cost data points
        """
        pass
    
    @abstractmethod
    def get_metrics(self, resource_id: str, resource_type: str, metric_names: List[str], 
                   start_time: str, end_time: str, period: int) -> Dict[str, Any]:
        """
        Get metrics for a specific resource.
        
        Args:
            resource_id: Resource ID
            resource_type: Resource type
            metric_names: List of metric names
            start_time: Start time (ISO format)
            end_time: End time (ISO format)
            period: Period in seconds
            
        Returns:
            Dictionary of metrics
        """
        pass
