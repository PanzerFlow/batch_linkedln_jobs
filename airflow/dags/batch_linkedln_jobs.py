#Importing supporting libraries
import boto3

#Importing core airflow libraries
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

#Importing airflow emr operators
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.contrib.operators.emr_terminate_job_flow_operator import EmrTerminateJobFlowOperator

JOB_FLOW_OVERRIDES = {
    "Name": "Batch Project EMR 220526001",
    "ReleaseLabel": "emr-5.29.0",
    "Applications": [{"Name": "Hadoop"}, {"Name": "Spark"}],
    "Configurations": [
        {
            "Classification": "spark-env",
            "Configurations": [
                {
                    "Classification": "export",
                    "Properties": {"PYSPARK_PYTHON": "/usr/bin/python3"},
                }
            ],
        }
    ],
    "Instances": {
        "Ec2KeyName" : "Ec2KEY_PersonalProject", #Use your own key here
        "InstanceGroups": [
            {
                "Name": "Master node",
                "Market": "SPOT",
                "InstanceRole": "MASTER",
                "InstanceType": "m4.xlarge",
                "InstanceCount": 1,
            },
            {
                "Name": "Core - 2",
                "Market": "SPOT",
                "InstanceRole": "CORE",
                "InstanceType": "m4.xlarge",
                "InstanceCount": 2,
            },
        ],
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
    },
    "JobFlowRole": "EMR_EC2_DefaultRole",
    "ServiceRole": "EMR_DefaultRole",
}

SPARK_STEPS = [
    {
        'Name': 'Process linkedln jobs data',
        'ActionOnFailure': "CONTINUE",
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            "Args": [
                    '/usr/bin/spark-submit'
                    ,'--py-files','s3://linkedln-jobs-etl/scripts/pyspark_script.zip'
                    ,'s3://linkedln-jobs-etl/scripts/workflow_entry.py'
                    ,'-p', "{'input_path': '{{task_instance.xcom_pull(task_ids='parse_request', key='s3location')}}', 'name': 'pyspark_test', 'file_type': 'linkedln', 'output_path': 's3://linkedln-jobs-etl/stg/jobs_{{ds}}/', 'partition_column': 'date'}"
                ]
        }
    }
]

"""
Local version of spark submit, tested
    bin/spark-submit 
    --master local 
    --py-files /home/ubuntu/development/spark-repos/test_pyspark_linkedln/job.zip /home/ubuntu/development/spark-repos/test_pyspark_linkedln/workflow_entry.py 
    -p "{'input_path': '/home/ubuntu/development/spark-repos/test_pyspark_linkedln/temp.json', 'name': 'pyspark_test', 'file_type': 'linkedln', 'output_path': '/home/ubuntu/development/spark-repos/test_pyspark_linkedln/linkedln_data', 'partition_column': 'date'}"
"""

#Define required function
def retrieve_s3_files(**kwargs):
    s3_location = kwargs['dag_run'].conf['s3_location']
    kwargs['ti'].xcom_push(key = 's3location', value = s3_location)

def trigger_crawler_stg():
    glue_client = boto3.client('glue', region_name='us-east-1')
    response = glue_client.start_crawler(Name='batch_linkedln_jobs')

#Create default args for each task

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['an.a@queensu.ca'],
    'email_on_failure': False,
    'email_on_retry': False
}

with DAG(
    dag_id="batch_linkedln_jobs"
    ,default_args=default_args
    ,description="Batch processing json with emr"
    ,schedule_interval=None
) as dag:
    
    start_of_data_pipeline = DummyOperator(task_id="start_of_data_pipeline")

    parse_request = PythonOperator(task_id = 'parse_request',
                                provide_context = True, # Airflow will pass a set of keyword arguments that can be used in your function
                                python_callable = retrieve_s3_files,
                                dag = dag
                                ) 

    create_emr_cluster = EmrCreateJobFlowOperator(
                                task_id = "create_emr_cluster"
                                ,job_flow_overrides = JOB_FLOW_OVERRIDES
                                ,aws_conn_id="aws_default"
                                )


    add_emr_steps = EmrAddStepsOperator(
        task_id = "add_emr_steps"
        ,job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}"
        ,aws_conn_id="aws_default"
        ,steps=SPARK_STEPS
    )

    last_step = len(SPARK_STEPS) - 1 #last step of the spark script

    # wait for the steps to complete
    check_emr_step = EmrStepSensor(
        task_id="check_emr_step",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull(task_ids='add_emr_steps', key='return_value')["
        + str(last_step)
        + "] }}",
        aws_conn_id="aws_default"
    )

    # Terminate the EMR cluster
    terminate_emr_cluster = EmrTerminateJobFlowOperator(
        task_id="terminate_emr_cluster",
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
        aws_conn_id="aws_default"
    )
    
    trigger_glue_crawler = PythonOperator(task_id = 'trigger_glue_crawler',
                                python_callable = trigger_crawler_stg,
                                dag = dag
                                ) 

    end_of_data_pipeline = DummyOperator(task_id="end_of_data_pipeline")
    
    
    #Define Pipeline tasks dependency 
    start_of_data_pipeline >> parse_request >> create_emr_cluster >> add_emr_steps >> check_emr_step >> terminate_emr_cluster >> trigger_glue_crawler >> end_of_data_pipeline
"""
Remove the options for

/usr/bin/spark-submit --py-files s3://linkedln-jobs-etl/scripts/pyspark_script.zip s3://linkedln-jobs-etl/scripts/workflow_entry.py -p "{'input_path': 's3://linkedln-jobs-etl/raw/linkedln_jobs_de_canada_20220526_23.json', 'name': 'pyspark_test', 'file_type': 'linkedln', 'output_path': 's3://linkedln-jobs-etl/stg/jobs/', 'partition_column': 'date'}"
"""