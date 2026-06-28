resource "google_project_iam_member" "db_schema_migration_cloudsql_client" {
    project = var.project_id
    role = "roles/cloudsql.client"
    member = "serviceAccount:${google_service_account.db_schema_migration.email}"
}