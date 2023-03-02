terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.16"
    }
  }

  backend "s3" {
    # to store state file save
    bucket = "jade-terraform-state"
    # key is folder inside where to save state
    key     = "jade/terraform.tfstate"
    region  = "us-east-1"
    profile = "default"
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-1"
  profile = "default"
}

locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Environment = terraform.workspace
    Project     = var.project
    Owner       = var.contact
    ManagedBy   = "Terraform"
  }
}

data "aws_ami" "ubuntu_server" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

# 10.0.0.0/17 is half of 10.0.0.0/16 other ip range left for in case of vpc peering (can't connect if IP overlap exists)
module "vpc" {
  source = "./modules/vpc"

  infra_role  = "vpc"
  vpc_cidr    = "10.0.0.0/17"
  prefix      = local.prefix
  common_tags = local.common_tags
}

module "web_server" {
  source = "./modules/ec2"

  infra_role                = "web"
  instance_size             = var.web_instance_size
  instance_ami              = data.aws_ami.ubuntu_server.id
  instance_root_device_size = var.web_instance_root_device_size
  prefix                    = local.prefix
  common_tags               = local.common_tags
  subnets                   = keys(module.vpc.vpc_public_subnets)
  security_groups           = [module.vpc.security_group_public]
  create_eip                = true
  account_id                = var.account_id
}