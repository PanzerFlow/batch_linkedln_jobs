#!/bin/bash

#Start up the docker compose containers
cd /home/ubuntu/development/batch_linkedln_jobs/airflow
docker-compose up -d #docker-compose restart -d
sleep 2m #Sleep to make sure containers are in health state
echo "Airflow is running"

#Copying the local AWS CLI config into airflow continaer as a connection
AWS_ACCESS_KEY=`aws configure get aws_access_key_id`
AWS_SECERT=`aws configure get aws_secret_access_key`
AWS_REGION=`aws configure get region`
echo "Adding aws connections to the Airflow connection param"
docker exec -d airflow_airflow-webserver_1 airflow connections add 'aws_default' \
--conn-type 'aws' --conn-login $AWS_ACCESS_KEY --conn-password $AWS_SECERT \
--conn-extra '{"region_name":"'$AWS_REGION'"}'
