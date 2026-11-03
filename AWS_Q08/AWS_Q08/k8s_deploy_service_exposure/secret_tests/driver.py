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
    print(f"{'NIIT REAL-TIME KUBERNETES AUDIT':^70}")
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
        max_duration = 60  # 60 Min assessment

        if elapsed_minutes > max_duration + 5: # 5 min grace
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating Resources for: {user_prefix}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        # --- TC1: Kubernetes Deployment & Replicas ---
        try:
            # Check kubectl get deployment
            dep_check = subprocess.run(["kubectl", "get", "deployment", "-o", "json"], capture_output=True, text=True)
            tc1_passed = False
            if dep_check.returncode == 0:
                try:
                    dep_data = json.loads(dep_check.stdout)
                    items = dep_data.get("items", [])
                    if len(items) > 0:
                        tc1_passed = True
                        if START_TIME:
                            creation_timestamp = items[0].get("metadata", {}).get("creationTimestamp")
                            if creation_timestamp:
                                ctime = datetime.fromisoformat(creation_timestamp.replace('Z', '+00:00'))
                                if ctime < START_TIME:
                                    tc1_passed = False
                                    print(f"[WARN] Kubernetes deployment was created before current session started (Old Session).")
                except Exception:
                    pass

            if tc1_passed:
                results['tc1'] = True
                print(f"TC1: Kubernetes Deployment & Replica Status .............. [PASSED] (10/10)")
            else:
                results['tc1'] = False
                print(f"TC1: Kubernetes Deployment & Replica Status .............. [FAILED] (0/10)")
                print(f"     └─ [Reason]: Deployment missing or created before current session.")
        except Exception as e:
            results['tc1'] = False
            print(f"TC1: Kubernetes Deployment & Replica Status .............. [FAILED] (0/10)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC2: Pod Health & Readiness ---
        if not results.get('tc1'):
            results['tc2'] = False
            print(f"TC2: Pod Health & Readiness Verification ............... [FAILED] (0/10)")
            print(f"     └─ [Reason]: Prerequisite failed (Deployment invalid).")
            results['tc3'] = False
            print(f"TC3: Service LoadBalancer Exposure & Port Check ........ [FAILED] (0/10)")
            print(f"     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                pod_check = subprocess.run(["kubectl", "get", "pods", "-o", "json"], capture_output=True, text=True)
                tc2_passed = False
                if pod_check.returncode == 0:
                    try:
                        pod_data = json.loads(pod_check.stdout)
                        items = pod_data.get("items", [])
                        if len(items) > 0:
                            tc2_passed = any(p.get("status", {}).get("phase") == "Running" for p in items)
                    except Exception:
                        pass

                if tc2_passed:
                    results['tc2'] = True
                    print(f"TC2: Pod Health & Readiness Verification ............... [PASSED] (10/10)")
                else:
                    results['tc2'] = False
                    print(f"TC2: Pod Health & Readiness Verification ............... [FAILED] (0/10)")
                    print(f"     └─ [Reason]: Pods are crashing, pending, or not ready in current session.")
            except Exception as e:
                results['tc2'] = False
                print(f"TC2: Pod Health & Readiness Verification ............... [FAILED] (0/10)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC3: Service LoadBalancer Exposure ---
            try:
                svc_check = subprocess.run(["kubectl", "get", "svc", "-o", "json"], capture_output=True, text=True)
                tc3_passed = False
                if svc_check.returncode == 0:
                    try:
                        svc_data = json.loads(svc_check.stdout)
                        items = svc_data.get("items", [])
                        tc3_passed = any(s.get("spec", {}).get("type") == "LoadBalancer" for s in items)
                    except Exception:
                        pass

                if tc3_passed:
                    results['tc3'] = True
                    print(f"TC3: Service LoadBalancer Exposure & Port Check ........ [PASSED] (10/10)")
                else:
                    results['tc3'] = False
                    print(f"TC3: Service LoadBalancer Exposure & Port Check ........ [FAILED] (0/10)")
                    print(f"     └─ [Reason]: Service is not LoadBalancer type or missing in current session.")
            except Exception as e:
                results['tc3'] = False
                print(f"TC3: Service LoadBalancer Exposure & Port Check ........ [FAILED] (0/10)")
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
