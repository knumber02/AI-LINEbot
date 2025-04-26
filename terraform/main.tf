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

# API Gateway
resource "aws_apigatewayv2_api" "lambda_api" {
  name          = "${var.app_name}-api"
  protocol_type = "HTTP"
}

# API GatewayのアクセスログをCloudWatchに保存
resource "aws_cloudwatch_log_group" "api_gw_logs" {
  name              = "/aws/api-gateway/${var.app_name}"
  retention_in_days = 14  # ログ保持期間
}

# API Gatewayのステージ
resource "aws_apigatewayv2_stage" "lambda_stage" {
  api_id      = aws_apigatewayv2_api.lambda_api.id
  name        = var.environment
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw_logs.arn
    format = jsonencode({
      requestId        = "$context.requestId",
      ip               = "$context.identity.sourceIp",
      requestTime      = "$context.requestTime",
      httpMethod       = "$context.httpMethod",
      routeKey         = "$context.routeKey",
      status           = "$context.status",
      protocol         = "$context.protocol",
      responseLength   = "$context.responseLength"
    })
  }
}

# API GatewayのLambda関数への統合
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.lambda_api.id
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  integration_uri    = aws_lambda_function.api_lambda.invoke_arn
}

# API Gatewayのルーティング
resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.lambda_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Lambda関数にAPI Gatewayからの実行許可を付与
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.lambda_api.execution_arn}/*/*"
}
