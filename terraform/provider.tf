terraform {
  required_version = ">= 0.14.6"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.16.0"
    }

  }
}


provider "docker" {
  host = "unix:///var/run/docker.sock"
}

