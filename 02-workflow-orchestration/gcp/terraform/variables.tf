variable "credentials" {
  description = "My Credentials"
  # Point to the location of service-account.json file
  default     = "./keys/service-account.json"
}

variable "project" {
  description = "Project"
  # Name of the Project ID whithin which the bucket will be created 
  default     = "data-engeenering-project" 
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
  default = "dezoomcamp_homework2_bucket"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  # Update to dataset name
  default = "dezoomcamp_homework2_dataset"
}
