import boto3
from botocore.exceptions import ClientError

class EC2Manager:
    def __init__(self):
        self.ec2 = boto3.client('ec2', region_name='eu-west-2')

    def provision(self, instance_name):
        pass # Add logic here
