"""
AWS Resource Manager for Cloud Cost Optimizer.
Handles AWS resource discovery, cost analysis, and optimization recommendations.
"""
import boto3
import json
import os
from typing import Dict, Any, Optional, List
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

from src.providers.aws.services.aws_account_manager import AWSAccountManager

class AWSResourceManager:
    """
    Manages AWS resources, discovery, cost analysis, and optimization recommendations.
    """
    
    def __init__(self, db_connection_string: str, account_manager: AWSAccountManager):
        """
        Initialize the AWS Resource Manager.
        
        Args:
            db_connection_string: PostgreSQL connection string
            account_manager: AWSAccountManager instance
        """
        self.db_connection_string = db_connection_string
        self.account_manager = account_manager
        self.logger = logging.getLogger(__name__)
    
    def _get_db_connection(self):
        """Get a database connection."""
        return psycopg2.connect(self.db_connection_string)
    
    def discover_resources(self, account_id: int, resource_types: List[str], regions: List[str]) -> Dict[str, Any]:
        """
        Discover AWS resources for an account.
        
        Args:
            account_id: Account ID
            resource_types: List of resource types to discover (e.g., 'ec2', 's3', 'rds')
            regions: List of AWS regions to discover resources in
            
        Returns:
            Dictionary containing discovery results
        """
        # Get boto3 session for account
        try:
            session = self.account_manager.get_boto3_session(account_id)
        except Exception as e:
            self.logger.error(f"Failed to get boto3 session: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to get boto3 session: {str(e)}"
            }
        
        # Discover resources
        discovered_resources = []
        
        for region in regions:
            for resource_type in resource_types:
                try:
                    if resource_type == 'ec2':
                        resources = self._discover_ec2_instances(session, region)
                    elif resource_type == 's3':
                        resources = self._discover_s3_buckets(session, region)
                    elif resource_type == 'rds':
                        resources = self._discover_rds_instances(session, region)
                    elif resource_type == 'lambda':
                        resources = self._discover_lambda_functions(session, region)
                    elif resource_type == 'eks':
                        resources = self._discover_eks_clusters(session, region)
                    else:
                        self.logger.warning(f"Unsupported resource type: {resource_type}")
                        continue
                    
                    discovered_resources.extend(resources)
                except Exception as e:
                    self.logger.error(f"Error discovering {resource_type} resources in {region}: {str(e)}")
        
        # Store resources in database
        conn = self._get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Delete existing resources for account
                cursor.execute(
                    "DELETE FROM resources WHERE account_id = %s",
                    (account_id,)
                )
                
                # Insert new resources
                for resource in discovered_resources:
                    cursor.execute(
                        """
                        INSERT INTO resources 
                        (account_id, provider, resource_type, resource_id, name, region, metadata)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            account_id,
                            'aws',
                            resource['resource_type'],
                            resource['resource_id'],
                            resource.get('name', ''),
                            resource.get('region', ''),
                            json.dumps(resource.get('metadata', {}))
                        )
                    )
                
                conn.commit()
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            return {
                'success': False,
                'error': f"Database error: {str(e)}"
            }
        finally:
            conn.close()
        
        return {
            'success': True,
            'resources_discovered': len(discovered_resources),
            'resource_types': resource_types,
            'regions': regions
        }
    
    def _discover_ec2_instances(self, session: boto3.Session, region: str) -> List[Dict[str, Any]]:
        """
        Discover EC2 instances in a region.
        
        Args:
            session: boto3 Session
            region: AWS region
            
        Returns:
            List of dictionaries containing EC2 instance information
        """
        ec2_client = session.client('ec2', region_name=region)
        
        # Get instances
        response = ec2_client.describe_instances()
        
        instances = []
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                # Get instance name from tags
                name = ''
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break
                
                instances.append({
                    'resource_type': 'ec2',
                    'resource_id': instance['InstanceId'],
                    'name': name,
                    'region': region,
                    'metadata': {
                        'instance_type': instance.get('InstanceType', ''),
                        'state': instance.get('State', {}).get('Name', ''),
                        'launch_time': instance.get('LaunchTime', '').isoformat() if instance.get('LaunchTime') else '',
                        'public_ip': instance.get('PublicIpAddress', ''),
                        'private_ip': instance.get('PrivateIpAddress', ''),
                        'tags': instance.get('Tags', [])
                    }
                })
        
        return instances
    
    def _discover_s3_buckets(self, session: boto3.Session, region: str) -> List[Dict[str, Any]]:
        """
        Discover S3 buckets.
        
        Args:
            session: boto3 Session
            region: AWS region (not used for S3, but kept for consistency)
            
        Returns:
            List of dictionaries containing S3 bucket information
        """
        s3_client = session.client('s3')
        
        # Get buckets
        response = s3_client.list_buckets()
        
        buckets = []
        for bucket in response.get('Buckets', []):
            # Get bucket region
            try:
                bucket_region = s3_client.get_bucket_location(Bucket=bucket['Name'])
                bucket_region = bucket_region.get('LocationConstraint', 'us-east-1')
                if bucket_region is None:
                    bucket_region = 'us-east-1'
            except Exception:
                bucket_region = 'unknown'
            
            buckets.append({
                'resource_type': 's3',
                'resource_id': bucket['Name'],
                'name': bucket['Name'],
                'region': bucket_region,
                'metadata': {
                    'creation_date': bucket.get('CreationDate', '').isoformat() if bucket.get('CreationDate') else ''
                }
            })
        
        return buckets
    
    def _discover_rds_instances(self, session: boto3.Session, region: str) -> List[Dict[str, Any]]:
        """
        Discover RDS instances in a region.
        
        Args:
            session: boto3 Session
            region: AWS region
            
        Returns:
            List of dictionaries containing RDS instance information
        """
        rds_client = session.client('rds', region_name=region)
        
        # Get instances
        response = rds_client.describe_db_instances()
        
        instances = []
        for instance in response.get('DBInstances', []):
            instances.append({
                'resource_type': 'rds',
                'resource_id': instance['DBInstanceIdentifier'],
                'name': instance['DBInstanceIdentifier'],
                'region': region,
                'metadata': {
                    'engine': instance.get('Engine', ''),
                    'engine_version': instance.get('EngineVersion', ''),
                    'instance_class': instance.get('DBInstanceClass', ''),
                    'storage': instance.get('AllocatedStorage', 0),
                    'status': instance.get('DBInstanceStatus', ''),
                    'multi_az': instance.get('MultiAZ', False),
                    'endpoint': instance.get('Endpoint', {}).get('Address', '') if instance.get('Endpoint') else ''
                }
            })
        
        return instances
    
    def _discover_lambda_functions(self, session: boto3.Session, region: str) -> List[Dict[str, Any]]:
        """
        Discover Lambda functions in a region.
        
        Args:
            session: boto3 Session
            region: AWS region
            
        Returns:
            List of dictionaries containing Lambda function information
        """
        lambda_client = session.client('lambda', region_name=region)
        
        # Get functions
        response = lambda_client.list_functions()
        
        functions = []
        for function in response.get('Functions', []):
            functions.append({
                'resource_type': 'lambda',
                'resource_id': function['FunctionName'],
                'name': function['FunctionName'],
                'region': region,
                'metadata': {
                    'runtime': function.get('Runtime', ''),
                    'memory': function.get('MemorySize', 0),
                    'timeout': function.get('Timeout', 0),
                    'last_modified': function.get('LastModified', ''),
                    'handler': function.get('Handler', ''),
                    'description': function.get('Description', '')
                }
            })
        
        return functions
    
    def _discover_eks_clusters(self, session: boto3.Session, region: str) -> List[Dict[str, Any]]:
        """
        Discover EKS clusters in a region.
        
        Args:
            session: boto3 Session
            region: AWS region
            
        Returns:
            List of dictionaries containing EKS cluster information
        """
        eks_client = session.client('eks', region_name=region)
        
        # Get clusters
        response = eks_client.list_clusters()
        
        clusters = []
        for cluster_name in response.get('clusters', []):
            # Get cluster details
            try:
                cluster = eks_client.describe_cluster(name=cluster_name)['cluster']
                
                clusters.append({
                    'resource_type': 'eks',
                    'resource_id': cluster_name,
                    'name': cluster_name,
                    'region': region,
                    'metadata': {
                        'version': cluster.get('version', ''),
                        'status': cluster.get('status', ''),
                        'endpoint': cluster.get('endpoint', ''),
                        'created_at': cluster.get('createdAt', '').isoformat() if cluster.get('createdAt') else '',
                        'vpc_id': cluster.get('resourcesVpcConfig', {}).get('vpcId', '') if cluster.get('resourcesVpcConfig') else ''
                    }
                })
            except Exception as e:
                self.logger.error(f"Error getting details for EKS cluster {cluster_name}: {str(e)}")
        
        return clusters
    
    def get_resources(self, account_id: Optional[int] = None, resource_type: Optional[str] = None, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get resources from the database.
        
        Args:
            account_id: Filter by account ID (optional)
            resource_type: Filter by resource type (optional)
            region: Filter by region (optional)
            
        Returns:
            List of dictionaries containing resource information
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM resources WHERE provider = 'aws'"
                params = []
                
                if account_id:
                    query += " AND account_id = %s"
                    params.append(account_id)
                
                if resource_type:
                    query += " AND resource_type = %s"
                    params.append(resource_type)
                
                if region:
                    query += " AND region = %s"
                    params.append(region)
                
                cursor.execute(query, params)
                resources = cursor.fetchall()
                
                # Convert metadata from JSON string to dictionary
                for resource in resources:
                    resource['metadata'] = json.loads(resource['metadata']) if resource['metadata'] else {}
                
                return [dict(resource) for resource in resources]
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def get_resource(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a resource by ID.
        
        Args:
            resource_id: Resource ID
            
        Returns:
            Dictionary containing resource information, or None if not found
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM resources WHERE resource_id = %s AND provider = 'aws'",
                    (resource_id,)
                )
                resource = cursor.fetchone()
                
                if not resource:
                    return None
                
                # Convert metadata from JSON string to dictionary
                resource['metadata'] = json.loads(resource['metadata']) if resource['metadata'] else {}
                
                return dict(resource)
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def get_costs(self, account_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get cost data for an account.
        
        Args:
            account_id: Account ID
            start_date: Start date in ISO format (optional, defaults to 30 days ago)
            end_date: End date in ISO format (optional, defaults to today)
            
        Returns:
            Dictionary containing cost data
        """
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.now().date().isoformat()
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).date().isoformat()
        
        # Get boto3 session for account
        try:
            session = self.account_manager.get_boto3_session(account_id)
        except Exception as e:
            self.logger.error(f"Failed to get boto3 session: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to get boto3 session: {str(e)}"
            }
        
        # Get cost data
        try:
            ce_client = session.client('ce')
            
            # Get cost and usage data
            response = ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {
                        'Type': 'DIMENSION',
                        'Key': 'SERVICE'
                    }
                ]
            )
            
            # Process response
            cost_data = {
                'start_date': start_date,
                'end_date': end_date,
                'daily_costs': [],
                'service_costs': {}
            }
            
            for result in response.get('ResultsByTime', []):
                date = result.get('TimePeriod', {}).get('Start', '')
                daily_cost = 0
                
                for group in result.get('Groups', []):
                    service = group.get('Keys', [''])[0]
                    amount = float(group.get('Metrics', {}).get('UnblendedCost', {}).get('Amount', 0))
                    currency = group.get('Metrics', {}).get('UnblendedCost', {}).get('Unit', 'USD')
                    
                    daily_cost += amount
                    
                    if service not in cost_data['service_costs']:
                        cost_data['service_costs'][service] = {
                            'amount': 0,
                            'currency': currency
                        }
                    
                    cost_data['service_costs'][service]['amount'] += amount
                
                cost_data['daily_costs'].append({
                    'date': date,
                    'amount': daily_cost,
                    'currency': 'USD'
                })
            
            # Store cost data in database
            conn = self._get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE accounts SET cost_data = %s, updated_at = NOW() WHERE id = %s",
                        (json.dumps(cost_data), account_id)
                    )
                    conn.commit()
            except Exception as e:
                conn.rollback()
                self.logger.error(f"Database error: {str(e)}")
            finally:
                conn.close()
            
            return {
                'success': True,
                'data': cost_data
            }
        except Exception as e:
            self.logger.error(f"Error getting cost data: {str(e)}")
            return {
                'success': False,
                'error': f"Error getting cost data: {str(e)}"
            }
    
    def get_recommendations(self, account_id: int) -> Dict[str, Any]:
        """
        Get optimization recommendations for an account.
        
        Args:
            account_id: Account ID
            
        Returns:
            Dictionary containing recommendations
        """
        # Get boto3 session for account
        try:
            session = self.account_manager.get_boto3_session(account_id)
        except Exception as e:
            self.logger.error(f"Failed to get boto3 session: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to get boto3 session: {str(e)}"
            }
        
        # Get recommendations
        try:
            recommendations = []
            
            # Get EC2 recommendations
            ec2_recommendations = self._get_ec2_recommendations(session)
            recommendations.extend(ec2_recommendations)
            
            # Get RDS recommendations
            rds_recommendations = self._get_rds_recommendations(session)
            recommendations.extend(rds_recommendations)
            
            return {
                'success': True,
                'recommendations': recommendations
            }
        except Exception as e:
            self.logger.error(f"Error getting recommendations: {str(e)}")
            return {
                'success': False,
                'error': f"Error getting recommendations: {str(e)}"
            }
    
    def _get_ec2_recommendations(self, session: boto3.Session) -> List[Dict[str, Any]]:
        """
        Get EC2 optimization recommendations.
        
        Args:
            session: boto3 Session
            
        Returns:
            List of dictionaries containing recommendations
        """
        recommendations = []
        
        # Get EC2 recommendations from AWS Cost Explorer
        try:
            ce_client = session.client('ce')
            
            # Get rightsizing recommendations
            response = ce_client.get_rightsizing_recommendation(
                Service='EC2',
                Configuration={
                    'RecommendationTarget': 'SAME_INSTANCE_FAMILY',
                    'BenefitsConsidered': True
                }
            )
            
            for recommendation in response.get('RightsizingRecommendations', []):
                current_instance = recommendation.get('CurrentInstance', {})
                recommended_options = recommendation.get('RightsizingOptions', [])
                
                if recommended_options:
                    recommended_option = recommended_options[0]
                    
                    recommendations.append({
                        'id': f"ec2-{current_instance.get('ResourceId', '')}",
                        'resource_type': 'ec2',
                        'resource_id': current_instance.get('ResourceId', ''),
                        'resource_name': current_instance.get('ResourceDetails', {}).get('EC2ResourceDetails', {}).get('InstanceName', ''),
                        'description': f"Resize EC2 instance from {current_instance.get('InstanceType', '')} to {recommended_option.get('TargetInstances', [])[0].get('InstanceType', '')}",
                        'estimated_savings': {
                            'amount': float(recommended_option.get('EstimatedMonthlySavings', 0)),
                            'currency': recommended_option.get('CurrencyCode', 'USD')
                        }
                    })
        except Exception as e:
            self.logger.error(f"Error getting EC2 recommendations: {str(e)}")
        
        return recommendations
    
    def _get_rds_recommendations(self, session: boto3.Session) -> List[Dict[str, Any]]:
        """
        Get RDS optimization recommendations.
        
        Args:
            session: boto3 Session
            
        Returns:
            List of dictionaries containing recommendations
        """
        recommendations = []
        
        # Get RDS recommendations
        try:
            rds_client = session.client('rds')
            
            # Get RDS instances
            response = rds_client.describe_db_instances()
            
            for instance in response.get('DBInstances', []):
                # Check for multi-AZ instances with low utilization
                if instance.get('MultiAZ', False):
                    recommendations.append({
                        'id': f"rds-{instance.get('DBInstanceIdentifier', '')}",
                        'resource_type': 'rds',
                        'resource_id': instance.get('DBInstanceIdentifier', ''),
                        'resource_name': instance.get('DBInstanceIdentifier', ''),
                        'description': f"Consider disabling Multi-AZ for RDS instance {instance.get('DBInstanceIdentifier', '')} if high availability is not required",
                        'estimated_savings': {
                            'amount': float(instance.get('DBInstanceClass', '').split('.')[1]) * 30,  # Rough estimate
                            'currency': 'USD'
                        }
                    })
        except Exception as e:
            self.logger.error(f"Error getting RDS recommendations: {str(e)}")
        
        return recommendations
