import json
import requests

from config.config import (
    API_URL,
    S3_BUCKET_NAME,
    BRONZE_KEY
)

from utils.s3_client import (
    get_s3_client
)


def fetch_api_data():

    response = requests.get(API_URL)

    response.raise_for_status()

    return response.json()


def upload_raw_to_s3(raw_data):

    s3 = get_s3_client()

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=BRONZE_KEY,
        Body=json.dumps(raw_data, indent=4),
        ContentType="application/json"
    )

    print("Bronze Layer Loaded")


def run_bronze():

    raw_data = fetch_api_data()

    upload_raw_to_s3(raw_data)

    return raw_data