# Provedor para interação com a AWS pela API
provider "aws" {
  region = "us-east-2"
}

# Centralização do controle de estado do Terraform
terraform {
  backend "s3" {
    bucket = "terraform-projeto-aplicado"
    key = "state/pa/terraform.tfstate"
    region = "us-east-2"
  }
}