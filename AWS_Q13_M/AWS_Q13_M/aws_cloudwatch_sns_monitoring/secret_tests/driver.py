import json
import os
import sys
from datetime import datetime, timezone

import boto3

# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"
EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('NIIT_EXAM_CODE') or os.getenv('EXAM_CODE') or 'UNKNOWN')

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'NIIT REAL-TIME AWS AUDIT':^70}")
    print("-"*70)

    total_score = 0
    results = {}

    try:
        # Time Info (non-blocking)
        session_start = START_TIME if START_TIME else datetime.now(timezone.utc)
        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - session_start).total_seconds() / 60

        print(f"[SYSTEM] Validating Resources for: {user_prefix}")
        if START_TIME:
            print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")
        else:
            print(f"[SYSTEM] No start time set — running in open mode\n")

        aws_region = None
        ec2_client = None
        valid_instance = None
        target_instance_id = None
        
        # --- TC1 & TC2: EC2 Instance & IAM Setup ---
        tc1_passed = False
        tc2_passed = False
        
        from datetime import timedelta
        
        for region in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
            temp_ec2 = boto3.client('ec2', region_name=region)
            try:
                instances = temp_ec2.describe_instances(Filters=[
                    {'Name': 'instance-state-name', 'Values': ['running', 'pending']}
                ])
                
                if instances.get('Reservations'):
                    for res in instances['Reservations']:
                        for inst in res.get('Instances', []):
                            name_tag = ""
                            for tag in inst.get('Tags', []):
                                if tag['Key'] == 'Name':
                                    name_tag = tag['Value']
                            
                            # Problem statement names instance as: {username}-{exam_code}
                            # Accept any instance whose name starts with the username
                            if name_tag.lower().startswith(user_prefix.lower()):
                                valid_instance = inst
                                break
                        if valid_instance:
                            break
            except Exception:
                pass
                
            if valid_instance:
                aws_region = region
                ec2_client = temp_ec2
                break
                
        if not aws_region:
            aws_region = os.getenv('AWS_DEFAULT_REGION', 'eu-west-1')
            ec2_client = boto3.client('ec2', region_name=aws_region)
            
        sns_client = boto3.client('sns', region_name=aws_region)
        cw_client = boto3.client('cloudwatch', region_name=aws_region)
        
        try:
            if valid_instance:
                tc1_passed = True
                target_instance_id = valid_instance.get('InstanceId')
                results['tc1'] = True
                print("TC1: EC2 Instance Setup [PASSED] (4/4)")
                
                if 'IamInstanceProfile' in valid_instance:
                    tc2_passed = True
                    results['tc2'] = True
                    print("TC2: IAM Instance Profile Setup [PASSED] (4/4)")
                else:
                    results['tc2'] = False
                    print("TC2: IAM Instance Profile Setup [FAILED] (0/4)")
                    print("     └─ [Reason]: IAM Instance Profile not attached.")
            else:
                results['tc1'] = False
                results['tc2'] = False
                print("TC1: EC2 Instance Setup [FAILED] (0/4)")
                print("     └─ [Reason]: EC2 instance missing or created before session start.")
                print("TC2: IAM Instance Profile Setup [FAILED] (0/4)")
                print("     └─ [Reason]: Prerequisite failed.")
        except Exception as e:
            results['tc1'] = False
            results['tc2'] = False
            print("TC1: EC2 Instance Setup [FAILED] (0/4)")
            print("TC2: IAM Instance Profile Setup [FAILED] (0/4)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC3: Amazon SNS Topic Setup ---
        tc3_passed = False
        target_topic_arn = None
        if not results.get('tc1'):
            results['tc3'] = False
            print("TC3: Amazon SNS Topic Setup [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite failed (TC1 invalid).")
            results['tc4'] = False
            print("TC4: CloudWatch Alarm Setup [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite failed.")
            results['tc5'] = False
            print("TC5: Alarm SNS Configuration [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                topics = sns_client.list_topics()
                for t in topics.get('Topics', []):
                    topic_name = t['TopicArn'].split(':')[-1].lower()
                    # Accept topic names that start with the username (format: {username}-{exam_code})
                    # Also accept legacy format: DevOps-Alerts-{username}
                    if topic_name.startswith(user_prefix.lower()) or \
                       t['TopicArn'].endswith(f':DevOps-Alerts-{user_prefix}'):
                        target_topic_arn = t['TopicArn']
                        break
                
                if target_topic_arn:
                    subs = sns_client.list_subscriptions_by_topic(TopicArn=target_topic_arn)
                    if subs.get('Subscriptions'):
                        tc3_passed = True
                        results['tc3'] = True
                        print("TC3: Amazon SNS Topic Setup [PASSED] (4/4)")
                    else:
                        results['tc3'] = False
                        print("TC3: Amazon SNS Topic Setup [FAILED] (0/4)")
                        print("     └─ [Reason]: SNS Topic exists but no email subscription configured.")
                else:
                    results['tc3'] = False
                    print("TC3: Amazon SNS Topic Setup [FAILED] (0/4)")
                    print(f"     └─ [Reason]: SNS Topic DevOps-Alerts-{user_prefix} missing.")
            except Exception as e:
                results['tc3'] = False
                print("TC3: Amazon SNS Topic Setup [FAILED] (0/4)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC4 & TC5: CloudWatch Alarm Configuration ---
            try:
                alarms = cw_client.describe_alarms(AlarmNames=['High-CPU-Alarm'])
                target_alarm = None
                if alarms.get('MetricAlarms'):
                    target_alarm = alarms['MetricAlarms'][0]
                    
                if target_alarm:
                    dimensions = {d['Name']: d['Value'] for d in target_alarm.get('Dimensions', [])}
                    is_correct_instance = dimensions.get('InstanceId') == target_instance_id
                    
                    if target_alarm.get('MetricName') == 'CPUUtilization' and \
                       target_alarm.get('Threshold') == 70.0 and \
                       target_alarm.get('Period') == 300 and \
                       target_alarm.get('EvaluationPeriods') == 1 and \
                       target_alarm.get('Namespace') == 'AWS/EC2' and \
                       is_correct_instance:
                        results['tc4'] = True
                        print("TC4: CloudWatch Alarm Setup [PASSED] (4/4)")
                        
                        if target_topic_arn and target_topic_arn in target_alarm.get('AlarmActions', []):
                            results['tc5'] = True
                            print("TC5: Alarm SNS Configuration [PASSED] (4/4)")
                        else:
                            results['tc5'] = False
                            print("TC5: Alarm SNS Configuration [FAILED] (0/4)")
                            print("     └─ [Reason]: Alarm SNS action invalid or not linked to the correct SNS topic.")
                    else:
                        results['tc4'] = False
                        results['tc5'] = False
                        print("TC4: CloudWatch Alarm Setup [FAILED] (0/4)")
                        print("     └─ [Reason]: CloudWatch Alarm settings are incorrect (check Threshold, Period, Metric or Target Instance).")
                        print("TC5: Alarm SNS Configuration [FAILED] (0/4)")
                        print("     └─ [Reason]: Prerequisite failed.")
                else:
                    results['tc4'] = False
                    results['tc5'] = False
                    print("TC4: CloudWatch Alarm Setup [FAILED] (0/4)")
                    print("     └─ [Reason]: CloudWatch Alarm 'High-CPU-Alarm' missing.")
                    print("TC5: Alarm SNS Configuration [FAILED] (0/4)")
                    print("     └─ [Reason]: Prerequisite failed.")
            except Exception as e:
                results['tc4'] = False
                results['tc5'] = False
                print("TC4: CloudWatch Alarm Setup [FAILED] (0/4)")
                print("TC5: Alarm SNS Configuration [FAILED] (0/4)")
                print(f"     └─ [Error]: {str(e)}")

        # Final Scoring
        total_score = sum([4 for r in results.values() if r])
        
        print("-" * 70)
        print(f"{'TOTAL SCORE:':<52} {total_score}/20")
        print("-" * 70 + "\n")

    except Exception as e:
        print(f"[ERROR] Real-time audit failed: {str(e)}")
        total_score = 0

    # Save Metadata for Central Evaluation
    solution_data = {
        'candidate_prefix': user_prefix,
        'assessment_start_time': start_time,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results,
        'exam_code': EXAM_CODE
    }
    
    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
            
        root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == '__main__':
    verify_task()
