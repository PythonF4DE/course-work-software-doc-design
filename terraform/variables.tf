variable "project_name" {
  description = "Project name used in AWS resource names"
  type        = string
  default     = "doctor-appointment-system"
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "doctorapp"
}

variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
  default     = "doctor_admin"
}

variable "db_port" {
  description = "PostgreSQL port"
  type        = number
  default     = 5432
}

variable "db_instance_class" {
  description = "RDS instance type"
  type        = string
  default     = "db.t3.micro"
}