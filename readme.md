# Linkedin Jobs ETL (Batch)

- [Linkedin Jobs ETL (Batch)](#beginner-de-project---batch-edition)
  - [1. Introduction](#1-introduction)
  - [2. Design](#2-design)
  - [3. Output](#3-output)
  - [4. Setup](#4-setup)
    - [4.1 Prerequisite](#41-prerequisite)
  - [5. Reference](#5-reference)

## 1. Introduction
The goal of this project is to build a data pipeline to **extract canadian data engineering job postings from Linkedin**. 
The final output of this project is an interactive PowerBI dashboard, which provides an overview of trends in canadian data engineering job market. 
The motivation was based on an interest in understanding various trends in the data engineering jobs market and how they evolve. 

This project also provides a good opportunity to develop skills and experience in a range of tools. 
As such, the project is more complex than required, utilising airflow, docker and a series of aws technology (S3,EC2,Glue,Atehna,lambda).

## 2. Design

This data pipeline will be 
Classifying movie reviews with Apache Spark.
Loading the classified movie reviews into the data warehouse.
Extract user purchase data from an OLTP database and load it into the data warehouse.
Joining the classified movie review data and user purchase data to get user behavior metric data.


Data Publisher >> S3 Raw >> Lambda >> Airflow >> EMR >> S3 Stage >> Glue Crawler >> Athena

Data Publisher -> Cron job on an ec2 modelling an data source
S3 Raw -> s3://linkedln-jobs-etl/raw/, file landing notification trigger the lambda function
Lambda -> Calling an rest API to an airflow instance
Airflow -> Trigger emr to process the data in raw and process the data into stage
S3 Stage -> Result Data location
Glue Crawler, Athena -> Provide sql engine for data processing
PowerBI-> Visual
## 3. Output

## 4. Setup

### 4.1 Prerequisite


## 5. Reference

[How To Install Google Chrome, Selenium & Chromedriver For AWS EC2 Instances](https://understandingdata.com/install-google-chrome-selenium-ec2-aws)

[linkedin-jobs-scraper 1.12.0](https://pypi.org/project/linkedin-jobs-scraper/)
