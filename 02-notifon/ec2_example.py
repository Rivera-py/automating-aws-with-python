# coding: utf-8
import boto3

session = boto3.Session(profile_name='pythonAutomation')
ec2 = session.resource('ec2')

key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)

with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)

import os, stat

os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)

ami_name = "amzn2-ami-hvm-2.0.20200520.1-x86_64-gp2"
filters = [{'Name': 'name', 'Values': [ami_name]}]
image = list(ec2.images.filter(Owners=['amazon'], Filters=filters))[0]
ami_id = image.id

instances = ec2.create_instances(ImageId=ami_id, MinCount=1,
                                 MaxCount=1, InstanceType='t2.micro',
                                 KeyName=key.key_name)

inst = instances[0]
public_ip = input("Please paste in your public IP address: ")

sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg.authorize_ingress(
    IpPermissions=[{'FromPort': 22,
                    'ToPort': 22,
                    'IpProtocol': 'TCP',
                    'IpRanges': [{'CidrIp': public_ip + '/32'}]}]
)

print("Pausing for public DNS please wait")
sleep(10)
inst.reload()

sg.authorize_ingress(
    IpPermissions=[{'FromPort': 80,
                    'ToPort': 80,
                    'IpProtocol': 'TCP',
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]
)

print("Finished! Try SSHing to your instance with:")
print("ssh -i python_automation_key ec2-user@" + inst.public_dns_name)
