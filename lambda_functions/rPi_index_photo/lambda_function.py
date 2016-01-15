# import necessary modules
from __future__ import print_function
import json
import boto3
import urllib

dynamodb_table = 'mattsona-rpi-camera_metadata' # replace with your DDB table

# connect to dynamodb & s3
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

print('Loading function')

def lambda_handler(event, context):

    # get details of s3 object & bucket
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')

    # connect to the dynamoDB table
    table = dynamodb.Table(dynamodb_table)

    try: 
        # grab the object 
        print('Grabbing S3 object data')
        response = s3.get_object(Bucket=bucket, Key=object_key)

        # index metadata to dynamoDB
        print('Putting item to DynamoDB')
        table.put_item(
            Item = {
                'device_id': response['Metadata']['rpi_id'],
                'epoch_time': int(response['Metadata']['epoch_time_stamp']),
                'image_time_stamp': response['Metadata']['image_time_stamp'],
                's3_object_path': (bucket + '/' + object_key)
                }
            )

    except Exception as e:
        print(e)
        raise e

    return "Done"