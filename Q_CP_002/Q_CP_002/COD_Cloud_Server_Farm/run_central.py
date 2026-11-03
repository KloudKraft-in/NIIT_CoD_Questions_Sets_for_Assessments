import sys
import os

# Fix encoding for Windows consoles printing emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure the script directory is in sys.path to resolve 'secret_tests' from any cwd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from secret_tests.driver_central import test_student_code

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 run_central.py <vm_tag> <solution_filename>")
        sys.exit(1)

    vm_tag = sys.argv[1]
    solution_filename = sys.argv[2]
    # Ensure full path for the solution file
    solution_path = os.path.abspath(solution_filename)

    print("🚀 Starting run_central.py (C++ Central Mode)...")
    print(f"📌 VM Tag       : {vm_tag}")
    print(f"📄 Solution file: {solution_filename}")
    print(f"📂 Full path    : {solution_path}")
    print("🧪 Running test_student_code via Central Driver...")

    if not os.path.exists(solution_path):
        print(f"❌ solution.cpp not found at: {solution_path}")
        sys.exit(1)

    test_student_code(solution_path, vm_tag)
    print("✅ test_student_code finished successfully.")
