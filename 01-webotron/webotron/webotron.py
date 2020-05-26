#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Webotron: Deploy websites with AWS.

Webotron automates the process of deploying static websites to AWS:
- Configure AWS S3 buckets
  - Create them
  - Set them up for static website hosting
  - Deploy local files to them
 - Configure DNS with AWS Route 53
   - Configure a Content Delivery Network and SSL with AWS CloudFront
"""


import boto3
import click
from bucket import BucketManager


# Entering our s3

session = boto3.Session(profile_name='pythonAutomation')
bucket_manager = BucketManager(session)
s3 = bucket_manager.s3


@click.group()
def cli():
    """Webotron deploys websites to AWS."""


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket.name)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List all objects in a bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj.key)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure s3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    bucket_manager.sync(pathname, bucket)


# Command to run if main file
if __name__ == '__main__':
    cli()
