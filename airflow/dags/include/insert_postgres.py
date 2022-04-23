# Importação Bibliotecas
import boto3
import pandas as pd
import sys
import sys
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import psycopg2.extras as extras
import numpy as np

# Acesso ao Bucket do S3
s3_client = boto3.client('s3')
s3_bucket_name = 'datalake-projeto-aplicado'
s3_file = 'staging/part-00000-21980f01-bc09-4390-9cbc-ab96a20f518b-c000.csv'
credentials = boto3.Session().get_credentials()
s3 = boto3.resource('s3',
                    credentials.access_key,
                    credentials.secret_key
                    )

# Leitura e tratamento para inserção no PostgrSQL

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
    names = column_name, 
    parse_dates=['dt_opcao_simples','dt_exclusao_simples','dt_opcao_mei','dt_exclusao_mei','dt_atualizacao']
)

# Tratamento
df_file = (
    df_file
    .replace({pd.NaT: None})
)

# Funções criadas para o processo

# Função para tratamento e parse das exceções da biblioteca psycopg2
def show_psycopg2_exception(err):
    
    # Detalhes da exceção
    err_type, err_obj, traceback = sys.exc_info()    
    
    # Linha que ocorreu a exceção
    line_n = traceback.tb_lineno    
    
    # Print do erro
    print ("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type) 
    
    # Dados adicionais do psycopg2 extensions.Diagnostics 
    print ("\nextensions.Diagnostics:", err.diag)    
    
    # Print do pgcode e pgerror
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    
# Função de conexão ao PostgreSQL
def connect(conn_params_dic):
    conn = None
    try:
        print('Conectando ao PostgreSQL...')
        conn = psycopg2.connect(**conn_params_dic)
        print("Conexão realizada com sucesso...")
        
    except OperationalError as err:
        # Exceção
        show_psycopg2_exception(err)        
        # Em caso de erro, conexão = None
        conn = None
    return conn

# Função para inserir o dataframe através do psycopg2.extras.execute_values()
def execute_values(conn, datafrm, table):
    
    # Criação de uma lista de tuplas do dataframe
    tpls = [tuple(x) for x in datafrm.to_numpy()]
    
    # Colunas separadas por vírgula
    cols = ','.join(list(datafrm.columns))
    
    # Insert
    sql = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, sql, tpls)
        conn.commit()
        print("Dados inseridos através do execute_values() com sucesso.")
    except (Exception, psycopg2.DatabaseError) as err:
        # Exceção
        show_psycopg2_exception(err)
        cursor.close()

# Parâmetros da conexão
conn_params_dic = {
    "host"      : "igti-projeto-aplicado.c1t9xo1yxfi6.us-east-2.rds.amazonaws.com",
    "database"  : "pg_projeto_aplicado",
    "user"      : "postgres",
    "password"  : "oUVaT34DxFJc"
}
# Conectar ao banco de dados
conn = connect(conn_params_dic)
conn.autocommit = True

# Excecutar a ingestão dos dados
execute_values(conn, df_file, 'pessoa_juridica.tbl_simples_simei')