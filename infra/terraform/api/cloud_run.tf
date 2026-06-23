resource "google_cloud_run_v2_service" "api" {
  name = var.service_name
  location = var.region

  deletion_protection = false

  template {
    service_account = google_service_account.api.email

    scaling {
      min_instance_count = 0
      max_instance_count = 2
    }

    volumes {
      name = "cloudsql"

      cloud_sql_instance {
        instances = [var.cloud_sql_connection_name]
      }
    }

    containers {
      image = var.image_uri

      ports {
        container_port = 8080
      }

      env {
        name = "PGHOST"
        value = local.db_host
      }

      env {
        name = "PGPORT"
        value = "5432"
      }

      env {
        name = "PGDATABASE"
        value = var.db_name
      }

      env {
        name = "PGUSER"
        value = var.db_user
      }

      
    }
  }
}