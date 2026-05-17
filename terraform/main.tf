terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
    }
  }
}

provider "docker" {
  host = "npipe:////.//pipe//docker_engine"
}

resource "docker_image" "bugtracker_image" {
  name = "bug-tracker:terraform"

  build {
    context = ".."
  }
}

resource "docker_container" "bugtracker_container" {
  image = docker_image.bugtracker_image.image_id
  name  = "bug-tracker-terraform"

  ports {
    internal = 5000
    external = 5001
  }
}