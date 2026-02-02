variable "credentials" {
  description = "My Credentials"
  # Point to the location of service-account.json file
  default     = "./keys/service-account.json"
}

variable "project" {
  description = "Project"
  # Name of the Project ID within which the bucket will be created 
  default     = "dezoomcamp-2026" 
}

variable "region" {
  description = "Region"
  # Desired region
  default = "europe-north1"
}

variable "location" {
  description = "Project Location"
  # Desired location
  default = "EU"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  # Update to a unique bucket name
  default = "homework_3_bucket_chum"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  # Update to dataset name
  default = "homework_3_dataset"
}
