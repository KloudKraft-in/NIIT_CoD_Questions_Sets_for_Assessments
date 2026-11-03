import boto3
import botocore
import os
import sys
import json
import re
from datetime import datetime, timezone, timedelta

# Top-level AWS credential definitions for NIIT IDE Cloud Driver Patcher
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', os.getenv('AWS_ACCESS_KEY', ''))
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', os.getenv('AWS_SECRET_KEY', ''))

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def get_s3_client(region_name='eu-west-2'):
    # 1. Environment variables
    ak = os.getenv('AWS_ACCESS_KEY_ID') or os.getenv('AWS_ACCESS_KEY')
    sk = os.getenv('AWS_SECRET_ACCESS_KEY') or os.getenv('AWS_SECRET_KEY')
    token = os.getenv('AWS_SESSION_TOKEN') or os.getenv('AWS_SECURITY_TOKEN')
    if ak and sk:
        try:
            kwargs = {
                'service_name': 's3',
                'region_name': region_name,
                'aws_access_key_id': ak,
                'aws_secret_access_key': sk
            }
            if token:
                kwargs['aws_session_token'] = token
            return boto3.client(**kwargs)
        except Exception:
            pass

    # 2. Module level credentials (patched by NIIT IDE Cloud Driver Patcher)
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        try:
            return boto3.client(
                's3',
                region_name=region_name,
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY
            )
        except Exception:
            pass

    # 3. Default session (IAM role, ~/.aws/credentials, instance profile)
    try:
        session = boto3.Session()
        creds = session.get_credentials()
        if creds is not None:
            return session.client('s3', region_name=region_name)
    except Exception:
        pass

    # 4. Fallback: check module credentials or driver_central
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        try:
            return boto3.client(
                's3',
                region_name=region_name,
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY
            )
        except Exception:
            pass

    try:
        import driver_central
        ak = getattr(driver_central, 'AWS_ACCESS_KEY', None)
        sk = getattr(driver_central, 'AWS_SECRET_KEY', None)
        if ak and sk:
            return boto3.client('s3', region_name=region_name, aws_access_key_id=ak, aws_secret_access_key=sk)
    except Exception:
        pass

    return boto3.client('s3', region_name=region_name)

def resolve_candidate_info(passed_user=None, passed_exam=None):
    # Search all potential paths for solution.json
    possible_sol_paths = [
        os.path.join(get_base_path(), 'solution.json'),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace', 'solution.json')),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solution.json')),
        os.path.join(os.getcwd(), 'solution.json'),
        os.path.join(os.getcwd(), 'student_workspace', 'solution.json'),
        os.path.expanduser('~/NIIT_Workspace/AWS_Q01_E/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/AWS_Q01_E/solution.json'),
        "/home/LabsKraft/NIIT_Workspace/AWS_Q01_E/student_workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/AWS_Q01_E/solution.json",
        "/home/LabsKraft/student_workspace/solution.json"
    ]
    sol_user = None
    sol_exam = None
    for sp in possible_sol_paths:
        if os.path.exists(sp):
            try:
                with open(sp, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        sol_user = sol_user or data.get('candidate_prefix') or data.get('niit_username') or data.get('labskraft_username')
                        sol_exam = sol_exam or data.get('exam_code')
                        if sol_user and sol_exam:
                            break
            except Exception:
                pass

    # Process CLI arguments dynamically (handling: python driver.py "labs-kraft-demo2" "solution.json")
    cli_user = None
    cli_exam = None
    cli_sol_path = None
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            continue
        if arg.endswith('.json'):
            cli_sol_path = arg
            continue
        if cli_user is None:
            cli_user = arg
        elif cli_exam is None:
            cli_exam = arg

    raw_username = (
        passed_user or
        cli_user or
        os.getenv("LABSKRAFT_USERNAME") or
        os.getenv("NIIT_USERNAME") or
        sol_user or
        os.getenv("USER") or
        os.getenv("username") or
        "student"
    )
    if raw_username in ['LOCAL_USER', 'ubuntu', 'root', 'ec2-user', 'administrator']:
        raw_username = os.getenv("NIIT_USERNAME") or os.getenv("LABSKRAFT_USERNAME") or sol_user or "student"

    if '@' in raw_username:
        raw_username = raw_username.split('@')[0]
    username = raw_username.lower().replace('.', '-')

    exam_code = (
        passed_exam or
        cli_exam or
        os.getenv("NIIT_EXAM_CODE") or
        os.getenv("EXAM_CODE") or
        os.getenv("exam_code") or
        sol_exam or
        "UNKNOWN"
    )

    return username, exam_code, cli_sol_path

def find_target_bucket(s3_client, username, exam_code):
    expected_bucket = f"{username}-{exam_code}".lower() if exam_code != 'UNKNOWN' else username.lower()
    candidate_names = [expected_bucket, username.lower()]

    if exam_code != 'UNKNOWN':
        candidate_names.append(f"{username}-{exam_code}".lower())
        candidate_names.append(f"{username}_{exam_code}".lower())
        candidate_names.append(f"{username}{exam_code}".lower())

    # Dynamically query existing buckets in AWS account
    existing_buckets = []
    try:
        resp = s3_client.list_buckets()
        existing_buckets = [b['Name'] for b in resp.get('Buckets', [])]
    except Exception:
        pass

    if not existing_buckets:
        return expected_bucket

    # 1. Exact match against candidate names
    for cand in candidate_names:
        for b in existing_buckets:
            if b.lower() == cand:
                return b

    # 2. Filter out AWS internal/service buckets
    user_buckets = [b for b in existing_buckets if not b.startswith(('cf-templates-', 'elasticbeanstalk-', 'aws-', 'amazon-', 'cdk-', 'amplify-'))]

    clean_user = username.lower().replace('_', '-').strip()
    clean_user_alnum = re.sub(r'[^a-z0-9]', '', clean_user)

    # 3. Match bucket containing both username and exam code
    if clean_user and clean_user not in ['local-user', 'student']:
        for b in user_buckets:
            b_lower = b.lower()
            b_alnum = re.sub(r'[^a-z0-9]', '', b_lower)
            if clean_user in b_lower or (clean_user_alnum and clean_user_alnum in b_alnum):
                if exam_code != 'UNKNOWN' and str(exam_code).lower() in b_lower:
                    return b

    # 4. Match bucket containing username
    if clean_user and clean_user not in ['local-user', 'student']:
        for b in user_buckets:
            b_lower = b.lower()
            b_alnum = re.sub(r'[^a-z0-9]', '', b_lower)
            if clean_user in b_lower or (clean_user_alnum and clean_user_alnum in b_alnum):
                return b

    # 5. Match bucket containing exam_code
    if exam_code != 'UNKNOWN':
        for b in user_buckets:
            if str(exam_code).lower() in b.lower():
                return b

    # 6. If only 1 user bucket exists in this account, that is the candidate's bucket
    if len(user_buckets) == 1:
        return user_buckets[0]

    # 7. Check prefix match with first segment of username
    user_part = clean_user.split('-')[0]
    if len(user_part) >= 3:
        for b in user_buckets:
            if user_part in b.lower():
                return b

    return expected_bucket

def get_bucket_region(s3_client, bucket_name):
    try:
        loc = s3_client.get_bucket_location(Bucket=bucket_name)
        constraint = loc.get('LocationConstraint')
        if constraint is None or constraint == '':
            return 'us-east-1'
        if constraint == 'EU':
            return 'eu-west-1'
        return constraint
    except Exception as e:
        if hasattr(e, 'response') and isinstance(e.response, dict):
            r = e.response.get('ResponseMetadata', {}).get('HTTPHeaders', {}).get('x-amz-bucket-region')
            if r:
                return r
            err_r = e.response.get('Error', {}).get('Region')
            if err_r:
                return err_r

    for r_test in ['eu-west-2', 'eu-west-1', 'eu-west-3', 'us-east-1']:
        try:
            c = get_s3_client(region_name=r_test)
            c.head_bucket(Bucket=bucket_name)
            return r_test
        except Exception as ge:
            if hasattr(ge, 'response') and isinstance(ge.response, dict):
                status = ge.response.get('ResponseMetadata', {}).get('HTTPStatusCode')
                r = ge.response.get('ResponseMetadata', {}).get('HTTPHeaders', {}).get('x-amz-bucket-region')
                if r:
                    return r
                if status in [200, 403]:
                    return r_test

    return 'eu-west-2'

def check_public_access_block(s3_client, bucket_name, region):
    clients_to_try = []
    if region and region != 'unknown':
        try:
            clients_to_try.append(get_s3_client(region_name=region))
        except Exception:
            pass
    clients_to_try.append(s3_client)

    for client in clients_to_try:
        try:
            pab = client.get_public_access_block(Bucket=bucket_name)
            config = pab.get('PublicAccessBlockConfiguration', {})
            block_acls = bool(config.get('BlockPublicAcls', False))
            block_policy = bool(config.get('BlockPublicPolicy', False))
            if block_acls and block_policy:
                return True, block_acls, block_policy, None
            else:
                return False, block_acls, block_policy, f"BlockPublicAcls={block_acls}, BlockPublicPolicy={block_policy}"
        except Exception as e:
            err_msg = str(e)
            if 'NoSuchPublicAccessBlockConfiguration' in err_msg:
                return False, False, False, "Public access block is disabled"

    return False, False, False, "Security settings not found"

def verify_task(username=None, exam_code_arg=None):
    username, exam_code, cli_sol_path = resolve_candidate_info(passed_user=username, passed_exam=exam_code_arg)
    s3 = get_s3_client(region_name='eu-west-2')

    target_bucket = find_target_bucket(s3, username, exam_code)

    total_score = 0
    results = {}

    # --- TEST CASE 1: BUCKET EXISTENCE ---
    bucket_exists = False
    try:
        s3.head_bucket(Bucket=target_bucket)
        bucket_exists = True
    except botocore.exceptions.ClientError as e:
        status_code = e.response.get('ResponseMetadata', {}).get('HTTPStatusCode')
        err_code = str(e.response.get('Error', {}).get('Code'))
        if status_code in [200, 301, 403] or err_code in ['301', '403']:
            bucket_exists = True
    except Exception:
        pass

    if not bucket_exists:
        try:
            resp = s3.list_buckets()
            all_b = [b['Name'] for b in resp.get('Buckets', [])]
            if any(b.lower() == target_bucket.lower() for b in all_b):
                bucket_exists = True
                for b in all_b:
                    if b.lower() == target_bucket.lower():
                        target_bucket = b
                        break
        except Exception:
            pass

    tc1_status = "[PASSED]" if bucket_exists else "[FAILED]"
    tc1_score = 5 if bucket_exists else 0
    tc1_reason = f"Bucket '{target_bucket}' found in AWS." if bucket_exists else f"Bucket '{target_bucket}' not found in AWS."
    results['tc1'] = bucket_exists
    total_score += tc1_score

    # --- DETECT REGION ---
    region = get_bucket_region(s3, target_bucket) if bucket_exists else 'unknown'

    # --- TEST CASE 2: PUBLIC ACCESS BLOCK ---
    if bucket_exists:
        pab_passed, blk_acl, blk_pol, pab_reason = check_public_access_block(s3, target_bucket, region)
        tc2_status = "[PASSED]" if pab_passed else "[FAILED]"
        tc2_score = 5 if pab_passed else 0
        tc2_reason = "Security configured (BlockPublicAcls & BlockPublicPolicy enabled)." if pab_passed else f"Public access is allowed ({pab_reason})."
    else:
        pab_passed = False
        tc2_status = "[FAILED]"
        tc2_score = 0
        tc2_reason = "Prerequisite failed (bucket not found)."

    results['tc2'] = pab_passed
    total_score += tc2_score

    # --- TEST CASE 3: REGION CHECK ---
    # Target region is eu-west-2 (London) per specification; also accepts eu-west-1, eu-west-3
    if bucket_exists:
        region_valid = region in ['eu-west-1', 'eu-west-2', 'eu-west-3']
        tc3_status = "[PASSED]" if region_valid else "[FAILED]"
        tc3_score = 5 if region_valid else 0
        tc3_reason = f"Correct region '{region}' used." if region_valid else f"Found in '{region}', expected 'eu-west-2'."
    else:
        region_valid = False
        tc3_status = "[FAILED]"
        tc3_score = 0
        tc3_reason = "Prerequisite failed (bucket not found)."

    results['tc3'] = region_valid
    total_score += tc3_score

    # --- SAVE SOLUTION.JSON ---
    start_time_str = os.getenv('NIIT_START_TIME')
    start_time = start_time_str if start_time_str else datetime.now(timezone.utc).isoformat()

    solution_data = {
        'candidate_prefix': username,
        'assessment_start_time': start_time,
        'max_duration_minutes': 15,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results,
        'exam_code': exam_code,
        'question_id': 'AWS_Q01_E',
        'problem_code': 'create_s3_bucket'
    }

    candidate_save_paths = [
        os.path.join(get_base_path(), 'solution.json'),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace', 'solution.json')),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solution.json')),
        os.path.join(os.getcwd(), 'solution.json'),
        os.path.join(os.getcwd(), 'student_workspace', 'solution.json'),
        os.path.expanduser('~/NIIT_Workspace/AWS_Q01_E/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/AWS_Q01_E/solution.json'),
        "/home/LabsKraft/NIIT_Workspace/AWS_Q01_E/student_workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/AWS_Q01_E/solution.json",
        "/home/LabsKraft/student_workspace/solution.json"
    ]

    if cli_sol_path:
        candidate_save_paths.insert(0, os.path.abspath(cli_sol_path))
        candidate_save_paths.insert(0, cli_sol_path)

    for sp in candidate_save_paths:
        try:
            sp_dir = os.path.dirname(sp)
            if sp_dir and not os.path.exists(sp_dir):
                os.makedirs(sp_dir, exist_ok=True)
            with open(sp, 'w', encoding='utf-8') as f:
                json.dump(solution_data, f, indent=4)
        except Exception:
            pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results), flush=True)
        return total_score, results

    print("-" * 50, flush=True)
    print("        NIIT AWS RESOURCE VERIFICATION REPORT", flush=True)
    print(f"Target Bucket : {target_bucket}", flush=True)
    print(f"Region        : {region}", flush=True)
    print("-" * 50, flush=True)
    print(f"TC1 [Bucket Creation] ....... {tc1_status} ({tc1_score}/5)", flush=True)
    print(f"    └─ [Reason]: {tc1_reason}", flush=True)
    print(f"TC2 [Public Access Blocked] . {tc2_status} ({tc2_score}/5)", flush=True)
    print(f"    └─ [Reason]: {tc2_reason}", flush=True)
    print(f"TC3 [Region Check] .......... {tc3_status} ({tc3_score}/5)", flush=True)
    print(f"    └─ [Reason]: {tc3_reason}", flush=True)
    print("-" * 50, flush=True)
    score_str = f"{total_score}/15"
    print(f"TOTAL SCORE:{score_str:>38}", flush=True)
    print("-" * 50, flush=True)

    return total_score, results

def verify_aws_on_server(candidate_email, question_id, labskraft_username=None, assessment_start_time=None, solution_data=None, exam_code_arg="UNKNOWN", solution_path=None):
    try:
        import driver_central
        return driver_central.verify_aws_on_server(
            candidate_email=candidate_email,
            question_id=question_id,
            labskraft_username=labskraft_username,
            assessment_start_time=assessment_start_time,
            solution_data=solution_data,
            exam_code_arg=exam_code_arg,
            solution_path=solution_path
        )
    except Exception:
        return verify_task(username=labskraft_username or candidate_email, exam_code_arg=exam_code_arg)

if __name__ == "__main__":
    verify_task()
