import sys
import os
import json
from datetime import datetime
from google.oauth2 import service_account
from google.cloud import storage

# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME') or os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', os.getenv('NIIT_USERNAME', os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')))
EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('NIIT_EXAM_CODE') or os.getenv('NIIT_EXAM_CODE') or 'UNKNOWN')

def verify_task():
    print("-" * 65)
    print(f"{'GCP STORAGE RESOURCE AUDIT':^65}")
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
            print("TC1: GCP Storage Access [FAILED] (0/0)")
            print("     └─ [Reason]: Missing GCP credentials (GCP_SERVICE_ACCOUNT_JSON or GOOGLE_APPLICATION_CREDENTIALS).")
            print("TC2: Storage Bucket Existence ......................... [FAILED] (0/4)")
            print("TC3: Bucket Location Validation ....................... [FAILED] (0/4)")
            print("TC4: Object Upload Validation (welcome.txt) ........... [FAILED] (0/4)")
            print("TC5: Object Versioning check .......................... [FAILED] (0/4)")
            print("TC6: Storage Class check .............................. [FAILED] (0/4)")
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

        # Target Bucket parameters
        project_id = credentials.project_id if hasattr(credentials, 'project_id') else os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            if gcp_json_str:
                try:
                    project_id = json.loads(gcp_json_str).get("project_id")
                except:
                    pass
        if not project_id:
            project_id = "ltm-assessment-project" # Default fallback

        bucket_name = f"bkt-{username}"

        # Initialize GCS client
        storage_client = storage.Client(credentials=credentials, project=project_id)

        # TC1: GCP Storage Access Check (0 Marks)
        tc1_passed = False
        try:
            # Try to list buckets to verify access
            list(storage_client.list_buckets(max_results=1))
            tc1_passed = True
            print("TC1: GCP Storage Access ............................... [PASSED] (0/0)")
        except Exception as e:
            print("TC1: GCP Storage Access ............................... [FAILED] (0/0)")
            print(f"     └─ [Reason]: Unable to connect or authorize. Details: {e}")
            print("TC2: Storage Bucket Existence ......................... [FAILED] (0/4)")
            print("TC3: Bucket Location Validation ....................... [FAILED] (0/4)")
            print("TC4: Object Upload Validation (welcome.txt) ........... [FAILED] (0/4)")
            print("TC5: Object Versioning check .......................... [FAILED] (0/4)")
            print("TC6: Storage Class check .............................. [FAILED] (0/4)")
            print("-" * 65)
            print("TOTAL SCORE: 0/20")
            print("-" * 65)
            return

        results['tc1'] = tc1_passed

        # Retrieve Bucket properties
        bucket = None
        tc2_passed = False
        try:
            bucket = storage_client.get_bucket(bucket_name)
            tc2_passed = True
            print("TC2: Storage Bucket Existence ......................... [PASSED] (4/4)")
        except Exception as e:
            print("TC2: Storage Bucket Existence ......................... [FAILED] (0/4)")
            print(f"     └─ [Reason]: Bucket '{bucket_name}' not found in project '{project_id}'. Details: {e}")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 4

        # TC3: Location validation (4 Marks)
        tc3_passed = False
        if bucket:
            loc = bucket.location.lower()
            if loc == "us-east4":
                tc3_passed = True
                print("TC3: Bucket Location Validation ....................... [PASSED] (4/4)")
            else:
                print("TC3: Bucket Location Validation ....................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: Location is '{bucket.location}', expected 'US-EAST4'.")
        else:
            print("TC3: Bucket Location Validation ....................... [FAILED] (0/4)")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 4

        # TC4: Object check (4 Marks)
        tc4_passed = False
        if bucket:
            blob = bucket.blob("welcome.txt")
            if blob.exists():
                tc4_passed = True
                print("TC4: Object Upload Validation (welcome.txt) ........... [PASSED] (4/4)")
            else:
                print("TC4: Object Upload Validation (welcome.txt) ........... [FAILED] (0/4)")
                print("     └─ [Reason]: 'welcome.txt' not found in root of bucket.")
        else:
            print("TC4: Object Upload Validation (welcome.txt) ........... [FAILED] (0/4)")

        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 4

        # TC5: Object Versioning check (4 Marks)
        tc5_passed = False
        if bucket:
            # Refresh bucket metadata to ensure accuracy
            bucket.reload()
            if bucket.versioning_enabled:
                tc5_passed = True
                print("TC5: Object Versioning check .......................... [PASSED] (4/4)")
            else:
                print("TC5: Object Versioning check .......................... [FAILED] (0/4)")
                print("     └─ [Reason]: Object Versioning is not enabled on this bucket.")
        else:
            print("TC5: Object Versioning check .......................... [FAILED] (0/4)")

        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 4

        # TC6: Storage Class check (4 Marks)
        tc6_passed = False
        if bucket:
            st_class = bucket.storage_class.upper()
            if st_class == "STANDARD":
                tc6_passed = True
                print("TC6: Storage Class check .............................. [PASSED] (4/4)")
            else:
                print("TC6: Storage Class check .............................. [FAILED] (0/4)")
                print(f"     └─ [Reason]: Storage Class is '{st_class}', expected 'STANDARD'.")
        else:
            print("TC6: Storage Class check .............................. [FAILED] (0/4)")

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
