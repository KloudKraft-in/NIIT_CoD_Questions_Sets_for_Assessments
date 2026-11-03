import json
import os
import sys
import subprocess
from datetime import datetime, timezone

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def find_active_jenkins_job(candidate_names, start_time):
    base_dirs = [
        "/var/lib/jenkins/jobs",
        "/var/snap/jenkins/common/jobs",
        "/var/snap/jenkins/current/jobs"
    ]
    snap_base = "/var/snap/jenkins"
    if os.path.exists(snap_base):
        for item in os.listdir(snap_base):
            if item.isdigit():
                base_dirs.append(os.path.join(snap_base, item, "jobs"))

    for b_dir in base_dirs:
        for name in candidate_names:
            p = os.path.join(b_dir, name)
            if os.path.exists(p):
                return p

    for b_dir in base_dirs:
        if os.path.exists(b_dir) and start_time:
            for j in os.listdir(b_dir):
                p = os.path.join(b_dir, j)
                if os.path.isdir(p):
                    c_files = [p, os.path.join(p, "config.xml"), os.path.join(p, "builds"), os.path.join(p, "nextBuildNumber")]
                    e_files = [f for f in c_files if os.path.exists(f)]
                    if e_files:
                        mt = datetime.fromtimestamp(max(os.path.getmtime(f) for f in e_files), timezone.utc)
                        if mt >= start_time:
                            return p

    return f"/var/lib/jenkins/jobs/{candidate_names[0]}"

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'NIIT REAL-TIME CI/CD AUDIT':^70}")
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

        # Dynamically locate the Jenkins job directory
        job_dir = find_active_jenkins_job(["github_jenkins_aws_ecr_push", "ECR-Push-Eval"], START_TIME)

        # --- TC1: GitHub Webhook ---
        try:
            tc1_passed = os.path.exists(job_dir)
            if START_TIME and tc1_passed:
                check_files = [job_dir, os.path.join(job_dir, "config.xml"), os.path.join(job_dir, "builds"), os.path.join(job_dir, "nextBuildNumber")]
                existing_files = [f for f in check_files if os.path.exists(f)]
                mtime = datetime.fromtimestamp(max(os.path.getmtime(f) for f in existing_files), timezone.utc)
                if mtime < START_TIME:
                    tc1_passed = False
                    print(f"[WARN] Jenkins job was created/modified before current session started (Old Session).")

            if tc1_passed:
                results['tc1'] = True
                print(f"TC1: GitHub Webhook Configuration & Auto-Trigger ....... [PASSED] (2/2)")
            else:
                results['tc1'] = False
                print(f"TC1: GitHub Webhook Configuration & Auto-Trigger ....... [FAILED] (0/2)")
                print(f"     └─ [Reason]: Webhook trigger not configured or activated in current session.")
        except Exception as e:
            results['tc1'] = False
            print(f"TC1: GitHub Webhook Configuration & Auto-Trigger ....... [FAILED] (0/2)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC2: Docker Image Build Check ---
        if not results.get('tc1'):
            results['tc2'] = False
            print(f"TC2: Docker Image Build Check .......................... [FAILED] (0/3)")
            print(f"     └─ [Reason]: Prerequisite failed (Webhook invalid).")
            results['tc3'] = False
            print(f"TC3: AWS ECR Authentication ............................ [FAILED] (0/2)")
            print(f"     └─ [Reason]: Prerequisite failed.")
            results['tc4'] = False
            print(f"TC4: AWS ECR Image Push Check .......................... [FAILED] (0/3)")
            print(f"     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                tc2_passed = False
                builds_base = os.path.join(job_dir, "builds")
                latest_log = ""
                if os.path.exists(builds_base):
                    build_dirs = [os.path.join(builds_base, d) for d in os.listdir(builds_base) if d.isdigit()]
                    for b_dir in build_dirs:
                        if os.path.isdir(b_dir):
                            b_mtime = datetime.fromtimestamp(os.path.getmtime(b_dir), timezone.utc)
                            if not START_TIME or b_mtime >= START_TIME:
                                build_xml = os.path.join(b_dir, "build.xml")
                                log_file = os.path.join(b_dir, "log")
                                success = False
                                if os.path.exists(build_xml):
                                    with open(build_xml, 'r', encoding='utf-8', errors='ignore') as f:
                                        if "<result>SUCCESS</result>" in f.read():
                                            success = True
                                if not success and os.path.exists(log_file):
                                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                                        if "Finished: SUCCESS" in f.read():
                                            success = True
                                if success and os.path.exists(log_file):
                                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                                        latest_log = f.read()
                                        if "docker build" in latest_log or "Successfully built" in latest_log or "docker" in latest_log:
                                            tc2_passed = True
                                            break

                if tc2_passed:
                    results['tc2'] = True
                    print(f"TC2: Docker Image Build Check .......................... [PASSED] (3/3)")
                else:
                    results['tc2'] = False
                    print(f"TC2: Docker Image Build Check .......................... [FAILED] (0/3)")
                    print(f"     └─ [Reason]: Docker image build not executed or failed in current session.")
            except Exception as e:
                results['tc2'] = False
                print(f"TC2: Docker Image Build Check .......................... [FAILED] (0/3)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC3 & TC4: AWS ECR Auth & Push ---
            try:
                tc3_passed = False
                tc4_passed = False
                if results.get('tc2') and latest_log:
                    # Look for ECR login
                    if "get-login-password" in latest_log or "Login Succeeded" in latest_log or "aws ecr" in latest_log:
                        tc3_passed = True
                    # Look for Docker push log indicators
                    if "docker push" in latest_log and (".dkr.ecr." in latest_log or "ecr" in latest_log.lower()):
                        tc4_passed = True

                if tc3_passed:
                    results['tc3'] = True
                    print(f"TC3: AWS ECR Authentication ............................ [PASSED] (2/2)")
                else:
                    results['tc3'] = False
                    print(f"TC3: AWS ECR Authentication ............................ [FAILED] (0/2)")
                    print(f"     └─ [Reason]: AWS ECR login not executed or failed in current session.")
                    
                if tc4_passed:
                    results['tc4'] = True
                    print(f"TC4: AWS ECR Image Push Check .......................... [PASSED] (3/3)")
                else:
                    results['tc4'] = False
                    print(f"TC4: AWS ECR Image Push Check .......................... [FAILED] (0/3)")
                    print(f"     └─ [Reason]: Docker image not pushed to AWS ECR in current session.")
            except Exception as e:
                results['tc3'] = False
                results['tc4'] = False
                print(f"TC3: AWS ECR Authentication ............................ [FAILED] (0/2)")
                print(f"TC4: AWS ECR Image Push Check .......................... [FAILED] (0/3)")
                print(f"     └─ [Error]: {str(e)}")

        # Final Scoring
        total_score = 0
        if results.get('tc1'): total_score += 2
        if results.get('tc2'): total_score += 3
        if results.get('tc3'): total_score += 2
        if results.get('tc4'): total_score += 3
        
        print("-" * 70)
        print(f"{'TOTAL SCORE:':<52} {total_score}/10")
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
        
        root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == '__main__':
    verify_task()
