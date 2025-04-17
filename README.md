# data-science-utilities
A repository to host data science utilities custom packages.

# `gc_temp_tables`
A Python utility packages for creating and querying temporary tables within Google Cloud Environments. Functions:
 ## `create_bq_session()`
 Allows you to create a session and manipulate tables within that sessions as if they were Google Big Query tables. Read more about GoogleBigQuery sessions here: https://cloud.google.com/bigquery/docs/sessions-intro
 
 ## `get_external_table_config(filename_in_bucket)`
 Optional: if using an external table in the query, this function allows you to easily obtain the configurations to be fed into the Google BigQuery client. The file must be located in a Google Cloud Bucket.
 The user can chose the bucket and bucket_directory. The defaults are the Google Cloud Workspace bucket and the root directory of the bucket.

 ## `create_temp_table(query)`. 
 Using this function, write a query using a '''CREATE TEMP TABLE''' statement to create a temp table. 
 You can use a session_id and/or external table configuration: `create_temp_table(query, session_id,  ext_table_def_dic = {'table_name':ext-config})`
 
 ## `query_temp_table(query)`
You can use a session_id and/or external table configuration: `query_temp_table(query, session_id,  ext_table_def_dic = {'table_name':ext-config})`

## `delete_temp_table(temp_table)`.
Delete temporary tables that are unsued. Google will auto delete them after 24 hours of being unused.

Read more about temporary tables here: https://cloud.google.com/bigquery/docs/multi-statement-queries#temporary_tables

