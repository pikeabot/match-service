terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

# VPC
module "vpc" {
 source  = "./modules/vpc"
}

# IAM Role
module "iam" {
 source  = "./modules/iam"
}

