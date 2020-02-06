data "aws_availability_zones" "available" {
}
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.21.0"

  name                 = "${var.project_name}-vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  # Tag to enable Node(s) discovery for Kubernetes
  # All EC2 nodes in this VPC with this tag can be discovered by Kubernetes
  # More info on Kubernetes Tags for EKS can be found here: https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html
  tags = {
    "kubernetes.io/cluster/${var.project_name}" = "shared"
  }
  # All subnets (public and private) that your cluster uses for resources should have this tag.

  # Kubernetes knows to use only those subnets for external load balancers
  public_subnet_tags = {
    "kubernetes.io/cluster/${var.project_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
  }

  # Kubernetes knows to use only those subnets for internal load balancers
  private_subnet_tags = {
    "kubernetes.io/cluster/${var.project_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }
}

