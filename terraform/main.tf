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

# IAM
module "iam" {
 source  = "./modules/iam"
}

# SQS Example Queue
module "sqs" {
  source = "./modules/sqs"

}

# S3 Bucket
resource "aws_s3_bucket" "match-service-lambda-deploy" {
   bucket = "match-service-lambda-deploy"
   acl    = "private"
}
