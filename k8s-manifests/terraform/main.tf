provider "aws" {
  region = var.region
}

data "aws_eks_cluster" "existing" {
  name = var.cluster_name
}

data "aws_eks_cluster_auth" "existing" {
  name = var.cluster_name
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.existing.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.existing.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.existing.token
}

resource "aws_ecr_repository" "backend" {
  name                 = "cloud-cost-optimizer-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "cloud-cost-optimizer-backend"
    Environment = var.environment
  }
}

resource "aws_ecr_repository" "frontend" {
  name                 = "cloud-cost-optimizer-frontend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "cloud-cost-optimizer-frontend"
    Environment = var.environment
  }
}

resource "aws_iam_policy" "cost_optimizer" {
  name        = "cloud-cost-optimizer-policy"
  description = "Policy for Cloud Cost Optimizer application"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
          "ec2:StartInstances",
          "ec2:StopInstances",
          "ec2:ModifyInstanceAttribute",
          "rds:Describe*",
          "rds:StartDBInstance",
          "rds:StopDBInstance",
          "rds:ModifyDBInstance",
          "s3:Get*",
          "s3:List*",
          "s3:PutLifecycleConfiguration",
          "ce:GetCostAndUsage",
          "ce:GetReservationUtilization",
          "ce:GetSavingsPlanUtilization",
          "ce:GetRecommendation"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "cost_optimizer" {
  name = "cloud-cost-optimizer-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRoleWithWebIdentity"
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${replace(data.aws_eks_cluster.existing.identity[0].oidc[0].issuer, "https://", "")}"
        }
        Condition = {
          StringEquals = {
            "${replace(data.aws_eks_cluster.existing.identity[0].oidc[0].issuer, "https://", "")}:sub" = "system:serviceaccount:cloud-cost-optimizer:cloud-cost-optimizer-sa"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "cost_optimizer" {
  role       = aws_iam_role.cost_optimizer.name
  policy_arn = aws_iam_policy.cost_optimizer.arn
}

data "aws_caller_identity" "current" {}

output "backend_repository_url" {
  value = aws_ecr_repository.backend.repository_url
}

output "frontend_repository_url" {
  value = aws_ecr_repository.frontend.repository_url
}

output "cost_optimizer_role_arn" {
  value = aws_iam_role.cost_optimizer.arn
}

output "kubectl_config_command" {
  value = "aws eks update-kubeconfig --region ${var.region} --name ${var.cluster_name}"
}

output "build_and_push_commands" {
  value = <<EOT
# Build and push backend image
docker build -t ${aws_ecr_repository.backend.repository_url}:latest -f Dockerfile.backend .
aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${aws_ecr_repository.backend.repository_url}
docker push ${aws_ecr_repository.backend.repository_url}:latest

# Build and push frontend image
cd src/ui/dashboard
docker build -t ${aws_ecr_repository.frontend.repository_url}:latest -f Dockerfile.frontend .
aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${aws_ecr_repository.frontend.repository_url}
docker push ${aws_ecr_repository.frontend.repository_url}:latest
EOT
}

output "deploy_commands" {
  value = <<EOT
# Update the image URLs in the kustomization config
cd k8s-manifests/overlays/production
sed -i 's|your-registry/cloud-cost-optimizer-backend:latest|${aws_ecr_repository.backend.repository_url}:latest|g' kustomization.yaml
sed -i 's|your-registry/cloud-cost-optimizer-frontend:latest|${aws_ecr_repository.frontend.repository_url}:latest|g' kustomization.yaml

# Update the service account annotation with the IAM role
sed -i 's|eks.amazonaws.com/role-arn: .*|eks.amazonaws.com/role-arn: ${aws_iam_role.cost_optimizer.arn}|g' ../../base/service-account.yaml

# Apply the Kubernetes manifests
kubectl apply -k .

# Check deployment status
kubectl get pods -n cloud-cost-optimizer
kubectl get svc -n cloud-cost-optimizer
EOT
}
