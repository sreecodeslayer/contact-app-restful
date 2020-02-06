# IAM policy that allows EKS nodes to pull images from AWS ECR
# Based on https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_EKS.html
resource "aws_iam_policy" "ecr-eks-policy" {
  name        = "${var.project_name}-ecr-eks-policy"
  description = "A policy to allow AWS EKS Worker node to pull images from AWS ECR"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:BatchCheckLayerAvailability",
                "ecr:BatchGetImage",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetAuthorizationToken"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

# https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/7.0.0
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "7.0.0"

  cluster_name = var.project_name

  # VPC where the cluster and workers will be deployed.
  vpc_id = module.vpc.vpc_id

  #  A list of subnets to place the EKS cluster and workers within
  subnets = module.vpc.private_subnets

  tags = {
    Name        = var.project_name
    Project     = var.project_name
    Environment = var.project_env
  }

  # A list of worker group configurations to be defined using AWS Launch Configurations.
  # A more indepth configuration can be found here:
  # https://github.com/dockup/terraform-aws/blob/936c25345fb886168ace276bde6735ad84438ced/modules/infra/workers.tf#L136
  worker_groups = [
    {
      name                          = "${var.project_name}-worker-nodes"
      instance_type                 = "t2.medium"
      additional_security_group_ids = [aws_security_group.worker-nodes.id]
      asg_desired_capacity          = 3
    }
  ]

  # Restrict worker node access using the security groups created specifically for these nodes
  worker_additional_security_group_ids = [aws_security_group.worker-nodes.id]

  # Use the policy from above to let worker nodes to pull images from ECR
  workers_additional_policies = [aws_iam_policy.ecr-eks-policy.arn]
  map_users                   = var.cluster_admins_arns
}
