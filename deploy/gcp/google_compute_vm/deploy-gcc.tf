# This code is compatible with Terraform 4.25.0 and versions that are backward compatible to 4.25.0.
# For information about validating this Terraform code, see https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#format-and-validate-the-configuration

resource "google_compute_instance" "instance-20241211-135046" {
  boot_disk {
    auto_delete = true
    device_name = "instance-20241211-135046"

    initialize_params {
      image = "projects/debian-cloud/global/images/debian-12-bookworm-v20241210"
      size  = 500
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = true
  deletion_protection = false
  enable_display      = false
  hostname            = "insureyourtech.cloud"

  labels = {
    goog-ec-src = "vm_add-tf"
  }

  machine_type = "e2-standard-2"
  name         = "instance-20241211-135046"

  network_interface {
    access_config {
      network_tier           = "PREMIUM"
      public_ptr_domain_name = "insureyourtech.cloud."
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/fuelbigdata-test1/regions/europe-west2/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "1063610512413-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol", "https://www.googleapis.com/auth/trace.append"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  tags = ["http-server", "https-server", "lb-health-check"]
  zone = "europe-west2-a"
}
