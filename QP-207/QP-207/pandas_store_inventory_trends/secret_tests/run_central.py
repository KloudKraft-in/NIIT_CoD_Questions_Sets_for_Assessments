#!/usr/bin/env python3
"""
Central server test runner for pandas_store_inventory_trends
Launches driver_central with server parameters
"""

import sys
import os

# Add the secret_tests directory to path to import driver_central
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from driver_central import test_student_code

def main():
    """Main entry point for central server testing."""
    
    if len(sys.argv) < 2:
        print("Usage: python run_central.py <solution_path> [vm_tag]")
        print("\nExample:")
        print("  python run_central.py /path/to/solution.py")
        print("  python run_central.py /path/to/solution.py vm_001")
        sys.exit(1)
    
    solution_path = sys.argv[1]
    vm_tag = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Verify solution path exists
    if not os.path.exists(solution_path):
        print(f"ERROR: Solution file not found: {solution_path}")
        sys.exit(1)
    
    # Run tests
    test_student_code(solution_path, vm_tag)

if __name__ == "__main__":
    main()
