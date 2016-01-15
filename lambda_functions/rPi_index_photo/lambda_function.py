# import necessary modules
from __future__ import print_function
import json
import boto3
import urllib

dynamodb_table = 'mattsona-rpi-camera_metadata' # replace with your DDB table

# connect to dynamodb
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

print('Loading function')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')

    try: 
        response = s3.get_object(Bucket=bucket, Key=object_key)
        print(response['Metadata']['image_time_stamp'])

    except Exception as e:
        print(e)
        raise e

    return "Done"