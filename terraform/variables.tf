

variable "local_db_name" {
  type        = string
  description = "Name of the local db used for timing"
  default     = "local_postgres_db"
}


variable "local_db_password" {
  type        = string
  description = "Password for the local db"
}


variable "postgres_external_port" {
  type = string
  description = "The external postgres port (host port)"
  default = 5432
}