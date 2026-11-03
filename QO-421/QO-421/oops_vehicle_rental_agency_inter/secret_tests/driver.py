import importlib.util
import os
import sys

def run_tests(solution_path=None):
    if solution_path is None:
        solution_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    if not hasattr(solution, "VehicleRentalAgency"):
        print("ERROR: VehicleRentalAgency class not found."); return

    test_cases = [
        {"desc": "Initialize complex fleet registry", "func": "__init__", "m": 0},
        {"desc": "Add vehicles with zero rental count", "func": "add_vehicle", "m": 2},
        {"desc": "Rental start with Maintenance trigger", "func": "initiate_rental", "m": 2},
        {"desc": "Bill with Hourly + Distance + Insurance", "func": "calculate_bill", "m": 2},
        {"desc": "Generate status report for full fleet", "func": "get_service_status", "m": 1},
        {"desc": "Project theoretical 24hr revenue", "func": "project_daily_revenue", "m": 1},
        {"desc": "Release vehicle from Maintenance cycle", "func": "clear_maintenance", "m": 2}
    ]

    total_score = 0
    print("Running Local Evaluation for: Vehicle Fleet Rental\n")

    for idx, case in enumerate(test_cases, 1):
        marks = int(case["m"])
        desc = case["desc"]
        try:
            agency = solution.VehicleRentalAgency()
            if not hasattr(agency, 'fleet'): agency.fleet = {}

            p_ok = False
            if idx == 1: 
                p_ok = isinstance(agency.fleet, dict)
            elif idx == 2: 
                agency.add_vehicle("V1", "Car", 50.0)
                p_ok = ("V1" in agency.fleet)
            elif idx == 3: 
                agency.fleet["V1"] = {'type': 'Car', 'rate': 50.0, 'count': 4, 'status': 'Available'}
                p_ok = (agency.initiate_rental("V1") == "Needs Maintenance." and agency.fleet["V1"]['status'] == "Maint")
            elif idx == 4: 
                agency.fleet["V1"] = {'type': 'Car', 'rate': 50.0, 'count': 1, 'status': 'Available'}
                p_ok = (agency.calculate_bill("V1", 10, 100, True) == 750.0)
            elif idx == 5: 
                agency.fleet = {"V1": {'status': 'Rented'}}
                p_ok = (agency.get_service_status() == {"V1": "Rented"})
            elif idx == 6: 
                agency.fleet = {"V1": {'rate': 50.0, 'status': 'Available'}, "V2": {'rate': 30, 'status': 'Rented'}}
                p_ok = (agency.project_daily_revenue() == 1200.0)
            elif idx == 7: 
                agency.fleet["V1"] = {'status': 'Maint'}
                p_ok = (agency.clear_maintenance("V1") == "Maintenance Clear for V1.")

            if p_ok: 
                total_score += marks
                print(f"PASS TC{idx} [{desc}] ({marks}/{marks})")
            else: 
                print(f"FAIL TC{idx} [{desc}] (0/{marks})")
        except Exception as e:
            print(f"FAIL TC{idx} [{desc}] (0/{marks}) | Error: {e}")

    print(f"\nSCORE: {total_score}/10 (Visible) | {total_score}/10 (Total)")

if __name__ == "__main__":
    run_tests()
