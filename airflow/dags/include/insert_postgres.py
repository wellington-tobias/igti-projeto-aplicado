# Importação Bibliotecas
import awswrangler as wr
import pandas as pd
from datetime import datetime
import pg8000

# Dados S3
s3_bucket_name = 'datalake-projeto-aplicado'
s3_path_origin = 'staging/'

# Leitura e tratamento para inserção no PostgrSQL

# Colunas
column_names = [
    'nr_cnpj_radical', 
    'flag_simples', 
    'dt_opcao_simples', 
    'dt_exclusao_simples',
    'flag_mei',
    'dt_opcao_mei',
    'dt_exclusao_mei',
    'dt_atualizacao'
]

# Leitura
df_postgres = wr.s3.read_parquet(
    f"s3://{s3_bucket_name}/{s3_path_origin}", 
    columns=column_names
)

# Conversão Colunas de Data
cols = ['dt_opcao_simples','dt_exclusao_simples','dt_opcao_mei','dt_exclusao_mei','dt_atualizacao']
df_postgres[cols] = df_postgres[cols].apply(pd.to_datetime, errors='coerce', format='%Y%m%d')

# connect to Postgresql database
conn = pg8000.connect(
    user="postgres",
    host="igti-projeto-aplicado.c1t9xo1yxfi6.us-east-2.rds.amazonaws.com",
    database="pg_projeto_aplicado",
    port=5432,
    password="insert-password-here"
)

# transfer data from DataFrame to PostgreSQL table
wr.postgresql.to_sql(
    df=df_postgres,
    table="tbl_simples_simei",
    schema="pessoa_juridica",
    con=conn
)