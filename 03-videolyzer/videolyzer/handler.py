import os
import json

import urllib

import boto3


def start_label_detection(bucket, key):
    rekognition_client = boto3.client('rekognition')
    non_url_key = urllib.parse.unquote_plus(key)

    response = rekognition_client.start_label_detection(
        Video={
            'S3Object': {
                'Bucket': bucket,
                'Name': non_url_key
            }
        },
        NotificationChannel={
            'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
        }
    )

    print(response)

    return None


def get_video_labels(job_id):
    rekognition_client = boto3.client('rekognition')

    response = rekognition_client.get_label_detection(JobId=job_id)

    next_token = response.get('NextToken', None)

    while next_token:
        next_page = rekognition_client.get_label_detection(
            JobId=job_id,
            NextToken=next_token
        )

        next_token = next_page.get('NextToken', None)

        response['Labels'].extend(next_page['Labels'])

    return response


def put_labels_in_db(data, video_name, video_bucket):
    pass


def start_processing_video(event, context):

    for record in event['Records']:
        start_label_detection(record['s3']['bucket']['name'],
                              record['s3']['object']['key'])

    return None


def handle_label_detection(event, context):
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        job_id = message['JobId']
        s3_object = message['Video']['S3ObjectName']
        s3_bucket = message['Video']['S3Bucket']

        response = get_video_labels(job_id)
        print(response)
        put_labels_in_db(response, s3_object, s3_bucket)

    return None
