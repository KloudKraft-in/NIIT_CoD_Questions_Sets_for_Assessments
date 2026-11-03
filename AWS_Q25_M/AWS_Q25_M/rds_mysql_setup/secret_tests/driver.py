# import sys
# import os
# import json
# import boto3
# from datetime import datetime, timezone, timedelta

# # Capture Assessment Start Time
# START_TIME_STR = os.getenv('NIIT_START_TIME')
# START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
# USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
# EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else 'UNKNOWN'

# def verify_task():
#     print("-" * 65)
#     print(f"{'AWS RDS MYSQL RESOURCE AUDIT':^65}")
#     print("-" * 65)

#     total_score = 0
#     results = {
#         'tc1': False,
#         'tc2': False,
#         'tc3': False,
#         'tc4': False,
#         'tc5': False,
#         'tc6': False
#     }

#     try:
#         # Find active AWS region where the RDS instance is running
#         aws_region = None
#         username = USER_PREFIX.lower().replace('.', '-').replace('@', '-')
#         target_instance_id = f"retail-mysql-db-{username}"
        
#         # Scan regions to locate the RDS DB instance
#         for r in ['ap-south-1', 'eu-west-2', 'us-east-1', 'eu-west-1', 'us-west-2']:
#             try:
#                 rds_temp = boto3.client('rds', region_name=r)
#                 db_instances = rds_temp.describe_db_instances(DBInstanceIdentifier=target_instance_id)
#                 if db_instances.get('DBInstances'):
#                     aws_region = r
#                     break
#             except Exception:
#                 pass

#         if not aws_region:
#             print("[SYSTEM] No RDS database 'retail-mysql-db' found in standard regions.")
#             aws_region = 'ap-south-1'  # fallback

#         rds_client = boto3.client('rds', region_name=aws_region)
#         ec2_client = boto3.client('ec2', region_name=aws_region)

#         # TC1: Environment active and verified (boto3 connection works)
#         tc1_passed = True
#         results['tc1'] = tc1_passed
#         print("TC1: VM Environment Verification ....................... [PASSED] (0/0)")

#         # Retrieve DB Instance details
#         db_instance = None
#         try:
#             db_instances = rds_client.describe_db_instances(DBInstanceIdentifier=target_instance_id)
#             if db_instances.get('DBInstances'):
#                 db_instance = db_instances['DBInstances'][0]
#         except Exception:
#             pass

#         # TC2: DB Instance exists, identifier is correct, and Engine is MySQL 8.0
#         tc2_passed = False
#         if db_instance:
#             engine = db_instance.get('Engine', '')
#             engine_version = db_instance.get('EngineVersion', '')
#             if engine == 'mysql' and engine_version.startswith('8.0'):
#                 tc2_passed = True
#                 print("TC2: RDS Instance and MySQL Engine ..................... [PASSED] (4/4)")
#             else:
#                 print("TC2: RDS Instance and MySQL Engine ..................... [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Expected engine 'mysql' (version 8.0), found '{engine}' (version {engine_version}).")
#         else:
#             print("TC2: RDS Instance and MySQL Engine ..................... [FAILED] (0/4)")
#             print("     └─ [Reason]: DB instance 'retail-mysql-db' could not be found.")

#         results['tc2'] = tc2_passed
#         if tc2_passed:
#             total_score += 4

#         # TC3: Instance Class db.t3.micro, 20 GiB storage, publicly inaccessible
#         tc3_passed = False
#         if db_instance:
#             db_class = db_instance.get('DBInstanceClass', '')
#             allocated_storage = db_instance.get('AllocatedStorage', 0)
#             public_access = db_instance.get('PubliclyAccessible', True)
            
#             if db_class == 'db.t3.micro' and allocated_storage == 20 and not public_access:
#                 tc3_passed = True
#                 print("TC3: Instance Class, Storage & Accessibility ........... [PASSED] (4/4)")
#             else:
#                 print("TC3: Instance Class, Storage & Accessibility ........... [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Class='{db_class}' (expected db.t3.micro), Storage={allocated_storage}GB (expected 20GB), PubliclyAccessible={public_access} (expected False)")
#         else:
#             print("TC3: Instance Class, Storage & Accessibility ........... [FAILED] (0/4)")
#             print("     └─ [Reason]: Prerequisite failed.")

#         results['tc3'] = tc3_passed
#         if tc3_passed:
#             total_score += 4

#         # TC4: Default database 'retaildb' created
#         tc4_passed = False
#         if db_instance:
#             db_name = db_instance.get('DBName', '')
#             if db_name == 'retaildb':
#                 tc4_passed = True
#                 print("TC4: Default Database Name Verification ................ [PASSED] (4/4)")
#             else:
#                 print("TC4: Default Database Name Verification ................ [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Expected default database 'retaildb', found '{db_name}'.")
#         else:
#             print("TC4: Default Database Name Verification ................ [FAILED] (0/4)")
#             print("     └─ [Reason]: Prerequisite failed.")

#         results['tc4'] = tc4_passed
#         if tc4_passed:
#             total_score += 4

#         # TC5: Attached Security Group allows inbound TCP traffic on port 3306
#         tc5_passed = False
#         if db_instance:
#             vpc_sgs = db_instance.get('VpcSecurityGroups', [])
#             sg_ids = [sg['VpcSecurityGroupId'] for sg in vpc_sgs]
            
#             port_3306_allowed = False
#             for sg_id in sg_ids:
#                 try:
#                     sgs = ec2_client.describe_security_groups(GroupIds=[sg_id])
#                     if sgs.get('SecurityGroups'):
#                         for rule in sgs['SecurityGroups'][0].get('IpPermissions', []):
#                             from_port = rule.get('FromPort')
#                             to_port = rule.get('ToPort')
#                             ip_proto = rule.get('IpProtocol')
                            
#                             # Check if TCP traffic on 3306 is allowed
#                             if ip_proto == 'tcp' and from_port <= 3306 and to_port >= 3306:
#                                 port_3306_allowed = True
#                                 break
#                 except Exception:
#                     pass
            
#             if port_3306_allowed:
#                 tc5_passed = True
#                 print("TC5: Inbound Security Group Ingress Rules .............. [PASSED] (4/4)")
#             else:
#                 print("TC5: Inbound Security Group Ingress Rules .............. [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: No Security Group attached to the RDS allows TCP inbound traffic on port 3306.")
#         else:
#             print("TC5: Inbound Security Group Ingress Rules .............. [FAILED] (0/4)")
#             print("     └─ [Reason]: Prerequisite failed.")

#         results['tc5'] = tc5_passed
#         if tc5_passed:
#             total_score += 4

#         # TC6: Storage Autoscaling is disabled
#         # Storage autoscaling is disabled if MaxAllocatedStorage is not set, or is equal to AllocatedStorage
#         tc6_passed = False
#         if db_instance:
#             max_storage = db_instance.get('MaxAllocatedStorage', 0)
#             allocated_storage = db_instance.get('AllocatedStorage', 20)
#             if max_storage == 0 or max_storage == allocated_storage:
#                 tc6_passed = True
#                 print("TC6: Storage Autoscaling Configuration ................. [PASSED] (4/4)")
#             else:
#                 print("TC6: Storage Autoscaling Configuration ................. [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Storage autoscaling is enabled (MaxAllocatedStorage limit is set to {max_storage} GB).")
#         else:
#             print("TC6: Storage Autoscaling Configuration ................. [FAILED] (0/4)")
#             print("     └─ [Reason]: Prerequisite failed.")

#         results['tc6'] = tc6_passed
#         if tc6_passed:
#             total_score += 4

#         print("-" * 65)
#         print(f"{'TOTAL SCORE:':<49} {total_score}/20")
#         print("-" * 65 + "\n")

#     except Exception as e:
#         print(f"[ERROR] Verification failed: {str(e)}")
#         total_score = 0

#     # Save Metadata for local/central verification
#     solution_data = {
#         'candidate_prefix': USER_PREFIX,
#         'assessment_start_time': START_TIME_STR,
#         'evaluation_type': 'REAL_TIME_API',
#         'score': total_score,
#         'results': results,
#         'exam_code': EXAM_CODE
#     }

#     try:
#         ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
#         os.makedirs(ws_path, exist_ok=True)
#         with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
#             json.dump(solution_data, f, indent=4)
            
#         root_ws = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
#         with open(os.path.join(root_ws, 'solution.json'), 'w') as f:
#             json.dump(solution_data, f, indent=4)
#     except Exception as e:
#         print(f"[ERROR] Could not write solution.json: {e}")

# if __name__ == '__main__':
#     verify_task()
import sys
import os
import json
import boto3
from datetime import datetime, timezone, timedelta

# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else 'UNKNOWN'

def verify_task():
    print("-" * 65)
    print(f"{'AWS RDS MYSQL RESOURCE AUDIT':^65}")
    print("-" * 65)

    total_score = 0
    results = {
        'tc1': False,
        'tc2': False,
        'tc3': False,
        'tc4': False,
        'tc5': False,
        'tc6': False
    }

    try:
        # Find active AWS region where the RDS instance is running
        aws_region = None
        username = USER_PREFIX.lower().replace('.', '-').replace('@', '-')
        target_instance_id = f"retail-mysql-db-{username}"
        
        # Scan regions to locate the RDS DB instance
        for r in ['ap-south-1', 'eu-west-2', 'us-east-1', 'eu-west-1', 'us-west-2']:
            try:
                rds_temp = boto3.client('rds', region_name=r)
                db_instances = rds_temp.describe_db_instances(DBInstanceIdentifier=target_instance_id)
                if db_instances.get('DBInstances'):
                    aws_region = r
                    break
            except Exception:
                pass

        if not aws_region:
            print("[SYSTEM] No RDS database 'retail-mysql-db' found in standard regions.")
            aws_region = 'ap-south-1'  # fallback

        rds_client = boto3.client('rds', region_name=aws_region)
        ec2_client = boto3.client('ec2', region_name=aws_region)

        # TC1: Environment active and verified (boto3 connection works)
        tc1_passed = True
        results['tc1'] = tc1_passed
        print("TC1: VM Environment Verification [PASSED] (0/0)")

        # Retrieve DB Instance details
        db_instance = None
        try:
            db_instances = rds_client.describe_db_instances(DBInstanceIdentifier=target_instance_id)
            if db_instances.get('DBInstances'):
                db_instance = db_instances['DBInstances'][0]
        except Exception:
            pass

        # TC2: DB Instance exists, identifier is correct, and Engine is MySQL 8.0
        tc2_passed = False
        if db_instance:
            engine = db_instance.get('Engine', '')
            engine_version = db_instance.get('EngineVersion', '')
            if engine == 'mysql' and engine_version.startswith('8.0'):
                tc2_passed = True
                print("TC2: RDS Instance and MySQL Engine [PASSED] (4/4)")
            else:
                print("TC2: RDS Instance and MySQL Engine [FAILED] (0/4)")
                print(f"     └─ [Reason]: Expected engine 'mysql' (version 8.0), found '{engine}' (version {engine_version}).")
        else:
            print("TC2: RDS Instance and MySQL Engine [FAILED] (0/4)")
            print("     └─ [Reason]: DB instance 'retail-mysql-db' could not be found.")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 4

        # TC3: Instance Class db.t3.micro, 20 GiB storage, publicly inaccessible
        tc3_passed = False
        if db_instance:
            db_class = db_instance.get('DBInstanceClass', '')
            allocated_storage = db_instance.get('AllocatedStorage', 0)
            public_access = db_instance.get('PubliclyAccessible', True)
            
            if db_class == 'db.t3.micro' and allocated_storage == 20 and not public_access:
                tc3_passed = True
                print("TC3: Instance Class, Storage & Accessibility [PASSED] (4/4)")
            else:
                print("TC3: Instance Class, Storage & Accessibility [FAILED] (0/4)")
                print(f"     └─ [Reason]: Class='{db_class}' (expected db.t3.micro), Storage={allocated_storage}GB (expected 20GB), PubliclyAccessible={public_access} (expected False)")
        else:
            print("TC3: Instance Class, Storage & Accessibility [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite failed.")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 4

        # TC4: Default database 'retaildb' created
        tc4_passed = False
        if db_instance:
            db_name = db_instance.get('DBName', '')
            if db_name == 'retaildb':
                tc4_passed = True
                print("TC4: Default Database Name Verification [PASSED] (4/4)")
            else:
                print("TC4: Default Database Name Verification [FAILED] (0/4)")
                print(f"     └─ [Reason]: Expected default database 'retaildb', found '{db_name}'.")
        else:
            print("TC4: Default Database Name Verification [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite failed.")

        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 4

        # TC5: Attached Security Group allows inbound TCP traffic on port 3306
        tc5_passed = False
        if db_instance:
            vpc_sgs = db_instance.get('VpcSecurityGroups', [])
            sg_ids = [sg['VpcSecurityGroupId'] for sg in vpc_sgs]
            
            port_3306_allowed = False
            for sg_id in sg_ids:
                try:
                    sgs = ec2_client.describe_security_groups(GroupIds=[sg_id])
                    if sgs.get('SecurityGroups'):
                        for rule in sgs['SecurityGroups'][0].get('IpPermissions', []):
                            from_port = rule.get('FromPort')
                            to_port = rule.get('ToPort')
                            ip_proto = rule.get('IpProtocol')
                            
                            # Check if TCP traffic on 3306 is allowed
                            if ip_proto == 'tcp' and from_port <= 3306 and to_port >= 3306:
                                port_3306_allowed = True
                                break
                except Exception:
                    pass
            
            if port_3306_allowed:
                tc5_passed = True
                print("TC5: Inbound Security Group Ingress Rules [PASSED] (4/4)")
            else:
                print("TC5: Inbound Security Group Ingress Rules [FAILED] (0/4)")
                print(f"     └─ [Reason]: No Security Group attached to the RDS allows TCP inbound traffic on port 3306.")
        else:
            print("TC5: Inbound Security Group Ingress Rules [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite failed.")

        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 4

        # TC6: Storage Autoscaling is disabled
        tc6_passed = False
        if db_instance:
            max_storage = db_instance.get('MaxAllocatedStorage', 0)
            allocated_storage = db_instance.get('AllocatedStorage', 20)
            if max_storage == 0 or max_storage == allocated_storage:
                tc6_passed = True
                print("TC6: Storage Autoscaling Configuration [PASSED] (4/4)")
            else:
                print("TC6: Storage Autoscaling Configuration [FAILED] (0/4)")
                print(f"     └─ [Reason]: Storage autoscaling is enabled (MaxAllocatedStorage limit is set to {max_storage} GB).")
        else:
            print("TC6: Storage Autoscaling Configuration [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite failed.")

        results['tc6'] = tc6_passed
        if tc6_passed:
            total_score += 4

        print("-" * 65)
        print(f"{'TOTAL SCORE:':<49} {total_score}/20")
        print("-" * 65 + "\n")

    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)}")
        total_score = 0

    # Save Metadata for local/central verification
    solution_data = {
        'candidate_prefix': USER_PREFIX,
        'assessment_start_time': START_TIME_STR,
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
            
        root_ws = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        with open(os.path.join(root_ws, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == '__main__':
    verify_task()
