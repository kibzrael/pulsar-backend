resource "google_project" "pulsarinc_alpha" {
  auto_create_network = true
  billing_account     = "0132BD-CB1EB0-25123C"
  labels = {
    firebase = "enabled"
  }
  name       = "pulsarinc-alpha"
  project_id = "pulsarinc-alpha"
}
# terraform import google_project.pulsarinc_alpha projects/pulsarinc-alpha
resource "google_sql_database_instance" "pulsar" {
  database_version = "POSTGRES_14"
  name             = "pulsar"
  project          = "pulsarinc-alpha"
  region           = "europe-west1"
  settings {
    activation_policy = "ALWAYS"
    availability_type = "ZONAL"
    backup_configuration {
      backup_retention_settings {
        retained_backups = 7
        retention_unit   = "COUNT"
      }
      enabled                        = true
      location                       = "eu"
      point_in_time_recovery_enabled = true
      start_time                     = "21:00"
      transaction_log_retention_days = 7
    }
    disk_autoresize       = true
    disk_autoresize_limit = 0
    disk_size             = 10
    disk_type             = "PD_HDD"
    insights_config {
      query_string_length = 0
    }
    ip_configuration {
      ipv4_enabled = true
    }
    location_preference {
      zone = "europe-west1-b"
    }
    pricing_plan = "PER_USE"
    tier         = "db-f1-micro"
  }
}
# terraform import google_sql_database_instance.pulsar projects/pulsarinc-alpha/instances/pulsar
resource "google_compute_firewall" "default_allow_icmp" {
  allow {
    protocol = "icmp"
  }
  description   = "Allow ICMP from anywhere"
  direction     = "INGRESS"
  name          = "default-allow-icmp"
  network       = "https://www.googleapis.com/compute/v1/projects/pulsarinc-alpha/global/networks/default"
  priority      = 65534
  project       = "pulsarinc-alpha"
  source_ranges = ["0.0.0.0/0"]
}
# terraform import google_compute_firewall.default_allow_icmp projects/pulsarinc-alpha/global/firewalls/default-allow-icmp
resource "google_compute_firewall" "default_allow_rdp" {
  allow {
    ports    = ["3389"]
    protocol = "tcp"
  }
  description   = "Allow RDP from anywhere"
  direction     = "INGRESS"
  name          = "default-allow-rdp"
  network       = "https://www.googleapis.com/compute/v1/projects/pulsarinc-alpha/global/networks/default"
  priority      = 65534
  project       = "pulsarinc-alpha"
  source_ranges = ["0.0.0.0/0"]
}
# terraform import google_compute_firewall.default_allow_rdp projects/pulsarinc-alpha/global/firewalls/default-allow-rdp
resource "google_compute_firewall" "default_allow_internal" {
  allow {
    ports    = ["0-65535"]
    protocol = "tcp"
  }
  allow {
    ports    = ["0-65535"]
    protocol = "udp"
  }
  allow {
    protocol = "icmp"
  }
  description   = "Allow internal traffic on the default network"
  direction     = "INGRESS"
  name          = "default-allow-internal"
  network       = "https://www.googleapis.com/compute/v1/projects/pulsarinc-alpha/global/networks/default"
  priority      = 65534
  project       = "pulsarinc-alpha"
  source_ranges = ["10.128.0.0/9"]
}
# terraform import google_compute_firewall.default_allow_internal projects/pulsarinc-alpha/global/firewalls/default-allow-internal
resource "google_compute_firewall" "default_allow_ssh" {
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  description   = "Allow SSH from anywhere"
  direction     = "INGRESS"
  name          = "default-allow-ssh"
  network       = "https://www.googleapis.com/compute/v1/projects/pulsarinc-alpha/global/networks/default"
  priority      = 65534
  project       = "pulsarinc-alpha"
  source_ranges = ["0.0.0.0/0"]
}
# terraform import google_compute_firewall.default_allow_ssh projects/pulsarinc-alpha/global/firewalls/default-allow-ssh
resource "google_service_account" "firebase_adminsdk_uixb7" {
  account_id   = "firebase-adminsdk-uixb7"
  description  = "Firebase Admin SDK Service Agent"
  display_name = "firebase-adminsdk"
  project      = "pulsarinc-alpha"
}
# terraform import google_service_account.firebase_adminsdk_uixb7 projects/pulsarinc-alpha/serviceAccounts/firebase-adminsdk-uixb7@pulsarinc-alpha.iam.gserviceaccount.com
resource "google_service_account" "pulsarinc_alpha" {
  account_id   = "pulsarinc-alpha"
  display_name = "App Engine default service account"
  project      = "pulsarinc-alpha"
}
# terraform import google_service_account.pulsarinc_alpha projects/pulsarinc-alpha/serviceAccounts/pulsarinc-alpha@pulsarinc-alpha.iam.gserviceaccount.com
resource "google_service_account" "822281553923_compute" {
  account_id   = "822281553923-compute"
  display_name = "Compute Engine default service account"
  project      = "pulsarinc-alpha"
}
# terraform import google_service_account.822281553923_compute projects/pulsarinc-alpha/serviceAccounts/822281553923-compute@pulsarinc-alpha.iam.gserviceaccount.com
resource "google_secret_manager_secret" "django_settings" {
  project = "822281553923"
  replication {
    automatic = true
  }
  secret_id = "django_settings"
}
# terraform import google_secret_manager_secret.django_settings projects/822281553923/secrets/django_settings
resource "google_secret_manager_secret_version" "projects_822281553923_secrets_django_settings_versions_1" {
  enabled     = true
  secret      = "projects/822281553923/secrets/django_settings"
  secret_data = "DATABASE_URL=postgres://root:kibzrael@//cloudsql/pulsarinc-alpha:europe-west1:pulsar/postgres\nDATABASE_HOST=/cloudsql/pulsarinc-alpha:europe-west1:pulsar\nGS_BUCKET_NAME=pulsarinc_media\nSECRET_KEY=django-insecure-ng40)%@94v9rjcrbcm$$s%z4=lee)xn=n5bi@=2m$^_sz9lvn#\nGOOGLE_CLIENT_ID=62932810627-p68t34ecdck99si4tbjl93ookv2prug2.apps.googleusercontent.com\nGOOGLE_CLIENT_SECRET=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"
}
# terraform import google_secret_manager_secret_version.projects_822281553923_secrets_django_settings_versions_1 projects/822281553923/secrets/django_settings/versions/1
resource "google_project_service" "appengine_googleapis_com" {
  project = "822281553923"
  service = "appengine.googleapis.com"
}
# terraform import google_project_service.appengine_googleapis_com 822281553923/appengine.googleapis.com
resource "google_project_service" "appenginereporting_googleapis_com" {
  project = "822281553923"
  service = "appenginereporting.googleapis.com"
}
# terraform import google_project_service.appenginereporting_googleapis_com 822281553923/appenginereporting.googleapis.com
resource "google_project_service" "appengineflex_googleapis_com" {
  project = "822281553923"
  service = "appengineflex.googleapis.com"
}
# terraform import google_project_service.appengineflex_googleapis_com 822281553923/appengineflex.googleapis.com
resource "google_project_service" "bigquery_googleapis_com" {
  project = "822281553923"
  service = "bigquery.googleapis.com"
}
# terraform import google_project_service.bigquery_googleapis_com 822281553923/bigquery.googleapis.com
resource "google_project_service" "bigquerymigration_googleapis_com" {
  project = "822281553923"
  service = "bigquerymigration.googleapis.com"
}
# terraform import google_project_service.bigquerymigration_googleapis_com 822281553923/bigquerymigration.googleapis.com
resource "google_project_service" "bigquerystorage_googleapis_com" {
  project = "822281553923"
  service = "bigquerystorage.googleapis.com"
}
# terraform import google_project_service.bigquerystorage_googleapis_com 822281553923/bigquerystorage.googleapis.com
resource "google_project_service" "cloudapis_googleapis_com" {
  project = "822281553923"
  service = "cloudapis.googleapis.com"
}
# terraform import google_project_service.cloudapis_googleapis_com 822281553923/cloudapis.googleapis.com
resource "google_project_service" "cloudbuild_googleapis_com" {
  project = "822281553923"
  service = "cloudbuild.googleapis.com"
}
# terraform import google_project_service.cloudbuild_googleapis_com 822281553923/cloudbuild.googleapis.com
resource "google_project_service" "clouddebugger_googleapis_com" {
  project = "822281553923"
  service = "clouddebugger.googleapis.com"
}
# terraform import google_project_service.clouddebugger_googleapis_com 822281553923/clouddebugger.googleapis.com
resource "google_project_service" "cloudresourcemanager_googleapis_com" {
  project = "822281553923"
  service = "cloudresourcemanager.googleapis.com"
}
# terraform import google_project_service.cloudresourcemanager_googleapis_com 822281553923/cloudresourcemanager.googleapis.com
resource "google_project_service" "cloudtrace_googleapis_com" {
  project = "822281553923"
  service = "cloudtrace.googleapis.com"
}
# terraform import google_project_service.cloudtrace_googleapis_com 822281553923/cloudtrace.googleapis.com
resource "google_project_service" "compute_googleapis_com" {
  project = "822281553923"
  service = "compute.googleapis.com"
}
# terraform import google_project_service.compute_googleapis_com 822281553923/compute.googleapis.com
resource "google_project_service" "containerregistry_googleapis_com" {
  project = "822281553923"
  service = "containerregistry.googleapis.com"
}
# terraform import google_project_service.containerregistry_googleapis_com 822281553923/containerregistry.googleapis.com
resource "google_project_service" "datastore_googleapis_com" {
  project = "822281553923"
  service = "datastore.googleapis.com"
}
# terraform import google_project_service.datastore_googleapis_com 822281553923/datastore.googleapis.com
resource "google_project_service" "deploymentmanager_googleapis_com" {
  project = "822281553923"
  service = "deploymentmanager.googleapis.com"
}
# terraform import google_project_service.deploymentmanager_googleapis_com 822281553923/deploymentmanager.googleapis.com
resource "google_project_service" "fcm_googleapis_com" {
  project = "822281553923"
  service = "fcm.googleapis.com"
}
# terraform import google_project_service.fcm_googleapis_com 822281553923/fcm.googleapis.com
resource "google_project_service" "firebase_googleapis_com" {
  project = "822281553923"
  service = "firebase.googleapis.com"
}
# terraform import google_project_service.firebase_googleapis_com 822281553923/firebase.googleapis.com
resource "google_project_service" "fcmregistrations_googleapis_com" {
  project = "822281553923"
  service = "fcmregistrations.googleapis.com"
}
# terraform import google_project_service.fcmregistrations_googleapis_com 822281553923/fcmregistrations.googleapis.com
resource "google_project_service" "firebaseappdistribution_googleapis_com" {
  project = "822281553923"
  service = "firebaseappdistribution.googleapis.com"
}
# terraform import google_project_service.firebaseappdistribution_googleapis_com 822281553923/firebaseappdistribution.googleapis.com
resource "google_project_service" "firebasedynamiclinks_googleapis_com" {
  project = "822281553923"
  service = "firebasedynamiclinks.googleapis.com"
}
# terraform import google_project_service.firebasedynamiclinks_googleapis_com 822281553923/firebasedynamiclinks.googleapis.com
resource "google_project_service" "firebasehosting_googleapis_com" {
  project = "822281553923"
  service = "firebasehosting.googleapis.com"
}
# terraform import google_project_service.firebasehosting_googleapis_com 822281553923/firebasehosting.googleapis.com
resource "google_project_service" "firebaseinstallations_googleapis_com" {
  project = "822281553923"
  service = "firebaseinstallations.googleapis.com"
}
# terraform import google_project_service.firebaseinstallations_googleapis_com 822281553923/firebaseinstallations.googleapis.com
resource "google_project_service" "firebaseremoteconfig_googleapis_com" {
  project = "822281553923"
  service = "firebaseremoteconfig.googleapis.com"
}
# terraform import google_project_service.firebaseremoteconfig_googleapis_com 822281553923/firebaseremoteconfig.googleapis.com
resource "google_project_service" "firebaseremoteconfigrealtime_googleapis_com" {
  project = "822281553923"
  service = "firebaseremoteconfigrealtime.googleapis.com"
}
# terraform import google_project_service.firebaseremoteconfigrealtime_googleapis_com 822281553923/firebaseremoteconfigrealtime.googleapis.com
resource "google_project_service" "firestore_googleapis_com" {
  project = "822281553923"
  service = "firestore.googleapis.com"
}
# terraform import google_project_service.firestore_googleapis_com 822281553923/firestore.googleapis.com
resource "google_project_service" "firebaserules_googleapis_com" {
  project = "822281553923"
  service = "firebaserules.googleapis.com"
}
# terraform import google_project_service.firebaserules_googleapis_com 822281553923/firebaserules.googleapis.com
resource "google_project_service" "monitoring_googleapis_com" {
  project = "822281553923"
  service = "monitoring.googleapis.com"
}
# terraform import google_project_service.monitoring_googleapis_com 822281553923/monitoring.googleapis.com
resource "google_project_service" "logging_googleapis_com" {
  project = "822281553923"
  service = "logging.googleapis.com"
}
# terraform import google_project_service.logging_googleapis_com 822281553923/logging.googleapis.com
resource "google_project_service" "identitytoolkit_googleapis_com" {
  project = "822281553923"
  service = "identitytoolkit.googleapis.com"
}
# terraform import google_project_service.identitytoolkit_googleapis_com 822281553923/identitytoolkit.googleapis.com
resource "google_project_service" "people_googleapis_com" {
  project = "822281553923"
  service = "people.googleapis.com"
}
# terraform import google_project_service.people_googleapis_com 822281553923/people.googleapis.com
resource "google_project_service" "oslogin_googleapis_com" {
  project = "822281553923"
  service = "oslogin.googleapis.com"
}
# terraform import google_project_service.oslogin_googleapis_com 822281553923/oslogin.googleapis.com
resource "google_project_service" "pubsub_googleapis_com" {
  project = "822281553923"
  service = "pubsub.googleapis.com"
}
# terraform import google_project_service.pubsub_googleapis_com 822281553923/pubsub.googleapis.com
resource "google_project_service" "mobilecrashreporting_googleapis_com" {
  project = "822281553923"
  service = "mobilecrashreporting.googleapis.com"
}
# terraform import google_project_service.mobilecrashreporting_googleapis_com 822281553923/mobilecrashreporting.googleapis.com
resource "google_project_service" "servicemanagement_googleapis_com" {
  project = "822281553923"
  service = "servicemanagement.googleapis.com"
}
# terraform import google_project_service.servicemanagement_googleapis_com 822281553923/servicemanagement.googleapis.com
resource "google_project_service" "runtimeconfig_googleapis_com" {
  project = "822281553923"
  service = "runtimeconfig.googleapis.com"
}
# terraform import google_project_service.runtimeconfig_googleapis_com 822281553923/runtimeconfig.googleapis.com
resource "google_project_service" "sql_component_googleapis_com" {
  project = "822281553923"
  service = "sql-component.googleapis.com"
}
# terraform import google_project_service.sql_component_googleapis_com 822281553923/sql-component.googleapis.com
resource "google_project_service" "storage_api_googleapis_com" {
  project = "822281553923"
  service = "storage-api.googleapis.com"
}
# terraform import google_project_service.storage_api_googleapis_com 822281553923/storage-api.googleapis.com
resource "google_project_service" "sqladmin_googleapis_com" {
  project = "822281553923"
  service = "sqladmin.googleapis.com"
}
# terraform import google_project_service.sqladmin_googleapis_com 822281553923/sqladmin.googleapis.com
resource "google_project_service" "storage_component_googleapis_com" {
  project = "822281553923"
  service = "storage-component.googleapis.com"
}
# terraform import google_project_service.storage_component_googleapis_com 822281553923/storage-component.googleapis.com
resource "google_project_service" "serviceusage_googleapis_com" {
  project = "822281553923"
  service = "serviceusage.googleapis.com"
}
# terraform import google_project_service.serviceusage_googleapis_com 822281553923/serviceusage.googleapis.com
resource "google_project_service" "secretmanager_googleapis_com" {
  project = "822281553923"
  service = "secretmanager.googleapis.com"
}
# terraform import google_project_service.secretmanager_googleapis_com 822281553923/secretmanager.googleapis.com
resource "google_project_service" "securetoken_googleapis_com" {
  project = "822281553923"
  service = "securetoken.googleapis.com"
}
# terraform import google_project_service.securetoken_googleapis_com 822281553923/securetoken.googleapis.com
resource "google_project_service" "storage_googleapis_com" {
  project = "822281553923"
  service = "storage.googleapis.com"
}
# terraform import google_project_service.storage_googleapis_com 822281553923/storage.googleapis.com
resource "google_project_service" "testing_googleapis_com" {
  project = "822281553923"
  service = "testing.googleapis.com"
}
# terraform import google_project_service.testing_googleapis_com 822281553923/testing.googleapis.com
resource "google_storage_bucket" "eu_artifacts_pulsarinc_alpha_appspot_com" {
  force_destroy            = false
  location                 = "EU"
  name                     = "eu.artifacts.pulsarinc-alpha.appspot.com"
  project                  = "pulsarinc-alpha"
  public_access_prevention = "inherited"
  storage_class            = "STANDARD"
}
# terraform import google_storage_bucket.eu_artifacts_pulsarinc_alpha_appspot_com eu.artifacts.pulsarinc-alpha.appspot.com
resource "google_storage_bucket" "pulsarinc_alpha_appspot_com" {
  force_destroy            = false
  location                 = "EU"
  name                     = "pulsarinc-alpha.appspot.com"
  project                  = "pulsarinc-alpha"
  public_access_prevention = "inherited"
  storage_class            = "STANDARD"
}
# terraform import google_storage_bucket.pulsarinc_alpha_appspot_com pulsarinc-alpha.appspot.com
resource "google_storage_bucket" "pulsarinc_media" {
  force_destroy            = false
  location                 = "EUROPE-WEST1"
  name                     = "pulsarinc_media"
  project                  = "pulsarinc-alpha"
  public_access_prevention = "inherited"
  storage_class            = "STANDARD"
}
# terraform import google_storage_bucket.pulsarinc_media pulsarinc_media
resource "google_storage_bucket" "staging_pulsarinc_alpha_appspot_com" {
  force_destroy = false
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age        = 15
      with_state = "ANY"
    }
  }
  location                 = "EU"
  name                     = "staging.pulsarinc-alpha.appspot.com"
  project                  = "pulsarinc-alpha"
  public_access_prevention = "inherited"
  storage_class            = "STANDARD"
}
# terraform import google_storage_bucket.staging_pulsarinc_alpha_appspot_com staging.pulsarinc-alpha.appspot.com
