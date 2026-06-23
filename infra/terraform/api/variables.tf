variable "project_id" {
  type = string
}

variable "region" {
  type = string
  default = "asia-northeast1"
}

variable "service_name" {
  type = string
  default = "api"
}

variable "image_uri" {
  type = string
}

variable "cloud_sql_connection_name" {
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

variable "allow_public_invoker" {
  type = bool
  default = true
}