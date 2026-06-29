resource "google_service_account" "db_schema_migration" {
  account_id = "db-schema-migration-sa"
  display_name = "DB Schema Migration Job Service Account"
}