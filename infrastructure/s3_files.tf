# Envio de arquivo para o bucket
# resource "aws_s3_bucket_object" "job_spark" {
#   bucket = aws_s3_bucket.bucket-pa.id
#   key    = "emr-code/pyspark/job_spark.py"
#   source = "../job_spark.py"
#   etag   = filemd5("../job_spark.py")
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