resource "google_project_iam_member" "db_schema_migration_cloudsql_client" {
    project = var.project_id
    role = "roles/cloudsql.client"
    member = "serviceAccount:${google_service_account.db_schema_migration.email}"
}

resource "google_secret_manager_secret_iam_member" "db_schema_migration_db_password_accessor" {
  project = var.project_id
  secret_id = var.db_password_secret_name
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${google_service_account.db_schema_migration.email}"
}
