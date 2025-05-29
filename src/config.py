"""
Configuration management for CloudCrawl application.
This module provides centralized configuration handling for all components.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigManager:
    """Configuration manager for CloudCrawl application."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one config manager exists."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the configuration manager."""
        if self._initialized:
            return
            
        self._config = {
            'app': {
                'debug': os.environ.get('DEBUG', 'False').lower() == 'true',
                'port': int(os.environ.get('PORT', 5000)),
                'host': os.environ.get('HOST', '0.0.0.0'),
                'secret_key': os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
            },
            'database': {
                'connection_string': os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/cloudcrawl'),
            },
            'security': {
                'encryption_key': os.environ.get('ENCRYPTION_KEY', 'dev-encryption-key-change-in-production'),
                'jwt_secret': os.environ.get('JWT_SECRET', 'dev-jwt-secret-change-in-production'),
                'jwt_expiration': int(os.environ.get('JWT_EXPIRATION', 3600)),
            },
            'aws': {
                'access_key': os.environ.get('AWS_ACCESS_KEY', ''),
                'secret_key': os.environ.get('AWS_SECRET_KEY', ''),
                'region': os.environ.get('AWS_REGION', 'us-east-1'),
            },
            'azure': {
                'client_id': os.environ.get('AZURE_CLIENT_ID', ''),
                'client_secret': os.environ.get('AZURE_CLIENT_SECRET', ''),
                'tenant_id': os.environ.get('AZURE_TENANT_ID', ''),
                'subscription_id': os.environ.get('AZURE_SUBSCRIPTION_ID', ''),
            },
            'gcp': {
                'credentials_path': os.environ.get('GCP_CREDENTIALS_PATH', ''),
                'project_id': os.environ.get('GCP_PROJECT_ID', ''),
            },
            'openai': {
                'api_key': os.environ.get('OPENAI_API_KEY', ''),
                'model': os.environ.get('OPENAI_MODEL', 'gpt-4'),
            },
            'terraform': {
                'templates_dir': os.environ.get('TERRAFORM_TEMPLATES_DIR', 'src/terraform/templates'),
                'working_dir': os.environ.get('TERRAFORM_WORKING_DIR', 'src/terraform/working'),
            },
            'kubernetes': {
                'config_path': os.environ.get('KUBERNETES_CONFIG_PATH', ''),
                'context': os.environ.get('KUBERNETES_CONTEXT', ''),
            },
        }
        
        # Load config from file if it exists
        config_path = os.environ.get('CONFIG_PATH', 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    self._update_nested_dict(self._config, file_config)
                logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                logger.error(f"Failed to load configuration from {config_path}: {str(e)}")
        
        # For development/testing, use mock values if real credentials are not available
        if os.environ.get('ENVIRONMENT', 'development') == 'development':
            self._setup_development_environment()
            
        self._initialized = True
        logger.info("Configuration manager initialized")
    
    def _update_nested_dict(self, d: Dict[str, Any], u: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a nested dictionary with another nested dictionary.
        
        Args:
            d: The original dictionary to update
            u: The dictionary with updates
            
        Returns:
            The updated dictionary
        """
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._update_nested_dict(d[k], v)
            else:
                d[k] = v
        return d
    
    def _setup_development_environment(self):
        """Set up development environment with mock values for testing."""
        logger.info("Setting up development environment with mock values")
        
        # Only override empty values in development mode
        if not self._config['database']['connection_string'].startswith('postgresql://postgres'):
            self._config['database']['connection_string'] = 'mock://database'
            
        if not self._config['aws']['access_key']:
            self._config['aws']['access_key'] = 'mock-aws-access-key'
            self._config['aws']['secret_key'] = 'mock-aws-secret-key'
            
        if not self._config['azure']['client_id']:
            self._config['azure']['client_id'] = 'mock-azure-client-id'
            self._config['azure']['client_secret'] = 'mock-azure-client-secret'
            self._config['azure']['tenant_id'] = 'mock-azure-tenant-id'
            self._config['azure']['subscription_id'] = 'mock-azure-subscription-id'
            
        if not self._config['gcp']['credentials_path']:
            self._config['gcp']['project_id'] = 'mock-gcp-project-id'
    
    def get(self, section: str, key: Optional[str] = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: The configuration section
            key: The specific key within the section, or None to get the entire section
            
        Returns:
            The configuration value, section, or None if not found
        """
        if section not in self._config:
            return None
            
        if key is None:
            return self._config[section]
            
        return self._config[section].get(key)
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get the entire configuration.
        
        Returns:
            The complete configuration dictionary
        """
        return self._config
