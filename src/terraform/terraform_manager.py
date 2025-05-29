"""
Enhanced Terraform manager for Cloud Cost Optimizer.
This module provides functionality for managing Terraform templates and deployments.
"""

import os
import json
import logging
import uuid
import shutil
import subprocess
import tempfile
from typing import Dict, List, Any, Optional
from datetime import datetime

class TerraformManager:
    """Manager for Terraform templates and deployments."""
    
    def __init__(self):
        """Initialize the Terraform manager."""
        self.logger = logging.getLogger(__name__)
        
        # In-memory storage for templates and deployments
        # In a real implementation, this would use a database
        self.templates = {}
        self.deployments = {}
        
        # Initialize with some sample templates
        self._initialize_sample_templates()
    
    def get_templates(self, provider: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all templates, optionally filtered by provider and category.
        
        Args:
            provider: Optional provider filter
            category: Optional category filter
            
        Returns:
            List of templates
        """
        templates = list(self.templates.values())
        
        # Apply filters
        if provider:
            templates = [t for t in templates if t['provider'].lower() == provider.lower()]
        
        if category:
            templates = [t for t in templates if t['category'].lower() == category.lower()]
        
        return templates
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific template by ID.
        
        Args:
            template_id: Template ID
            
        Returns:
            Template or None if not found
        """
        return self.templates.get(template_id)
    
    def get_template_files(self, template_id: str) -> Optional[Dict[str, str]]:
        """
        Get the files for a specific template.
        
        Args:
            template_id: Template ID
            
        Returns:
            Dictionary mapping file paths to content, or None if template not found
        """
        template = self.templates.get(template_id)
        if not template:
            return None
        
        return template.get('files', {})
    
    def create_template(self, name: str, provider: str, category: str, description: str,
                       files: Dict[str, str], variables: List[Dict[str, Any]] = None,
                       tags: List[str] = None) -> str:
        """
        Create a new template.
        
        Args:
            name: Template name
            provider: Cloud provider (aws, gcp, azure)
            category: Template category (compute, storage, network, etc.)
            description: Template description
            files: Dictionary mapping file paths to content
            variables: Optional list of variable definitions
            tags: Optional list of tags
            
        Returns:
            Template ID
        """
        # Generate template ID
        template_id = str(uuid.uuid4())
        
        # Create template
        template = {
            'id': template_id,
            'name': name,
            'provider': provider,
            'category': category,
            'description': description,
            'files': files,
            'variables': variables or [],
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Store template
        self.templates[template_id] = template
        
        return template_id
    
    def update_template(self, template_id: str, name: Optional[str] = None,
                       provider: Optional[str] = None, category: Optional[str] = None,
                       description: Optional[str] = None, files: Optional[Dict[str, str]] = None,
                       variables: Optional[List[Dict[str, Any]]] = None,
                       tags: Optional[List[str]] = None) -> bool:
        """
        Update a template.
        
        Args:
            template_id: Template ID
            name: Optional new name
            provider: Optional new provider
            category: Optional new category
            description: Optional new description
            files: Optional new files
            variables: Optional new variables
            tags: Optional new tags
            
        Returns:
            True if template was updated, False if not found
        """
        template = self.templates.get(template_id)
        if not template:
            return False
        
        # Update fields
        if name is not None:
            template['name'] = name
        
        if provider is not None:
            template['provider'] = provider
        
        if category is not None:
            template['category'] = category
        
        if description is not None:
            template['description'] = description
        
        if files is not None:
            template['files'] = files
        
        if variables is not None:
            template['variables'] = variables
        
        if tags is not None:
            template['tags'] = tags
        
        # Update timestamp
        template['updated_at'] = datetime.now().isoformat()
        
        return True
    
    def delete_template(self, template_id: str) -> bool:
        """
        Delete a template.
        
        Args:
            template_id: Template ID
            
        Returns:
            True if template was deleted, False if not found
        """
        if template_id not in self.templates:
            return False
        
        # Delete template
        del self.templates[template_id]
        
        return True
    
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
    
    def create_deployment(self, name: str, template_id: str, variables: Dict[str, Any],
                         cloud_account_id: str, description: str = '') -> str:
        """
        Create a new deployment.
        
        Args:
            name: Deployment name
            template_id: Template ID
            variables: Variable values
            cloud_account_id: Cloud account ID
            description: Optional deployment description
            
        Returns:
            Deployment ID
        """
        # Check if template exists
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Generate deployment ID
        deployment_id = str(uuid.uuid4())
        
        # Create deployment
        deployment = {
            'id': deployment_id,
            'name': name,
            'template_id': template_id,
            'template_name': template['name'],
            'provider': template['provider'],
            'variables': variables,
            'cloud_account_id': cloud_account_id,
            'description': description,
            'status': 'created',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'last_operation': None,
            'resources': []
        }
        
        # Store deployment
        self.deployments[deployment_id] = deployment
        
        return deployment_id
    
    def plan_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """
        Generate a Terraform plan for a deployment.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Plan result
        """
        # Get deployment
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        # Get template
        template = self.templates.get(deployment['template_id'])
        if not template:
            raise ValueError(f"Template {deployment['template_id']} not found")
        
        # Update deployment status
        deployment['status'] = 'planning'
        deployment['updated_at'] = datetime.now().isoformat()
        deployment['last_operation'] = {
            'type': 'plan',
            'status': 'running',
            'started_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        # In a real implementation, this would run Terraform plan
        # For demonstration, we'll simulate a plan
        
        # Simulate plan execution
        # In a real implementation, this would create a temporary directory,
        # write the template files, and run Terraform plan
        
        # Update deployment status
        deployment['status'] = 'planned'
        deployment['updated_at'] = datetime.now().isoformat()
        deployment['last_operation'] = {
            'type': 'plan',
            'status': 'completed',
            'started_at': deployment['last_operation']['started_at'],
            'completed_at': datetime.now().isoformat(),
            'result': {
                'add': 3,
                'change': 0,
                'destroy': 0
            }
        }
        
        # Return plan result
        return {
            'deployment_id': deployment_id,
            'status': 'completed',
            'started_at': deployment['last_operation']['started_at'],
            'completed_at': deployment['last_operation']['completed_at'],
            'result': deployment['last_operation']['result']
        }
    
    def apply_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """
        Apply a Terraform deployment.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Apply result
        """
        # Get deployment
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        # Get template
        template = self.templates.get(deployment['template_id'])
        if not template:
            raise ValueError(f"Template {deployment['template_id']} not found")
        
        # Update deployment status
        deployment['status'] = 'applying'
        deployment['updated_at'] = datetime.now().isoformat()
        deployment['last_operation'] = {
            'type': 'apply',
            'status': 'running',
            'started_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        # In a real implementation, this would run Terraform apply
        # For demonstration, we'll simulate an apply
        
        # Simulate apply execution
        # In a real implementation, this would create a temporary directory,
        # write the template files, and run Terraform apply
        
        # Generate sample resources
        resources = []
        
        if template['provider'] == 'aws':
            if 'ec2' in template['name'].lower():
                resources.append({
                    'id': f"i-{uuid.uuid4().hex[:8]}",
                    'type': 'aws_instance',
                    'name': 'example',
                    'attributes': {
                        'instance_type': 't3.micro',
                        'ami': 'ami-0c55b159cbfafe1f0',
                        'region': 'us-west-2'
                    }
                })
            
            if 's3' in template['name'].lower():
                resources.append({
                    'id': f"example-bucket-{uuid.uuid4().hex[:8]}",
                    'type': 'aws_s3_bucket',
                    'name': 'example',
                    'attributes': {
                        'bucket': f"example-bucket-{uuid.uuid4().hex[:8]}",
                        'region': 'us-west-2',
                        'acl': 'private'
                    }
                })
        
        elif template['provider'] == 'gcp':
            if 'compute' in template['name'].lower():
                resources.append({
                    'id': f"projects/example/zones/us-central1-a/instances/{uuid.uuid4().hex[:8]}",
                    'type': 'google_compute_instance',
                    'name': 'example',
                    'attributes': {
                        'machine_type': 'e2-medium',
                        'zone': 'us-central1-a'
                    }
                })
            
            if 'storage' in template['name'].lower():
                resources.append({
                    'id': f"example-bucket-{uuid.uuid4().hex[:8]}",
                    'type': 'google_storage_bucket',
                    'name': 'example',
                    'attributes': {
                        'name': f"example-bucket-{uuid.uuid4().hex[:8]}",
                        'location': 'US'
                    }
                })
        
        elif template['provider'] == 'azure':
            if 'vm' in template['name'].lower():
                resources.append({
                    'id': f"/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example/providers/Microsoft.Compute/virtualMachines/{uuid.uuid4().hex[:8]}",
                    'type': 'azurerm_virtual_machine',
                    'name': 'example',
                    'attributes': {
                        'vm_size': 'Standard_DS1_v2',
                        'location': 'eastus'
                    }
                })
            
            if 'storage' in template['name'].lower():
                resources.append({
                    'id': f"/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example/providers/Microsoft.Storage/storageAccounts/{uuid.uuid4().hex[:8]}",
                    'type': 'azurerm_storage_account',
                    'name': 'example',
                    'attributes': {
                        'account_tier': 'Standard',
                        'account_replication_type': 'LRS',
                        'location': 'eastus'
                    }
                })
        
        # Update deployment status
        deployment['status'] = 'applied'
        deployment['updated_at'] = datetime.now().isoformat()
        deployment['last_operation'] = {
            'type': 'apply',
            'status': 'completed',
            'started_at': deployment['last_operation']['started_at'],
            'completed_at': datetime.now().isoformat(),
            'result': {
                'add': len(resources),
                'change': 0,
                'destroy': 0
            }
        }
        deployment['resources'] = resources
        
        # Return apply result
        return {
            'deployment_id': deployment_id,
            'status': 'completed',
            'started_at': deployment['last_operation']['started_at'],
            'completed_at': deployment['last_operation']['completed_at'],
            'result': deployment['last_operation']['result'],
            'resources': resources
        }
    
    def destroy_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """
        Destroy a Terraform deployment.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Destroy result
        """
        # Get deployment
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        # Update deployment status
        deployment['status'] = 'destroying'
        deployment['updated_at'] = datetime.now().isoformat()
        deployment['last_operation'] = {
            'type': 'destroy',
            'status': 'running',
            'started_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        # In a real implementation, this would run Terraform destroy
        # For demonstration, we'll simulate a destroy
        
        # Get number of resources
        num_resources = len(deployment.get('resources', []))
        
        # Update deployment status
        deployment['status'] = 'destroyed'
        deployment['updated_at'] = datetime.now().isoformat()
        deployment['last_operation'] = {
            'type': 'destroy',
            'status': 'completed',
            'started_at': deployment['last_operation']['started_at'],
            'completed_at': datetime.now().isoformat(),
            'result': {
                'add': 0,
                'change': 0,
                'destroy': num_resources
            }
        }
        deployment['resources'] = []
        
        # Return destroy result
        return {
            'deployment_id': deployment_id,
            'status': 'completed',
            'started_at': deployment['last_operation']['started_at'],
            'completed_at': deployment['last_operation']['completed_at'],
            'result': deployment['last_operation']['result']
        }
    
    def delete_deployment(self, deployment_id: str) -> bool:
        """
        Delete a deployment.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            True if deployment was deleted, False if not found
        """
        if deployment_id not in self.deployments:
            return False
        
        # Delete deployment
        del self.deployments[deployment_id]
        
        return True
    
    def _initialize_sample_templates(self):
        """Initialize with some sample templates."""
        # AWS EC2 Instance
        aws_ec2_template_id = str(uuid.uuid4())
        self.templates[aws_ec2_template_id] = {
            'id': aws_ec2_template_id,
            'name': 'AWS EC2 Instance',
            'provider': 'aws',
            'category': 'compute',
            'description': 'Creates an AWS EC2 instance with customizable instance type and AMI.',
            'files': {
                'main.tf': '''
provider "aws" {
  region = var.region
}

resource "aws_instance" "example" {
  ami           = var.ami
  instance_type = var.instance_type
  
  tags = {
    Name = var.name
  }
}

output "instance_id" {
  value = aws_instance.example.id
}

output "public_ip" {
  value = aws_instance.example.public_ip
}
''',
                'variables.tf': '''
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "ami" {
  description = "AMI ID"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"
}

variable "instance_type" {
  description = "Instance type"
  type        = string
  default     = "t3.micro"
}

variable "name" {
  description = "Name tag"
  type        = string
  default     = "example-instance"
}
'''
            },
            'variables': [
                {
                    'name': 'region',
                    'description': 'AWS region',
                    'type': 'string',
                    'default': 'us-west-2',
                    'required': False
                },
                {
                    'name': 'ami',
                    'description': 'AMI ID',
                    'type': 'string',
                    'default': 'ami-0c55b159cbfafe1f0',
                    'required': False
                },
                {
                    'name': 'instance_type',
                    'description': 'Instance type',
                    'type': 'string',
                    'default': 't3.micro',
                    'required': False
                },
                {
                    'name': 'name',
                    'description': 'Name tag',
                    'type': 'string',
                    'default': 'example-instance',
                    'required': False
                }
            ],
            'tags': ['aws', 'ec2', 'compute'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # AWS S3 Bucket
        aws_s3_template_id = str(uuid.uuid4())
        self.templates[aws_s3_template_id] = {
            'id': aws_s3_template_id,
            'name': 'AWS S3 Bucket',
            'provider': 'aws',
            'category': 'storage',
            'description': 'Creates an AWS S3 bucket with customizable settings.',
            'files': {
                'main.tf': '''
provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "example" {
  bucket = var.bucket_name
  acl    = var.acl
  
  versioning {
    enabled = var.versioning_enabled
  }
  
  tags = {
    Name = var.bucket_name
  }
}

output "bucket_id" {
  value = aws_s3_bucket.example.id
}

output "bucket_arn" {
  value = aws_s3_bucket.example.arn
}
''',
                'variables.tf': '''
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "bucket_name" {
  description = "S3 bucket name"
  type        = string
}

variable "acl" {
  description = "Bucket ACL"
  type        = string
  default     = "private"
}

variable "versioning_enabled" {
  description = "Enable versioning"
  type        = bool
  default     = false
}
'''
            },
            'variables': [
                {
                    'name': 'region',
                    'description': 'AWS region',
                    'type': 'string',
                    'default': 'us-west-2',
                    'required': False
                },
                {
                    'name': 'bucket_name',
                    'description': 'S3 bucket name',
                    'type': 'string',
                    'required': True
                },
                {
                    'name': 'acl',
                    'description': 'Bucket ACL',
                    'type': 'string',
                    'default': 'private',
                    'required': False
                },
                {
                    'name': 'versioning_enabled',
                    'description': 'Enable versioning',
                    'type': 'bool',
                    'default': False,
                    'required': False
                }
            ],
            'tags': ['aws', 's3', 'storage'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # GCP Compute Instance
        gcp_compute_template_id = str(uuid.uuid4())
        self.templates[gcp_compute_template_id] = {
            'id': gcp_compute_template_id,
            'name': 'GCP Compute Instance',
            'provider': 'gcp',
            'category': 'compute',
            'description': 'Creates a Google Cloud Platform Compute Engine instance.',
            'files': {
                'main.tf': '''
provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_compute_instance" "example" {
  name         = var.name
  machine_type = var.machine_type
  
  boot_disk {
    initialize_params {
      image = var.image
    }
  }
  
  network_interface {
    network = "default"
    
    access_config {
      // Ephemeral IP
    }
  }
}

output "instance_id" {
  value = google_compute_instance.example.id
}

output "instance_name" {
  value = google_compute_instance.example.name
}
''',
                'variables.tf': '''
variable "project" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "name" {
  description = "Instance name"
  type        = string
  default     = "example-instance"
}

variable "machine_type" {
  description = "Machine type"
  type        = string
  default     = "e2-medium"
}

variable "image" {
  description = "Boot disk image"
  type        = string
  default     = "debian-cloud/debian-10"
}
'''
            },
            'variables': [
                {
                    'name': 'project',
                    'description': 'GCP project ID',
                    'type': 'string',
                    'required': True
                },
                {
                    'name': 'region',
                    'description': 'GCP region',
                    'type': 'string',
                    'default': 'us-central1',
                    'required': False
                },
                {
                    'name': 'zone',
                    'description': 'GCP zone',
                    'type': 'string',
                    'default': 'us-central1-a',
                    'required': False
                },
                {
                    'name': 'name',
                    'description': 'Instance name',
                    'type': 'string',
                    'default': 'example-instance',
                    'required': False
                },
                {
                    'name': 'machine_type',
                    'description': 'Machine type',
                    'type': 'string',
                    'default': 'e2-medium',
                    'required': False
                },
                {
                    'name': 'image',
                    'description': 'Boot disk image',
                    'type': 'string',
                    'default': 'debian-cloud/debian-10',
                    'required': False
                }
            ],
            'tags': ['gcp', 'compute', 'instance'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Azure Virtual Machine
        azure_vm_template_id = str(uuid.uuid4())
        self.templates[azure_vm_template_id] = {
            'id': azure_vm_template_id,
            'name': 'Azure Virtual Machine',
            'provider': 'azure',
            'category': 'compute',
            'description': 'Creates an Azure Virtual Machine with customizable settings.',
            'files': {
                'main.tf': '''
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "example" {
  name                = "${var.name}-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_subnet" "example" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_network_interface" "example" {
  name                = "${var.name}-nic"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_virtual_machine" "example" {
  name                  = var.name
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  network_interface_ids = [azurerm_network_interface.example.id]
  vm_size               = var.vm_size

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "${var.name}-osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = var.name
    admin_username = var.admin_username
    admin_password = var.admin_password
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}

output "vm_id" {
  value = azurerm_virtual_machine.example.id
}

output "vm_name" {
  value = azurerm_virtual_machine.example.name
}
''',
                'variables.tf': '''
variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "example-resources"
}

variable "location" {
  description = "Azure location"
  type        = string
  default     = "eastus"
}

variable "name" {
  description = "VM name"
  type        = string
  default     = "example-vm"
}

variable "vm_size" {
  description = "VM size"
  type        = string
  default     = "Standard_DS1_v2"
}

variable "admin_username" {
  description = "Admin username"
  type        = string
  default     = "adminuser"
}

variable "admin_password" {
  description = "Admin password"
  type        = string
  sensitive   = true
}
'''
            },
            'variables': [
                {
                    'name': 'resource_group_name',
                    'description': 'Resource group name',
                    'type': 'string',
                    'default': 'example-resources',
                    'required': False
                },
                {
                    'name': 'location',
                    'description': 'Azure location',
                    'type': 'string',
                    'default': 'eastus',
                    'required': False
                },
                {
                    'name': 'name',
                    'description': 'VM name',
                    'type': 'string',
                    'default': 'example-vm',
                    'required': False
                },
                {
                    'name': 'vm_size',
                    'description': 'VM size',
                    'type': 'string',
                    'default': 'Standard_DS1_v2',
                    'required': False
                },
                {
                    'name': 'admin_username',
                    'description': 'Admin username',
                    'type': 'string',
                    'default': 'adminuser',
                    'required': False
                },
                {
                    'name': 'admin_password',
                    'description': 'Admin password',
                    'type': 'string',
                    'sensitive': True,
                    'required': True
                }
            ],
            'tags': ['azure', 'vm', 'compute'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
