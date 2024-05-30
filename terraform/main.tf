resource "docker_image" "postgres" {
  name         = "postgres:latest"
  keep_locally = true
}


resource "docker_image" "airflow" {
  name         = "apache/airflow:2.9.1"
  keep_locally = true
}

resource "docker_container" "postgres" {
  image = docker_image.postgres.name
  name  = "mono_local_db"
  env = ["POSTGRES_PASSWORD=${var.local_db_password}"]
  ports {
    internal = 5432
    external = var.postgres_external_port
  }
}



