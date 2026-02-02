output "bucket_name" {
  value       = google_storage_bucket.local_variable_name_for_bucket.name
  description = "The generated name of the GCS bucket"
}
