variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "Name of the existing EKS cluster"
  type        = string
  default     = "PrimusAllCluster"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}
