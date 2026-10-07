data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_db_subnet_group" "postgres" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name    = "${var.project_name}-db-subnet-group"
    Project = var.project_name
  }
}

resource "aws_security_group" "postgres" {
  name        = "${var.project_name}-postgres-sg"
  description = "Allow PostgreSQL access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "PostgreSQL from anywhere IPv4"
    from_port   = var.db_port
    to_port     = var.db_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description      = "PostgreSQL from anywhere IPv6"
    from_port        = var.db_port
    to_port          = var.db_port
    protocol         = "tcp"
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name    = "${var.project_name}-postgres-sg"
    Project = var.project_name
  }
}

resource "random_password" "db_password" {
  length  = 24
  special = true

  override_special = "!#$%&*+-=?"
}

resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-postgres"

  engine         = "postgres"
  engine_version = "18.6"

  instance_class = var.db_instance_class

  allocated_storage     = 20
  max_allocated_storage = 50
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result
  port     = var.db_port

  publicly_accessible = true

  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [
    aws_security_group.postgres.id
  ]

  backup_retention_period = 1

  auto_minor_version_upgrade = true

  multi_az = false

  deletion_protection = false

  skip_final_snapshot = true

  apply_immediately = true

  tags = {
    Name    = "${var.project_name}-postgres"
    Project = var.project_name
  }
}