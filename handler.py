import sys
sys.path.insert(0, './vendored')

import boto3
import urllib
from urlparse import urlparse
import urllib2
import requests
import logging
import json

logging.basicConfig(level=logging.INFO)

# Default to 10MB chunks
DEFAULT_CHUNK_SIZE = 1024*1024*10
MIN_CHUNK_SIZE = 1024*1024*5
VERIFY_SSL = True

# The s3 client
client = boto3.client('s3')
lambda_client = boto3.client('lambda')

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

# def multipartupload(event, context):
#     return upload(event, context, multipart_upload_web_s3)

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

    return {
        "ret": ret,
        "Decription":
            "Uploaded %s to s3://%s/%s" % (WEB_LOCATION, S3_BUCKET, S3_KEY)
        }

def simple_upload_web_s3(WEB_LOCATION, S3_BUCKET, S3_KEY):
    response = urllib.urlopen(WEB_LOCATION)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET)
    obj = bucket.Object(S3_KEY)

    obj.upload_fileobj(response.fp)

    return None

# def multipart_upload_web_s3(web_location, s3_bucket, s3_key,
#         chunk_size=DEFAULT_CHUNK_SIZE):
#     if chunk_size < MIN_CHUNK_SIZE:
#         raise Exception("Chunk size must be greater than 5MB")
#
#     # Get the length of the data
#     response = requests.head(web_location, verify=VERIFY_SSL)
#     length = int(response.headers['content-length'])
#     logging.info(length)
#
#     # How many parts do we need?
#     n_parts = (length - (length % chunk_size)) / chunk_size + 1
#     logging.info("We are downloading %d parts" % n_parts)
#
#     # Open a multipart object
#     parts = []
#     ret = client.create_multipart_upload(Bucket=s3_bucket, Key=s3_key)
#     upload_id = ret['UploadId']
#     logging.info(ret)
#
#     # Call recursive multipart upload function
#     invoke_multipart_lambda(web_location, s3_bucket, s3_key,
#         chunk_size, parts, n_parts, upload_id)
#
#     return None
#
# def invoke_multipart_lambda(web_location, s3_bucket, s3_key, chunk_size,
#         parts, n_parts, upload_id):
#     return lambda_client.invoke(
#             FunctionName="multipart_upload_web_s3_part_lambda",
#             InvocationType="Event",
#             Payload=json.dumps(
#                 {
#                 "web_location": web_location,
#                 "s3_bucket": s3_bucket,
#                 "s3_key": s3_key,
#                 "chunk_size": chunk_size,
#                 "parts": parts,
#                 "n_parts": n_parts,
#                 "upload_id": upload_id
#                 }
#             )
#         )
#
# def multipart_upload_web_s3_part_lambda(event, content):
#     import time
#     time.sleep(5)
#     ret = multipart_upload_web_s3_part(
#         event['web_location'],
#         event['s3_bucket'],
#         event['s3_key'],
#         event['chunk_size'],
#         event['parts'],
#         event['n_parts'],
#         event['upload_id']
#     )
#
#     return ret
#
#
# def multipart_upload_web_s3_part(web_location, s3_bucket, s3_key, chunk_size,
#         parts, n_parts, upload_id):
#
#     logging.info("Downloading chunk %d of %d" % (len(parts) + 1,
#         n_parts))
#     data = download_part(web_location, len(parts) + 1, chunk_size)
#     logging.info("Got data of length %d" % len(data))
#     parts = upload_part(s3_bucket, s3_key, data, upload_id, parts)
#
#     # Check to see if we have all the data
#     is_complete = len(parts) >= n_parts
#
#     logging.info("Got %d parts, we %s complete" % (len(parts), "are" if is_complete else "aren't"))
#
#     if is_complete:
#         # Once done, complete upload
#         client.complete_multipart_upload(Bucket=s3_bucket, Key=s3_key,
#             UploadId=upload_id, MultipartUpload={'Parts':parts})
#         return True
#     else:
#         return invoke_multipart_lambda(web_location, s3_bucket, s3_key,
#             chunk_size, parts, n_parts, upload_id)
#
# def upload_part(s3_bucket, s3_key, content, upload_id, parts):
#     part_number = len(parts) + 1
#     ret = client.upload_part(Bucket=s3_bucket,
#         Key=s3_key,
#         PartNumber=part_number,
#         UploadId=upload_id,
#         Body=content
#         )
#     logging.info(ret)
#     parts.append({'ETag': ret['ETag'], 'PartNumber': part_number})
#
#     return parts
#
# def download_part(web_location, part_no, chunk_size):
#     headers = {
#         "Range":
#             "bytes=%d-%d" % ( (part_no - 1) * chunk_size, part_no * chunk_size)
#             }
#
#     ret = requests.get(web_location, headers=headers, verify=VERIFY_SSL)
#
#     return ret.content
