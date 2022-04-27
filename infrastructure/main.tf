
# Criação do Datalake - S3
 resource "aws_s3_bucket" "bucket-pa" {
  # Parâmetros de configuração
  bucket = var.bucket
 }
/*
# Envio de arquivo para o bucket
resource "aws_s3_bucket_object" "arquivo_simples_simei" {
  bucket = aws_s3_bucket.bucket-pa.id
  key    = "dados-abertos/F.K03200$W.SIMPLES.CSV.D20312.csv"
  source = "../F.K03200$W.SIMPLES.CSV.D20312.csv"
  etag   = filemd5("../F.K03200$W.SIMPLES.CSV.D20312.csv")
}
*/
# Criação do Elasticsearch - OpenSearch Service
# resource "aws_elasticsearch_domain" "es" {
#   domain_name           = var.domain
#   elasticsearch_version = "7.10"
 
#   cluster_config {
#     instance_type = var.instance_type
#   }

#   ebs_options {
#     ebs_enabled = var.ebs_volume_size > 0 ? true : false
#     volume_size = var.ebs_volume_size
#     volume_type = var.volume_type
#   }
#   tags = {
#     Domain = var.tag_domain
#   }
# }

# Recurso para gerar senha randômica (ficará gravada no terraform.tfstate)
# resource "random_string" "pg-db-password" {
#   length  = 12
#   upper   = true
#   number  = true
#   special = false
# }

# Criação do PostgreSql - RDS 
# resource "aws_db_instance" "default" {
#   allocated_storage    = 20
#   engine               = "postgres"
#   identifier           =  "igti-projeto-aplicado"     
#   engine_version       = "13"
#   instance_class       = "db.t3.micro"
#   db_name              = "pg_projeto_aplicado"
#   username             = "postgres"
#   password             = "random_string.pg-db-password.result"
#   skip_final_snapshot  = true
#   publicly_accessible  = true
# }
