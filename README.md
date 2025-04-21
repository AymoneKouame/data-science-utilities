This repository hosts custom data science utilities functions and packages written by Aymone Kouame. Only released packages will be explained below.

## 1 - Package 'gc_temp_tables'
A Python utility packages for creating and querying temporary tables within Google Cloud Environments (https://pypi.org/project/gc-temp-tables/). Functions and arguments:

### * `create_bq_session()`
Allows you to create a session and interactively query temp tables within that session.
 
### * `get_external_table_config(filename_in_bucket)`
If using an external table (or federated table) in the query, this function allows the user to easily obtain the configurations to be fed into the query job configurations. Currently, the external data must be located in a Google Cloud Bucket. The supported files are CSV, PARQUET, JSON, ORC, and Avro.Future releases will add options for Google sheets, bigtables, Spanner external dataset and AWS Glue federated dataset.
- **'filename_in_bucket'** (required): A string. The name of the file in the external storage, including extension.
- 'bucket': A string. The name of the bucket where the external file is located ('gs://bucketname'). The default is the All of Us Google Workspace bucket.
- 'bucket_directory': A string. The name of the directory within the bucket where the external file is located. The default is the root bucket directory.

### * `create_temp_table(query)`. 
Function to create a temp table. You can use a session_id and/or external table configuration as follows `create_temp_table(query, session_id,  ext_table_def_dic = {'table_name':ext-config})`
- **'query'** (required): A string. A '''CREATE TEMP TABLE''' sql statement.
- 'dataset': A string . If using a BigQuery table in the query, define the dataset project and name ('project_id.dataset_name'). The default is the All of Us Google Workspace dataset project and name. 
- 'session_id': A string. If using a session, the unique id of the session obtained using `create_bq_session()`.
- 'ext_table_def_dic': A dictionary {'external_table_name':ext_table_config}. If using an external table, the desired name of the external table to use in the query as well as the configuration obtained using `get_external_table_config()`

### * `query_temp_table(query)`
Using this function, query the temporary table as you would any Google BigQuery dataset.
You can use a session_id and/or external table configuration as follows `query_temp_table(query, session_id,  ext_table_def_dic = {'table_name':ext-config})`
- **'query'** (required): A string. A SQL statement.
- 'dataset': A string . If using a BigQuery table in the query, define the dataset project and name ('project_id.dataset_name'). The default is the All of Us Google Workspace dataset project and name. 
- 'session_id': A string. If using a session, the unique id of the session obtained using `create_bq_session()`.
- 'ext_table_def_dic': A dictionary {'external_table_name':ext_table_config}. If using an external table, the desired name of the external table to use in the query as well as the configuration obtained using `get_external_table_config()`
  
### * `drop_temp_table(temp_table)`.
Delete temporary tables that are unsued (recommended). Google will auto delete them after 24 hours of being unused. 
- **'temp_table'** (required): A string. The name of the temporary table to delete. PLEASE USE with caution.
- 'session_id': A string. If using a session, the unique id of the session obtained using `create_bq_session()`.

### Example code
```
# 1.install the package if not already done
pip install --upgrade gc_temp_tables 

# 2. import the module
from gc_temp_tables import gc_temp_tables as gct

# 3. create/initialize a session 
session_id = gct.create_bq_session()

# 5. create a temporay table from an external file

## 5.a Grab external table configuration
ext_config = gct.get_external_table_config(filename_in_bucket='example.parquet')

## 5.b Create table
gct.create_temp_table(f'''CREATE TEMP TABLE example_table AS (SELECT * FROM example)'''
		       , ext_table_def_dic = {example: ext_config}, session_id = session_id)

# 6. query the table and join with another table in Google Big Query
df = gct.query_temp_table(f'''
	SELECT t.*,  age
	FROM example_table
	JOIN person USING(person_id)''', session_id = session_id)

# 7. Drop unused temp tables
df = gct.drop_temp_table('example_table', session_id = session_id)
```
Read more about:
- Google BigQuery sessions: https://cloud.google.com/bigquery/docs/sessions-intro
- temporary tables: https://cloud.google.com/bigquery/docs/multi-statement-queries#temporary_tables
- external tables: https://cloud.google.com/bigquery/docs/external-tables

