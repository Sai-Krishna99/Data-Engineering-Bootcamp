variable "credentials"{
    description = "GCP Credentials"
    default = "./gcloud_keys/my-creds.json"
}

variable "project_id"{
    description = "Project ID"
    default = "pelagic-tracker-414819"
}

variable "region"{
    description = "Project Region"
    default = "us-central1"
}

variable "location"{
    description = "Project Location"
    default = "US"
}

variable "gcs_storage_class"{
    description = "Bucket Storage Class"
    default = "STANDARD"
}

variable "gcs_bucket_name"{
    description = "GCS Bucket Name"
    default = "terraform-practice-bucket-de"
}

variable "bq_dataset_name"{
    description = "My BigQuery Dataset Name"
    default = "demo_dataset"
}