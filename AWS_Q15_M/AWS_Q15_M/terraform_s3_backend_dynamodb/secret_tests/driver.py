import sys, os, boto3, json

def verify_task():
    username = os.getenv('NIIT_USERNAME', 'LOCAL_USER')
    bucket_name = f"terraform-state-bucket-{username}"
    table_name = f"terraform-lock-table-{username}"
    print("-" * 40); print("AWS RESOURCE VERIFICATION REPORT"); print("-" * 40)
    
    aws_region = 'eu-west-2'
    for r in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
        try:
            temp_ddb = boto3.client('dynamodb', region_name=r)
            temp_ddb.describe_table(TableName=table_name)
            aws_region = r
            break
        except Exception:
            pass

    try:
        s3 = boto3.client('s3')
        dynamodb = boto3.client('dynamodb', region_name=aws_region)
    except Exception as e:
        print(f"FAILED: Could not connect to AWS. Error: {e}"); return

    tc1_passed = False
    try:
        s3.head_bucket(Bucket=bucket_name)
        print("TC1 [Bucket Exists] (4/4) - Success: Verified.")
        tc1_passed = True
    except:
        print("TC1 [Bucket Exists] (0/4) - Failed.")

    if tc1_passed:
        try:
            ver = s3.get_bucket_versioning(Bucket=bucket_name)
            if ver.get('Status') == 'Enabled': print("TC2 [Versioning] (3/3) - Success: Verified.")
            else: print("TC2 [Versioning] (0/3) - Failed.")
        except: print("TC2 [Versioning] (0/3) - Failed.")
            
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket_name)
            rules = enc.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
            if rules and rules[0].get('ApplyServerSideEncryptionByDefault'): print("TC3 [Encryption] (3/3) - Success: Verified.")
            else: print("TC3 [Encryption] (0/3) - Failed.")
        except: print("TC3 [Encryption] (0/3) - Failed.")
    else:
        print("TC2 [Versioning] (0/3) - Failed (Prereq TC1).")
        print("TC3 [Encryption] (0/3) - Failed (Prereq TC1).")

    try:
        desc = dynamodb.describe_table(TableName=table_name)['Table']
        print("TC4 [Table Exists] (4/4) - Success: Verified.")
        
        keys = desc.get('KeySchema', [])
        if keys and keys[0].get('AttributeName') == 'LockID': print("TC5 [Partition Key LockID] (3/3) - Success: Verified.")
        else: print("TC5 [Partition Key LockID] (0/3) - Failed.")
            
        if desc.get('BillingModeSummary', {}).get('BillingMode') == 'PAY_PER_REQUEST' or desc.get('BillingMode') == 'PAY_PER_REQUEST':
            print("TC6 [Billing Mode] (3/3) - Success: Verified.")
        else: print("TC6 [Billing Mode] (0/3) - Failed.")
    except:
        print("TC4 [Table Exists] (0/4) - Failed.")
        print("TC5 [Partition Key] (0/3) - Failed.")
        print("TC6 [Billing Mode] (0/3) - Failed.")
        
    print("-" * 40)

if __name__ == "__main__":
    verify_task()
