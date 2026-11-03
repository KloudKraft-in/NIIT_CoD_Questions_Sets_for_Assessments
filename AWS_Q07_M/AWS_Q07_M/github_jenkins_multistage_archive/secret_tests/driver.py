import json
import os
import sys
import glob
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'NIIT REAL-TIME JENKINS AUDIT':^70}")
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

        # Support both job names
        job_dir_primary = "/var/lib/jenkins/jobs/Multi-Stage-Pipeline"
        job_dir_fallback = "/var/lib/jenkins/jobs/github_jenkins_multistage_archive"
        job_dir = job_dir_primary if os.path.exists(job_dir_primary) else job_dir_fallback

        # --- TC1: GitHub Webhook Configuration ---
        try:
            tc1_passed = os.path.exists(job_dir)
            if START_TIME and tc1_passed:
                mtime = datetime.fromtimestamp(os.path.getmtime(job_dir), timezone.utc)
                if mtime < (START_TIME - timedelta(minutes=30)):
                    tc1_passed = False
                    print(f"[WARN] Jenkins job was created/modified before current session started (Old Session).")

            if tc1_passed:
                results['tc1'] = True
                print(f"TC1: GitHub Webhook Configuration ...................... [PASSED] (4/4)")
            else:
                results['tc1'] = False
                print(f"TC1: GitHub Webhook Configuration ...................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: Webhook trigger not configured or activated in current session.")
        except Exception as e:
            results['tc1'] = False
            print(f"TC1: GitHub Webhook Configuration ...................... [FAILED] (0/4)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC2: Jenkins Pipeline Job Creation ---
        if not results.get('tc1'):
            results['tc2'] = False
            print(f"TC2: Jenkins Pipeline Job Creation ..................... [FAILED] (0/4)")
            print(f"     └─ [Reason]: Prerequisite failed (Webhook invalid).")
            results['tc3'] = False
            print(f"TC3: Lint & Build Stage Execution ...................... [FAILED] (0/4)")
            print(f"     └─ [Reason]: Prerequisite failed.")
            results['tc4'] = False
            print(f"TC4: Artifact Creation Verification .................... [FAILED] (0/4)")
            print(f"     └─ [Reason]: Prerequisite failed.")
            results['tc5'] = False
            print(f"TC5: Artifact Archiving Verification ................... [FAILED] (0/4)")
            print(f"     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                tc2_passed = os.path.exists(os.path.join(job_dir, "config.xml"))
                if tc2_passed:
                    results['tc2'] = True
                    print(f"TC2: Jenkins Pipeline Job Creation ..................... [PASSED] (4/4)")
                else:
                    results['tc2'] = False
                    print(f"TC2: Jenkins Pipeline Job Creation ..................... [FAILED] (0/4)")
                    print(f"     └─ [Reason]: Job config not found.")
            except Exception as e:
                results['tc2'] = False
                print(f"TC2: Jenkins Pipeline Job Creation ..................... [FAILED] (0/4)")
                print(f"     └─ [Error]: {str(e)}")

            # --- TC3 & TC4: Stage Execution & Artifact Creation ---
            try:
                builds_path = f"{job_dir}/builds"
                all_builds = glob.glob(f"{builds_path}/[0-9]*") if os.path.exists(builds_path) else []
                
                # Robust build resolution: Parse build.xml to avoid unreliable symlinks
                successful_build_dir = None
                
                # Sort numerically by build ID descending
                try:
                    all_builds_sorted = sorted(all_builds, key=lambda x: int(os.path.basename(x)), reverse=True)
                except ValueError:
                    all_builds_sorted = all_builds
                
                for b_dir in all_builds_sorted:
                    build_xml = os.path.join(b_dir, "build.xml")
                    if os.path.exists(build_xml):
                        try:
                            tree = ET.parse(build_xml)
                            root = tree.getroot()
                            result_elem = root.find('result')
                            if result_elem is not None and result_elem.text == 'SUCCESS':
                                successful_build_dir = b_dir
                                break
                        except Exception:
                            continue
                
                tc3_passed = successful_build_dir is not None
                
                if START_TIME and tc3_passed:
                    mtime = datetime.fromtimestamp(os.path.getmtime(successful_build_dir), timezone.utc)
                    if mtime < (START_TIME - timedelta(minutes=30)):
                        tc3_passed = False
                        print(f"[WARN] Jenkins build was completed before current session started (Old Session).")

                if tc3_passed:
                    results['tc3'] = True
                    print(f"TC3: Lint & Build Stage Execution ...................... [PASSED] (4/4)")
                else:
                    results['tc3'] = False
                    print(f"TC3: Lint & Build Stage Execution ...................... [FAILED] (0/4)")
                    if len(all_builds) == 0:
                        print(f"     └─ [Reason]: No builds found! The Webhook did NOT trigger Jenkins, or you haven't run a build yet.")
                    else:
                        print(f"     └─ [Reason]: Builds exist, but NONE were successful. Checked {len(all_builds)} builds for a SUCCESS result in build.xml.")
                        
                tc4_passed = tc3_passed
                if tc4_passed:
                    results['tc4'] = True
                    print(f"TC4: Artifact Creation Verification .................... [PASSED] (4/4)")
                else:
                    results['tc4'] = False
                    print(f"TC4: Artifact Creation Verification .................... [FAILED] (0/4)")
                    print(f"     └─ [Reason]: Pipeline did not succeed.")
            except Exception as e:
                results['tc3'] = False
                results['tc4'] = False
                print(f"TC3: Lint & Build Stage Execution ...................... [FAILED] (0/4)")
                print(f"TC4: Artifact Creation Verification .................... [FAILED] (0/4)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC5: Artifact Archiving ---
            try:
                tc5_passed = False
                archive_dir = None
                
                if successful_build_dir:
                    archive_dir = f"{successful_build_dir}/archive"
                    tc5_passed = os.path.exists(archive_dir) and len(os.listdir(archive_dir)) > 0
                    
                    if START_TIME and tc5_passed:
                        mtime = datetime.fromtimestamp(os.path.getmtime(archive_dir), timezone.utc)
                        if mtime < (START_TIME - timedelta(minutes=30)):
                            tc5_passed = False

                if tc5_passed:
                    results['tc5'] = True
                    print(f"TC5: Artifact Archiving Verification ................... [PASSED] (4/4)")
                else:
                    results['tc5'] = False
                    print(f"TC5: Artifact Archiving Verification ................... [FAILED] (0/4)")
                    if not successful_build_dir:
                        print(f"     └─ [Reason]: Prerequisite failed (No successful build found).")
                    else:
                        print(f"     └─ [Reason]: Build was successful, but NO artifacts were found in {archive_dir}. Check your archiveArtifacts directive.")
            except Exception as e:
                results['tc5'] = False
                print(f"TC5: Artifact Archiving Verification ................... [FAILED] (0/4)")
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
