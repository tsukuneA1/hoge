output "job_name" {
  value = google_cloud_run_v2_job.db_schema_migration.name
}

output "job_location" {
  value = google_cloud_run_v2_job.db_schema_migration.location
}

output "service_account_email" {
  value = google_service_account.db_schema_migration.email
}