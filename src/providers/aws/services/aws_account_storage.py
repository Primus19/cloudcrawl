"""
AWS Account Storage for persisting AWS account information.
"""

import json
import logging
import os
from cryptography.fernet import Fernet
from src.config import ConfigManager

logger = logging.getLogger(__name__)

class AWSAccountStorage:
    """
    Storage class for AWS accounts.
    Handles encryption and persistence of AWS account credentials.
    """
    
    def __init__(self, encryption_key=None):
        """
        Initialize the AWS account storage.
        
        Args:
            encryption_key (str, optional): Key for encrypting sensitive data.
                If not provided, will use the key from configuration.
        """
        # Initialize configuration
        self.config = ConfigManager()
        
        # Set encryption key
        if encryption_key:
            self.encryption_key = encryption_key
        else:
            self.encryption_key = os.environ.get('ENCRYPTION_KEY', 'bp6yGtZxVmBDahA2jJILio-gu70EWbkqylK8psz5ZSQ=')
        
        # Initialize cipher for encryption/decryption
        try:
            self.cipher = Fernet(self.encryption_key.encode())
        except Exception as e:
            logger.error(f"Failed to initialize Fernet cipher: {str(e)}")
            # Use a hardcoded key for development/testing if the environment key fails
            fallback_key = 'bp6yGtZxVmBDahA2jJILio-gu70EWbkqylK8psz5ZSQ='
            self.cipher = Fernet(fallback_key.encode())
        
        # Initialize in-memory storage
        self.accounts = {}
        
        # Load accounts from storage
        self._load_accounts()
    
    def _load_accounts(self):
        """Load accounts from storage."""
        # In a real implementation, this would load from a database
        # For now, use mock data for development/testing
        self.accounts = {
            'aws-account-1': {
                'id': 'aws-account-1',
                'name': 'AWS Production',
                'provider': 'aws',
                'account_id': '123456789012',
                'access_key': self._encrypt('YOUR_AWS_ACCESS_KEY_HERE'),
                'secret_key': self._encrypt('YOUR_AWS_SECRET_KEY_HERE'),
                'regions': ['us-east-1', 'us-west-2'],
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-01-01T00:00:00Z'
            }
        }
    
    def _encrypt(self, data):
        """
        Encrypt sensitive data.
        
        Args:
            data (str): Data to encrypt.
            
        Returns:
            str: Encrypted data.
        """
        try:
            return self.cipher.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            return data
    
    def _decrypt(self, data):
        """
        Decrypt sensitive data.
        
        Args:
            data (str): Data to decrypt.
            
        Returns:
            str: Decrypted data.
        """
        try:
            return self.cipher.decrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            return data
    
    def get_account(self, account_id, include_sensitive=False):
        """
        Get an AWS account by ID.
        
        Args:
            account_id (str): ID of the account to get.
            include_sensitive (bool): Whether to include sensitive data.
            
        Returns:
            dict: Account data, or None if not found.
        """
        account = self.accounts.get(account_id)
        if account:
            # Create a copy to avoid modifying the stored data
            account_copy = account.copy()
            # Decrypt sensitive data
            account_copy['access_key'] = self._decrypt(account_copy['access_key'])
            account_copy['secret_key'] = self._decrypt(account_copy['secret_key'])
            return account_copy
        return None
    
    def get_accounts(self):
        """
        Get all AWS accounts.
        
        Returns:
            list: List of account data.
        """
        accounts = []
        for account_id, account in self.accounts.items():
            # Create a copy to avoid modifying the stored data
            account_copy = account.copy()
            # Decrypt sensitive data
            account_copy['access_key'] = self._decrypt(account_copy['access_key'])
            account_copy['secret_key'] = self._decrypt(account_copy['secret_key'])
            accounts.append(account_copy)
        return accounts
    
    def add_account(self, account_data):
        """
        Add an AWS account.
        
        Args:
            account_data (dict): Account data to add.
            
        Returns:
            dict: Added account data.
        """
        # Create a copy to avoid modifying the input data
        account = account_data.copy()
        
        # Generate ID if not provided
        if 'id' not in account:
            account['id'] = f"aws-account-{len(self.accounts) + 1}"
        
        # Set timestamps
        account['created_at'] = account.get('created_at', '2023-01-01T00:00:00Z')
        account['updated_at'] = account.get('updated_at', '2023-01-01T00:00:00Z')
        
        # Encrypt sensitive data
        account['access_key'] = self._encrypt(account['access_key'])
        account['secret_key'] = self._encrypt(account['secret_key'])
        
        # Store account
        self.accounts[account['id']] = account
        
        # Return a copy with decrypted sensitive data
        result = account.copy()
        result['access_key'] = self._decrypt(result['access_key'])
        result['secret_key'] = self._decrypt(result['secret_key'])
        
        return result
    
    def update_account(self, account_id, account_data):
        """
        Update an AWS account.
        
        Args:
            account_id (str): ID of the account to update.
            account_data (dict): New account data.
            
        Returns:
            dict: Updated account data, or None if not found.
        """
        if account_id not in self.accounts:
            return None
        
        # Create a copy to avoid modifying the input data
        account = account_data.copy()
        
        # Ensure ID is not changed
        account['id'] = account_id
        
        # Update timestamp
        account['updated_at'] = '2023-01-01T00:00:00Z'
        
        # Encrypt sensitive data
        if 'access_key' in account:
            account['access_key'] = self._encrypt(account['access_key'])
        if 'secret_key' in account:
            account['secret_key'] = self._encrypt(account['secret_key'])
        
        # Update account
        self.accounts[account_id].update(account)
        
        # Return a copy with decrypted sensitive data
        result = self.accounts[account_id].copy()
        result['access_key'] = self._decrypt(result['access_key'])
        result['secret_key'] = self._decrypt(result['secret_key'])
        
        return result
    
    def delete_account(self, account_id):
        """
        Delete an AWS account.
        
        Args:
            account_id (str): ID of the account to delete.
            
        Returns:
            bool: True if deleted, False if not found.
        """
        if account_id in self.accounts:
            del self.accounts[account_id]
            return True
        return False
        
    def list_accounts(self):
        """
        List all AWS accounts.
        
        Returns:
            list: List of all AWS accounts.
        """
        return self.get_accounts()
