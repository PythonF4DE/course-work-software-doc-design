resource "aws_secretsmanager_secret" "postgres" {
  name = "${var.project_name}/postgres"

  description = "PostgreSQL connection credentials for Doctor Appointment System"

  tags = {
    Project = var.project_name
  }
}

resource "aws_secretsmanager_secret_version" "postgres" {
  secret_id = aws_secretsmanager_secret.postgres.id

  secret_string = jsonencode({
    host         = aws_db_instance.postgres.address
    port         = aws_db_instance.postgres.port
    username     = var.db_username
    password     = random_password.db_password.result
    database     = var.db_name

    database_url = "postgresql://${var.db_username}:${urlencode(random_password.db_password.result)}@${aws_db_instance.postgres.address}:${aws_db_instance.postgres.port}/${var.db_name}"
  })
}