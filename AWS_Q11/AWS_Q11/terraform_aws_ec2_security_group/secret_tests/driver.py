import json
import os
import sys
import subprocess
from datetime import datetime, timezone

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'NIIT REAL-TIME TERRAFORM AUDIT':^70}")
    print("-"*70)

    total_score = 0
    results = {}

    try:
        # Time Enforcement Logic
        if not START_TIME:
            print("[ERROR] KLOUDKRAFT_START_TIME environment variable is missing.")
            raise Exception("Invalid Session")

        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - START_TIME).total_seconds() / 60
        max_duration = 75  # 75 Min assessment

        if elapsed_minutes > max_duration + 5: # 5 min grace
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating Resources for: {user_prefix}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        # --- TC1: Terraform Plan ---
        try:
            tf_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
            tc1_passed = False
            if os.path.exists(os.path.join(tf_dir, "main.tf")):
                val_check = subprocess.run(["terraform", "validate", "-json"], cwd=tf_dir, capture_output=True, text=True)
                if val_check.returncode == 0:
                    tc1_passed = True

            if tc1_passed:
                results['tc1'] = True
                print(f"TC1: Terraform Plan & State Initialization Check ....... [PASSED] (10/10)")
            else:
                results['tc1'] = False
                print(f"TC1: Terraform Plan & State Initialization Check ....... [FAILED] (0/10)")
                print(f"     └─ [Reason]: terraform validate/plan failed or main.tf missing.")
        except Exception as e:
            results['tc1'] = False
            print(f"TC1: Terraform Plan & State Initialization Check ....... [FAILED] (0/10)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC2: Security Group ---
        if not results.get('tc1'):
            results['tc2'] = False
            print(f"TC2: Security Group Ingress Rules Verification ......... [FAILED] (0/10)")
            print(f"     └─ [Reason]: Prerequisite failed (Terraform invalid).")
            results['tc3'] = False
            print(f"TC3: EC2 Instance State & Tagging Verification ......... [FAILED] (0/10)")
            print(f"     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                tf_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
                state_file = os.path.join(tf_dir, "terraform.tfstate")
                tc2_passed = False
                if os.path.exists(state_file):
                    with open(state_file, "r") as sf:
                        state_data = json.load(sf)
                        resources = state_data.get("resources", [])
                        has_sg = any(r.get("type") == "aws_security_group" for r in resources)
                        if has_sg:
                            tc2_passed = True
                            if START_TIME:
                                mtime = datetime.fromtimestamp(os.path.getmtime(state_file), timezone.utc)
                                if mtime < START_TIME:
                                    tc2_passed = False
                                    print(f"[WARN] Terraform state was created before current session started (Old Session).")

                if tc2_passed:
                    results['tc2'] = True
                    print(f"TC2: Security Group Ingress Rules Verification ......... [PASSED] (10/10)")
                else:
                    results['tc2'] = False
                    print(f"TC2: Security Group Ingress Rules Verification ......... [FAILED] (0/10)")
                    print(f"     └─ [Reason]: Security Group missing in state in current session.")
            except Exception as e:
                results['tc2'] = False
                print(f"TC2: Security Group Ingress Rules Verification ......... [FAILED] (0/10)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC3: EC2 Instance ---
            try:
                tf_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
                state_file = os.path.join(tf_dir, "terraform.tfstate")
                tc3_passed = False
                if os.path.exists(state_file):
                    with open(state_file, "r") as sf:
                        state_data = json.load(sf)
                        resources = state_data.get("resources", [])
                        has_ec2 = any(r.get("type") == "aws_instance" for r in resources)
                        if has_ec2:
                            tc3_passed = True
                            if START_TIME:
                                mtime = datetime.fromtimestamp(os.path.getmtime(state_file), timezone.utc)
                                if mtime < START_TIME:
                                    tc3_passed = False
                                    print(f"[WARN] Terraform state was created before current session started (Old Session).")

                if tc3_passed:
                    results['tc3'] = True
                    print(f"TC3: EC2 Instance State & Tagging Verification ......... [PASSED] (10/10)")
                else:
                    results['tc3'] = False
                    print(f"TC3: EC2 Instance State & Tagging Verification ......... [FAILED] (0/10)")
                    print(f"     └─ [Reason]: EC2 instance missing in state in current session.")
            except Exception as e:
                results['tc3'] = False
                print(f"TC3: EC2 Instance State & Tagging Verification ......... [FAILED] (0/10)")
                print(f"     └─ [Error]: {str(e)}")

        # Final Scoring
        total_score = sum([10 for r in results.values() if r])
        
        print("-" * 70)
        print(f"{'TOTAL SCORE:':<52} {total_score}/30")
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
        'results': results
    }
    
    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == '__main__':
    verify_task()
