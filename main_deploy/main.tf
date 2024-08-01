provider "google" {
  credentials = file("datahub-project-430801-c216773b2d70.json")
  project     = "datahub-project-430801"
  region      = "asia-southeast1"
}

resource "google_compute_instance" "default" {
  name         = "aksesoris-pria-vm"
  machine_type = "e2-standard-2"
  zone         = "asia-southeast1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  service_account {
    email = "terraform-sa@datahub-project-430801.iam.gserviceaccount.com"
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  scheduling{
    preemptible = true
    automatic_restart = false
    provisioning_model = "SPOT"
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    echo "hello"
    apt-get update
    apt-get install -y docker.io
    gsutil -m cp -r gs://data_scrap_azhar/base_with_docker/vm_config/aksesoris_pria /home
    cd /home/aksesoris_pria
    sudo docker build -t my-app .
    sudo docker run -d -it my-app
    echo "hello end"
  EOF
}

resource "google_compute_instance" "default2" {
  name         = "aksesoris-wanita-vm"
  machine_type = "e2-standard-2"
  zone         = "asia-southeast1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  service_account {
    email = "terraform-sa@datahub-project-430801.iam.gserviceaccount.com"
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  scheduling{
    preemptible = true
    automatic_restart = false
    provisioning_model = "SPOT"
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    echo "hello"
    apt-get update
    apt-get install -y docker.io
    gsutil -m cp -r gs://data_scrap_azhar/base_with_docker/vm_config/aksesoris_wanita /home
    cd /home/aksesoris_wanita
    sudo docker build -t my-app .
    sudo docker run -d -it my-app
    echo "hello end"
  EOF
}



resource "google_compute_instance" "default3" {
  name         = "atasan-pria-vm"
  machine_type = "e2-standard-2"
  zone         = "asia-southeast1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  service_account {
    email = "terraform-sa@datahub-project-430801.iam.gserviceaccount.com"
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  scheduling{
    preemptible = true
    automatic_restart = false
    provisioning_model = "SPOT"
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    echo "hello"
    apt-get update
    apt-get install -y docker.io
    gsutil -m cp -r gs://data_scrap_azhar/base_with_docker/vm_config/atasan_pria /home
    cd /home/atasan_pria
    sudo docker build -t my-app .
    sudo docker run -d -it my-app
    echo "hello end"
  EOF
}




resource "google_compute_instance" "default4" {
  name         = "atasan-wanita-vm"
  machine_type = "e2-standard-2"
  zone         = "asia-southeast1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  service_account {
    email = "terraform-sa@datahub-project-430801.iam.gserviceaccount.com"
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  scheduling{
    preemptible = true
    automatic_restart = false
    provisioning_model = "SPOT"
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    echo "hello"
    apt-get update
    apt-get install -y docker.io
    gsutil -m cp -r gs://data_scrap_azhar/base_with_docker/vm_config/atasan_wanita /home
    cd /home/atasan_wanita
    sudo docker build -t my-app .
    sudo docker run -d -it my-app
    echo "hello end"
  EOF
}




