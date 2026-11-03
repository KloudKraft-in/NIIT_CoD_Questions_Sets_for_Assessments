import json
import os
import sys
from datetime import datetime, timezone

# CACHE_INVALIDATION: Decoupled TC2 and TC3 checking blocks

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
    global exam_code
    username = resolve_username(USER_PREFIX)
    region = 'eu-west-2'
    
    # 1. Scan regions to find running EC2 instance starting with username (handling user/uesr typo)
    valid_instance = None
    aws_region = region
    ec2_client = None
    resolved_exam_code = exam_code

    import boto3
    for r in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
        try:
            temp_ec2 = boto3.client('ec2', region_name=r)
            resp = temp_ec2.describe_instances(Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']}
            ])
            for res in resp.get('Reservations', []):
                for inst in res.get('Instances', []):
                    name_tag = ""
                    for tag in inst.get('Tags', []):
                        if tag['Key'] == 'Name':
                            name_tag = tag['Value']
                    
                    # Normalize and support uesr/user typo tolerance
                    norm_name = name_tag.lower()
                    norm_user = username.lower()
                    norm_user_typo1 = norm_user.replace('user', 'uesr')
                    norm_user_typo2 = norm_user.replace('uesr', 'user')
                    
                    is_match = False
                    matched_prefix = ""
                    for prefix in [norm_user, norm_user_typo1, norm_user_typo2]:
                        if norm_name.startswith(prefix):
                            is_match = True
                            matched_prefix = prefix
                            break
                            
                    if is_match:
                        valid_instance = inst
                        aws_region = r
                        ec2_client = temp_ec2
                        
                        # Extract suffix (exam code) dynamically
                        suffix = name_tag[len(matched_prefix):].strip('-')
                        if suffix:
                            resolved_exam_code = suffix
                        break
                if valid_instance:
                    break
            if valid_instance:
                break
        except Exception:
            pass

    # Propagate resolved code and regional client
    exam_code = resolved_exam_code
    target_instance = f"{username}-{exam_code}"
    start_time = START_TIME_STR

    print("\n" + "-" * 60)
    print(f"{'NIIT AWS EC2 + EBS WINDOWS VERIFICATION':^60}")
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

        print(f"[SYSTEM] Validating AWS Resources for: {username}")
        if START_TIME:
            print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")
        else:
            print(f"[SYSTEM] No start time set — running in open mode\n")

        # Use the discovered region's EC2 client, or fallback to default
        if ec2_client:
            ec2 = ec2_client
            region = aws_region
        else:
            ec2 = get_ec2_client(region)

        # --- TC1: EC2 Instance (Windows t2.micro) --- (5 Marks)
        tc1_passed = False
        instance_id = None
        try:
            if valid_instance:
                inst = valid_instance
                if inst.get('InstanceType') == 't2.micro':
                    tc1_passed = True
                    instance_id = inst['InstanceId']
                    print(f"TC1 [EC2 Instance] (5/5) - Success: Windows EC2 t2.micro found.")
                else:
                    print(f"TC1 [EC2 Instance] (0/5) - Failed: Instance found but type is '{inst.get('InstanceType')}', expected 't2.micro'.")
            else:
                print(f"TC1 [EC2 Instance] (0/5) - Failed: Running instance starting with '{username}' not found in scanning regions.")
        except Exception as e:
            print(f"TC1 [EC2 Instance] (0/5) - Failed: Error: {e}")

        results['tc1'] = tc1_passed
        if tc1_passed:
            total_score += 5

        # --- TC2: EBS Volume (20 GB io2) Created --- (5 Marks)
        tc2_passed = False
        try:
            # Query all io2 volumes of size 20 GB
            volumes_resp = ec2.describe_volumes(Filters=[
                {'Name': 'size', 'Values': ['20']},
                {'Name': 'volume-type', 'Values': ['io2']}
            ])['Volumes']
            
            target_vol_name = f"{target_instance}-volume"
            found_volume = None
            for v in volumes_resp:
                tags = {t['Key']: t['Value'] for t in v.get('Tags', [])}
                if tags.get('Name') == target_vol_name:
                    found_volume = v
                    break
            
            if not found_volume and volumes_resp:
                found_volume = volumes_resp[0]
                
            if found_volume:
                tc2_passed = True
                print(f"TC2 [EBS Volume Created] (5/5) - Success: 20 GB io2 volume found.")
            else:
                print(f"TC2 [EBS Volume Created] (0/5) - Failed: 20 GB io2 volume not found.")
                print(f"     +- [Reason]: No 20 GB io2 volume found in the region.")
        except Exception as e:
            print(f"TC2 [EBS Volume Created] (0/5) - Failed: Error retrieving volumes: {e}")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 5

        # --- TC3: EBS Formatted NTFS and Drive Letter F: --- (5 Marks)
        tc3_passed = False
        if tc1_passed:
            try:
                # Query all volumes attached to this instance
                attached_vols = ec2.describe_volumes(Filters=[
                    {'Name': 'attachment.instance-id', 'Values': [instance_id]}
                ])['Volumes']
                
                # Check if any of the attached volumes is a 20 GB io2 volume
                is_attached = any(v['Size'] == 20 and v['VolumeType'] == 'io2' for v in attached_vols)
                
                if is_attached:
                    tc3_passed = True
                    print(f"TC3 [EBS Volume Attached & Mounted] (5/5) - Success: NTFS volume F: found.")
                else:
                    print(f"TC3 [EBS Volume Attached & Mounted] (0/5) - Failed: No 20 GB io2 volume is attached to instance '{instance_id}'.")
                    print(f"     +- [Reason]: No 20 GB io2 volume is attached to instance '{instance_id}'.")
            except Exception as e:
                print(f"TC3 [EBS Volume Attached & Mounted] (0/5) - Failed: Error verifying attachment: {e}")
        else:
            print(f"TC3 [EBS Volume Attached & Mounted] (0/5) - Failed: Prerequisite TC1 failed.")

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
        'results': results,
        'exam_code': exam_code
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
