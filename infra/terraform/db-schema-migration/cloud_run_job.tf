resource "google_cloud_run_v2_job" "db_schema_migration" {
  name = var.job_name
  location = var.region

  deletion_protection = false

  template {
    template {
      service_account = google_service_account.db_schema_migration.email

      timeout = "600s"

      volumes {
        name = "cloudsql"

        cloud_sql_instance {
          instances = [var.cloudsql_connection_name]
        }
      }

      containers {
        image = var.image_uri

        args = ["diff"]

        env {
          name = "PGHOST"
          value = "/cloudsql/${var.cloudsql_connection_name}"
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

        env {
          name = "PGPASSWORD"

          value_source {
            secret_key_ref {
              secret = var.db_password_secret_name
              version = "latest"
            }
          }
        }

        volume_mounts {
          name = "cloudsql"
          mount_path = "/cloudsql"
        }

        resources {
          limits = {
            cpu = "1"
            memory = "512Mi"
          }
        }
      }
    }
  }

  depends_on = [ 
    google_project_iam_member.db_schema_migration_cloudsql_client,
    google_secret_manager_secret_iam_member.db_schema_migration_db_password_accessor,
   ]
}