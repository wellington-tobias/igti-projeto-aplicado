# Importação bibliotecas
import psycopg2
import pandas as pd

# Leitura
df = pd.read_csv('local')

# Função p/ inserir dados
def copy_query(c, file_path, table_name, cols_tuple):
    schema = 'projeto_aplicado',
    schema_table = schema+table_name
    with open(file_path, 'r') as f:
        c.copy_from(f, schema_table, sep=',', null='null', columns=cols_tuple)

# Teste
file_p = 'caminho do arquivo de origem'
table_n = 'tabela de destino'
cols_t = 'lista de colunas'

# Função para conectar no PostgreSQL
try:
    connection = psycopg2.connect(user = 'postgres',
                                  password = 'oUVaT34DxFJc',
                                  host = 'igti-projeto-aplicado.c1t9xo1yxfi6.us-east-2.rds.amazonaws.com',
                                  port = '5432',
                                  database = 'pg_projeto_aplicado')
    
    cursor = connection.cursor()
    # Insert
    copy_query(cursor, file_p, table_n, cols_t)
    # Commit
    connection.commit()

except(Exception, psycopg2.Error) as erro:
    print("Erro de conexão ao PostgreSQL", erro)

finally:
    if(connection):
        cursor.close()
        connection.close()