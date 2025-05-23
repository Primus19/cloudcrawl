"""
AWS Account Manager for Cloud Cost Optimizer.
Handles AWS account authentication, credential management, and API interactions.
"""
import boto3
import json
import os
from typing import Dict, Any, Optional, List
import logging
from cryptography.fernet import Fernet
import psycopg2
from psycopg2.extras import RealDictCursor

class AWSAccountManager:
    """
    Manages AWS accounts, credentials, and API interactions.
    """
    
    def __init__(self, db_connection_string: str, encryption_key: str):
        """
        Initialize the AWS Account Manager.
        
        Args:
            db_connection_string: PostgreSQL connection string
            encryption_key: Key for encrypting/decrypting credentials
        """
        self.db_connection_string = db_connection_string
        self.encryption_key = encryption_key
        self.cipher_suite = Fernet(encryption_key.encode())
        self.logger = logging.getLogger(__name__)
    
    def _get_db_connection(self):
        """Get a database connection."""
        return psycopg2.connect(self.db_connection_string)
    
    def _encrypt_credentials(self, credentials: Dict[str, Any]) -> str:
        """
        Encrypt account credentials.
        
        Args:
            credentials: Dictionary containing credentials
            
        Returns:
            Encrypted credentials as a string
        """
        credentials_json = json.dumps(credentials)
        encrypted_data = self.cipher_suite.encrypt(credentials_json.encode())
        return encrypted_data.decode()
    
    def _decrypt_credentials(self, encrypted_data: str) -> Dict[str, Any]:
        """
        Decrypt account credentials.
        
        Args:
            encrypted_data: Encrypted credentials string
            
        Returns:
            Dictionary containing decrypted credentials
        """
        decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
        return json.loads(decrypted_data.decode())
    
    def create_account(self, name: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new AWS account.
        
        Args:
            name: Account name
            credentials: Dictionary containing AWS credentials
                For role_arn: {'credential_type': 'role_arn', 'role_arn': 'arn:aws:iam::123456789012:role/MyRole'}
                For access_key: {'credential_type': 'access_key', 'access_key_id': 'AKIAIOSFODNN7EXAMPLE', 'secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'}
            
        Returns:
            Dictionary containing account information
        """
        # Validate credentials
        credential_type = credentials.get('credential_type')
        if credential_type not in ['role_arn', 'access_key']:
            raise ValueError("Invalid credential type. Must be 'role_arn' or 'access_key'.")
        
        if credential_type == 'role_arn' and 'role_arn' not in credentials:
            raise ValueError("Role ARN is required for 'role_arn' credential type.")
        
        if credential_type == 'access_key' and ('access_key_id' not in credentials or 'secret_access_key' not in credentials):
            raise ValueError("Access key ID and secret access key are required for 'access_key' credential type.")
        
        # Test connection
        try:
            self._test_aws_connection(credentials)
        except Exception as e:
            self.logger.error(f"Failed to connect to AWS: {str(e)}")
            raise ValueError(f"Failed to connect to AWS: {str(e)}")
        
        # Encrypt credentials
        encrypted_credentials = self._encrypt_credentials(credentials)
        
        # Store account in database
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Insert account
                cursor.execute(
                    "INSERT INTO accounts (name, provider, status) VALUES (%s, %s, %s) RETURNING id, name, provider, status, created_at, updated_at",
                    (name, 'aws', 'active')
                )
                account = cursor.fetchone()
                
                # Insert credentials
                cursor.execute(
                    "INSERT INTO account_credentials (account_id, credential_type, credential_data) VALUES (%s, %s, %s)",
                    (account['id'], credential_type, encrypted_credentials)
                )
                
                conn.commit()
                return dict(account)
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def get_accounts(self) -> List[Dict[str, Any]]:
        """
        Get all AWS accounts.
        
        Returns:
            List of dictionaries containing account information
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT id, name, provider, status, created_at, updated_at FROM accounts WHERE provider = 'aws'"
                )
                accounts = cursor.fetchall()
                return [dict(account) for account in accounts]
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def get_account(self, account_id: int) -> Optional[Dict[str, Any]]:
        """
        Get an AWS account by ID.
        
        Args:
            account_id: Account ID
            
        Returns:
            Dictionary containing account information, or None if not found
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT id, name, provider, status, created_at, updated_at FROM accounts WHERE id = %s AND provider = 'aws'",
                    (account_id,)
                )
                account = cursor.fetchone()
                return dict(account) if account else None
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def update_account(self, account_id: int, name: Optional[str] = None, credentials: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Update an AWS account.
        
        Args:
            account_id: Account ID
            name: New account name (optional)
            credentials: New credentials (optional)
            
        Returns:
            Updated account information, or None if not found
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Check if account exists
                cursor.execute(
                    "SELECT id FROM accounts WHERE id = %s AND provider = 'aws'",
                    (account_id,)
                )
                if not cursor.fetchone():
                    return None
                
                # Update account name if provided
                if name:
                    cursor.execute(
                        "UPDATE accounts SET name = %s, updated_at = NOW() WHERE id = %s",
                        (name, account_id)
                    )
                
                # Update credentials if provided
                if credentials:
                    # Validate credentials
                    credential_type = credentials.get('credential_type')
                    if credential_type not in ['role_arn', 'access_key']:
                        raise ValueError("Invalid credential type. Must be 'role_arn' or 'access_key'.")
                    
                    if credential_type == 'role_arn' and 'role_arn' not in credentials:
                        raise ValueError("Role ARN is required for 'role_arn' credential type.")
                    
                    if credential_type == 'access_key' and ('access_key_id' not in credentials or 'secret_access_key' not in credentials):
                        raise ValueError("Access key ID and secret access key are required for 'access_key' credential type.")
                    
                    # Test connection
                    try:
                        self._test_aws_connection(credentials)
                    except Exception as e:
                        self.logger.error(f"Failed to connect to AWS: {str(e)}")
                        raise ValueError(f"Failed to connect to AWS: {str(e)}")
                    
                    # Encrypt credentials
                    encrypted_credentials = self._encrypt_credentials(credentials)
                    
                    # Update credentials
                    cursor.execute(
                        "UPDATE account_credentials SET credential_type = %s, credential_data = %s WHERE account_id = %s",
                        (credential_type, encrypted_credentials, account_id)
                    )
                
                # Get updated account
                cursor.execute(
                    "SELECT id, name, provider, status, created_at, updated_at FROM accounts WHERE id = %s",
                    (account_id,)
                )
                account = cursor.fetchone()
                
                conn.commit()
                return dict(account)
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def delete_account(self, account_id: int) -> bool:
        """
        Delete an AWS account.
        
        Args:
            account_id: Account ID
            
        Returns:
            True if account was deleted, False if not found
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check if account exists
                cursor.execute(
                    "SELECT id FROM accounts WHERE id = %s AND provider = 'aws'",
                    (account_id,)
                )
                if not cursor.fetchone():
                    return False
                
                # Delete account (cascade will delete credentials)
                cursor.execute(
                    "DELETE FROM accounts WHERE id = %s",
                    (account_id,)
                )
                
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def test_connection(self, account_id: int) -> Dict[str, Any]:
        """
        Test connection to an AWS account.
        
        Args:
            account_id: Account ID
            
        Returns:
            Dictionary containing test results
        """
        # Get account credentials
        credentials = self._get_account_credentials(account_id)
        if not credentials:
            raise ValueError(f"Account {account_id} not found or has no credentials")
        
        # Test connection
        try:
            self._test_aws_connection(credentials)
            
            # Update account status
            conn = self._get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE accounts SET status = 'active', updated_at = NOW() WHERE id = %s",
                        (account_id,)
                    )
                    conn.commit()
            finally:
                conn.close()
            
            return {
                'success': True,
                'message': 'Connection successful'
            }
        except Exception as e:
            # Update account status
            conn = self._get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE accounts SET status = 'error', updated_at = NOW() WHERE id = %s",
                        (account_id,)
                    )
                    conn.commit()
            finally:
                conn.close()
            
            return {
                'success': False,
                'message': f'Connection failed: {str(e)}'
            }
    
    def _get_account_credentials(self, account_id: int) -> Optional[Dict[str, Any]]:
        """
        Get credentials for an AWS account.
        
        Args:
            account_id: Account ID
            
        Returns:
            Dictionary containing credentials, or None if not found
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT credential_type, credential_data FROM account_credentials WHERE account_id = %s",
                    (account_id,)
                )
                credential_record = cursor.fetchone()
                
                if not credential_record:
                    return None
                
                # Decrypt credentials
                credentials = self._decrypt_credentials(credential_record['credential_data'])
                credentials['credential_type'] = credential_record['credential_type']
                
                return credentials
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def _test_aws_connection(self, credentials: Dict[str, Any]) -> None:
        """
        Test connection to AWS using provided credentials.
        
        Args:
            credentials: Dictionary containing AWS credentials
            
        Raises:
            Exception if connection fails
        """
        credential_type = credentials.get('credential_type')
        
        if credential_type == 'role_arn':
            # Create STS client
            sts_client = boto3.client('sts')
            
            # Assume role
            response = sts_client.assume_role(
                RoleArn=credentials['role_arn'],
                RoleSessionName='CloudCostOptimizerTest'
            )
            
            # Create session with temporary credentials
            session = boto3.Session(
                aws_access_key_id=response['Credentials']['AccessKeyId'],
                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                aws_session_token=response['Credentials']['SessionToken']
            )
        elif credential_type == 'access_key':
            # Create session with access key
            session = boto3.Session(
                aws_access_key_id=credentials['access_key_id'],
                aws_secret_access_key=credentials['secret_access_key']
            )
        else:
            raise ValueError(f"Unsupported credential type: {credential_type}")
        
        # Test connection by listing S3 buckets
        s3_client = session.client('s3')
        s3_client.list_buckets()
    
    def get_boto3_session(self, account_id: int) -> boto3.Session:
        """
        Get a boto3 session for an AWS account.
        
        Args:
            account_id: Account ID
            
        Returns:
            boto3.Session object
            
        Raises:
            ValueError if account not found or connection fails
        """
        # Get account credentials
        credentials = self._get_account_credentials(account_id)
        if not credentials:
            raise ValueError(f"Account {account_id} not found or has no credentials")
        
        credential_type = credentials.get('credential_type')
        
        if credential_type == 'role_arn':
            # Create STS client
            sts_client = boto3.client('sts')
            
            # Assume role
            response = sts_client.assume_role(
                RoleArn=credentials['role_arn'],
                RoleSessionName='CloudCostOptimizer'
            )
            
            # Create session with temporary credentials
            return boto3.Session(
                aws_access_key_id=response['Credentials']['AccessKeyId'],
                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                aws_session_token=response['Credentials']['SessionToken']
            )
        elif credential_type == 'access_key':
            # Create session with access key
            return boto3.Session(
                aws_access_key_id=credentials['access_key_id'],
                aws_secret_access_key=credentials['secret_access_key']
            )
        else:
            raise ValueError(f"Unsupported credential type: {credential_type}")
