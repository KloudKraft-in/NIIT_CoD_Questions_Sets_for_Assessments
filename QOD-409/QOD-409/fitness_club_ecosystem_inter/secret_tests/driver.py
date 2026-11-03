import importlib.util
import os
import sys

def _setup_member(solution, name, tier):
    """Helper to create a hydrated MemberProfile for independent testing."""
    if not hasattr(solution, "MemberProfile"): return None
    p = solution.MemberProfile(name, tier)
    p.name = name; p.tier = tier; p.session_logs = []
    return p

def run_tests(solution_path=None):
    if solution_path is None:
        solution_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    
    # Load Student Solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    if not hasattr(solution, "ClubRegistry"):
        print("ERROR: ClubRegistry class not found."); return

    test_cases = [
        {"desc": "Verification of registry initialization", "func": "__init__", "m": 0},
        {"desc": "Registering a valid profile", "func": "add_member", "m": 1},
        {"desc": "Verification of tiered zone access", "func": "can_access_zone", "m": 1},
        {"desc": "Scheduling unique workout slots", "func": "schedule_session", "m": 1},
        {"desc": "Membership tier upgrade logic", "func": "upgrade_tier", "m": 1},
        {"desc": "Logging attendance record", "func": "mark_attendance", "m": 2},
        {"desc": "Membership + trainer fees calculation", "func": "get_monthly_fee", "m": 2},
        {"desc": "Member engagement analytics", "func": "get_member_stats", "m": 2}
    ]

    total_score = 0
    print("Running Local Evaluation for: Smart Fitness Club Ecosystem\n")

    for idx, case in enumerate(test_cases, 1):
        marks = int(case["m"])
        desc = case["desc"]
        try:
            reg = solution.ClubRegistry()
            # ULTIMATE INDEPENDENCE: State Injection
            if idx > 1 and not hasattr(reg, 'members'): reg.members = {}

            p_ok = False
            if idx == 1: 
                p_ok = (hasattr(reg, 'members') and isinstance(reg.members, dict) and len(reg.members) == 0)
            elif idx == 2: 
                p_ok = (reg.add_member("M1", "Standard") and "M1" in reg.members)
            elif idx == 3: 
                reg.members["M1"] = _setup_member(solution, "M1", "Premium")
                p_ok = (reg.can_access_zone("M1", "Pool") == True)
            elif idx == 4: 
                reg.members["M1"] = _setup_member(solution, "M1", "Standard")
                p_ok = (reg.schedule_session("M1", "2026-04-01", "10:00", "T1") == True)
            elif idx == 5: 
                reg.members["M1"] = _setup_member(solution, "M1", "Standard")
                p_ok = (reg.upgrade_tier("M1", "VIP") and reg.members["M1"].tier == "VIP")
            elif idx == 6: 
                prof = _setup_member(solution, "M1", "Standard")
                prof.session_logs.append({'date': "2026-04-01", 'time': "10:00", 'trainer': "T1", 'attended': False})
                reg.members["M1"] = prof
                p_ok = (reg.mark_attendance("M1", "2026-04-01", "10:00") == True)
            elif idx == 7: 
                prof = _setup_member(solution, "M1", "Premium")
                prof.session_logs.append({'date': "D1", 'time': "T1", 'trainer': "Tr1", 'attended': False})
                reg.members["M1"] = prof
                p_ok = (float(reg.get_monthly_fee("M1")) == 100.0)
            elif idx == 8: 
                prof = _setup_member(solution, "M1", "Standard")
                prof.session_logs = [{'date': "D1", 'attended': True}, {'date': "D2", 'attended': False}]
                reg.members["M1"] = prof
                stats = reg.get_member_stats("M1")
                p_ok = (stats.get('total_sessions') == 2 and stats.get('attendance_rate') == 50.0)

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
