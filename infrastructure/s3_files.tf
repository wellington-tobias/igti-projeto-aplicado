# Envio de arquivo para o bucket
# resource "aws_s3_bucket_object" "etl_simples_simei" {
#   bucket = aws_s3_bucket.bucket-pa.id
#   key    = "etl/etl_simples_simei.py"
#   source = "../airflow/dags/etl_simples_simei.py"
#   etag   = filemd5("../airflow/dags/etl_simples_simei.py")
# }

# resource "aws_s3_bucket_object" "processa_dados_brutos" {
#   bucket = aws_s3_bucket.bucket-pa.id
#   key    = "etl/process_raw_data.py"
#   source = "../airflow/dags/include/process_raw_data.py"
#   etag   = filemd5("../airflow/dags/include/process_raw_data.py")
# }

# resource "aws_s3_bucket_object" "insere_postgres" {
#   bucket = aws_s3_bucket.bucket-pa.id
#   key    = "etl/insert_postgres.py"
#   source = "../airflow/dags/include/insert_postgres.py"
#   etag   = filemd5("../airflow/dags/include/insert_postgres.py")
# }

# resource "aws_s3_bucket_object" "insere_elasticsearch" {
#   bucket = aws_s3_bucket.bucket-pa.id
#   key    = "etl/insert_elasticsearch.py"
#   source = "../airflow/dags/include/insert_elasticsearch.py"
#   etag   = filemd5("../airflow/dags/include/insert_elasticsearch.py")
# }