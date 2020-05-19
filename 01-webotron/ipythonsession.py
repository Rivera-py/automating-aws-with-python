# coding: utf-8
import boto3

# Entering our s3
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

# Prints all buckets in AWS account
for bucket in s3.buckets.all():
    print(bucket.name)
