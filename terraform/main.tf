provider "aws" {
  region = var.aws_region
}
data "aws_caller_identity" "current" {}


resource "aws_s3_bucket" "lambda_bucket" {
  bucket = var.app_name
}
