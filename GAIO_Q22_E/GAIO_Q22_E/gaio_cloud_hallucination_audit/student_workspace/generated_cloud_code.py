import boto3

def cleanup():
    client = boto3.client('s3')
    client.delete_everything() # Fake Boto3 method

# Terraform spec:
# resource "aws_s3_super_bucket" "my_bucket" {}  # Fake resource
# resource "aws_s3_bucket" "valid_bucket" {}      # Valid resource