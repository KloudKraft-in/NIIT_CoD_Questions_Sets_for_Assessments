import os
import sys
import json
import traceback

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except Exception:
    script_dir = os.getcwd()

paths_to_insert = [
    os.path.join(script_dir, 'secret_tests'),
    os.path.join(script_dir, 'secret_test'),
    script_dir
]

for path in reversed(paths_to_insert):
    abs_path = os.path.abspath(path)
    if abs_path in sys.path:
        sys.path.remove(abs_path)
    sys.path.insert(0, abs_path)

from driver_central import verify_task_central

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    vm_tag = sys.argv[1]
    if len(sys.argv) > 2:
        solution_filename = sys.argv[2]
        solution_path = os.path.abspath(solution_filename)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        solution_path = os.path.join(script_dir, "..", "student_workspace", "solution.json")

    exam_code = sys.argv[3] if len(sys.argv) > 3 else "UNKNOWN"

    if not os.path.exists(solution_path):
        for ext in ['.java', '.py', '.json']:
            alt_path = solution_path.rsplit('.', 1)[0] + ext
            if os.path.exists(alt_path):
                solution_path = alt_path
                break

    try:
        if os.path.exists(solution_path):
            with open(solution_path, 'r') as f:
                try:
                    data = json.load(f)
                    start_time = data.get('assessment_start_time')
                except json.JSONDecodeError:
                    start_time = None
            verify_task_central(vm_tag, start_time, exam_code, solution_path=solution_path)
        else:
            verify_task_central(vm_tag, None, exam_code)
    except Exception as e:
        verify_task_central(vm_tag, None, exam_code)

if __name__ == "__main__":
    main()
