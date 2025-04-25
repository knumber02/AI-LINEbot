provider "aws" {
  region = var.aws_region
}
data "aws_caller_identity" "current" {}

# Lambdaのデプロイパッケージを保存するS3バケット
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = var.app_name
}

# Lambda関数用のIAMロール
resource "aws_iam_role" "lambda_role" {
  name = "${var.app_name}-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Lambda関数
resource "aws_lambda_function" "api_lambda" {
  function_name = var.app_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "demo_app.lambda_handler.handler"
  runtime       = "python3.9"

  s3_bucket = aws_s3_bucket.lambda_bucket.bucket
  s3_key    = "lambda_package.zip"

  environment {
    variables = {
      STAGE = var.environment
    }
  }
}
