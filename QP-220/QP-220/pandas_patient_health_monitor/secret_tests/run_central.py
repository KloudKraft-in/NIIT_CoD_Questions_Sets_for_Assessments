import sys
import os
from driver import test_student_code

if __name__ == "__main__":
    # Allow 3 OR 4 arguments now, so it doesn't crash
    if len(sys.argv) < 3:
        print("Usage: python3 run.py <vm_tag> <solution_filename> [exam_code]")
        sys.exit(1)

    vm_tag = sys.argv[1]
    solution_filename = sys.argv[2]
    
    # Safely capture exam_code if it exists
    exam_code = sys.argv[3] if len(sys.argv) > 3 else "UNKNOWN"

    solution_path = os.path.abspath(solution_filename)

    print("🚀 Starting run.py...")
    print(f"📌 VM Tag       : {vm_tag}")
    print(f"📌 Exam Code    : {exam_code}")
    print(f"📄 Solution file: {solution_filename}")
    print(f"📂 Full path    : {solution_path}")
    print("🧪 Running test_student_code...")

    if not os.path.exists(solution_path):
        print(f"❌ solution.py not found at: {solution_path}")
        sys.exit(1)

    # Note: If your driver.py can be updated, you can pass exam_code here!
    test_student_code(solution_path, vm_tag, exam_code) 
    
    print("✅ test_student_code finished successfully.")
