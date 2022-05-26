# Linkedin Jobs ETL (Batch)

- [Linkedin Jobs ETL (Batch)](#beginner-de-project---batch-edition)
  - [1. Introduction](#1-introduction)
  - [2. Objective](#2-objective)
  - [3. Design](#3-design)
  - [4. Setup](#4-setup)
    - [4.1 Prerequisite](#41-prerequisite)
  - [5. Reference](#5-reference)

## 1. Introduction

Data Publisher >> S3 Raw >> Lambda >> Airflow >> EMR >> S3 Stage >> Glue Crawler >> Athena

Data Publisher -> Cron job on an ec2 modelling an data source
S3 Raw -> s3://linkedln-jobs-etl/raw/, file landing notification trigger the lambda function
Lambda -> Calling an rest API to an airflow instance
Airflow -> Trigger emr to process the data in raw and process the data into stage
S3 Stage -> Result Data location
Glue Crawler, Athena -> Provide sql engine for data processing


## 1. Place holder


## 2. Objective


## 3. Design


## 4. Setup

### 4.1 Prerequisite


## 5. Reference

[How To Install Google Chrome, Selenium & Chromedriver For AWS EC2 Instances](https://understandingdata.com/install-google-chrome-selenium-ec2-aws)

[linkedin-jobs-scraper 1.12.0](https://pypi.org/project/linkedin-jobs-scraper/)

[A Complete Guide to Web Scraping LinkedIn Job Postings](https://maoviola.medium.com/a-complete-guide-to-web-scraping-linkedin-job-postings-ad290fcaa97f)

