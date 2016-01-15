#!/usr/bin/python
# import critical modules
from __future__ import print_function # support python 2.7 & 3
import picamera
import datetime
import boto3
import time
import os
import calendar

s3_bucket_name = 'mattsona-rpi-camera' # update with your bucket name - this assumes your cred policies allow writes (put_object) to this bucket
rPi_id = 'my_rPi' # update with your rPi's 'name'; this will be used as primary key in dynamoDB table & added to S3 metadata

# set up the camera
camera = picamera.PiCamera()
camera.vflip = True

# set up AWS connectivity
s3_session = boto3.resource('s3')

def start():

    while True:

        # set the file name; will need to go in to the loop
        image_time_stamp = datetime.datetime.isoformat(datetime.datetime.now())
        file_time_stamp = image_time_stamp.replace(':','_') # replace semicolon with underscores
        image_file_name = 'capture_' + file_time_stamp + '.jpg'
        epoch_time_stamp = calendar.timegm(datetime.datetime.strptime(image_time_stamp, "%Y-%m-%dT%H:%M:%S.%f").timetuple())

        # take a picture
        camera.capture(image_file_name)

        try: 
            # store picture in S3
            image_file_data = open(image_file_name, 'rb')
            image_file_location = 'images/' + rPi_id + '/' + image_file_name
            s3_session.Bucket(s3_bucket_name).put_object(Key=image_file_location, 
                Body=image_file_data,
                Metadata={
                    'image_time_stamp': image_time_stamp,
                    'epoch_time_stamp': str(epoch_time_stamp),
                    'rPi_id': rPi_id
                }
            )

            print('Uploaded ' + image_file_name)
            # delete the local image file
            os.remove(image_file_name)

        except Exception as e:

            print(e)

        # wait 5 seconds
        time.sleep(5)

if __name__ == "__main__":

    start()
