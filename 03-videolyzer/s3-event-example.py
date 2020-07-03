# coding: utf-8
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2020-06-21T18:48:23.635Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDAYEMNC2KIJNSDAUEVE'}, 'requestParameters': {'sourceIPAddress': '31.205.46.114'}, 'responseElements': {'x-amz-request-id': '96C1127DCFF880A8', 'x-amz-id-2': 'D+BTvKUQq2vyttMu71oCL+O5gWQmAneq42zBa6+tscox3bVBu3HIl9Pkb5D9wLKKPUlt3q/ed27uM+s+0uSyAcLk+ORPvuX0'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '5c869551-6c1b-4648-a8e5-f0ed4f375fce', 'bucket': {'name': 'jackvideolyzer01', 'ownerIdentity': {'principalId': 'A3753COX99H5TC'}, 'arn': 'arn:aws:s3:::jackvideolyzer01'}, 'object': {'key': 'Man+Riding+a+Bike.mp4', 'size': 6378345, 'eTag': '4e3634627987633405ab7eef7a0977e7', 'sequencer': '005EEFAB6F36E64B22'}}}]}
event
len(event['Records'])
event['Records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['object']['key']
import urllib
urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
