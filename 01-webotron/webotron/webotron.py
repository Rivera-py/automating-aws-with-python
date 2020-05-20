import boto3, click
from botocore.exceptions import ClientError

# Entering our s3
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"

    for bucket in s3.buckets.all():
        print(bucket.name)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Create and configure s3 bucket"
    s3_bucket = None

    # If the bucket exists grab it, if not create it
    try:
        s3_bucket = s3.create_bucket(
                Bucket = bucket,
                CreateBucketConfiguration = {
                    'LocationConstraint': session.region_name
                }
            )
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e

    # Configures the website policy
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
    """ % s3_bucket.name
    policy = policy.strip()

    # Configures the actual website
    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }})

    return




# Command to run if main file
if __name__ == '__main__':
    cli()
