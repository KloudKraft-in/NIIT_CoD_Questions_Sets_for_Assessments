import sys, os, boto3, urllib.request

def verify_task():
    username = os.getenv('NIIT_USERNAME', 'LOCAL_USER')
    instance_name = f"nginx-server-{username}"
    print("-" * 40); print("AWS RESOURCE VERIFICATION REPORT"); print("-" * 40)
    aws_region = 'eu-west-2'
    for r in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
        try:
            temp_ec2 = boto3.client('ec2', region_name=r)
            res = temp_ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}, {'Name': 'instance-state-name', 'Values': ['running']}])
            if len(res['Reservations']) > 0:
                aws_region = r
                break
        except Exception:
            pass

    try: ec2 = boto3.client('ec2', region_name=aws_region)
    except Exception as e: print(f"FAILED: Could not connect to AWS. Error: {e}"); return
    
    try:
        res = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}, {'Name': 'instance-state-name', 'Values': ['running']}])
        if len(res['Reservations']) > 0:
            inst = res['Reservations'][0]['Instances'][0]
            print("TC1 [EC2 Running] (2/2) - Success: Verified.")
            
            sg_id = inst['SecurityGroups'][0]['GroupId']
            sg_res = ec2.describe_security_groups(GroupIds=[sg_id])
            perms = sg_res['SecurityGroups'][0]['IpPermissions']
            
            if any(p.get('FromPort') == 80 for p in perms): print("TC2 [SG HTTP] (1/1) - Success: Verified.")
            else: print("TC2 [SG HTTP] (0/1) - Failed.")
                
            if any(p.get('FromPort') == 22 for p in perms): print("TC3 [SG SSH] (2/2) - Success: Verified.")
            else: print("TC3 [SG SSH] (0/2) - Failed.")
                
            public_ip = inst.get('PublicIpAddress')
            if public_ip:
                print("TC4 [Public IP] (2/2) - Success: Verified.")
                try:
                    req = urllib.request.urlopen(f"http://{public_ip}", timeout=3)
                    if req.getcode() == 200: print("TC6 [Nginx HTTP] (2/2) - Success: Verified.")
                    else: print("TC6 [Nginx HTTP] (0/2) - Failed.")
                except: print("TC6 [Nginx HTTP] (0/2) - Failed.")
            else:
                print("TC4 [Public IP] (0/2) - Failed.")
                print("TC6 [Nginx HTTP] (0/2) - Failed.")
                
            ud = ec2.describe_instance_attribute(InstanceId=inst['InstanceId'], Attribute='userData')
            if ud.get('UserData', {}).get('Value'): print("TC5 [User Data] (1/1) - Success: Verified.")
            else: print("TC5 [User Data] (0/1) - Failed.")
        else: raise Exception("Not found")
    except:
        print("TC1 [EC2 Running] (0/2) - Failed.")
        print("TC2 [SG HTTP] (0/1) - Failed.")
        print("TC3 [SG SSH] (0/2) - Failed.")
        print("TC4 [Public IP] (0/2) - Failed.")
        print("TC5 [User Data] (0/1) - Failed.")
        print("TC6 [Nginx HTTP] (0/2) - Failed.")

    print("-" * 40)

if __name__ == "__main__":
    verify_task()
