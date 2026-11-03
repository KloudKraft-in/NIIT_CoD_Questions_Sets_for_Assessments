import importlib.util
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_central.py <vm_tag> [solution_filename]")
        sys.exit(1)

    vm_tag = sys.argv[1]
    solution_filename = sys.argv[2] if len(sys.argv) > 2 else "solution.py"
    
    # Get script directory and construct solution path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    solution_path = os.path.join(script_dir, "..", "student_workspace", solution_filename)
    
    # Load and run driver_central tests
    driver_central_path = os.path.join(script_dir, "driver_central.py")
    spec = importlib.util.spec_from_file_location("driver_central", driver_central_path)
    driver_central = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_central)
    
    driver_central.test_student_code(solution_path, vm_tag)
