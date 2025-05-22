"""
Base provider interface for cloud provider integrations.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from uuid import UUID


class CloudProviderInterface(ABC):
    """Interface for cloud provider integrations."""
    
    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with the cloud provider."""
        pass
    
    @abstractmethod
    def get_resources(self, resource_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get resources from the cloud provider."""
        pass
    
    @abstractmethod
    def get_resource(self, resource_id: str, resource_type: str) -> Dict[str, Any]:
        """Get a specific resource from the cloud provider."""
        pass
    
    @abstractmethod
    def get_cost_data(self, start_date: str, end_date: str, granularity: str) -> List[Dict[str, Any]]:
        """Get cost data from the cloud provider."""
        pass
    
    @abstractmethod
    def get_metrics(self, resource_id: str, resource_type: str, metric_names: List[str], 
                   start_time: str, end_time: str, period: int) -> Dict[str, Any]:
        """Get metrics for a specific resource."""
        pass
    
    @abstractmethod
    def execute_action(self, action_type: str, resource_id: str, resource_type: str, 
                      parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action on a resource."""
        pass
    
    @abstractmethod
    def tag_resource(self, resource_id: str, resource_type: str, tags: Dict[str, str]) -> bool:
        """Tag a resource."""
        pass
    
    @abstractmethod
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Get cost optimization recommendations from the cloud provider."""
        pass
