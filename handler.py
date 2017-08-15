import boto3
import urllib.request
from urllib.parse import urlparse

def simpleupload(event, context):
    if not type(event) == dict:
        return {"error": "you need to pass me json"}

    for key in ['web_location', 's3_bucket']:
        if not key in event:
            return {"error": "no %s specified" % key}

    WEB_LOCATION = event['web_location']
    S3_BUCKET = event['s3_bucket']
    S3_LOCATION = event.get('s3_location', '/')

    return upload_web_s3(WEB_LOCATION, S3_BUCKET, S3_LOCATION)

def upload_web_s3(WEB_LOCATION, S3_BUCKET, S3_LOCATION):
    filename = WEB_LOCATION
    S3_FILENAME = urlparse(WEB_LOCATION).path.split('/')[-1]

    S3_KEY = '/'.join([S3_LOCATION, S3_FILENAME])

    response = urllib.request.urlopen(WEB_LOCATION)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET)
    obj = bucket.Object(S3_KEY)

    obj.upload_fileobj(response.fp)

    return {}
