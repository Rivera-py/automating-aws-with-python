# coding: utf-8
event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-west-2:559178502800:handleLabelDetectionTopic:ec9e1a4b-16e2-400a-90ab-aef6c6600d7e', 'Sns': {'Type': 'Notification', 'MessageId': '934d29f9-1ec8-5f66-a2f2-7e85fe2880ff', 'TopicArn': 'arn:aws:sns:eu-west-2:559178502800:handleLabelDetectionTopic', 'Subject': None, 'Message': '{"JobId":"ad5a9c50150924ba1a3c987056569538e97e741136b27fbf498707e8624d93cf","Status":"SUCCEEDED","API":"StartLabelDetection","Timestamp":1594023584494,"Video":{"S3ObjectName":"Man Riding a Bike.mp4","S3Bucket":"jackvideolyzer02"}}', 'Timestamp': '2020-07-06T08:19:44.682Z', 'SignatureVersion': '1', 'Signature': 'h0J+s3JYWPY9zle0mwVTDAYr7yq0MN12442HXkOMJ8ygM0jOD+ZkdyrZ3K9VjwBsrQGU44uVCRwY7l6CYY1KgLDNuwUoUR6FGvDpdtqXTdSmb+xEu5v0odqCLlCw+SoxBmKwh2MHf8DHJ7J6PeP1zVDus5OTkFr1wLKb0FxlL/Y8tzfbZL6aoTbFIkjQIX39lMfJWbQn5J0d9w7Vr97ack264RkyZB6qrPvM9q1gW6BU2yed6R67R0dKsQXCaK96a4Jtg9csf+V0mVk6GKL+R7yRAFmx4YAFSJL6B/Gos4liyxpTwPJgnGQbNqqjItykWqzMpT/vbGAdrfbhBvTwsQ==', 'SigningCertUrl': 'https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:559178502800:handleLabelDetectionTopic:ec9e1a4b-16e2-400a-90ab-aef6c6600d7e', 'MessageAttributes': {}}}]}
event
event.keys()
event["Records"]
event["Records"][0].keys()
record = event["Records"][0]
record["EventSource"]
record["EventVersion"]
record["EventSubscriptionArn"]
record["EventSns"]
record["Sns"]
record["Sns"].keys()
msg = record["Sns"]["Message"]
msg
import json
json.loads(msg)
