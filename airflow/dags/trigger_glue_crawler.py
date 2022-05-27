#Importing core airflow libraries
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import boto3

#Define required function
def trigger_crawler_stg():
    glue_client = boto3.client('glue', region_name='us-east-1')
    response = glue_client.start_crawler(Name='batch_linkedln_jobs')


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['an.a@queensu.ca'],
    'email_on_failure': False,
    'email_on_retry': False
}

with DAG(
    dag_id="trigger_glue_crawler"
    ,default_args=default_args
    ,description="Testing the glue crawler"
    ,schedule_interval=None
) as dag:
    
    trigger_glue_crawler = PythonOperator(task_id = 'trigger_glue_crawler',
                                python_callable = trigger_crawler_stg,
                                dag = dag
                                ) 