"""
Provider factory for creating cloud provider instances.
"""
from typing import Dict, Any

from src.providers.base import CloudProviderInterface
from src.providers.aws.services.aws_provider import AWSProvider
from src.providers.azure.services.azure_provider import AzureProvider
from src.providers.gcp.services.gcp_provider import GCPProvider


class ProviderFactory:
    """Factory for creating cloud provider instances."""
    
    @staticmethod
    def create_provider(provider_type: str) -> CloudProviderInterface:
        """Create a cloud provider instance based on provider type."""
        if provider_type.lower() == 'aws':
            return AWSProvider()
        elif provider_type.lower() == 'azure':
            return AzureProvider()
        elif provider_type.lower() in ['gcp', 'google']:
            return GCPProvider()
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
