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