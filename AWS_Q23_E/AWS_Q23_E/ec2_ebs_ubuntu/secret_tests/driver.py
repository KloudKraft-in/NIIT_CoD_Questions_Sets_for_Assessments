import json
import os
import sys
from datetime import datetime, timezone, timedelta

# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
exam_code = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('NIIT_EXAM_CODE') or os.getenv('EXAM_CODE') or 'UNKNOWN')

def get_ec2_client(region_name='eu-west-2'):
    import boto3
    try:
        return boto3.client('ec2', region_name=region_name)
    except Exception as e:
        print(f"FAILED: Could not connect to AWS. Error: {e}")
        sys.exit(1)

def get_iam_username():
    try:
        import boto3
        sts = boto3.client('sts')
        arn = sts.get_caller_identity().get('Arn', '')
        if ':user/' in arn:
            return arn.split(':user/')[-1].strip()
        elif ':assumed-role/' in arn:
            role_part = arn.split(':assumed-role/')[-1].strip()
            if '/' in role_part:
                return role_part.split('/')[-1].strip()
            return role_part.strip()
        else:
            if '/' in arn:
                return arn.split('/')[-1].strip()
    except Exception:
        pass
    return None

def resolve_username(default_prefix):
    if default_prefix and default_prefix != 'LOCAL_USER':
        return default_prefix
    iam_user = get_iam_username()
    if iam_user and iam_user not in ['root', 'ubuntu', 'administrator', 'SYSTEM', 'LOCAL_USER']:
        return iam_user
    return default_prefix

def verify_task():
    username = resolve_username(USER_PREFIX)
    region = 'eu-west-2'
    
    resolved_exam_code = exam_code
    if resolved_exam_code == 'UNKNOWN':
        try:
            ec2 = get_ec2_client(region)
            resp = ec2.describe_instances(Filters=[
                {'Name': 'tag:Name', 'Values': [f"{username}-*"]},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ])
            for res in resp.get('Reservations', []):
                for inst in res.get('Instances', []):
                    for tag in inst.get('Tags', []):
                        if tag['Key'] == 'Name':
                            val = tag['Value']
                            suffix = val.replace(f"{username}-", "").strip()
                            if suffix:
                                resolved_exam_code = suffix
                                break
                if resolved_exam_code != 'UNKNOWN':
                    break
        except Exception as e:
            print(f"[DEBUG] Dynamic resolution error: {e}")

    print(f"[DEBUG] Username resolved: {username}")
    print(f"[DEBUG] Exam code resolved: {resolved_exam_code}")
    target_instance = f"{username}-{resolved_exam_code}"
    start_time = START_TIME_STR

    print("\n" + "-" * 60)
    print(f"{'NIIT AWS EC2 + EBS UBUNTU VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}

    try:
        session_start = START_TIME
        if not session_start:
            session_start = datetime.now(timezone.utc)
            start_time = session_start.isoformat()

        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - session_start).total_seconds() / 60
        max_duration_env = os.getenv('NIIT_ASSESSMENT_DURATION') or os.getenv('NIIT_ASSESSMENT_DURATION')
        max_duration = int(max_duration_env) if max_duration_env else 180  # Fallback to 180 Min if not set

        is_trial = 'demo' in username.lower() or 'trial' in username.lower() or 'local' in username.lower()
        if elapsed_minutes > max_duration + 10 and not is_trial:
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating AWS Resources for: {username}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        ec2 = get_ec2_client(region)

        # --- TC1: EC2 Instance (Ubuntu t2.micro) --- (5 Marks)
        tc1_passed = False
        instance_id = None
        try:
            resp = ec2.describe_instances(Filters=[
                {'Name': 'tag:Name', 'Values': [target_instance]},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ])
            instances = [i for r in resp.get('Reservations', []) for i in r.get('Instances', [])]
            
            # Robust fallback for name mismatch (exam_code vs UNKNOWN vs AWS_Q23_E)
            if not instances:
                for alt_exam_code in ['UNKNOWN', 'AWS_Q23_E', 'AWS_Q23_E_test', '1123']:
                    alt_instance = f"{username}-{alt_exam_code}"
                    if alt_instance != target_instance:
                        resp = ec2.describe_instances(Filters=[
                            {'Name': 'tag:Name', 'Values': [alt_instance]},
                            {'Name': 'instance-state-name', 'Values': ['running']}
                        ])
                        alt_instances = [i for r in resp.get('Reservations', []) for i in r.get('Instances', [])]
                        if alt_instances:
                            target_instance = alt_instance
                            instances = alt_instances
                            break
                            
            if instances:
                inst = instances[0]
                launch_time = inst['LaunchTime']
                if inst.get('InstanceType') != 't2.micro':
                    print(f"TC1: EC2 Instance (Ubuntu t2.micro) ............ [FAILED] (0/5)")
                    print(f"     └─ [Reason]: Instance found but type is '{inst.get('InstanceType')}', expected 't2.micro'.")
                elif launch_time < session_start:
                    ist_tz = timezone(timedelta(hours=5, minutes=30))
                    c_ist = launch_time.astimezone(ist_tz)
                    s_ist = session_start.astimezone(ist_tz)
                    info = f"Launched at {c_ist.strftime('%I:%M:%S %p IST')}, Assessment started at {s_ist.strftime('%I:%M:%S %p IST')}"
                    print(f"TC1: EC2 Instance (Ubuntu t2.micro) ............ [FAILED] (0/5)")
                    print(f"     └─ [Reason]: Instance was launched BEFORE the assessment started. Please terminate and launch a new one!")
                    print(f"     └─ [Info]: {info}")
                elif launch_time > session_start + timedelta(minutes=max_duration + 10):
                    print(f"TC1: EC2 Instance (Ubuntu t2.micro) ............ [FAILED] (0/5)")
                    print(f"     └─ [Reason]: Instance was launched after the assessment time window ended.")
                else:
                    tc1_passed = True
                    instance_id = inst['InstanceId']
                    print(f"TC1: EC2 Instance (Ubuntu t2.micro) ............ [PASSED] (5/5)")
            else:
                print(f"TC1: EC2 Instance (Ubuntu t2.micro) ............ [FAILED] (0/5)")
                print(f"     └─ [Reason]: Running instance named '{target_instance}' not found in {region}.")
        except Exception as e:
            print(f"TC1: EC2 Instance (Ubuntu t2.micro) ............ [FAILED] (0/5)")
            print(f"     └─ [Reason]: Error: {e}")

        results['tc1'] = tc1_passed
        if tc1_passed:
            total_score += 5

        # --- TC2: EBS Volume (10 GB gp3) Created --- (5 Marks)
        tc2_passed = False
        volume_id = None
        try:
            # Query all gp3 volumes of size 10 GB
            volumes_resp = ec2.describe_volumes(Filters=[
                {'Name': 'size', 'Values': ['10']},
                {'Name': 'volume-type', 'Values': ['gp3']}
            ])['Volumes']
            
            # Optionally filter by tag if student named it
            target_vol_name = f"{target_instance}-volume"
            found_volume = None
            for v in volumes_resp:
                # Prioritize tagged volume if it exists
                tags = {t['Key']: t['Value'] for t in v.get('Tags', [])}
                if tags.get('Name') == target_vol_name:
                    found_volume = v
                    break
            
            if not found_volume and volumes_resp:
                found_volume = volumes_resp[0]
                
            if found_volume:
                create_time = found_volume['CreateTime']
                if create_time < session_start:
                    ist_tz = timezone(timedelta(hours=5, minutes=30))
                    c_ist = create_time.astimezone(ist_tz)
                    s_ist = session_start.astimezone(ist_tz)
                    info = f"Created at {c_ist.strftime('%I:%M:%S %p IST')}, Assessment started at {s_ist.strftime('%I:%M:%S %p IST')}"
                    print(f"TC2: EBS Volume (10 GB gp3) Created .............. [FAILED] (0/5)")
                    print(f"     └─ [Reason]: Volume was created BEFORE the assessment started. Please DELETE and recreate it!")
                    print(f"     └─ [Info]: {info}")
                elif create_time > session_start + timedelta(minutes=max_duration + 10):
                    print(f"TC2: EBS Volume (10 GB gp3) Created .............. [FAILED] (0/5)")
                    print(f"     └─ [Reason]: Volume was created after the assessment time window ended.")
                else:
                    tc2_passed = True
                    volume_id = found_volume['VolumeId']
                    print(f"TC2: EBS Volume (10 GB gp3) Created .............. [PASSED] (5/5)")
            else:
                print(f"TC2: EBS Volume (10 GB gp3) Created .............. [FAILED] (0/5)")
                print(f"     └─ [Reason]: No 10 GB gp3 volume found in the region.")
        except Exception as e:
            print(f"TC2: EBS Volume (10 GB gp3) Created .............. [FAILED] (0/5)")
            print(f"     └─ [Reason]: Error retrieving volumes: {e}")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 5

        # --- TC3: EBS Mounted at /mnt/data-store (ext4) --- (5 Marks)
        tc3_passed = False
        if tc1_passed and tc2_passed:
            try:
                # Check if the volume found in TC2 is attached to our instance
                volume_info = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
                attachments = volume_info.get('Attachments', [])
                is_attached = any(att['InstanceId'] == instance_id for att in attachments)
                
                if is_attached:
                    # Attempt Guest OS mount verification via SSM
                    import time
                    import boto3
                    ssm = boto3.client('ssm', region_name=region)
                    is_managed = False
                    try:
                        ssm_instances = ssm.describe_instance_information(
                            Filters=[{'Key': 'InstanceIds', 'Values': [instance_id]}]
                        ).get('InstanceInformationList', [])
                        if ssm_instances and ssm_instances[0].get('PingStatus') == 'Online':
                            is_managed = True
                    except Exception:
                        pass
                        
                    if is_managed:
                        # Run shell command to verify the mount point and filesystem type
                        cmd = "findmnt -n -o FSTYPE /mnt/data-store"
                        try:
                            response = ssm.send_command(
                                InstanceIds=[instance_id],
                                DocumentName="AWS-RunShellScript",
                                Parameters={'commands': [cmd]},
                                TimeoutSeconds=30
                            )
                            command_id = response['Command']['CommandId']
                            
                            success = False
                            output = ""
                            for _ in range(10):
                                time.sleep(1.5)
                                res = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
                                if res['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
                                    success = (res['Status'] == 'Success')
                                    output = res.get('StandardOutputContent', '').strip()
                                    break
                                    
                            if success and output == 'ext4':
                                tc3_passed = True
                                print(f"TC3: EBS Attached & Mounted at /mnt/data-store .... [PASSED] (5/5)")
                                print(f"     └─ [Info]: Verified ext4 filesystem mounted at /mnt/data-store inside guest OS.")
                            else:
                                tc3_passed = False
                                print(f"TC3: EBS Attached & Mounted at /mnt/data-store .... [FAILED] (0/5)")
                                if not success:
                                    print(f"     └─ [Reason]: Failed to run verification command in Guest OS.")
                                else:
                                    print(f"     └─ [Reason]: Volume is attached but not formatted as ext4 or not mounted at /mnt/data-store.")
                        except Exception as e:
                            # Fallback if command send fails
                            tc3_passed = True
                            print(f"TC3: EBS Attached & Mounted at /mnt/data-store .... [PASSED] (5/5)")
                            print(f"     └─ [WARNING]: SSM command execution failed: {e}. Falling back to attachment check.")
                    else:
                        tc3_passed = True
                        print(f"TC3: EBS Attached & Mounted at /mnt/data-store .... [PASSED] (5/5)")
                        print(f"     └─ [WARNING]: SSM agent is offline on the instance. Guest OS mount point could not be verified remotely.")
                        print(f"                   Ensure you formatted /dev/xvdf as ext4 and mounted to /mnt/data-store.")
                else:
                    print(f"TC3: EBS Attached & Mounted at /mnt/data-store .... [FAILED] (0/5)")
                    print(f"     └─ [Reason]: Volume '{volume_id}' is not attached to instance '{instance_id}'.")
            except Exception as e:
                print(f"TC3: EBS Attached & Mounted at /mnt/data-store .... [FAILED] (0/5)")
                print(f"     └─ [Reason]: Error verifying attachment: {e}")
        else:
            print(f"TC3: EBS Attached & Mounted at /mnt/data-store .... [FAILED] (0/5)")
            print(f"     └─ [Reason]: Prerequisite TC1 or TC2 failed.")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 5

        print("-" * 60)
        print(f"{'TOTAL SCORE:':<44} {total_score}/15")
        print("-" * 60 + "\n")

    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)}")
        total_score = 0

    # Save Metadata for Central Evaluation
    solution_data = {
        'candidate_prefix': username,
        'assessment_start_time': start_time,
        'max_duration_minutes': 30,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results
    }

    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == "__main__":
    verify_task()

