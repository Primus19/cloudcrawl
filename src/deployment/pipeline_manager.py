"""
Deployment pipeline manager for Cloud Cost Optimizer.
This module provides functionality for managing CI/CD pipelines and deployments.
"""

import os
import json
import logging
import uuid
import yaml
import tempfile
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime

class DeploymentPipelineManager:
    """Manager for deployment pipelines."""
    
    def __init__(self):
        """Initialize the deployment pipeline manager."""
        self.logger = logging.getLogger(__name__)
        
        # Base directory for pipeline configurations
        self.pipelines_dir = os.path.join(os.path.dirname(__file__), 'pipelines')
        os.makedirs(self.pipelines_dir, exist_ok=True)
        
        # In-memory storage for deployments
        self.deployments = {}
        
        # Initialize with sample pipeline configurations
        self._initialize_sample_pipelines()
    
    def get_pipelines(self) -> List[Dict[str, Any]]:
        """
        Get all pipeline configurations.
        
        Returns:
            List of pipeline configurations
        """
        pipelines = []
        
        # Get all YAML files in the pipelines directory
        for filename in os.listdir(self.pipelines_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                file_path = os.path.join(self.pipelines_dir, filename)
                
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Parse YAML
                    pipeline = yaml.safe_load(content)
                    
                    # Add metadata
                    pipelines.append({
                        'name': os.path.splitext(filename)[0],
                        'filename': filename,
                        'path': file_path,
                        'type': pipeline.get('type', 'Unknown'),
                        'provider': pipeline.get('provider', 'Unknown'),
                        'content': content
                    })
                except Exception as e:
                    self.logger.error(f"Error parsing pipeline {filename}: {str(e)}")
        
        return pipelines
    
    def get_pipeline(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific pipeline configuration by name.
        
        Args:
            name: Pipeline name
            
        Returns:
            Pipeline configuration or None if not found
        """
        # Get all pipelines
        pipelines = self.get_pipelines()
        
        # Find pipeline by name
        for pipeline in pipelines:
            if pipeline['name'] == name:
                return pipeline
        
        return None
    
    def create_pipeline(self, name: str, content: str) -> bool:
        """
        Create a new pipeline configuration.
        
        Args:
            name: Pipeline name
            content: YAML content
            
        Returns:
            True if pipeline was created, False otherwise
        """
        try:
            # Validate YAML
            pipeline = yaml.safe_load(content)
            if not pipeline:
                raise ValueError("Invalid YAML content")
            
            # Create file
            filename = f"{name}.yaml"
            file_path = os.path.join(self.pipelines_dir, filename)
            
            # Check if file already exists
            if os.path.exists(file_path):
                raise ValueError(f"Pipeline {name} already exists")
            
            # Write file
            with open(file_path, 'w') as f:
                f.write(content)
            
            return True
        except Exception as e:
            self.logger.error(f"Error creating pipeline {name}: {str(e)}")
            return False
    
    def update_pipeline(self, name: str, content: str) -> bool:
        """
        Update a pipeline configuration.
        
        Args:
            name: Pipeline name
            content: New YAML content
            
        Returns:
            True if pipeline was updated, False otherwise
        """
        try:
            # Validate YAML
            pipeline = yaml.safe_load(content)
            if not pipeline:
                raise ValueError("Invalid YAML content")
            
            # Get file path
            filename = f"{name}.yaml"
            file_path = os.path.join(self.pipelines_dir, filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                raise ValueError(f"Pipeline {name} not found")
            
            # Write file
            with open(file_path, 'w') as f:
                f.write(content)
            
            return True
        except Exception as e:
            self.logger.error(f"Error updating pipeline {name}: {str(e)}")
            return False
    
    def delete_pipeline(self, name: str) -> bool:
        """
        Delete a pipeline configuration.
        
        Args:
            name: Pipeline name
            
        Returns:
            True if pipeline was deleted, False otherwise
        """
        try:
            # Get file path
            filename = f"{name}.yaml"
            file_path = os.path.join(self.pipelines_dir, filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                raise ValueError(f"Pipeline {name} not found")
            
            # Delete file
            os.remove(file_path)
            
            return True
        except Exception as e:
            self.logger.error(f"Error deleting pipeline {name}: {str(e)}")
            return False
    
    def validate_pipeline(self, content: str) -> Dict[str, Any]:
        """
        Validate a pipeline configuration.
        
        Args:
            content: YAML content
            
        Returns:
            Validation result
        """
        try:
            # Validate YAML
            pipeline = yaml.safe_load(content)
            if not pipeline:
                return {
                    'valid': False,
                    'errors': ['Invalid YAML content']
                }
            
            # Check required fields
            required_fields = ['type', 'provider', 'stages']
            missing_fields = [field for field in required_fields if field not in pipeline]
            
            if missing_fields:
                return {
                    'valid': False,
                    'errors': [f"Missing required field: {field}" for field in missing_fields]
                }
            
            # Check stages
            if not isinstance(pipeline['stages'], list) or not pipeline['stages']:
                return {
                    'valid': False,
                    'errors': ['Stages must be a non-empty list']
                }
            
            # In a real implementation, this would perform more detailed validation
            # For demonstration, we'll just check the basic structure
            
            return {
                'valid': True,
                'errors': []
            }
        except Exception as e:
            return {
                'valid': False,
                'errors': [str(e)]
            }
    
    def get_deployments(self) -> List[Dict[str, Any]]:
        """
        Get all deployments.
        
        Returns:
            List of deployments
        """
        return list(self.deployments.values())
    
    def get_deployment(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific deployment by ID.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Deployment or None if not found
        """
        return self.deployments.get(deployment_id)
    
    def create_deployment(self, pipeline_name: str, environment: str, version: str) -> str:
        """
        Create a new deployment.
        
        Args:
            pipeline_name: Pipeline name
            environment: Deployment environment (e.g., dev, staging, prod)
            version: Version to deploy
            
        Returns:
            Deployment ID
        """
        # Check if pipeline exists
        pipeline = self.get_pipeline(pipeline_name)
        if not pipeline:
            raise ValueError(f"Pipeline {pipeline_name} not found")
        
        # Generate deployment ID
        deployment_id = str(uuid.uuid4())
        
        # Create deployment
        deployment = {
            'id': deployment_id,
            'pipeline_name': pipeline_name,
            'environment': environment,
            'version': version,
            'status': 'created',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'stages': [],
            'current_stage': None,
            'logs': []
        }
        
        # Parse pipeline stages
        pipeline_config = yaml.safe_load(pipeline['content'])
        stages = pipeline_config.get('stages', [])
        
        # Initialize stages
        for i, stage in enumerate(stages):
            deployment['stages'].append({
                'name': stage.get('name', f"Stage {i+1}"),
                'status': 'pending',
                'started_at': None,
                'completed_at': None
            })
        
        # Set current stage
        if deployment['stages']:
            deployment['current_stage'] = deployment['stages'][0]['name']
            deployment['stages'][0]['status'] = 'running'
            deployment['stages'][0]['started_at'] = datetime.now().isoformat()
        
        # Store deployment
        self.deployments[deployment_id] = deployment
        
        return deployment_id
    
    def update_deployment_status(self, deployment_id: str, status: str) -> bool:
        """
        Update a deployment status.
        
        Args:
            deployment_id: Deployment ID
            status: New status
            
        Returns:
            True if deployment was updated, False otherwise
        """
        # Get deployment
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            return False
        
        # Update status
        deployment['status'] = status
        deployment['updated_at'] = datetime.now().isoformat()
        
        return True
    
    def advance_deployment_stage(self, deployment_id: str) -> bool:
        """
        Advance a deployment to the next stage.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            True if deployment was advanced, False otherwise
        """
        # Get deployment
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            return False
        
        # Find current stage
        current_stage_name = deployment.get('current_stage')
        if not current_stage_name:
            return False
        
        current_stage_index = None
        for i, stage in enumerate(deployment['stages']):
            if stage['name'] == current_stage_name:
                current_stage_index = i
                break
        
        if current_stage_index is None:
            return False
        
        # Complete current stage
        deployment['stages'][current_stage_index]['status'] = 'completed'
        deployment['stages'][current_stage_index]['completed_at'] = datetime.now().isoformat()
        
        # Advance to next stage
        next_stage_index = current_stage_index + 1
        if next_stage_index < len(deployment['stages']):
            deployment['current_stage'] = deployment['stages'][next_stage_index]['name']
            deployment['stages'][next_stage_index]['status'] = 'running'
            deployment['stages'][next_stage_index]['started_at'] = datetime.now().isoformat()
        else:
            # All stages completed
            deployment['current_stage'] = None
            deployment['status'] = 'completed'
        
        deployment['updated_at'] = datetime.now().isoformat()
        
        return True
    
    def add_deployment_log(self, deployment_id: str, message: str) -> bool:
        """
        Add a log message to a deployment.
        
        Args:
            deployment_id: Deployment ID
            message: Log message
            
        Returns:
            True if log was added, False otherwise
        """
        # Get deployment
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            return False
        
        # Add log
        deployment['logs'].append({
            'timestamp': datetime.now().isoformat(),
            'message': message
        })
        
        return True
    
    def _initialize_sample_pipelines(self):
        """Initialize with sample pipeline configurations."""
        # GitHub Actions CI/CD Pipeline
        github_actions_pipeline = """
type: github_actions
provider: github
name: CloudCrawl CI/CD Pipeline
description: GitHub Actions workflow for building, testing, and deploying CloudCrawl

stages:
  - name: build
    description: Build the application
    steps:
      - name: Checkout code
        action: actions/checkout@v2
      - name: Set up Node.js
        action: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install dependencies
        run: |
          npm ci
      - name: Build
        run: |
          npm run build

  - name: test
    description: Run tests
    steps:
      - name: Run unit tests
        run: |
          npm test
      - name: Run integration tests
        run: |
          npm run test:integration

  - name: deploy
    description: Deploy to environment
    steps:
      - name: Set up kubectl
        action: azure/setup-kubectl@v1
      - name: Set up Helm
        action: azure/setup-helm@v1
      - name: Deploy to Kubernetes
        run: |
          helm upgrade --install cloudcrawl ./charts/cloudcrawl --namespace ${{ env.NAMESPACE }} --set image.tag=${{ env.VERSION }}
"""
        
        # GitLab CI/CD Pipeline
        gitlab_pipeline = """
type: gitlab_ci
provider: gitlab
name: CloudCrawl GitLab CI/CD Pipeline
description: GitLab CI/CD pipeline for building, testing, and deploying CloudCrawl

stages:
  - name: build
    description: Build the application
    script:
      - npm ci
      - npm run build
    artifacts:
      paths:
        - dist/

  - name: test
    description: Run tests
    script:
      - npm test
      - npm run test:integration
    dependencies:
      - build

  - name: deploy
    description: Deploy to environment
    script:
      - helm upgrade --install cloudcrawl ./charts/cloudcrawl --namespace $NAMESPACE --set image.tag=$VERSION
    dependencies:
      - build
      - test
    only:
      - main
"""
        
        # Jenkins Pipeline
        jenkins_pipeline = """
type: jenkins
provider: jenkins
name: CloudCrawl Jenkins Pipeline
description: Jenkins pipeline for building, testing, and deploying CloudCrawl

stages:
  - name: checkout
    description: Checkout code
    steps:
      - checkout scm

  - name: build
    description: Build the application
    steps:
      - sh 'npm ci'
      - sh 'npm run build'

  - name: test
    description: Run tests
    steps:
      - sh 'npm test'
      - sh 'npm run test:integration'

  - name: deploy
    description: Deploy to environment
    steps:
      - sh 'helm upgrade --install cloudcrawl ./charts/cloudcrawl --namespace ${NAMESPACE} --set image.tag=${VERSION}'
"""
        
        # Create pipeline files
        self.create_pipeline('github-actions', github_actions_pipeline)
        self.create_pipeline('gitlab-ci', gitlab_pipeline)
        self.create_pipeline('jenkins', jenkins_pipeline)
