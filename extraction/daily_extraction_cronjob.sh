#!/bin/bash

#Declare local folder for saving the result of the extraction
dir_path="/home/ubuntu/data/raw/linkedln"

#Trigger the extraction script to pull the job posting and save it as json in the local environment
python3 /home/ubuntu/development/batch_linkedln_jobs/extraction/linkedln_job_scraper.py --result_path_folder $dir_path --pull_limit 5
echo "Extraction is complete and result is saved to $dir_path"
#Trigger the python script to upload the result json to S3

for i in `ls $dir_path`
do
    python3 /home/ubuntu/development/batch_linkedln_jobs/extraction/upload_to_s3.py --local_path $dir_path/$i --bucket linkedln-jobs-etl --s3path raw/$i
    echo "$i is successfully uploaded to S3" 
done

