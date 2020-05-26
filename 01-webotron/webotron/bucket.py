"""Manage an S3 bucket with this class."""
# -*- coding: utf-8 -*-

import mimetypes
from pathlib import Path

from botocore.exceptions import ClientError


class BucketManager:
    """Create a BucketManager object."""

    def __init__(self, session):
        """Grabs the S3 resource for managing."""
        self.s3 = session.resource('s3')
        self.region = session.region_name

    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get an iterator for all objects in a bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Either create a new or grab an existing bucket."""
        s3_bucket = None

        try:
            s3_bucket = self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': self.region
                    }
                )
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise error

        return s3_bucket

    @staticmethod
    def set_policy(bucket):
        """Configure the website policy."""
        policy = """
        {
            "Version": "2012-10-17",
            "Id": "Policy1589997684341",
            "Statement": [
                {
                    "Sid": "Stmt1589997675646",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::%s/*"
                }
            ]
        }
        """ % bucket.name
        policy = policy.strip()

        pol = bucket.Policy()
        pol.put(Policy=policy)

    @staticmethod
    def configure_website(bucket):
        """Configure the static website to be hosted by our bucket."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }})

    @staticmethod
    def upload_file(bucket, path, key):
        """Python wrapper for the upload_file method for buckets in boto3."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            })

    def sync(self, pathname, bucket_name):
        """Sync a directory to an S3 bucket for uploading website content."""
        root = Path(pathname).expanduser().resolve()

        s3_bucket = self.s3.Bucket(bucket_name)

        def handle_directory(target):
            for path in target.iterdir():
                if path.is_dir():
                    handle_directory(path)
                if path.is_file():
                    self.upload_file(s3_bucket,
                                     str(path),
                                     str(path.relative_to(root)))

        handle_directory(root)
