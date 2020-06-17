# coding: utf-8

import boto3


session = boto3.Session(profile_name='pythonAutomation')
as_client = session.client('autoscaling')


if __name__ == "__main__":
    as_client.execute_policy(
        AutoScalingGroupName='Notifon Example Group',
        PolicyName='Scale Out'
    )
