"""
AWS provider implementation for cloud cost optimizer.
"""
import boto3
import datetime
from typing import Dict, List, Any, Optional
from uuid import UUID

from src.providers.base import CloudProviderInterface


class AWSProvider(CloudProviderInterface):
    """AWS provider implementation."""
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ec2_client = None
        self.rds_client = None
        self.s3_client = None
        self.ce_client = None  # Cost Explorer
        self.cloudwatch_client = None
        self.authenticated = False
    
    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with AWS."""
        try:
            # Check authentication method
            if 'role_arn' in credentials:
                # Use role-based authentication
                sts_client = boto3.client(
                    'sts',
                    region_name=self.region,
                    aws_access_key_id=credentials.get('access_key_id'),
                    aws_secret_access_key=credentials.get('secret_access_key')
                )
                
                assumed_role = sts_client.assume_role(
                    RoleArn=credentials['role_arn'],
                    RoleSessionName="CloudCostOptimizerSession"
                )
                
                session = boto3.Session(
                    aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
                    aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
                    aws_session_token=assumed_role['Credentials']['SessionToken'],
                    region_name=self.region
                )
            else:
                # Use direct credentials
                session = boto3.Session(
                    aws_access_key_id=credentials.get('access_key_id'),
                    aws_secret_access_key=credentials.get('secret_access_key'),
                    region_name=self.region
                )
            
            # Initialize clients
            self.ec2_client = session.client('ec2')
            self.rds_client = session.client('rds')
            self.s3_client = session.client('s3')
            self.ce_client = session.client('ce')
            self.cloudwatch_client = session.client('cloudwatch')
            
            # Test authentication
            self.ec2_client.describe_regions()
            
            self.authenticated = True
            return True
        except Exception as e:
            print(f"AWS authentication error: {str(e)}")
            self.authenticated = False
            return False
    
    def get_resources(self, resource_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get resources from AWS."""
        if not self.authenticated:
            raise Exception("Not authenticated with AWS")
        
        resources = []
        
        if resource_type is None or resource_type == 'ec2_instance':
            # Get EC2 instances
            response = self.ec2_client.describe_instances()
            for reservation in response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    resources.append({
                        'id': instance['InstanceId'],
                        'type': 'ec2_instance',
                        'name': self._get_name_from_tags(instance.get('Tags', [])),
                        'region': self.region,
                        'status': instance['State']['Name'],
                        'created_at': instance.get('LaunchTime', '').isoformat() if isinstance(instance.get('LaunchTime'), datetime.datetime) else None,
                        'properties': {
                            'instance_type': instance.get('InstanceType'),
                            'availability_zone': instance.get('Placement', {}).get('AvailabilityZone'),
                            'private_ip': instance.get('PrivateIpAddress'),
                            'public_ip': instance.get('PublicIpAddress'),
                            'vpc_id': instance.get('VpcId'),
                            'subnet_id': instance.get('SubnetId'),
                            'security_groups': [sg['GroupId'] for sg in instance.get('SecurityGroups', [])]
                        },
                        'tags': self._convert_aws_tags(instance.get('Tags', []))
                    })
        
        if resource_type is None or resource_type == 'rds_instance':
            # Get RDS instances
            response = self.rds_client.describe_db_instances()
            for db_instance in response.get('DBInstances', []):
                resources.append({
                    'id': db_instance['DBInstanceIdentifier'],
                    'type': 'rds_instance',
                    'name': db_instance['DBInstanceIdentifier'],
                    'region': self.region,
                    'status': db_instance['DBInstanceStatus'],
                    'created_at': db_instance.get('InstanceCreateTime', '').isoformat() if isinstance(db_instance.get('InstanceCreateTime'), datetime.datetime) else None,
                    'properties': {
                        'engine': db_instance.get('Engine'),
                        'engine_version': db_instance.get('EngineVersion'),
                        'instance_class': db_instance.get('DBInstanceClass'),
                        'allocated_storage': db_instance.get('AllocatedStorage'),
                        'multi_az': db_instance.get('MultiAZ'),
                        'endpoint': db_instance.get('Endpoint', {}).get('Address'),
                        'port': db_instance.get('Endpoint', {}).get('Port'),
                        'vpc_id': db_instance.get('DBSubnetGroup', {}).get('VpcId')
                    },
                    'tags': self._get_rds_tags(db_instance['DBInstanceIdentifier'])
                })
        
        if resource_type is None or resource_type == 's3_bucket':
            # Get S3 buckets
            response = self.s3_client.list_buckets()
            for bucket in response.get('Buckets', []):
                # Get bucket location
                try:
                    location = self.s3_client.get_bucket_location(Bucket=bucket['Name'])
                    region = location.get('LocationConstraint') or 'us-east-1'
                except:
                    region = 'unknown'
                
                resources.append({
                    'id': bucket['Name'],
                    'type': 's3_bucket',
                    'name': bucket['Name'],
                    'region': region,
                    'status': 'available',
                    'created_at': bucket.get('CreationDate', '').isoformat() if isinstance(bucket.get('CreationDate'), datetime.datetime) else None,
                    'properties': {
                        'region': region
                    },
                    'tags': self._get_s3_tags(bucket['Name'])
                })
        
        return resources
    
    def get_resource(self, resource_id: str, resource_type: str) -> Dict[str, Any]:
        """Get a specific resource from AWS."""
        if not self.authenticated:
            raise Exception("Not authenticated with AWS")
        
        if resource_type == 'ec2_instance':
            response = self.ec2_client.describe_instances(InstanceIds=[resource_id])
            for reservation in response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    return {
                        'id': instance['InstanceId'],
                        'type': 'ec2_instance',
                        'name': self._get_name_from_tags(instance.get('Tags', [])),
                        'region': self.region,
                        'status': instance['State']['Name'],
                        'created_at': instance.get('LaunchTime', '').isoformat() if isinstance(instance.get('LaunchTime'), datetime.datetime) else None,
                        'properties': {
                            'instance_type': instance.get('InstanceType'),
                            'availability_zone': instance.get('Placement', {}).get('AvailabilityZone'),
                            'private_ip': instance.get('PrivateIpAddress'),
                            'public_ip': instance.get('PublicIpAddress'),
                            'vpc_id': instance.get('VpcId'),
                            'subnet_id': instance.get('SubnetId'),
                            'security_groups': [sg['GroupId'] for sg in instance.get('SecurityGroups', [])]
                        },
                        'tags': self._convert_aws_tags(instance.get('Tags', []))
                    }
            raise Exception(f"EC2 instance {resource_id} not found")
        
        elif resource_type == 'rds_instance':
            response = self.rds_client.describe_db_instances(DBInstanceIdentifier=resource_id)
            for db_instance in response.get('DBInstances', []):
                return {
                    'id': db_instance['DBInstanceIdentifier'],
                    'type': 'rds_instance',
                    'name': db_instance['DBInstanceIdentifier'],
                    'region': self.region,
                    'status': db_instance['DBInstanceStatus'],
                    'created_at': db_instance.get('InstanceCreateTime', '').isoformat() if isinstance(db_instance.get('InstanceCreateTime'), datetime.datetime) else None,
                    'properties': {
                        'engine': db_instance.get('Engine'),
                        'engine_version': db_instance.get('EngineVersion'),
                        'instance_class': db_instance.get('DBInstanceClass'),
                        'allocated_storage': db_instance.get('AllocatedStorage'),
                        'multi_az': db_instance.get('MultiAZ'),
                        'endpoint': db_instance.get('Endpoint', {}).get('Address'),
                        'port': db_instance.get('Endpoint', {}).get('Port'),
                        'vpc_id': db_instance.get('DBSubnetGroup', {}).get('VpcId')
                    },
                    'tags': self._get_rds_tags(db_instance['DBInstanceIdentifier'])
                }
            raise Exception(f"RDS instance {resource_id} not found")
        
        elif resource_type == 's3_bucket':
            # Check if bucket exists
            self.s3_client.head_bucket(Bucket=resource_id)
            
            # Get bucket location
            try:
                location = self.s3_client.get_bucket_location(Bucket=resource_id)
                region = location.get('LocationConstraint') or 'us-east-1'
            except:
                region = 'unknown'
            
            # Get bucket creation date (not directly available, using workaround)
            response = self.s3_client.list_buckets()
            creation_date = None
            for bucket in response.get('Buckets', []):
                if bucket['Name'] == resource_id:
                    creation_date = bucket.get('CreationDate')
                    break
            
            return {
                'id': resource_id,
                'type': 's3_bucket',
                'name': resource_id,
                'region': region,
                'status': 'available',
                'created_at': creation_date.isoformat() if isinstance(creation_date, datetime.datetime) else None,
                'properties': {
                    'region': region
                },
                'tags': self._get_s3_tags(resource_id)
            }
        
        else:
            raise Exception(f"Unsupported resource type: {resource_type}")
    
    def get_cost_data(self, start_date: str, end_date: str, granularity: str) -> List[Dict[str, Any]]:
        """Get cost data from AWS Cost Explorer."""
        if not self.authenticated:
            raise Exception("Not authenticated with AWS")
        
        # Validate granularity
        valid_granularities = ['DAILY', 'MONTHLY']
        if granularity.upper() not in valid_granularities:
            granularity = 'DAILY'
        
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity=granularity.upper(),
            Metrics=['UnblendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )
        
        results = []
        for time_period in response.get('ResultsByTime', []):
            for group in time_period.get('Groups', []):
                service = group.get('Keys', ['Unknown'])[0]
                amount = float(group.get('Metrics', {}).get('UnblendedCost', {}).get('Amount', 0))
                currency = group.get('Metrics', {}).get('UnblendedCost', {}).get('Unit', 'USD')
                
                results.append({
                    'timestamp': time_period.get('TimePeriod', {}).get('Start'),
                    'service': service,
                    'amount': amount,
                    'currency': currency,
                    'granularity': granularity.lower()
                })
        
        return results
    
    def get_metrics(self, resource_id: str, resource_type: str, metric_names: List[str], 
                   start_time: str, end_time: str, period: int) -> Dict[str, Any]:
        """Get metrics for a specific resource."""
        if not self.authenticated:
            raise Exception("Not authenticated with AWS")
        
        metrics_data = {}
        
        # Convert string dates to datetime objects
        start_datetime = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_datetime = datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        if resource_type == 'ec2_instance':
            namespace = 'AWS/EC2'
            dimensions = [{'Name': 'InstanceId', 'Value': resource_id}]
            
            for metric_name in metric_names:
                response = self.cloudwatch_client.get_metric_statistics(
                    Namespace=namespace,
                    MetricName=metric_name,
                    Dimensions=dimensions,
                    StartTime=start_datetime,
                    EndTime=end_datetime,
                    Period=period,
                    Statistics=['Average', 'Maximum']
                )
                
                datapoints = []
                for datapoint in response.get('Datapoints', []):
                    datapoints.append({
                        'timestamp': datapoint.get('Timestamp', '').isoformat() if isinstance(datapoint.get('Timestamp'), datetime.datetime) else None,
                        'average': datapoint.get('Average'),
                        'maximum': datapoint.get('Maximum'),
                        'unit': datapoint.get('Unit')
                    })
                
                metrics_data[metric_name] = {
                    'datapoints': datapoints,
                    'label': metric_name
                }
        
        elif resource_type == 'rds_instance':
            namespace = 'AWS/RDS'
            dimensions = [{'Name': 'DBInstanceIdentifier', 'Value': resource_id}]
            
            for metric_name in metric_names:
                response = self.cloudwatch_client.get_metric_statistics(
                    Namespace=namespace,
                    MetricName=metric_name,
                    Dimensions=dimensions,
                    StartTime=start_datetime,
                    EndTime=end_datetime,
                    Period=period,
                    Statistics=['Average', 'Maximum']
                )
                
                datapoints = []
                for datapoint in response.get('Datapoints', []):
                    datapoints.append({
                        'timestamp': datapoint.get('Timestamp', '').isoformat() if isinstance(datapoint.get('Timestamp'), datetime.datetime) else None,
                        'average': datapoint.get('Average'),
                        'maximum': datapoint.get('Maximum'),
                        'unit': datapoint.get('Unit')
                    })
                
                metrics_data[metric_name] = {
                    'datapoints': datapoints,
                    'label': metric_name
                }
        
        return metrics_data
    
    def execute_action(self, action_type: str, resource_id: str, resource_type: str, 
                      parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action on a resource."""
        if not self.authenticated:
            raise Exception("Not authenticated with AWS")
        
        result = {
            'action_type': action_type,
            'resource_id': resource_id,
            'resource_type': resource_type,
            'success': False,
            'message': '',
            'details': {}
        }
        
        try:
            # EC2 Instance Actions
            if resource_type == 'ec2_instance':
                if action_type == 'start_instance':
                    response = self.ec2_client.start_instances(InstanceIds=[resource_id])
                    result['success'] = True
                    result['message'] = f"Started EC2 instance {resource_id}"
                    result['details'] = response
                
                elif action_type == 'stop_instance':
                    response = self.ec2_client.stop_instances(InstanceIds=[resource_id])
                    result['success'] = True
                    result['message'] = f"Stopped EC2 instance {resource_id}"
                    result['details'] = response
                
                elif action_type == 'terminate_instance':
                    response = self.ec2_client.terminate_instances(InstanceIds=[resource_id])
                    result['success'] = True
                    result['message'] = f"Terminated EC2 instance {resource_id}"
                    result['details'] = response
                
                elif action_type == 'resize_instance':
                    instance_type = parameters.get('instance_type')
                    if not instance_type:
                        raise ValueError("instance_type parameter is required")
                    
                    # Check if instance is running
                    response = self.ec2_client.describe_instances(InstanceIds=[resource_id])
                    instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
                    
                    # Stop instance if running
                    if instance_state == 'running':
                        self.ec2_client.stop_instances(InstanceIds=[resource_id])
                        waiter = self.ec2_client.get_waiter('instance_stopped')
                        waiter.wait(InstanceIds=[resource_id])
                    
                    # Modify instance type
                    response = self.ec2_client.modify_instance_attribute(
                        InstanceId=resource_id,
                        InstanceType={'Value': instance_type}
                    )
                    
                    # Start instance if it was running
                    if instance_state == 'running':
                        self.ec2_client.start_instances(InstanceIds=[resource_id])
                    
                    result['success'] = True
                    result['message'] = f"Resized EC2 instance {resource_id} to {instance_type}"
                    result['details'] = {'new_instance_type': instance_type}
            
            # RDS Instance Actions
            elif resource_type == 'rds_instance':
                if action_type == 'start_instance':
                    response = self.rds_client.start_db_instance(DBInstanceIdentifier=resource_id)
                    result['success'] = True
                    result['message'] = f"Started RDS instance {resource_id}"
                    result['details'] = {'status': response['DBInstance']['DBInstanceStatus']}
                
                elif action_type == 'stop_instance':
                    response = self.rds_client.stop_db_instance(DBInstanceIdentifier=resource_id)
                    result['success'] = True
                    result['message'] = f"Stopped RDS instance {resource_id}"
                    result['details'] = {'status': response['DBInstance']['DBInstanceStatus']}
                
                elif action_type == 'resize_instance':
                    instance_class = parameters.get('instance_class')
                    if not instance_class:
                        raise ValueError("instance_class parameter is required")
                    
                    apply_immediately = parameters.get('apply_immediately', False)
                    
                    response = self.rds_client.modify_db_instance(
                        DBInstanceIdentifier=resource_id,
                        DBInstanceClass=instance_class,
                        ApplyImmediately=apply_immediately
                    )
                    
                    result['success'] = True
                    result['message'] = f"Resized RDS instance {resource_id} to {instance_class}"
                    result['details'] = {
                        'new_instance_class': instance_class,
                        'apply_immediately': apply_immediately,
                        'status': response['DBInstance']['DBInstanceStatus']
                    }
            
            # S3 Bucket Actions
            elif resource_type == 's3_bucket':
                if action_type == 'delete_bucket':
                    # Check if bucket is empty
                    empty = parameters.get('force_empty', False)
                    if empty:
                        # Delete all objects
                        paginator = self.s3_client.get_paginator('list_objects_v2')
                        for page in paginator.paginate(Bucket=resource_id):
                            if 'Contents' in page:
                                objects = [{'Key': obj['Key']} for obj in page['Contents']]
                                self.s3_client.delete_objects(
                                    Bucket=resource_id,
                                    Delete={'Objects': objects}
                                )
                    
                    # Delete bucket
                    self.s3_client.delete_bucket(Bucket=resource_id)
                    result['success'] = True
                    result['message'] = f"Deleted S3 bucket {resource_id}"
                
                elif action_type == 'update_lifecycle':
                    lifecycle_config = parameters.get('lifecycle_configuration')
                    if not lifecycle_config:
                        raise ValueError("lifecycle_configuration parameter is required")
                    
                    self.s3_client.put_bucket_lifecycle_configuration(
                        Bucket=resource_id,
                        LifecycleConfiguration=lifecycle_config
                    )
                    
                    result['success'] = True
                    result['message'] = f"Updated lifecycle configuration for S3 bucket {resource_id}"
            
            else:
                result['message'] = f"Unsupported resource type: {resource_type}"
        
        except Exception as e:
            result['message'] = str(e)
        
        return result
    
    def tag_resource(self, resource_id: str, resource_type: str, tags: Dict[str, str]) -> bool:
        """Tag a resource."""
        if not self.authenticated:
            raise Exception("Not authenticated with AWS")
        
        try:
            aws_tags = [{'Key': k, 'Value': v} for k, v in tags.items()]
            
            if resource_type == 'ec2_instance':
                self.ec2_client.create_tags(
                    Resources=[resource_id],
                    Tags=aws_tags
                )
                return True
            
            elif resource_type == 'rds_instance':
                arn = f"arn:aws:rds:{self.region}:{self._get_account_id()}:db:{resource_id}"
                self.rds_client.add_tags_to_resource(
                    ResourceName=arn,
                    Tags=aws_tags
                )
                return True
            
            elif resource_type == 's3_bucket':
                self.s3_client.put_bucket_tagging(
                    Bucket=resource_id,
                    Tagging={'TagSet': aws_tags}
                )
                return True
            
            else:
                return False
        
        except Exception as e:
            print(f"Error tagging resource: {str(e)}")
            return False
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Get cost optimization recommendations from AWS."""
        if not self.authenticated:
            raise Exception("Not authenticated with AWS")
        
        recommendations = []
        
        try:
            # Get EC2 rightsizing recommendations
            response = self.ce_client.get_rightsizing_recommendation(
                Service='AmazonEC2',
                Configuration={
                    'RecommendationTarget': 'SAME_INSTANCE_FAMILY',
                    'BenefitsConsidered': True
                }
            )
            
            for rec in response.get('RightsizingRecommendations', []):
                current_instance = rec.get('CurrentInstance', {})
                recommended_options = rec.get('RightsizingOptions', [])
                
                if recommended_options:
                    option = recommended_options[0]  # Take first recommendation
                    
                    recommendations.append({
                        'id': current_instance.get('ResourceId', ''),
                        'type': 'rightsizing',
                        'resource_type': 'ec2_instance',
                        'resource_id': current_instance.get('ResourceId', ''),
                        'description': f"Rightsize EC2 instance from {current_instance.get('InstanceType')} to {option.get('TargetInstances', [{}])[0].get('InstanceType')}",
                        'estimated_savings': float(option.get('EstimatedMonthlySavings', {}).get('Value', 0)),
                        'savings_currency': option.get('EstimatedMonthlySavings', {}).get('Unit', 'USD'),
                        'savings_period': 'monthly',
                        'details': {
                            'current_instance_type': current_instance.get('InstanceType'),
                            'recommended_instance_type': option.get('TargetInstances', [{}])[0].get('InstanceType'),
                            'savings_percentage': float(option.get('SavingsPercentage', 0)),
                            'risk': option.get('RiskLevel', 'unknown')
                        }
                    })
            
            # Get reservation recommendations
            response = self.ce_client.get_reservation_purchase_recommendation(
                Service='AmazonEC2',
                TermInYears='1',
                LookbackPeriodInDays='SIXTY_DAYS',
                PaymentOption='NO_UPFRONT'
            )
            
            for rec in response.get('Recommendations', []):
                for detail in rec.get('RecommendationDetails', []):
                    recommendations.append({
                        'id': f"reservation-{detail.get('InstanceDetails', {}).get('InstanceType', '')}-{len(recommendations)}",
                        'type': 'reservation',
                        'resource_type': 'ec2_instance',
                        'resource_id': None,
                        'description': f"Purchase Reserved Instances for {detail.get('InstanceDetails', {}).get('InstanceType', '')}",
                        'estimated_savings': float(detail.get('EstimatedMonthlySavings', 0)),
                        'savings_currency': 'USD',
                        'savings_period': 'monthly',
                        'details': {
                            'instance_type': detail.get('InstanceDetails', {}).get('InstanceType', ''),
                            'recommended_quantity': detail.get('RecommendedNumberOfInstancesToPurchase', 0),
                            'upfront_cost': float(detail.get('UpfrontCost', 0)),
                            'estimated_roi': float(detail.get('EstimatedROI', 0)) * 100,
                            'break_even_months': detail.get('EstimatedBreakEvenInMonths', 0)
                        }
                    })
        
        except Exception as e:
            print(f"Error getting AWS recommendations: {str(e)}")
        
        return recommendations
    
    # Helper methods
    
    def _get_name_from_tags(self, tags: List[Dict[str, str]]) -> str:
        """Extract Name from AWS tags."""
        for tag in tags:
            if tag.get('Key') == 'Name':
                return tag.get('Value', '')
        return ''
    
    def _convert_aws_tags(self, tags: List[Dict[str, str]]) -> Dict[str, str]:
        """Convert AWS tags to dictionary."""
        return {tag.get('Key'): tag.get('Value') for tag in tags if 'Key' in tag}
    
    def _get_rds_tags(self, db_identifier: str) -> Dict[str, str]:
        """Get tags for an RDS instance."""
        try:
            arn = f"arn:aws:rds:{self.region}:{self._get_account_id()}:db:{db_identifier}"
            response = self.rds_client.list_tags_for_resource(ResourceName=arn)
            return self._convert_aws_tags(response.get('TagList', []))
        except Exception:
            return {}
    
    def _get_s3_tags(self, bucket_name: str) -> Dict[str, str]:
        """Get tags for an S3 bucket."""
        try:
            response = self.s3_client.get_bucket_tagging(Bucket=bucket_name)
            return self._convert_aws_tags(response.get('TagSet', []))
        except Exception:
            return {}
    
    def _get_account_id(self) -> str:
        """Get the AWS account ID."""
        try:
            sts_client = boto3.client('sts')
            return sts_client.get_caller_identity()['Account']
        except Exception:
            return ''
