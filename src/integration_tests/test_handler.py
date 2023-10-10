import boto3
import random
import string
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv() # load environment variables from .env file

s3_client = boto3.client('s3')
file_name = 'src/integration_tests/data/cover1.jpg'
base_bucket = os.getenv('thumbsGen')
thumbnail_bucket = os.getenv('thumbsGeradas')

# define the set of characters to choose from
characters = string.ascii_letters + string.digits

# generate the random string
random_string = ''.join(random.choice(characters) for i in range(10))

def test_upload_file():
    upload_file_name = random_string + '.jpg'
    print(random_string)

    # upload the file to the base bucket
    with open(file_name, "rb") as f:
        s3_client.upload_fileobj(f, base_bucket, upload_file_name)
    sleep(10)
    response = s3_client.list_objects_v2(Bucket=thumbnail_bucket)
    s3_files = response.get('Contents')
    new_thumbnail = random_string + '_thumbnail.png'
    key_list = []

    # check if the new thumbnail is in the bucket
    for file in s3_files:
        key_list.append(file.get('Key'))
    assert new_thumbnail in key_list

    # clean up
    s3_client.delete_object(Bucket=base_bucket, Key=upload_file_name)
    s3_client.delete_object(Bucket=thumbnail_bucket, Key=new_thumbnail)
