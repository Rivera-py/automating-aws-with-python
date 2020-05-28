# -*- coding: utf-8 -*-

"""Manage an S3 bucket with this class."""

import mimetypes
from pathlib import Path
from hashlib import md5
from functools import reduce

import boto3
from botocore.exceptions import ClientError

import util


class BucketManager:
    """Create a BucketManager object."""

    CHUNK_SIZE = 8388608

    def __init__(self, session):
        """Grab the S3 resource for managing."""
        self.s3 = session.resource('s3')
        self.region = session.region_name
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize=self.CHUNK_SIZE,
            multipart_threshold=self.CHUNK_SIZE)
        self.manifest = {}

    def load_manifest(self, bucket):
        """Load manifest for caching purposes."""
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')

        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.manifest[obj['Key']] = obj['ETag']

    @staticmethod
    def hash_data(data):
        """Generate md5 hash for data."""
        hash = md5()
        hash.update(data)

        return hash

    def gen_etag(self, path):
        """Generate ETag for file."""
        hashes = []

        with open(path, 'rb') as f:
            while True:
                data = f.read(self.CHUNK_SIZE)

                if not data:
                    break

                hashes.append(self.hash_data(data))

        if not hashes:
            return None
        elif len(hashes) == 1:
            return '"{}"'.format(hashes[0].hexdigest())
        else:
            hash = self.hash_data(reduce(lambda x, y: x + y,
                                         (h.digest() for h in hashes)))

        return '"{}-{}"'.format(hash.hexdigest(), len(hashes))

    def get_region_name(self, bucket):
        """Get the bucket's region name."""
        bucket_location = self.s3.meta.client.get_bucket_location(
            Bucket=bucket.name)

        return bucket_location["LocationConstraint"] or "us-east-1"

    def get_bucket(self, bucket_name):
        """Get a bucket object by name."""
        return self.s3.Bucket(bucket_name)

    def get_bucket_url(self, bucket):
        """Get the website URL for this bucket."""
        return "http://{}.{}".format(
            bucket.name,
            util.get_endpoint(self.get_region_name(bucket)).host)

    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get an iterator for all objects in a bucket."""
        return self.get_bucket(bucket_name).objects.all()

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
                s3_bucket = self.get_bucket(bucket_name)
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

    def upload_file(self, bucket, path, key):
        """Python wrapper for the upload_file method for buckets in boto3."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        etag = self.gen_etag(path)
        if self.manifest.get(key, "") == etag:
            print("Skipping {}, etags match".format(key))
            return None

        bucket.upload_file(
            path, key, ExtraArgs={'ContentType': content_type},
            Config=self.transfer_config)

    def sync(self, pathname, bucket_name):
        """Sync a directory to an S3 bucket for uploading website content."""
        root = Path(pathname).expanduser().resolve()

        s3_bucket = self.get_bucket(bucket_name)
        self.load_manifest(s3_bucket)

        def handle_directory(target):
            for path in target.iterdir():
                if path.is_dir():
                    handle_directory(path)
                if path.is_file():
                    self.upload_file(s3_bucket,
                                     str(path),
                                     str(path.relative_to(root)))

        handle_directory(root)
