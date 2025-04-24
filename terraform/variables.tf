variable "aws_region" {
  description = "AWSリージョン"
  default     = "ap-northeast-1"
}

variable "app_name" {
  description = "アプリケーション名"
  default     = "fastapi-line-bot"
}

variable "environment" {
  description = "環境（dev, staging, prod）"
  default     = "dev"
} 
