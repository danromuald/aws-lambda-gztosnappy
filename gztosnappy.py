from __future__ import print_function

import logging
import json
import boto3
import gzip
import snappy

__author__="Dan R. Mbanga"

# Set up a logger

logger = logging.getLogger()
logger.setLevel(logging.INFO)


logger.info("Loading function")

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def lambda_handler(event, context):

    # Get the object from the event and show its content type
    in_bucket = event['Records'][0]['s3']['bucket']['name']
    in_key = event['Records'][0]['s3']['object']['key']
    in_key_file_name = in_key.split('/')[-1]
    out_bucket = '<YOUR OUTPUT BUCKET>'
    out_prefix = 'stg/processed-snappy/'
    out_key = out_prefix + in_key_file_name.split('.')[0] + '.snappy'

    try:
        s3_client.download_file(in_bucket, in_key, '/tmp/file_in.gz')

        with gzip.open('/tmp/file_in.gz','rb') as file_in:
            with open('/tmp/file_out.snappy','wb') as file_out:
                snappy.stream_compress(file_in,file_out)



        s3_client.upload_file('/tmp/file_out.snappy', out_bucket, out_key)

        log = "Successfully converted " + in_key + " into " + out_key

        logger.info(log)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(in_key, in_bucket))
        raise e
