import boto3
from io import BytesIO
from PIL import Image, ImageOps
import os
import json

s3_client = boto3.client('s3')
size = 128

SEND_THUMBS_BUCKET = os.environ['SEND_THUMBS_BUCKET']

def upload_to_s3(key, image):
    out_thumbnail = BytesIO()
    image.save(out_thumbnail, 'PNG')
    out_thumbnail.seek(0)

    response = s3_client.put_object(
        # ACL='public-read',
        Body=out_thumbnail,
        Bucket=SEND_THUMBS_BUCKET,
        ContentType='image/png',
        Key=key
    )

    url = '{}/{}/{}'.format(s3_client.meta.endpoint_url, SEND_THUMBS_BUCKET, key)
    return url

def get_s3_image(bucket, key):
    print("Getting image from S3 with key: {}".format(key))
    response = s3_client.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()

    img = Image.open(BytesIO(image_content))
    return img


def image_to_thumbnail(image):
    return ImageOps.fit(image, (size, size), Image.LANCZOS)


def new_filename(key):
    key_split = key.rsplit('.', 1)
    return key_split[0] + "_thumbnail.png"

def s3_thumbnail_generator(event, context):
    print(json.dumps(event))
    records = event.get('Records', [])
    if len(records):
        bucket = records[0].get('s3', {}).get('bucket', {}).get('name')
        key = records[0].get('s3', {}).get('object', {}).get('key')
        # only create a thumbnail on non thumbnail pictures
        if bucket and key:
            # get the image
            image = get_s3_image(bucket, key)
            # resize the image
            thumbnail = image_to_thumbnail(image)
            # get the new filename
            thumbnail_key = new_filename(key)
            # upload the file
            url = upload_to_s3(thumbnail_key, thumbnail)
            return url
