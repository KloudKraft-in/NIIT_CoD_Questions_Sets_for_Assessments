# import sys
# import os
# import json
# from datetime import datetime
# from google.oauth2 import service_account
# from google.cloud import compute_v1

# # Capture Assessment Start Time
# START_TIME_STR = os.getenv('NIIT_START_TIME') or os.getenv('NIIT_START_TIME')
# START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
# USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', os.getenv('NIIT_USERNAME', os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')))
# EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('NIIT_EXAM_CODE') or os.getenv('NIIT_EXAM_CODE') or 'UNKNOWN')

# def verify_task():
#     print("-" * 65)
#     print(f"{'GCP COMPUTE RESOURCE AUDIT':^65}")
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
#         # Load GCP credentials
#         gcp_json_str = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")
#         credentials = None

#         if gcp_json_str:
#             try:
#                 key_dict = json.loads(gcp_json_str)
#                 credentials = service_account.Credentials.from_service_account_info(key_dict)
#             except Exception as e:
#                 print(f"[ERROR] Failed to parse GCP_SERVICE_ACCOUNT_JSON: {e}")

#         # Fallback to application default credentials path
#         if not credentials and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
#             try:
#                 credentials = service_account.Credentials.from_service_account_file(
#                     os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
#                 )
#             except Exception as e:
#                 print(f"[ERROR] Failed to load credentials from file: {e}")

#         if not credentials:
#             print("TC1: GCP Project Access [FAILED] (0/0)")
#             print("     └─ [Reason]: Missing GCP credentials (GCP_SERVICE_ACCOUNT_JSON or GOOGLE_APPLICATION_CREDENTIALS).")
#             print("TC2: Virtual Machine existence ........................ [FAILED] (0/4)")
#             print("TC3: Machine type validation .......................... [FAILED] (0/4)")
#             print("TC4: OS Image validation .............................. [FAILED] (0/4)")
#             print("TC5: Boot Disk Configuration check ................... [FAILED] (0/4)")
#             print("TC6: VM Running Status check .......................... [FAILED] (0/4)")
#             print("-" * 65)
#             print("TOTAL SCORE: 0/20")
#             print("-" * 65)
#             return

#         # Load solution.json to get gcp_username if available
#         solution_data = {}
#         try:
#             for p in ['solution.json', '../student_workspace/solution.json', '../../student_workspace/solution.json']:
#                 if os.path.exists(p):
#                     with open(p, 'r') as f:
#                         solution_data = json.load(f)
#                     break
#         except Exception:
#             pass

#         gcp_username = solution_data.get('gcp_username') or os.environ.get('gcp_username') or os.environ.get('GCP_USERNAME') or USER_PREFIX
#         if '@' in gcp_username:
#             raw_username = gcp_username.split('@')[0]
#         else:
#             raw_username = gcp_username
#         if '_' in raw_username:
#             raw_username = raw_username.split('_')[0]
#         username = raw_username.lower().replace('.', '-')

#         # Target VM parameters
#         project_id = credentials.project_id if hasattr(credentials, 'project_id') else os.environ.get("GCP_PROJECT_ID")
#         if not project_id:
#             # Fallback check inside JSON key if we can read it
#             if gcp_json_str:
#                 try:
#                     project_id = json.loads(gcp_json_str).get("project_id")
#                 except:
#                     pass
        
#         if not project_id:
#             project_id = "ltm-assessment-project" # Default fallback

#         zone = "us-east4-a"
#         vm_name = f"vm-{username}"

#         # Initialize Google Compute Client
#         compute_client = compute_v1.InstancesClient(credentials=credentials)

#         # TC1: Project Connection (0 Marks)
#         tc1_passed = False
#         try:
#             # Try to list instances to verify API access
#             list(compute_client.list(project=project_id, zone=zone))
#             tc1_passed = True
#             print("TC1: GCP Project Access ............................... [PASSED] (0/0)")
#         except Exception as e:
#             print("TC1: GCP Project Access ............................... [FAILED] (0/0)")
#             print(f"     └─ [Reason]: Unable to connect or authorize. Details: {e}")
#             print("TC2: Virtual Machine existence ........................ [FAILED] (0/4)")
#             print("TC3: Machine type validation .......................... [FAILED] (0/4)")
#             print("TC4: OS Image validation .............................. [FAILED] (0/4)")
#             print("TC5: Boot Disk Configuration check ................... [FAILED] (0/4)")
#             print("TC6: VM Running Status check .......................... [FAILED] (0/4)")
#             print("-" * 65)
#             print("TOTAL SCORE: 0/20")
#             print("-" * 65)
#             return

#         results['tc1'] = tc1_passed

#         # Retrieve the VM instance details
#         instance = None
#         tc2_passed = False
#         try:
#             instance = compute_client.get(project=project_id, zone=zone, instance=vm_name)
#             tc2_passed = True
#             print("TC2: Virtual Machine Existence ........................ [PASSED] (4/4)")
#         except Exception as e:
#             print("TC2: Virtual Machine Existence ........................ [FAILED] (0/4)")
#             print(f"     └─ [Reason]: Instance '{vm_name}' not found in project '{project_id}' and zone '{zone}'.")

#         results['tc2'] = tc2_passed
#         if tc2_passed:
#             total_score += 4

#         # TC3: Machine type validation (4 Marks)
#         tc3_passed = False
#         if instance:
#             m_type = instance.machine_type.split('/')[-1]
#             if m_type == "n1-standard-1":
#                 tc3_passed = True
#                 print("TC3: Machine Type Validation .......................... [PASSED] (4/4)")
#             else:
#                 print("TC3: Machine Type Validation .......................... [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Machine type is '{m_type}', expected 'n1-standard-1'.")
#         else:
#             print("TC3: Machine Type Validation .......................... [FAILED] (0/4)")

#         results['tc3'] = tc3_passed
#         if tc3_passed:
#             total_score += 4

#         # TC4: OS Image validation (4 Marks)
#         tc4_passed = False
#         if instance:
#             is_ubuntu = False
#             for disk in instance.disks:
#                 if disk.boot:
#                     # Check licenses or source image reference
#                     licenses = [lic.split('/')[-1] for lic in disk.licenses]
#                     if any("ubuntu" in lic.lower() for lic in licenses) or "ubuntu" in str(disk.source).lower():
#                         is_ubuntu = True
#                         break
            
#             if is_ubuntu:
#                 tc4_passed = True
#                 print("TC4: OS Image Validation .............................. [PASSED] (4/4)")
#             else:
#                 print("TC4: OS Image Validation .............................. [FAILED] (0/4)")
#                 print("     └─ [Reason]: Boot disk is not running Ubuntu.")
#         else:
#             print("TC4: OS Image Validation .............................. [FAILED] (0/4)")

#         results['tc4'] = tc4_passed
#         if tc4_passed:
#             total_score += 4

#         # TC5: Boot disk size & type validation (4 Marks)
#         tc5_passed = False
#         if instance:
#             boot_disk_size = 0
#             boot_disk_type = ""
#             for disk in instance.disks:
#                 if disk.boot:
#                     boot_disk_size = disk.disk_size_gb
#                     # disk.type_ is a full URL link to the disk type resource
#                     if disk.type_:
#                         boot_disk_type = disk.type_.split('/')[-1]
#                     break

#             # Sometimes disk type URL looks like '.../diskTypes/pd-ssd'
#             is_ssd = "pd-ssd" in boot_disk_type or "ssd" in boot_disk_type.lower()
#             if boot_disk_size == 10 and is_ssd:
#                 tc5_passed = True
#                 print("TC5: Boot Disk Configuration check ................... [PASSED] (4/4)")
#             else:
#                 print("TC5: Boot Disk Configuration check ................... [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Size = {boot_disk_size} GB (expected 10 GB), Type = '{boot_disk_type}' (expected pd-ssd).")
#         else:
#             print("TC5: Boot Disk Configuration check ................... [FAILED] (0/4)")

#         results['tc5'] = tc5_passed
#         if tc5_passed:
#             total_score += 4

#         # TC6: Instance running status (4 Marks)
#         tc6_passed = False
#         if instance:
#             if instance.status == "RUNNING":
#                 tc6_passed = True
#                 print("TC6: VM Running Status check .......................... [PASSED] (4/4)")
#             else:
#                 print("TC6: VM Running Status check .......................... [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: VM state is '{instance.status}', expected 'RUNNING'.")
#         else:
#             print("TC6: VM Running Status check .......................... [FAILED] (0/4)")

#         results['tc6'] = tc6_passed
#         if tc6_passed:
#             total_score += 4

#     except Exception as e:
#         print(f"[ERROR] An unexpected error occurred: {e}")

#     print("-" * 65)
#     print(f"TOTAL SCORE: {total_score}/20")
#     print("-" * 65)

# if __name__ == "__main__":
#     verify_task()
import sys
import os
import json
from datetime import datetime
from google.oauth2 import service_account
from google.cloud import compute_v1

# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME') or os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', os.getenv('NIIT_USERNAME', os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')))
EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('NIIT_EXAM_CODE') or os.getenv('NIIT_EXAM_CODE') or 'UNKNOWN')

def verify_task():
    print("-" * 65)
    print(f"{'GCP COMPUTE RESOURCE AUDIT':^65}")
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
        # Load GCP credentials
        gcp_json_str = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")
        credentials = None

        if gcp_json_str:
            try:
                key_dict = json.loads(gcp_json_str)
                credentials = service_account.Credentials.from_service_account_info(key_dict)
            except Exception as e:
                print(f"[ERROR] Failed to parse GCP_SERVICE_ACCOUNT_JSON: {e}")

        # Fallback to application default credentials path
        if not credentials and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
                )
            except Exception as e:
                print(f"[ERROR] Failed to load credentials from file: {e}")

        if not credentials:
            print("TC1: GCP Project Access [FAILED] (0/0)")
            print("     └─ [Reason]: Missing GCP credentials (GCP_SERVICE_ACCOUNT_JSON or GOOGLE_APPLICATION_CREDENTIALS).")
            print("TC2: Virtual Machine existence ........................ [FAILED] (0/4)")
            print("TC3: Machine type validation .......................... [FAILED] (0/4)")
            print("TC4: OS Image validation .............................. [FAILED] (0/4)")
            print("TC5: Boot Disk Configuration check ................... [FAILED] (0/4)")
            print("TC6: VM Running Status check .......................... [FAILED] (0/4)")
            print("-" * 65)
            print("TOTAL SCORE: 0/20")
            print("-" * 65)
            return

        # Load solution.json to get gcp_username if available
        solution_data = {}
        try:
            for p in ['solution.json', '../student_workspace/solution.json', '../../student_workspace/solution.json']:
                if os.path.exists(p):
                    with open(p, 'r') as f:
                        solution_data = json.load(f)
                    break
        except Exception:
            pass

        gcp_username = solution_data.get('gcp_username') or os.environ.get('gcp_username') or os.environ.get('GCP_USERNAME') or USER_PREFIX
        if '@' in gcp_username:
            raw_username = gcp_username.split('@')[0]
        else:
            raw_username = gcp_username
        if '_' in raw_username:
            raw_username = raw_username.split('_')[0]
        username = raw_username.lower().replace('.', '-')

        # Target VM parameters
        project_id = credentials.project_id if hasattr(credentials, 'project_id') else os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            # Fallback check inside JSON key if we can read it
            if gcp_json_str:
                try:
                    project_id = json.loads(gcp_json_str).get("project_id")
                except:
                    pass
        
        if not project_id:
            project_id = "ltm-assessment-project" # Default fallback

        zone = "us-east4-a"
        vm_name = f"vm-{username}"

        # Initialize Google Compute Client
        compute_client = compute_v1.InstancesClient(credentials=credentials)

        # TC1: Project Connection (0 Marks)
        tc1_passed = False
        try:
            # Try to list instances to verify API access
            list(compute_client.list(project=project_id, zone=zone))
            tc1_passed = True
            print("TC1: GCP Project Access ............................... [PASSED] (0/0)")
        except Exception as e:
            print("TC1: GCP Project Access ............................... [FAILED] (0/0)")
            print(f"     └─ [Reason]: Unable to connect or authorize. Details: {e}")
            print("TC2: Virtual Machine existence ........................ [FAILED] (0/4)")
            print("TC3: Machine type validation .......................... [FAILED] (0/4)")
            print("TC4: OS Image validation .............................. [FAILED] (0/4)")
            print("TC5: Boot Disk Configuration check ................... [FAILED] (0/4)")
            print("TC6: VM Running Status check .......................... [FAILED] (0/4)")
            print("-" * 65)
            print("TOTAL SCORE: 0/20")
            print("-" * 65)
            return

        results['tc1'] = tc1_passed

        # Retrieve the VM instance details
        instance = None
        tc2_passed = False
        try:
            instance = compute_client.get(project=project_id, zone=zone, instance=vm_name)
            tc2_passed = True
            print("TC2: Virtual Machine Existence ........................ [PASSED] (4/4)")
        except Exception as e:
            print("TC2: Virtual Machine Existence ........................ [FAILED] (0/4)")
            print(f"     └─ [Reason]: Instance '{vm_name}' not found in project '{project_id}' and zone '{zone}'.")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 4

        # TC3: Machine type validation (4 Marks)
        tc3_passed = False
        if instance:
            m_type = instance.machine_type.split('/')[-1]
            if m_type == "n1-standard-1":
                tc3_passed = True
                print("TC3: Machine Type Validation .......................... [PASSED] (4/4)")
            else:
                print("TC3: Machine Type Validation .......................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: Machine type is '{m_type}', expected 'n1-standard-1'.")
        else:
            print("TC3: Machine Type Validation .......................... [FAILED] (0/4)")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 4

        # TC4: OS Image validation (4 Marks)
        tc4_passed = False
        if instance:
            is_ubuntu = False
            for disk in instance.disks:
                if disk.boot:
                    # Check licenses or source image reference
                    licenses = [lic.split('/')[-1] for lic in disk.licenses]
                    if any("ubuntu" in lic.lower() for lic in licenses) or "ubuntu" in str(disk.source).lower():
                        is_ubuntu = True
                        break
            
            if is_ubuntu:
                tc4_passed = True
                print("TC4: OS Image Validation .............................. [PASSED] (4/4)")
            else:
                print("TC4: OS Image Validation .............................. [FAILED] (0/4)")
                print("     └─ [Reason]: Boot disk is not running Ubuntu.")
        else:
            print("TC4: OS Image Validation .............................. [FAILED] (0/4)")

        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 4

        # TC5: Boot disk size & type validation (4 Marks)
        tc5_passed = False
        if instance:
            boot_disk_size = 0
            boot_disk_type = ""
            for disk in instance.disks:
                if disk.boot:
                    boot_disk_size = disk.disk_size_gb
                    try:
                        disks_client = compute_v1.DisksClient(credentials=credentials)
                        disk_name = disk.source.split('/')[-1]
                        disk_detail = disks_client.get(project=project_id, zone=zone, disk=disk_name)
                        if disk_detail and disk_detail.type_:
                            boot_disk_type = disk_detail.type_.split('/')[-1]
                    except Exception as e:
                        boot_disk_type = str(disk.type)
                    break

            # Sometimes disk type URL looks like '.../diskTypes/pd-ssd'
            is_ssd = "pd-ssd" in boot_disk_type or "ssd" in boot_disk_type.lower()
            if boot_disk_size == 10 and is_ssd:
                tc5_passed = True
                print("TC5: Boot Disk Configuration check ................... [PASSED] (4/4)")
            else:
                print("TC5: Boot Disk Configuration check ................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: Size = {boot_disk_size} GB (expected 10 GB), Type = '{boot_disk_type}' (expected pd-ssd).")
        else:
            print("TC5: Boot Disk Configuration check ................... [FAILED] (0/4)")

        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 4

        # TC6: Instance running status (4 Marks)
        tc6_passed = False
        if instance:
            if instance.status == "RUNNING":
                tc6_passed = True
                print("TC6: VM Running Status check .......................... [PASSED] (4/4)")
            else:
                print("TC6: VM Running Status check .......................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: VM state is '{instance.status}', expected 'RUNNING'.")
        else:
            print("TC6: VM Running Status check .......................... [FAILED] (0/4)")

        results['tc6'] = tc6_passed
        if tc6_passed:
            total_score += 4

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

    print("-" * 65)
    print(f"TOTAL SCORE: {total_score}/20")
    print("-" * 65)

if __name__ == "__main__":
    verify_task()
