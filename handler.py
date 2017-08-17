import boto3
import urllib
from urlparse import urlparse
import urllib2
import requests
import logging

logging.basicConfig(level=logging.INFO)

# Default to 10MB chunks
DEFAULT_CHUNK_SIZE = 1024*1024*10
MIN_CHUNK_SIZE = 1024*1024*5
VERIFY_SSL = True

# The s3 client
client = boto3.client('s3')

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
    return upload(event, context, simple_upload_web_s3)

def multipartupload(event, context):
    return upload(event, context, multipart_upload_web_s3)

def upload(event, context, handler):
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

    ret = handler(WEB_LOCATION, S3_BUCKET, S3_KEY)

    return {"ret": ret, "Decription": "Uploaded %s to s3://%s/%s" % (WEB_LOCATION, S3_BUCKET, S3_KEY)}

def simple_upload_web_s3(WEB_LOCATION, S3_BUCKET, S3_KEY):
    response = urllib.urlopen(WEB_LOCATION)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET)
    obj = bucket.Object(S3_KEY)

    obj.upload_fileobj(response.fp)

    return None

def multipart_upload_web_s3(web_location, S3_BUCKET, S3_KEY, chunk_size=DEFAULT_CHUNK_SIZE):
    if chunk_size < MIN_CHUNK_SIZE:
        raise Exception("Chunk size must be greater than 5MB")

    # Get the length of the data
    response = requests.head(web_location, verify=VERIFY_SSL)
    length = int(response.headers['content-length'])
    logging.info(length)

    # Open a multipart object
    parts = []
    ret = client.create_multipart_upload(Bucket=S3_BUCKET, Key=S3_KEY)
    upload_id = ret['UploadId']
    logging.info(ret)

    # Loop until we have all the chunks
    while len(parts) * chunk_size < length:
        logging.info("Downloading chunk %d of %d" % (len(parts) + 1,
            (length - (length % chunk_size)) / chunk_size  + 1))
        data = download_part(web_location, len(parts) + 1, chunk_size)
        logging.info("Got data of length %d" % len(data))
        parts = upload_part(S3_BUCKET, S3_KEY, data, upload_id, parts)

    logging.info(parts)
    client.complete_multipart_upload(Bucket=S3_BUCKET, Key=S3_KEY,
        UploadId=upload_id, MultipartUpload={'Parts':parts})

    return None

def upload_part(s3_bucket, s3_key, content, upload_id, parts):
    part_number = len(parts) + 1
    ret = client.upload_part(Bucket=s3_bucket, Key=s3_key, PartNumber=part_number,
        UploadId=upload_id, Body=content)
    logging.info(ret)
    parts.append({'ETag': ret['ETag'], 'PartNumber': part_number})

    return parts

def download_part(web_location, part_no, chunk_size):
    headers = {
        "Range":
            "bytes=%d-%d" % ( (part_no - 1) * chunk_size, part_no * chunk_size)
            }

    ret = requests.get(web_location, headers=headers, verify=VERIFY_SSL)

    return ret.content
