This repository to host custom data science utilities functions and packages written by Aymone Kouame. Only functions in released packages will be explained below.

## 1 - Package 'gc_temp_tables'
A Python utility packages for creating and querying temporary tables within Google Cloud Environments (https://pypi.org/project/gc-temp-tables/). Functions:

### - `create_bq_session()`
 Allows you to create a session and manipulate tables within that sessions as if they were Google Big Query tables. Read more about GoogleBigQuery sessions here: https://cloud.google.com/bigquery/docs/sessions-intro
 
### - `get_external_table_config(filename_in_bucket)`
 Optional: if using an external table in the query, this function allows you to easily obtain the configurations to be fed into the Google BigQuery client. The file must be located in a Google Cloud Bucket.
 The user can chose the bucket and bucket_directory. The defaults are the Google Cloud Workspace bucket and the root directory of the bucket.

### - `create_temp_table(query)`. 
 Using this function, write a '''CREATE TEMP TABLE''' statement to create a temp table. 
 You can use a session_id and/or external table configuration: `create_temp_table(query, session_id,  ext_table_def_dic = {'table_name':ext-config})`
 
### - `query_temp_table(query)`
You can use a session_id and/or external table configuration: `query_temp_table(query, session_id,  ext_table_def_dic = {'table_name':ext-config})`

### - `delete_temp_table(temp_table)`.
Delete temporary tables that are unsued. Google will auto delete them after 24 hours of being unused.

```
# Example code

# 1.install the package if not already done
pip install gc_temp_tables 

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

# 7. Delete unused temp tables
df = gct.delete_temp_table('example_table', session_id = session_id)
```
Read more about:
- temporary tables: https://cloud.google.com/bigquery/docs/multi-statement-queries#temporary_tables
- external tables: https://cloud.google.com/bigquery/docs/external-tables

