#####
# DB
#####
# https://registry.terraform.io/modules/terraform-aws-modules/rds/aws/2.5.0
module "db" {
  source     = "terraform-aws-modules/rds/aws"
  identifier = "${var.project_name}-rds-postgres"

  engine            = "postgres"
  engine_version    = "9.5"
  instance_class    = "db.t2.large"
  allocated_storage = 100
  storage_encrypted = false
  name              = var.database_name
  # NOTE: Do NOT use 'user' as the value for 'username' as it throws:
  # "Error creating DB Instance: InvalidParameterValue: MasterUsername
  # user cannot be used as it is a reserved word used by the engine"
  # Also password should be atleast 8 characters long, else that throws and error too
  username = var.database_username
  password = var.database_password
  # If changing this, make sure to change in security_groups as well for the rule
  port = 5432

  # Enable replica stand by for High Availability
  multi_az = true

  # [ PostgreSQL  1,000–80,000 IOPS   100 GiB–64 TiB | are the ranges]
  # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html#USER_PIOPS
  # The amount of provisioned IOPS. Setting this implies a storage_type of 'io1'
  # AWS: For production application that requires fast and consistent I/O performance, we recommend Provisioned IOPS
  iops         = 1000
  storage_type = "io1"

  # Specifies whether any database modifications are applied immediately,
  # or during the next maintenance window
  # Set to true, only for faster trials while scripting infrastructure
  apply_immediately = true

  # The ARN for the KMS encryption key. If creating an encrypted replica, set this to the destination KMS ARN.
  # If storage_encrypted is set to true and kms_key_id is not specified the default KMS key created in your account will be used
  # kms_key_id        = "arm:aws:kms:<region>:<account id>:key/<kms key id>"

  # Include the security group that was created for restricting access to RDS only from EKS worker nodes
  vpc_security_group_ids = [aws_security_group.nodes-rds-security.id]

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"

  # disable backups to create DB faster
  backup_retention_period = 0

  tags = {
    Name        = "PostgreSQL"
    Project     = var.project_name
    Environment = var.project_env
  }

  # DB subnet group
  subnet_ids = module.vpc.private_subnets

  # Snapshot name upon DB deletion
  final_snapshot_identifier = "${var.project_name}-rds-postgres-snapshot"

  # Database Deletion Protection :  The database can't be deleted when this value is set to true
  deletion_protection = false
}
