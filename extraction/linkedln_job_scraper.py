#Import linkedin_jobs_scraper for crawling linkedin jobs page
import logging
import argparse
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, RemoteFilters

#Import the rest of libraries for data processing
from datetime import date
import time
import json


#Setup logging for the scraper
def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.job_id)
    jobs_json.append({
        'title': data.title,
        'company': data.company,
        'place': data.place,
        'job_id':data.job_id,
        'date': date.today(),
        'link': data.link,
        'insights': data.insights,
        'description': data.description.replace('\n', ' ')
    })
def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('[ON_END]')

#Trigger scraper
def trigger_scraper(jobs_limit:int=10):

    scraper = LinkedinScraper(
        headless=True,  # Overrides headless mode
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=1,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    )

    # Add event listeners
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    queries = [
        Query(
            query='Data Engineer',
            options=QueryOptions(
                locations=['Canada'],
                optimize=True,
                apply_link = True,  # Try to extract apply link (slower because it needs to open a new tab for each job). Default to false
                limit= jobs_limit, # Most days the posting number is around 700.
                filters=QueryFilters(              
                    relevance=RelevanceFilters.RELEVANT,
                    time=TimeFilters.DAY,
                )
            )
        ),
    ]

    scraper.run(queries)

def save_result(jobs_json,result_folder_path):
    timestr = time.strftime("%Y%m%d_%H")
    filename = result_folder_path+"/linkedln_jobs_de_canada_"+timestr+'.json'

    with open(filename, "w") as temp:
        for job in jobs_json:
            temp.write(json.dumps(job, default=str))
            temp.write("\n")
    return filename



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Extracting canadian data engineering job postings from linkedin')
    parser.add_argument('-rpf','--result_path_folder',type=str ,metavar='',required=True,help='Full folder path to save the result')
    parser.add_argument('-pl','--pull_limit',type=int,metavar='',required=True,help='Amount of job posting you want to pull')
    args = parser.parse_args()

    logging.basicConfig(level = logging.INFO)
    
    jobs_json = []

    startTime = time.time()
    trigger_scraper(args.pull_limit)
    executionTime = (time.time() - startTime)
    filename=save_result(jobs_json,args.result_path_folder)

    print('Execution time in seconds: ' + str(executionTime))


"""
Result should be similar to this 
https://www.linkedin.com/jobs/search/?f_TPR=r86400&keywords=data%20engineer&location=Canada

Trigger the script
python3 /home/ubuntu/development/batch_linkedln_jobs/extraction/linkedln_job_scraper.py --result_path_folder /home/ubuntu/data/raw/linkedln --pull_limit 5
"""
