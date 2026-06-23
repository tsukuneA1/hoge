resource "google_project_iam_member" "api_cloudsql_client" {
  project = var.project_id
  role = "roles/cloudsql.client"
  member = "serviceAccount:${google_service_account.api.email}"
}

resource "google_secret_manager_secret_iam_member" "api_db_password_accessor" {
  project = var.project_id
  secret_id = var.db_password_secret_name
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${google_service_account.api.email}"
}

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  count = var.allow_public_invoker ? 1 : 0

  project = var.project_id
  location = var.region
  name = google_cloud_run_v2_service.api.name
  role = "roles/run.invoker"
  member = "allUsers"
}
