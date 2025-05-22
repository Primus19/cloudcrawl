"""
Terraform integration service for Cloud Cost Optimizer.
This module provides functionality to manage Terraform templates and deployments.
"""

import os
import json
import uuid
import subprocess
import tempfile
import shutil
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TerraformManager:
    """
    Manages Terraform templates and deployments for infrastructure provisioning and cost optimization.
    """
    
    def __init__(self, templates_dir: str, state_dir: str):
        """
        Initialize the Terraform Manager.
        
        Args:
            templates_dir: Directory to store Terraform templates
            state_dir: Directory to store Terraform state files
        """
        self.templates_dir = templates_dir
        self.state_dir = state_dir
        
        # Create directories if they don't exist
        os.makedirs(templates_dir, exist_ok=True)
        os.makedirs(state_dir, exist_ok=True)
        
        # Load existing templates and deployments
        self.templates = self._load_templates()
        self.deployments = self._load_deployments()
    
    def _load_templates(self) -> Dict[str, Dict]:
        """Load existing templates from the templates directory."""
        templates = {}
        
        if os.path.exists(os.path.join(self.templates_dir, 'templates.json')):
            try:
                with open(os.path.join(self.templates_dir, 'templates.json'), 'r') as f:
                    templates = json.load(f)
            except Exception as e:
                logger.error(f"Error loading templates: {e}")
        
        return templates
    
    def _save_templates(self):
        """Save templates to the templates directory."""
        try:
            with open(os.path.join(self.templates_dir, 'templates.json'), 'w') as f:
                json.dump(self.templates, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving templates: {e}")
    
    def _load_deployments(self) -> Dict[str, Dict]:
        """Load existing deployments from the state directory."""
        deployments = {}
        
        if os.path.exists(os.path.join(self.state_dir, 'deployments.json')):
            try:
                with open(os.path.join(self.state_dir, 'deployments.json'), 'r') as f:
                    deployments = json.load(f)
            except Exception as e:
                logger.error(f"Error loading deployments: {e}")
        
        return deployments
    
    def _save_deployments(self):
        """Save deployments to the state directory."""
        try:
            with open(os.path.join(self.state_dir, 'deployments.json'), 'w') as f:
                json.dump(self.deployments, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving deployments: {e}")
    
    def get_templates(self) -> List[Dict]:
        """
        Get all available Terraform templates.
        
        Returns:
            List of template objects
        """
        return list(self.templates.values())
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """
        Get a specific Terraform template by ID.
        
        Args:
            template_id: ID of the template to retrieve
            
        Returns:
            Template object or None if not found
        """
        return self.templates.get(template_id)
    
    def create_template(self, name: str, description: str, variables: Dict, content: str) -> Dict:
        """
        Create a new Terraform template.
        
        Args:
            name: Name of the template
            description: Description of the template
            variables: Dictionary of variables with their descriptions, types, defaults, and required status
            content: Terraform configuration content
            
        Returns:
            Newly created template object
        """
        template_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        template = {
            'id': template_id,
            'name': name,
            'description': description,
            'variables': variables,
            'content': content,
            'createdAt': now,
            'updatedAt': now
        }
        
        # Save template content to file
        template_dir = os.path.join(self.templates_dir, template_id)
        os.makedirs(template_dir, exist_ok=True)
        
        with open(os.path.join(template_dir, 'main.tf'), 'w') as f:
            f.write(content)
        
        # Add to templates dictionary
        self.templates[template_id] = template
        self._save_templates()
        
        return template
    
    def update_template(self, template_id: str, updates: Dict) -> Optional[Dict]:
        """
        Update an existing Terraform template.
        
        Args:
            template_id: ID of the template to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated template object or None if not found
        """
        if template_id not in self.templates:
            return None
        
        template = self.templates[template_id]
        
        # Update fields
        for key, value in updates.items():
            if key in ['name', 'description', 'variables', 'content']:
                template[key] = value
        
        template['updatedAt'] = datetime.utcnow().isoformat()
        
        # Update template content file if needed
        if 'content' in updates:
            template_dir = os.path.join(self.templates_dir, template_id)
            os.makedirs(template_dir, exist_ok=True)
            
            with open(os.path.join(template_dir, 'main.tf'), 'w') as f:
                f.write(updates['content'])
        
        self._save_templates()
        
        return template
    
    def delete_template(self, template_id: str) -> bool:
        """
        Delete a Terraform template.
        
        Args:
            template_id: ID of the template to delete
            
        Returns:
            True if successful, False otherwise
        """
        if template_id not in self.templates:
            return False
        
        # Remove template from dictionary
        del self.templates[template_id]
        self._save_templates()
        
        # Remove template directory
        template_dir = os.path.join(self.templates_dir, template_id)
        if os.path.exists(template_dir):
            shutil.rmtree(template_dir)
        
        return True
    
    def get_deployments(self) -> List[Dict]:
        """
        Get all Terraform deployments.
        
        Returns:
            List of deployment objects
        """
        return list(self.deployments.values())
    
    def get_deployment(self, deployment_id: str) -> Optional[Dict]:
        """
        Get a specific Terraform deployment by ID.
        
        Args:
            deployment_id: ID of the deployment to retrieve
            
        Returns:
            Deployment object or None if not found
        """
        return self.deployments.get(deployment_id)
    
    def deploy_template(self, template_id: str, variables: Dict) -> Optional[Dict]:
        """
        Deploy a Terraform template with the provided variables.
        
        Args:
            template_id: ID of the template to deploy
            variables: Dictionary of variable values for the deployment
            
        Returns:
            Deployment object or None if template not found
        """
        template = self.get_template(template_id)
        if not template:
            return None
        
        deployment_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        deployment = {
            'id': deployment_id,
            'templateId': template_id,
            'status': 'planning',
            'variables': variables,
            'logs': '',
            'createdAt': now
        }
        
        # Add to deployments dictionary
        self.deployments[deployment_id] = deployment
        self._save_deployments()
        
        # Start deployment in a separate thread
        import threading
        thread = threading.Thread(target=self._execute_deployment, args=(deployment_id,))
        thread.daemon = True
        thread.start()
        
        return deployment
    
    def _execute_deployment(self, deployment_id: str):
        """
        Execute a Terraform deployment in a separate process.
        
        Args:
            deployment_id: ID of the deployment to execute
        """
        deployment = self.deployments[deployment_id]
        template_id = deployment['templateId']
        template = self.templates[template_id]
        variables = deployment['variables']
        
        # Create deployment directory
        deployment_dir = os.path.join(self.state_dir, deployment_id)
        os.makedirs(deployment_dir, exist_ok=True)
        
        # Copy template content to deployment directory
        with open(os.path.join(deployment_dir, 'main.tf'), 'w') as f:
            f.write(template['content'])
        
        # Create variables file
        with open(os.path.join(deployment_dir, 'terraform.tfvars.json'), 'w') as f:
            json.dump(variables, f, indent=2)
        
        # Initialize Terraform
        logs = "Terraform initialization started...\n"
        self._update_deployment_logs(deployment_id, logs)
        
        try:
            result = subprocess.run(
                ['terraform', 'init'],
                cwd=deployment_dir,
                capture_output=True,
                text=True,
                check=True
            )
            logs += result.stdout + "\n"
            self._update_deployment_logs(deployment_id, logs)
            
            # Plan
            logs += "Planning Terraform changes...\n"
            self._update_deployment_logs(deployment_id, logs)
            self._update_deployment_status(deployment_id, 'planning')
            
            result = subprocess.run(
                ['terraform', 'plan', '-var-file=terraform.tfvars.json', '-out=tfplan'],
                cwd=deployment_dir,
                capture_output=True,
                text=True,
                check=True
            )
            logs += result.stdout + "\n"
            self._update_deployment_logs(deployment_id, logs)
            
            # Apply
            logs += "Applying Terraform changes...\n"
            self._update_deployment_logs(deployment_id, logs)
            self._update_deployment_status(deployment_id, 'applying')
            
            result = subprocess.run(
                ['terraform', 'apply', '-auto-approve', 'tfplan'],
                cwd=deployment_dir,
                capture_output=True,
                text=True,
                check=True
            )
            logs += result.stdout + "\n"
            
            # Get outputs
            output_result = subprocess.run(
                ['terraform', 'output', '-json'],
                cwd=deployment_dir,
                capture_output=True,
                text=True
            )
            
            if output_result.returncode == 0:
                try:
                    outputs = json.loads(output_result.stdout)
                    # Convert complex output structure to simple key-value pairs
                    simplified_outputs = {}
                    for key, value in outputs.items():
                        simplified_outputs[key] = value.get('value')
                    
                    self._update_deployment_output(deployment_id, simplified_outputs)
                except json.JSONDecodeError:
                    logs += "Warning: Could not parse Terraform outputs\n"
            
            logs += "Deployment completed successfully!\n"
            self._update_deployment_logs(deployment_id, logs)
            self._update_deployment_status(deployment_id, 'completed')
            self._update_deployment_completed_at(deployment_id)
            
        except subprocess.CalledProcessError as e:
            logs += f"Error: {e.stderr}\n"
            self._update_deployment_logs(deployment_id, logs)
            self._update_deployment_status(deployment_id, 'failed')
            self._update_deployment_completed_at(deployment_id)
    
    def _update_deployment_logs(self, deployment_id: str, logs: str):
        """Update the logs for a deployment."""
        if deployment_id in self.deployments:
            self.deployments[deployment_id]['logs'] = logs
            self._save_deployments()
    
    def _update_deployment_status(self, deployment_id: str, status: str):
        """Update the status for a deployment."""
        if deployment_id in self.deployments:
            self.deployments[deployment_id]['status'] = status
            self._save_deployments()
    
    def _update_deployment_output(self, deployment_id: str, output: Dict):
        """Update the output for a deployment."""
        if deployment_id in self.deployments:
            self.deployments[deployment_id]['output'] = output
            self._save_deployments()
    
    def _update_deployment_completed_at(self, deployment_id: str):
        """Update the completedAt timestamp for a deployment."""
        if deployment_id in self.deployments:
            self.deployments[deployment_id]['completedAt'] = datetime.utcnow().isoformat()
            self._save_deployments()


# Example usage
if __name__ == "__main__":
    # Create a Terraform manager instance
    manager = TerraformManager(
        templates_dir='./terraform/templates',
        state_dir='./terraform/state'
    )
    
    # Create a simple template
    template = manager.create_template(
        name="AWS S3 Bucket",
        description="Creates an S3 bucket with lifecycle policy for cost optimization",
        variables={
            "bucket_name": {
                "description": "The name of the S3 bucket",
                "type": "string",
                "required": True
            },
            "transition_days": {
                "description": "Days after which to transition objects to Glacier",
                "type": "number",
                "default": 90,
                "required": False
            }
        },
        content="""
provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "example" {
  bucket = var.bucket_name
  
  lifecycle_rule {
    id      = "archive"
    enabled = true
    
    transition {
      days          = var.transition_days
      storage_class = "GLACIER"
    }
  }
}

variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "transition_days" {
  description = "Days after which to transition objects to Glacier"
  type        = number
  default     = 90
}

output "bucket_id" {
  value = aws_s3_bucket.example.id
}
"""
    )
    
    print(f"Created template: {template['id']}")
    
    # List all templates
    templates = manager.get_templates()
    print(f"Templates: {len(templates)}")
    
    # Deploy the template (this would normally be done through the API)
    # deployment = manager.deploy_template(
    #     template_id=template['id'],
    #     variables={
    #         "bucket_name": "my-cost-optimizer-bucket",
    #         "transition_days": 30
    #     }
    # )
    # 
    # print(f"Created deployment: {deployment['id']}")
