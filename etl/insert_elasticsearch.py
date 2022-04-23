# Importação Bibliotecas
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import awswrangler as wr

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
# wr.opensearch.delete_index(
#     client=search,
#     index="pessoa_juridica_simples_simei"
    
# )

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
                        "format" : 'yyyy-MM-dd'
                    }
                }
            }
        ]
    }   
)

# Leitura e tratamento para inserção no Elasticsearch

# Colunas
column_name = [
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
df_file = pd.read_csv(
    f"s3://{s3_bucket_name}/{s3_file}",
    names = column_name#, 
    #parse_dates=['dt_opcao_simples','dt_exclusao_simples','dt_opcao_mei','dt_exclusao_mei','dt_atualizacao']
)

# Tratamento
df_file = (
    df_file
    .replace({np.nan: None})
)

# Inserir dados do Dataframe
wr.opensearch.index_df(
    search,
    df=df_file,
    index="pessoa_juridica_simples_simei",
    bulk_size=1000
)