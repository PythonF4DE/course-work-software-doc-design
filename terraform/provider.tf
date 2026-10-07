provider "aws" {
  region = "eu-north-1"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.57.0"
    }
  }

  backend "s3" {
    bucket         = "iot-data-bucket-dev-94546305"
    key            = "state/rds-db/terraform.tfstate"
    use_lockfile   = true
    region         = "eu-north-1"
    encrypt        = true
  }
}