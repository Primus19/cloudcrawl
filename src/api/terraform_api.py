"""
Terraform API endpoints for CloudCrawl application.
This module provides API endpoints for managing Terraform templates and deployments.
"""

import logging
import uuid
from datetime import datetime
from flask import Blueprint, jsonify, request, g
from src.config import ConfigManager
from src.terraform.terraform_manager import TerraformManager
from .auth import require_auth

logger = logging.getLogger(__name__)

# Create blueprint
terraform_bp = Blueprint('terraform', __name__, url_prefix='/api/v1/terraform')

# Initialize configuration
config = ConfigManager()

# Initialize Terraform manager
terraform_manager = TerraformManager()

# Mock templates for development/testing
MOCK_TEMPLATES = [
    {
        "id": "aws-vpc",
        "name": "AWS VPC with Subnets",
        "description": "Creates a VPC with public and private subnets across multiple availability zones",
        "provider": "aws",
        "category": "networking",
        "variables": [
            {
                "name": "vpc_name",
                "description": "Name of the VPC",
                "type": "string",
                "default": "main-vpc",
                "required": True
            },
            {
                "name": "cidr_block",
                "description": "CIDR block for the VPC",
                "type": "string",
                "default": "10.0.0.0/16",
                "required": True
            },
            {
                "name": "region",
                "description": "AWS region",
                "type": "string",
                "default": "us-east-1",
                "required": True
            }
        ],
        "content": """
resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
  
  tags = {
    Name = var.vpc_name
  }
}

resource "aws_subnet" "public" {
  count = 2
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr_block, 8, count.index)
  availability_zone = "${var.region}${count.index == 0 ? "a" : "b"}"
  
  tags = {
    Name = "${var.vpc_name}-public-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count = 2
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr_block, 8, count.index + 2)
  availability_zone = "${var.region}${count.index == 0 ? "a" : "b"}"
  
  tags = {
    Name = "${var.vpc_name}-private-${count.index + 1}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.vpc_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count = 2
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
""",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "aws-eks",
        "name": "AWS EKS Cluster",
        "description": "Deploys a production-ready Kubernetes cluster with worker nodes and networking",
        "provider": "aws",
        "category": "containers",
        "variables": [
            {
                "name": "cluster_name",
                "description": "Name of the EKS cluster",
                "type": "string",
                "default": "production-cluster",
                "required": True
            },
            {
                "name": "kubernetes_version",
                "description": "Kubernetes version",
                "type": "string",
                "default": "1.27",
                "required": True
            },
            {
                "name": "node_instance_type",
                "description": "EC2 instance type for worker nodes",
                "type": "string",
                "default": "t3.medium",
                "required": True
            }
        ],
        "content": """
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids = aws_subnet.private[*].id
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
  ]
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.cluster_name}-workers"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = aws_subnet.private[*].id
  instance_types  = [var.node_instance_type]

  scaling_config {
    desired_size = 2
    max_size     = 5
    min_size     = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_policy,
  ]
}

resource "aws_iam_role" "eks_cluster" {
  name = "${var.cluster_name}-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

resource "aws_iam_role" "eks_nodes" {
  name = "${var.cluster_name}-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_worker_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes.name
}
""",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "aws-rds",
        "name": "AWS RDS Database",
        "description": "Sets up a highly available RDS database with backups and monitoring",
        "provider": "aws",
        "category": "database",
        "variables": [
            {
                "name": "db_name",
                "description": "Name of the database",
                "type": "string",
                "default": "production-db",
                "required": True
            },
            {
                "name": "engine",
                "description": "Database engine",
                "type": "string",
                "default": "postgres",
                "required": True
            },
            {
                "name": "instance_class",
                "description": "Database instance class",
                "type": "string",
                "default": "db.t3.medium",
                "required": True
            }
        ],
        "content": """
resource "aws_db_instance" "main" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = var.engine
  engine_version       = "13.4"
  instance_class       = var.instance_class
  name                 = var.db_name
  username             = "admin"
  password             = random_password.db_password.result
  parameter_group_name = "default.${var.engine}13"
  skip_final_snapshot  = true
  multi_az             = true
  backup_retention_period = 7
  backup_window        = "03:00-04:00"
  maintenance_window   = "mon:04:00-mon:05:00"
  
  tags = {
    Name = var.db_name
  }
}

resource "random_password" "db_password" {
  length  = 16
  special = false
}

resource "aws_secretsmanager_secret" "db_credentials" {
  name = "${var.db_name}-credentials"
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = aws_db_instance.main.username
    password = random_password.db_password.result
    engine   = var.engine
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    dbname   = var.db_name
  })
}
""",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "gcp-gke",
        "name": "GCP GKE Cluster",
        "description": "Creates a Google Kubernetes Engine cluster with auto-scaling node pools",
        "provider": "gcp",
        "category": "containers",
        "variables": [
            {
                "name": "cluster_name",
                "description": "Name of the GKE cluster",
                "type": "string",
                "default": "production-cluster",
                "required": True
            },
            {
                "name": "region",
                "description": "GCP region",
                "type": "string",
                "default": "us-central1",
                "required": True
            },
            {
                "name": "node_count",
                "description": "Number of nodes per zone",
                "type": "number",
                "default": "1",
                "required": True
            }
        ],
        "content": """
resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.region
  
  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "${var.cluster_name}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  node_config {
    preemptible  = true
    machine_type = "e2-medium"

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  
  autoscaling {
    min_node_count = 1
    max_node_count = 5
  }
}
""",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "azure-aks",
        "name": "Azure Kubernetes Service",
        "description": "Deploys an AKS cluster with virtual network integration",
        "provider": "azure",
        "category": "containers",
        "variables": [
            {
                "name": "cluster_name",
                "description": "Name of the AKS cluster",
                "type": "string",
                "default": "production-aks",
                "required": True
            },
            {
                "name": "location",
                "description": "Azure region",
                "type": "string",
                "default": "eastus",
                "required": True
            },
            {
                "name": "kubernetes_version",
                "description": "Kubernetes version",
                "type": "string",
                "default": "1.27.3",
                "required": True
            }
        ],
        "content": """
resource "azurerm_resource_group" "main" {
  name     = "${var.cluster_name}-resources"
  location = var.location
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.cluster_name}-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "internal" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.0.0/22"]
}

resource "azurerm_kubernetes_cluster" "main" {
  name                = var.cluster_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = var.cluster_name
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name           = "default"
    node_count     = 2
    vm_size        = "Standard_DS2_v2"
    vnet_subnet_id = azurerm_subnet.internal.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
    network_policy    = "calico"
  }
}
""",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "multi-cloud-network",
        "name": "Multi-Cloud Network",
        "description": "Establishes secure network connectivity between AWS, GCP, and Azure",
        "provider": "multi",
        "category": "networking",
        "variables": [
            {
                "name": "project_name",
                "description": "Name of the project",
                "type": "string",
                "default": "multi-cloud-network",
                "required": True
            },
            {
                "name": "aws_region",
                "description": "AWS region",
                "type": "string",
                "default": "us-east-1",
                "required": True
            },
            {
                "name": "gcp_region",
                "description": "GCP region",
                "type": "string",
                "default": "us-central1",
                "required": True
            },
            {
                "name": "azure_region",
                "description": "Azure region",
                "type": "string",
                "default": "eastus",
                "required": True
            }
        ],
        "content": """
# AWS Resources
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "${var.project_name}-aws-vpc"
  }
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  
  tags = {
    Name = "${var.project_name}-aws-subnet"
  }
}

resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.project_name}-aws-vpn-gateway"
  }
}

# GCP Resources
resource "google_compute_network" "main" {
  name                    = "${var.project_name}-gcp-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "main" {
  name          = "${var.project_name}-gcp-subnet"
  ip_cidr_range = "10.1.0.0/24"
  region        = var.gcp_region
  network       = google_compute_network.main.id
}

resource "google_compute_vpn_gateway" "main" {
  name    = "${var.project_name}-gcp-vpn-gateway"
  network = google_compute_network.main.id
  region  = var.gcp_region
}

# Azure Resources
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-resources"
  location = var.azure_region
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.project_name}-azure-network"
  address_space       = ["10.2.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "main" {
  name                 = "${var.project_name}-azure-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.2.1.0/24"]
}

resource "azurerm_virtual_network_gateway" "main" {
  name                = "${var.project_name}-azure-vpn-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  type     = "Vpn"
  vpn_type = "RouteBased"
  
  active_active = false
  enable_bgp    = true
  sku           = "VpnGw1"
  
  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.main.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}

resource "azurerm_public_ip" "main" {
  name                = "${var.project_name}-azure-gateway-ip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Dynamic"
}

resource "azurerm_subnet" "gateway" {
  name                 = "GatewaySubnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.2.255.0/27"]
}
""",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "aws-lambda-api",
        "name": "AWS Lambda with API Gateway",
        "description": "Deploys a serverless API using Lambda and API Gateway",
        "provider": "aws",
        "category": "serverless",
        "variables": [
            {
                "name": "api_name",
                "description": "Name of the API",
                "type": "string",
                "default": "serverless-api",
                "required": True
            },
            {
                "name": "lambda_runtime",
                "description": "Lambda runtime",
                "type": "string",
                "default": "nodejs18.x",
                "required": True
            },
            {
                "name": "stage_name",
                "description": "API Gateway stage name",
                "type": "string",
                "default": "prod",
                "required": True
            }
        ],
        "content": """
resource "aws_lambda_function" "api" {
  function_name = var.api_name
  handler       = "index.handler"
  runtime       = var.lambda_runtime
  role          = aws_iam_role.lambda_exec.arn
  
  filename      = "lambda_function.zip"
  
  environment {
    variables = {
      STAGE = var.stage_name
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "${var.api_name}-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_apigatewayv2_api" "main" {
  name          = var.api_name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = var.stage_name
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "main" {
  api_id             = aws_apigatewayv2_api.main.id
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  integration_uri    = aws_lambda_function.api.invoke_arn
}

resource "aws_apigatewayv2_route" "main" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.main.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}
""",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "aws-s3-cloudfront",
        "name": "AWS S3 with CloudFront",
        "description": "Sets up a static website hosting with S3 and CloudFront CDN",
        "provider": "aws",
        "category": "web",
        "variables": [
            {
                "name": "website_name",
                "description": "Name of the website",
                "type": "string",
                "default": "my-static-website",
                "required": True
            },
            {
                "name": "domain_name",
                "description": "Domain name for the website",
                "type": "string",
                "default": "example.com",
                "required": True
            },
            {
                "name": "enable_https",
                "description": "Enable HTTPS",
                "type": "bool",
                "default": "true",
                "required": True
            }
        ],
        "content": """
resource "aws_s3_bucket" "website" {
  bucket = var.website_name
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.website.arn}/*"
      }
    ]
  })
}

resource "aws_cloudfront_distribution" "website" {
  origin {
    domain_name = aws_s3_bucket_website_configuration.website.website_endpoint
    origin_id   = "S3-${var.website_name}"
    
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }
  
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  
  aliases = [var.domain_name]
  
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${var.website_name}"
    
    forwarded_values {
      query_string = false
      
      cookies {
        forward = "none"
      }
    }
    
    viewer_protocol_policy = var.enable_https ? "redirect-to-https" : "allow-all"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    cloudfront_default_certificate = !var.enable_https
    acm_certificate_arn            = var.enable_https ? aws_acm_certificate.cert[0].arn : null
    ssl_support_method             = var.enable_https ? "sni-only" : null
  }
}

resource "aws_acm_certificate" "cert" {
  count = var.enable_https ? 1 : 0
  
  domain_name       = var.domain_name
  validation_method = "DNS"
  
  lifecycle {
    create_before_destroy = true
  }
}
""",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
]

@terraform_bp.route('/templates', methods=['GET'])
@require_auth
def list_templates():
    """List all Terraform templates."""
    try:
        # In a real implementation, this would fetch from a database
        # For now, return mock data for development/testing
        return jsonify(MOCK_TEMPLATES), 200
    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        return jsonify({'error': 'Failed to list templates'}), 500

@terraform_bp.route('/templates/<template_id>', methods=['GET'])
@require_auth
def get_template(template_id):
    """Get a specific Terraform template."""
    try:
        # In a real implementation, this would fetch from a database
        # For now, search in mock data for development/testing
        template = next((t for t in MOCK_TEMPLATES if t['id'] == template_id), None)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        return jsonify(template), 200
    except Exception as e:
        logger.error(f"Error getting template: {str(e)}")
        return jsonify({'error': 'Failed to get template'}), 500

@terraform_bp.route('/templates', methods=['POST'])
@require_auth
def create_template():
    """Create a new Terraform template."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['name', 'description', 'provider', 'category', 'variables', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # In a real implementation, this would store in a database
        # For now, create a new mock template for development/testing
        template_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        new_template = {
            'id': template_id,
            'name': data['name'],
            'description': data['description'],
            'provider': data['provider'],
            'category': data['category'],
            'variables': data['variables'],
            'content': data['content'],
            'created_at': now,
            'updated_at': now
        }
        
        # In a real implementation, this would be added to a database
        # For now, just return the new template for development/testing
        
        return jsonify(new_template), 201
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}")
        return jsonify({'error': 'Failed to create template'}), 500

@terraform_bp.route('/templates/<template_id>', methods=['PUT'])
@require_auth
def update_template(template_id):
    """Update a Terraform template."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # In a real implementation, this would update in a database
        # For now, search in mock data for development/testing
        template = next((t for t in MOCK_TEMPLATES if t['id'] == template_id), None)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        # Update fields
        for key, value in data.items():
            if key in template and key not in ['id', 'created_at']:
                template[key] = value
        
        template['updated_at'] = datetime.now().isoformat()
        
        return jsonify(template), 200
    except Exception as e:
        logger.error(f"Error updating template: {str(e)}")
        return jsonify({'error': 'Failed to update template'}), 500

@terraform_bp.route('/templates/<template_id>', methods=['DELETE'])
@require_auth
def delete_template(template_id):
    """Delete a Terraform template."""
    try:
        # In a real implementation, this would delete from a database
        # For now, search in mock data for development/testing
        template = next((t for t in MOCK_TEMPLATES if t['id'] == template_id), None)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        # In a real implementation, this would remove from a database
        # For now, just return success for development/testing
        
        return jsonify({'message': 'Template deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting template: {str(e)}")
        return jsonify({'error': 'Failed to delete template'}), 500

@terraform_bp.route('/deployments', methods=['GET'])
@require_auth
def list_deployments():
    """List all Terraform deployments."""
    try:
        # In a real implementation, this would fetch from a database
        # For now, return mock data for development/testing
        deployments = [
            {
                'id': 'deployment-1',
                'template_id': 'aws-vpc',
                'name': 'Production VPC',
                'status': 'completed',
                'variables': {
                    'vpc_name': 'production-vpc',
                    'cidr_block': '10.0.0.0/16',
                    'region': 'us-east-1'
                },
                'outputs': {
                    'vpc_id': 'vpc-0123456789abcdef0',
                    'public_subnet_ids': 'subnet-0123456789abcdef0,subnet-0123456789abcdef1',
                    'private_subnet_ids': 'subnet-0123456789abcdef2,subnet-0123456789abcdef3'
                },
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-01-01T01:00:00Z'
            },
            {
                'id': 'deployment-2',
                'template_id': 'aws-eks',
                'name': 'Production EKS',
                'status': 'completed',
                'variables': {
                    'cluster_name': 'production-cluster',
                    'kubernetes_version': '1.27',
                    'node_instance_type': 't3.medium'
                },
                'outputs': {
                    'cluster_endpoint': 'https://example.eks.amazonaws.com',
                    'cluster_name': 'production-cluster',
                    'kubeconfig_command': 'aws eks update-kubeconfig --name production-cluster --region us-east-1'
                },
                'created_at': '2023-01-02T00:00:00Z',
                'updated_at': '2023-01-02T01:00:00Z'
            }
        ]
        
        return jsonify(deployments), 200
    except Exception as e:
        logger.error(f"Error listing deployments: {str(e)}")
        return jsonify({'error': 'Failed to list deployments'}), 500

@terraform_bp.route('/deployments/<deployment_id>', methods=['GET'])
@require_auth
def get_deployment(deployment_id):
    """Get a specific Terraform deployment."""
    try:
        # In a real implementation, this would fetch from a database
        # For now, return mock data for development/testing
        if deployment_id == 'deployment-1':
            deployment = {
                'id': 'deployment-1',
                'template_id': 'aws-vpc',
                'name': 'Production VPC',
                'status': 'completed',
                'variables': {
                    'vpc_name': 'production-vpc',
                    'cidr_block': '10.0.0.0/16',
                    'region': 'us-east-1'
                },
                'outputs': {
                    'vpc_id': 'vpc-0123456789abcdef0',
                    'public_subnet_ids': 'subnet-0123456789abcdef0,subnet-0123456789abcdef1',
                    'private_subnet_ids': 'subnet-0123456789abcdef2,subnet-0123456789abcdef3'
                },
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-01-01T01:00:00Z'
            }
            return jsonify(deployment), 200
        elif deployment_id == 'deployment-2':
            deployment = {
                'id': 'deployment-2',
                'template_id': 'aws-eks',
                'name': 'Production EKS',
                'status': 'completed',
                'variables': {
                    'cluster_name': 'production-cluster',
                    'kubernetes_version': '1.27',
                    'node_instance_type': 't3.medium'
                },
                'outputs': {
                    'cluster_endpoint': 'https://example.eks.amazonaws.com',
                    'cluster_name': 'production-cluster',
                    'kubeconfig_command': 'aws eks update-kubeconfig --name production-cluster --region us-east-1'
                },
                'created_at': '2023-01-02T00:00:00Z',
                'updated_at': '2023-01-02T01:00:00Z'
            }
            return jsonify(deployment), 200
        else:
            return jsonify({'error': 'Deployment not found'}), 404
    except Exception as e:
        logger.error(f"Error getting deployment: {str(e)}")
        return jsonify({'error': 'Failed to get deployment'}), 500

@terraform_bp.route('/deployments', methods=['POST'])
@require_auth
def create_deployment():
    """Create a new Terraform deployment."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['template_id', 'name', 'variables']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # In a real implementation, this would create a deployment in a database and start a Terraform job
        # For now, return mock data for development/testing
        deployment_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        new_deployment = {
            'id': deployment_id,
            'template_id': data['template_id'],
            'name': data['name'],
            'status': 'planning',
            'variables': data['variables'],
            'outputs': {},
            'created_at': now,
            'updated_at': now
        }
        
        return jsonify(new_deployment), 201
    except Exception as e:
        logger.error(f"Error creating deployment: {str(e)}")
        return jsonify({'error': 'Failed to create deployment'}), 500

@terraform_bp.route('/deployments/<deployment_id>/apply', methods=['POST'])
@require_auth
def apply_deployment(deployment_id):
    """Apply a Terraform deployment."""
    try:
        # In a real implementation, this would trigger a Terraform apply job
        # For now, return mock data for development/testing
        return jsonify({
            'id': deployment_id,
            'status': 'applying',
            'message': 'Deployment apply started'
        }), 200
    except Exception as e:
        logger.error(f"Error applying deployment: {str(e)}")
        return jsonify({'error': 'Failed to apply deployment'}), 500

@terraform_bp.route('/deployments/<deployment_id>/destroy', methods=['POST'])
@require_auth
def destroy_deployment(deployment_id):
    """Destroy a Terraform deployment."""
    try:
        # In a real implementation, this would trigger a Terraform destroy job
        # For now, return mock data for development/testing
        return jsonify({
            'id': deployment_id,
            'status': 'destroying',
            'message': 'Deployment destroy started'
        }), 200
    except Exception as e:
        logger.error(f"Error destroying deployment: {str(e)}")
        return jsonify({'error': 'Failed to destroy deployment'}), 500
