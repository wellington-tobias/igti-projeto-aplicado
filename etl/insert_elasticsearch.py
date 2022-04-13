#pip install boto3
#pip install pandas
import boto3
import pandas as pd
def read_from_s3(file_path):
    '''
    to read files from the s3 bucket.
    file_path: refers to the s3 bucket's path for read data.
    '''
    s3 = boto3.client(
                 's3',aws_access_key_id = 'your_access_key_id'
                 ,aws_secret_access_key = 'your_access_key'
                 ,region_name = 'your_region_name'
                 )
    response = s3.get_object(Bucket='your_bucket_name',    Key=file_path)
    df=pd.read_csv(response.get("Body"))
    return df.copy()

from elasticsearch import Elasticsearch
from elasticsearch import helpers
def es_doc_generator(df_final, index_name):
    '''
    to generate elasticsearch document from dataframe
    df_final: processed df
    index_name: the index name that you put to elasticsearch
    '''
    df_iter = df_final.iterrows()
    use_these_keys = df_final.columns
    for index, document in df_iter:
        yield {
               "_index": index_name
               ,"_type": "_doc"
               ,"_id" : f"{document['id']}"
               ,"_source": es_filter_keys(document, use_these_keys)
             }
    print('Document has generated and moved successfully, please create index on kibana to use data at your dashboards')
    return document
def es_filter_keys(document, keys):
    '''
    to generate _source of document from the final df's columns
    '''
    return {key: document[key] for key in keys }
def post_to_ES(df_final,index_name):
    '''
    to put the final dataframe to elasticsearch
    df_final: processed df
    index_name: the index name that you put to elasticsearch
    '''
    es_client = None
    es_client = Elasticsearch(['http://localhost:9200'],http_compress=True)
    if es_client.ping():
        print('Elasticsearch Connection Succesful !')
        helpers.bulk(es_client,     es_doc_generator(df_final,index_name))
    else:
        print('Control the Elasticsearch host, connection unsuccessful ')