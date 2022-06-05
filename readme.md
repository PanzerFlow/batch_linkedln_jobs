# Linkedin Jobs ETL (Batch)

- [Linkedin Jobs ETL (Batch)]
  - [1. Introduction](#1-introduction)
  - [2. Design](#2-design)
  - [3. Output](#3-output)
  - [4. Reference](#4-reference)

## 1. Introduction
The goal of this project is to build a data pipeline to **extract and transform Canadian data engineering job postings from Linkedin**. 
The final output of this project is an interactive PowerBI dashboard, which provides an overview of trends in the Canadian data engineering job market. 
The motivation of the project was based on an interest in understanding various trends in the data engineering jobs market and how they evolve. 

This project also provides an excellent opportunity to develop skills and experience in a range of tools. 
As such, the project is more complex than required, utilizing airflow, docker, and a series of AWS technology (S3, EC2,Glue,Athena, lambda).

## 2. Design
### Architecture
<img src="https://github.com/PanzerFlow/batch_linkedln_jobs/blob/main/images/Arch.PNG" width=110% height=110%>

<img src="https://github.com/PanzerFlow/batch_linkedln_jobs/blob/main/images/DAG.PNG" width=100% height=100%>

Components
- Data Publisher
  - The architecture of this project is designed to be event-driven. The pipeline will be triggered once data arrives in S3.
  - Currently, the data source is a cron job that triggers a shell script which then starts a LinkedIn scraper written in python. 

- Cloud Storage
  - A dedicated S3 bucket is used as the cloud storage. There are 3 different folders in this bucket that serves different purposes. 
  - /raw is where the raw data will land in. Any put request in this folder will start an event notification to the lambda function
  - /stg is where the processed data live.
  - /scripts is where the pyspark script is located. There is also an automated GitHub action setup that uploads the script to this location after each git push. 

- Orchestration
  - Airflow is used as the orchestration tool to schedule EMR and glue activity.
  - Airflow is set up using the EC2 instance and docker-compose.
  - S3 event notification and lambda function is used to trigger airflow dag via REST API.

- Compute resources
  - EC2 is used to host the data publisher and airflow. The data publisher can be moved in the future.
  - EMR is used to transform the data once it arrives in /raw.
  - Glue crawler and Athena are used as the compute engine which powers the dashboard. 

- Visualization
  - PowerBI is used for dashboarding


## 3. Output
<img src="https://github.com/PanzerFlow/batch_linkedln_jobs/blob/main/images/Demo Dash.PNG" width=100% height=100%>

## 4. Reference

[How To Install Google Chrome, Selenium & Chromedriver For AWS EC2 Instances](https://understandingdata.com/install-google-chrome-selenium-ec2-aws)

[linkedin-jobs-scraper 1.12.0](https://pypi.org/project/linkedin-jobs-scraper/)
