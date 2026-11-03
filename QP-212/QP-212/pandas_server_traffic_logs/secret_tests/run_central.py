import importlib.util
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_central.py <vm_tag> [solution_filename]")
        print("  python run_central.py <solution_path> [vm_tag]")
        sys.exit(1)

    arg1 = sys.argv[1]
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None

    # Inspect arg1 to determine if it is a path or a tag
    if arg1.endswith(".py") or "/" in arg1 or "\\" in arg1 or os.path.exists(arg1):
        # Format: python run_central.py <solution_path> [vm_tag]
        solution_path = os.path.abspath(arg1)
        vm_tag = arg2 if arg2 else "DEFAULT"
    else:
        # Format: python run_central.py <vm_tag> [solution_filename]
        vm_tag = arg1
        sol_name = arg2 if arg2 else "solution.py"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        solution_path = os.path.join(script_dir, "..", "student_workspace", sol_name)
    
    # Load and run driver_central tests
    script_dir = os.path.dirname(os.path.abspath(__file__))
    driver_central_path = os.path.join(script_dir, "driver_central.py")
    spec = importlib.util.spec_from_file_location("driver_central", driver_central_path)
    driver_central = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_central)
    
    driver_central.test_student_code(solution_path, vm_tag)
