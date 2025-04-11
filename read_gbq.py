import os
from google.cloud import bigquery
client = bigquery.Client()

def BQ(query:str, dataset = os.getenv('WORKSPACE_CDR')):
    
    job_config = bigquery.QueryJobConfig(default_dataset=dataset)
    query_job = client.query(query, job_config =job_config)  # API request
    df = query_job.result().to_dataframe()
        
    return df


#Using an external table
def get_external_table_config(filename_in_bucket, bucket_dir, my_bucket =  os.getenv('WORKSPACE_BUCKET')):
    ext = filename_in_bucket.split('.')[1].upper()
    external_table_config = bigquery.ExternalConfig(ext)
    external_table_config.source_uris = f'{my_bucket}/{bucket_dir}/{filename_in_bucket}'
    external_table_config.autodetect = True #[bigquery.SchemaField('person_id', 'INTEGER') ]
    external_table_config.options.skip_leading_rows = 1
    
    return external_table_config

def BQ(query:str, ext_table_def_dic = {} #FORMAT ={'table_name': external_table_config}
       , dataset = os.getenv('WORKSPACE_CDR')):
    
    job_config = bigquery.QueryJobConfig(default_dataset=dataset, table_definitions = ext_table_def_dic)
    query_job = client.query(query, job_config =job_config)  # API request
    df = query_job.result().to_dataframe()
        
    return df
