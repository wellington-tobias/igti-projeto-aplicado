# Importação Bibliotecas
import awswrangler as wr
import boto3
import pandas as pd
from datetime import datetime

# Dados S3
s3_bucket_name = 'datalake-projeto-aplicado'
s3_file_origin = 'raw/amostra.csv'
s3_path_destiny = 'staging/'

# Colunas
column_names = [
    'nr_cnpj_radical', 
    'flag_simples', 
    'dt_opcao_simples', 
    'dt_exclusao_simples',
    'flag_mei',
    'dt_opcao_mei',
    'dt_exclusao_mei'
]

# Leitura
df_wrangler = wr.s3.read_csv(f"s3://{s3_bucket_name}/{s3_file_origin}", sep=';', names=column_names)

# Adição coluna dt_atualizacao
df_wrangler['dt_atualizacao'] = pd.to_datetime('today').strftime("%Y%m%d")

# Gravação
wr.s3.to_parquet(
    df=df_wrangler,
    path=f"s3://{s3_bucket_name}/{s3_path_destiny}",
    dataset=True,
    mode="overwrite"
)