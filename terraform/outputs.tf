output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "RDS PostgreSQL port"
  value       = aws_db_instance.postgres.port
}

output "secret_arn" {
  description = "ARN of the AWS Secrets Manager secret"
  value       = aws_secretsmanager_secret.postgres.arn
}

output "secret_name" {
  description = "AWS Secrets Manager secret name"
  value       = aws_secretsmanager_secret.postgres.name
}