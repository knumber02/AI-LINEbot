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

# Lambda関数用のセキュリティグループ
resource "aws_security_group" "lambda_sg" {
  name        = "${var.app_name}-lambda-sg"
  description = "Lambda outbound access to RDS"
  vpc_id      = aws_vpc.main.id

  # Lambdaは外に出るだけなので、ingressは不要

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
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
      DB_HOST = var.db_host
      DB_PORT = var.db_port
      DB_USER = var.db_username
      DB_PASSWORD = var.db_password
      DB_NAME = var.db_name
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

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.app_name}-vpc"
  }
}

# インターネットゲートウェイ
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.app_name}-igw"
  }
}

# ルートテーブル
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.app_name}-public-rt"
  }
}


# サブネット
# Subnet1（AZ1）
resource "aws_subnet" "db_public1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-northeast-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.app_name}-db-public-subnet-1"
  }
}

# Subnet2（AZ2）
resource "aws_subnet" "db_public2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "ap-northeast-1c"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.app_name}-db-public-subnet-2"
  }
}

# ルートテーブルとサブネットの関連付け
resource "aws_route_table_association" "public1" {
  subnet_id      = aws_subnet.db_public1.id
  route_table_id = aws_route_table.public.id
}
resource "aws_route_table_association" "public2" {
  subnet_id      = aws_subnet.db_public2.id
  route_table_id = aws_route_table.public.id
}

# RDSのサブネットグループ
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${var.app_name}-subnet-group"
  subnet_ids = [
    aws_subnet.db_public1.id,
    aws_subnet.db_public2.id
  ]

  tags = {
    Name = "${var.app_name}-subnet-group"
  }
}


# RDSのインスタンス
resource "aws_db_instance" "rds_instance" {
  identifier              = "${var.app_name}-db"
  engine                  = "mysql"
  engine_version          = "8.0"
  instance_class          = "db.t3.micro"  # 最小スペック
  allocated_storage       = 20             # 20GB
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
  publicly_accessible     = true            # 外部接続を許可
  skip_final_snapshot     = true            # 削除時スナップショット不要
  deletion_protection     = false
  vpc_security_group_ids  = [aws_security_group.rds_sg.id] # セキュリティグループ設定
}

# RDSのセキュリティグループ
resource "aws_security_group" "rds_sg" {
  name        = "${var.app_name}-rds-sg"
  description = "Allow MySQL inbound traffic from Lambda only"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id] # LambdaのSGからのみ許可
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
}
