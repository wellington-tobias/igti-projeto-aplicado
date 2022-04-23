# Variáveis S3
variable "bucket" {
    default = "datalake-projeto-aplicado"
}

# Variáveis Elasticsearch
variable "domain" {
    type = string
}
variable "instance_type" {
    type = string
}
variable "tag_domain" {
    type = string
}
variable "volume_type" {
    type = string
}
variable "ebs_volume_size" {}

# Variáveis - EC2
variable "key_pair_name" {
    default = "igti-projeto-aplicado"
}

variable "airflow_subnet_id" {
    default = "subnet-08c574adfdb9b16ec"
}

variable "vpc_id" {
    default = "vpc-0c0cad633fa9efa3f"
}