#Import libraries for uploading to s3
import boto3
from botocore.exceptions import ClientError
import os
import argparse
import logging



def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Upload file from local to s3')
    parser.add_argument('-l','--local',type=str ,metavar='',required=True,help='Full local file path')
    parser.add_argument('-b','--bucket',type=str,metavar='',required=True,help='S3 Bucket name')
    parser.add_argument('-s','--s3path',type=str,metavar='',required=True,help='S3 object name')

    args = parser.parse_args()

    upload_file(file_name=args.local,bucket=args.bucket,object_name=args.s3path)

#Testing - python3 upload_to_s3.py -l readme.md -b linkedln-jobs-etl -s raw/readme.md