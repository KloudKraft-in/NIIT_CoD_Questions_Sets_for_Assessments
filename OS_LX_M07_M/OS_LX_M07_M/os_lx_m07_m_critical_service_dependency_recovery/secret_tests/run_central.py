import os
import sys
import json
import traceback

try:
    from driver_central import verify_task_central
except ImportError:
    from driver import verify_task_central

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_central.py <vm_tag> [solution_filename] [exam_code]")
        sys.exit(1)

    vm_tag = sys.argv[1]
    if len(sys.argv) > 2:
        solution_filename = sys.argv[2]
        solution_path = os.path.abspath(solution_filename)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        solution_path = os.path.join(script_dir, "..", "student_workspace", "solution.json")

    exam_code = sys.argv[3] if len(sys.argv) > 3 else "UNKNOWN"

    print("\n🚀 Starting Central Evaluation...")
    if not os.path.exists(solution_path):
        print(f"❌ Solution file not found at: {solution_path}")
        sys.exit(1)

    try:
        with open(solution_path, 'r') as f:
            data = json.load(f)
            start_time = data.get('assessment_start_time')
            verify_task_central(vm_tag, start_time, exam_code, solution_path)
        print("✅ Central Evaluation finished successfully.")
    except Exception as e:
        print(f"❌ An error occurred during evaluation: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
