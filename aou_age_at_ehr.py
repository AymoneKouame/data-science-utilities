import pandas as pd
import os
from google.cloud import bigquery
client = bigquery.Client()

# Function to query GBQ
def BQ(query:str, dataset = os.getenv('WORKSPACE_CDR')):
    
    job_config = bigquery.QueryJobConfig(default_dataset=dataset)
    query_job = client.query(query, job_config =job_config)  # API request
    df = query_job.result().to_dataframe()
        
    return df

# Function to get age at EHR per EHR domain.
# See usage example at the end
def age_at_ehr(ehr_domain, cohort_pid_list:list=[], add_columns = ''):
    
    ehr_domain = ehr_domain.lower()
    queries_dd = {
    'measurement': f"""
        SELECT DISTINCT person_id, measurement_concept_id
        , DATE_DIFF(measurement_date, dob, YEAR) as age_at_measurement, {add_columns}
        FROM measurement
        JOIN measurement_ext USING(measurement_id)
        JOIN cb_search_person USING(person_id)
        WHERE LOWER(src_id) LIKE '%ehr%' 
        """,
     
    'condition': f"""
        SELECT DISTINCT person_id, condition_concept_id
        , DATE_DIFF(condition_start_date, dob, YEAR) as age_at_condition_start
        , DATE_DIFF(condition_end_date, dob, YEAR) as age_at_condition_end, {add_columns}
        FROM condition_occurrence
        JOIN condition_occurrence_ext using(condition_occurrence_id)
        JOIN cb_search_person USING(person_id)
        WHERE LOWER(src_id) LIKE '%ehr%'
         """,

    'device': f""" 
        SELECT DISTINCT person_id, device_concept_id
        , DATE_DIFF(device_exposure_start_date, dob, YEAR) as age_at_device_start
        , DATE_DIFF(device_exposure_end_date, dob, YEAR) as age_at_device_end, {add_columns}
        FROM device_exposure
        JOIN device_exposure_ext using(device_exposure_id)
        JOIN cb_search_person USING(person_id)
        WHERE LOWER(src_id) LIKE '%ehr%'""",
     
    'drug': f"""
        SELECT DISTINCT person_id, drug_concept_id
        , DATE_DIFF(drug_exposure_start_date, dob, YEAR) as age_at_drug_start
        , DATE_DIFF(drug_exposure_end_date, dob, YEAR) as age_at_drug_end, {add_columns}
        FROM drug_exposure
        JOIN drug_exposure_ext USING(drug_exposure_id)
        JOIN cb_search_person USING(person_id)
        WHERE LOWER(src_id) LIKE '%ehr%'
        """,
     
    'observation': f"""
        SELECT DISTINCT person_id
        , observation_concept_id, observation_concept_id
        , DATE_DIFF(observation_date, dob, YEAR) as age_at_observation, {add_columns}
        FROM observation
        JOIN observation_ext USING(observation_id)
        JOIN cb_search_person USING(person_id)
        WHERE LOWER(src_id) LIKE '%ehr%'""",
     
    'procedure': f"""
        SELECT DISTINCT person_id, procedure_concept_id
        , DATE_DIFF(procedure_date, dob, YEAR) as age_at_procedure, {add_columns}
        FROM procedure_occurrence
        JOIN procedure_occurrence_ext USING(procedure_occurrence_id)
        JOIN cb_search_person USING(person_id)
        WHERE LOWER(src_id) LIKE '%ehr%'
        """,
     
    'visit': f"""
        SELECT DISTINCT person_id
        , visit_concept_id
        , DATE_DIFF(visit_start_date, dob, YEAR) as age_at_visit_start
        , DATE_DIFF(visit_end_date, dob, YEAR) as age_at_visit_end, {add_columns}
        FROM visit_occurrence
        JOIN visit_occurrence_ext USING(visit_occurrence_id)
        JOIN cb_search_person USING(person_id)
        WHERE LOWER(src_id) LIKE '%ehr%'
        """
    }
    
    QUERY = queries_dd[ehr_domain]
    print('Base query:\n' + QUERY)
    if cohort_pid_list.empty == False:
        cohort_pid_list = list(set(cohort_pid_list))
        print(f'''
NOTE: The query might break if your cohort size is too large. 
You have {len(cohort_pid_list)} participants in the cohort.''')
        cohort_pid_tp = tuple(cohort_pid_list)
        QUERY = QUERY+f' AND person_id IN {cohort_pid_tp}'

    df = BQ(QUERY)
    return df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Example ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
##basic usage
ages_at_condition = age_at_ehr(ehr_domain = 'condition')

##filter age data for cohort
mycohort = BQ('''SELECT DISTINCT person_id, race from cb_search_person where age_at_cdr =18''')
ages_at_condition_for_cohort = age_at_ehr(ehr_domain = 'condition', cohort_pid_list = mycohort['person_id'])

##filter age data for cohort - add additional column(s) to the returned table
ages_at_condition_for_cohort = age_at_ehr(ehr_domain = 'condition'
                                          , add_columns ='condition_start_date'
                                          , cohort_pid_list = mycohort['person_id'])

    
