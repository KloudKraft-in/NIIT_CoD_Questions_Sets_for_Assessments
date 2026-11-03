import importlib.util
import os
import sys

def _setup_room(solution, r_no, r_type, rate, status="Available", ci_count=0):
    room = solution.Room(r_no, r_type, rate)
    room.room_no = r_no; room.r_type = r_type; room.rate = rate
    room.status = status; room.checkin_count = ci_count
    return room

def run_tests(solution_path=None):
    if solution_path is None:
        solution_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    if not hasattr(solution, "SmartHotelManager"):
        print("ERROR: SmartHotelManager class not found."); return

    test_cases = [
        {"desc": "Instantiate complex structures", "func": "__init__", "m": 0},
        {"desc": "Register a new Room object", "func": "register_room", "m": 1},
        {"desc": "Check-in with status validation", "func": "secure_check_in", "m": 2},
        {"desc": "Bill with Season & Type multipliers", "func": "calculate_checkout_bill", "m": 2},
        {"desc": "Housekeeping vs Maintenance trigger", "func": "complete_stay", "m": 2},
        {"desc": "Professional Release of Room to Avail", "func": "system_release", "m": 2},
        {"desc": "Calculate 24hr potential of all rooms", "func": "total_inventory_potential", "m": 1}
    ]

    total_score = 0
    print("Running Local Evaluation for: Smart Hotel Reservation\n")

    for idx, case in enumerate(test_cases, 1):
        marks = int(case["m"])
        desc = case["desc"]
        try:
            hotel = solution.SmartHotelManager()
            has_init_state = hasattr(hotel, 'rooms')
            if not has_init_state: hotel.rooms = {}

            p_ok = False
            if idx == 1: 
                p_ok = has_init_state and isinstance(hotel.rooms, dict)
            elif idx == 2: 
                hotel.register_room(101, "Deluxe", 200.0)
                p_ok = (101 in hotel.rooms)
            elif idx == 3: 
                hotel.rooms[101] = _setup_room(solution, 101, "Standard", 100.0)
                p_ok = (hotel.secure_check_in(101) == "Check-in: 101" and hotel.rooms[101].status == "Occupied")
            elif idx == 4: 
                hotel.rooms[101] = _setup_room(solution, 101, "Deluxe", 100.0)
                p_ok = (abs(hotel.calculate_checkout_bill(101, 10, True) - 1800.0) < 0.01)
            elif idx == 5: 
                hotel.rooms[101] = _setup_room(solution, 101, "Standard", 100.0, ci_count=3)
                p_ok = (hotel.complete_stay(101) == "Direct to Maintenance." and hotel.rooms[101].status == "Maint")
            elif idx == 6: 
                hotel.rooms[101] = _setup_room(solution, 101, "Standard", 100.0, status="Cleaning")
                p_ok = (hotel.system_release(101) == "Room 101 is Free." and hotel.rooms[101].status == "Available")
            elif idx == 7: 
                hotel.rooms = {101: _setup_room(solution, 101, "Standard", 100.0)}
                p_ok = (hotel.total_inventory_potential() == 2400.0)

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
