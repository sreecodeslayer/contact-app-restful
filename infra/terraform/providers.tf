#
# Provider Configuration
#

provider "aws" {
  version = ">= 2.28.1"
  region  = var.aws_region
}

data "aws_eks_cluster_auth" "application" {
  name = var.project_name
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  token                  = data.aws_eks_cluster_auth.application.token
  # Use Token and certificate from above to authenticate with K8s master instead of Kubeconfig
  # for CIs where file creation is not possible:
  # IRONY: Can't use Kubeconfig in TF Cloud [facepalm]
  load_config_file       = false
}
