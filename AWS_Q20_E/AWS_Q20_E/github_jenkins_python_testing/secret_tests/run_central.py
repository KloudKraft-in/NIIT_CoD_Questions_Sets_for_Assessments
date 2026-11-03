import os
import sys
import json
import traceback

# Handle both Local Repo naming (driver_central) and Central Server naming (driver)
try:
    from driver import verify_aws_on_server
except ImportError:
    from driver_central import verify_aws_on_server

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 run_central.py <vm_tag> <solution_filename>")
        sys.exit(1)

    vm_tag = sys.argv[1]
    solution_filename = sys.argv[2]
    solution_path = os.path.abspath(solution_filename)

    print("\n[SYSTEM] Starting DevOps Distributed Jenkins Central Evaluation...")
    print(f"[INFO] VM Tag       : {vm_tag}")
    print(f"[INFO] Solution file: {solution_filename}")
    print(f"[INFO] Full path    : {solution_path}")
    print("[INFO] Invoking verify_aws_on_server from central driver...")

    if not os.path.exists(solution_path):
        print(f"[ERROR] Solution file not found at: {solution_path}")
        sys.exit(1)

    if not solution_filename.endswith('.json'):
        print(f"[ERROR] Invalid submission format. DevOps assessments require a solution.json metadata file.")
        sys.exit(1)

    try:
        with open(solution_path, 'r') as f:
            data = json.load(f)
            niit_user = data.get('niit_username') or data.get('candidate_prefix')
            start_time = data.get('assessment_start_time')
            verify_aws_on_server(data.get('email', 'GUEST'), data.get('question_id', 'AWS_Q20_E'), niit_user, start_time, solution_data=data)
        
        print("[SUCCESS] Central Evaluation finished successfully.")
    except Exception as e:
        print(f"[ERROR] An error occurred during evaluation: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
