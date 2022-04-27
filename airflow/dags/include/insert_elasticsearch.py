# Importação Bibliotecas
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import awswrangler as wr
import pandas as pd

# Dados para conexão
host = 'search-igti-projeto-aplicado-zsn2tt2u3zhcj37wq4faqqpofe.us-east-2.es.amazonaws.com'
region = 'us-east-2'

# Parâmetros de conexão
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Função pra conexão
search = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

# delete index if exists
wr.opensearch.delete_index(
    client=search,
    index="pessoa_juridica_simples_simei"
)

# Criação do Índice
wr.opensearch.create_index(
    client=search,
    index="pessoa_juridica_simples_simei",
    mappings={
         "dynamic_templates" : [
            {
                "dates" : {
                   "match" : "dt*",
                    "mapping" : {
                        "type" : "date",
                        "format" : 'dateOptionalTime'
                    }
                }
            }
        ]
    }   
)

# Leitura e tratamento para inserção no Elasticsearch

# Dados S3
s3_bucket_name = 'datalake-projeto-aplicado'
s3_path_origin = 'staging/'

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
df_elastic = wr.s3.read_parquet(
    f"s3://{s3_bucket_name}/{s3_path_origin}", 
    columns=column_names
)

# Conversão Colunas de Data
cols = ['dt_opcao_simples','dt_exclusao_simples','dt_opcao_mei','dt_exclusao_mei','dt_atualizacao']
df_elastic[cols] = df_elastic[cols].apply(pd.to_datetime, errors='coerce', format='%Y%m%d')


# Inserir dados do Dataframe
wr.opensearch.index_df(
    search,
    df=df_elastic,
    index="pessoa_juridica_simples_simei",
    bulk_size=1000000
)