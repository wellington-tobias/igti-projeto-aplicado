from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import boto3
from airflow.models import Variable

aws_access_key_id = Variable.get("aws_access_key_id")
aws_secret_access_key = Variable.get("aws_secret_access_key")

s3client = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

default_args = {
    'owner': 'Wellington Tobias',
    "depends_on_past": False,
    "start_date": days_ago(2),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False
}


with DAG(
    dag_id='ETL-Simples-Simei',
    description="Processamento Simples/Simei Dados Abertos",
    default_args=default_args, 
    schedule_interval=None, 
    catchup=False,
) as dag:

    process_raw_data = BashOperator(
        task_id='process_raw_data',
        bash_command='python /usr/local/airflow/dags/include/process_raw_data.py',
    )
    insert_postgres = BashOperator(
        task_id='insert_postgres',
        bash_command='python /usr/local/airflow/dags/include/insert_postgres.py',
    )
    insert_elasticseach = BashOperator(
        task_id='insert_elasticsearch',
        bash_command='python /usr/local/airflow/dags/include/insert_elasticsearch.py',
    )

    process_raw_data >> [insert_postgres, insert_elasticseach]
    