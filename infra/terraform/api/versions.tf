terraform {
  required_version = ">= 1.8.0"

  backend "gcs" {
    bucket = "waseda-syllabus-project-terraform-state"
    prefix = "api"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}