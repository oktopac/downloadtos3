import boto3
import urllib
from urlparse import urlparse

def create_s3_key(web_location, s3_location, filename=None):
    if filename is None:
        filename = urlparse(web_location).path.split('/')[-1]

    if len(filename) == 0:
        raise Exception("No filename provided")

    if s3_location == None or s3_location == '/':
        return filename

    s3key = '/'.join([s3_location.rstrip('/'), filename])
    return s3key

def simpleupload(event, context):
    if not type(event) == dict:
        return {"error": "you need to pass me json"}

    for key in ['web_location', 's3_bucket']:
        if not key in event:
            return {"error": "no %s specified" % key}

    WEB_LOCATION = event['web_location']
    S3_BUCKET = event['s3_bucket']
    S3_LOCATION = event.get('s3_location', '/')
    FILENAME = event.get('filename')

    S3_KEY = create_s3_key(WEB_LOCATION, S3_LOCATION, filename=FILENAME)

    ret = upload_web_s3(WEB_LOCATION, S3_BUCKET, S3_KEY)

    return {"ret": ret, "Decription": "Uploaded %s to s3://%s/%s" % (WEB_LOCATION, S3_BUCKET, S3_KEY)}

def upload_web_s3(WEB_LOCATION, S3_BUCKET, S3_KEY):
    response = urllib.urlopen(WEB_LOCATION)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET)
    obj = bucket.Object(S3_KEY)

    obj.upload_fileobj(response.fp)

    return None
