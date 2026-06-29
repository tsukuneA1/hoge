variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "asia-northeast1"
}

variable "job_name" {
  type = string
  default = "db-schema-migration"
}

variable "image_uri" {
  type = string
}

variable "cloudsql_connection_name" {
  type = string
}

variable "db_name" {
  type = string
}

variable "db_user" {
  type = string
}

variable "db_password_secret_name" {
  type = string
}