# Importação das Bibliotecas
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType
from pyspark.sql.functions import *
from pyspark.sql import SparkSession

# Criação da sessão do Spark
spark = (
    SparkSession.builder.appName("amostraSpark")
    .getOrCreate()
)


# Definição do Schema
schema = StructType([
    StructField("nr_cnpj_radical", IntegerType(), True),
    StructField("flag_simples", StringType(), True),
    StructField("dt_opcao_simples", StringType(), True),
    StructField("dt_exclusao_simples", StringType(), True),
    StructField("flag_mei", StringType(), True),
    StructField("dt_opcao_mei", StringType(), True),
    StructField("dt_exclusao_mei", StringType(), True)
])

# Ler os dados do arquivo
simples = (
    spark
    .read
    .format("csv")
    .option("header", False)
    .schema(schema)
    .option("delimiter", ";")
    .load("s3://datalake-projeto-aplicado/raw/F.K03200$W.SIMPLES.CSV.D20312.csv")
)

# Dataframe contendo colunas convertidas e nova coluna
df_completo = (
    simples
    .withColumn('dt_opcao_simples', to_date(col('dt_opcao_simples'),'yyyyMMdd'))
    .withColumn('dt_exclusao_simples', to_date(col('dt_exclusao_simples'),'yyyyMMdd'))
    .withColumn('dt_opcao_mei', to_date(col('dt_opcao_mei'),'yyyyMMdd'))
    .withColumn('dt_exclusao_mei', to_date(col('dt_exclusao_mei'),'yyyyMMdd'))
    .withColumn('dt_atualizacao', date_format(current_timestamp(), 'yyyy-MM-dd'))
)


# Gravação do Arquivo 
(
    df_completo
    .write
    .mode("overwrite")
    .format("parquet")
    .save("s3://datalake-projeto-aplicado/staging/")
)