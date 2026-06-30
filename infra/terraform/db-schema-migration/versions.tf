terraform {
  required_version = ">=1.8.0"

  backend "gcs" {
    bucket = "waseda-syllabus-project-terraform-state"
    prefix = "db-schema-migration"
  }

  required_providers {
    google = {
        source = "hashicorp/google"
        version = "~> 6.0"
    }
  }
}