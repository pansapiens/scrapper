import json
from io import BytesIO
from typing import Any, Optional

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from settings import S3_BUCKET, S3_ENDPOINT_URL, S3_ACCESS_KEY, S3_SECRET_KEY
from .base import Cache


class S3Cache(Cache):
    def __init__(self, bucket: str = S3_BUCKET, key_prefix: str = "user_data/_res"):
        self.bucket = bucket
        self.key_prefix = key_prefix
        self.s3 = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            config=Config(
                signature_version="s3v4",
                retries=dict(
                    max_attempts=3,
                    mode="adaptive",
                ),
            ),
        )

    def dump_result(
        self, data: Any, key: str, screenshot: Optional[bytes] = None
    ) -> None:
        # Save JSON data
        json_key = f"{self.key_prefix}/{key[:2]}/{key}"
        json_data = json.dumps(data, ensure_ascii=True)
        self.s3.put_object(
            Bucket=self.bucket,
            Key=json_key,
            Body=json_data.encode(),
            ContentType="application/json",
        )

        # Save screenshot if provided
        if screenshot:
            screenshot_key = f"{self.key_prefix}/{key[:2]}/{key}.png"
            self.s3.put_object(
                Bucket=self.bucket,
                Key=screenshot_key,
                Body=screenshot,
                ContentType="image/png",
            )

    def load_result(self, key: str) -> Optional[Any]:
        json_key = f"{self.key_prefix}/{key[:2]}/{key}"
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=json_key)
            return json.loads(response["Body"].read().decode())
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            raise
