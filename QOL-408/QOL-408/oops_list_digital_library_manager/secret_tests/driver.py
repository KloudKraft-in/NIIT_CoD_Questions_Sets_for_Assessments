import importlib.util
import os
import sys

def _setup_book(solution, title, cat, avail, days):
    b = solution.Book(title, cat, avail, days)
    b.title = title; b.category = cat; b.is_available = avail; b.days_borrowed = days
    return b

def run_tests(solution_path=None):
    if solution_path is None:
        solution_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    if not hasattr(solution, "DigitalLibraryManager"):
        print("ERROR: DigitalLibraryManager class not found."); return

    test_cases = [
        {"desc": "Instantiate complex structures", "func": "__init__", "m": 0},
        {"desc": "Add Book objects to system", "func": "add_book", "m": 3},
        {"desc": "Borrow with state initialization", "func": "borrow_book", "m": 3},
        {"desc": "Simulate multi-day holding period", "func": "pass_time", "m": 3},
        {"desc": "Calculate late fines (Tech vs General)", "func": "get_fine", "m": 3},
        {"desc": "Filter available titles by category", "func": "available_in_category", "m": 4},
        {"desc": "Return logic with fine-block check", "func": "return_book", "m": 4}
    ]

    total_score = 0
    print("Running Local Evaluation for: Digital Library Manager\n")

    for idx, case in enumerate(test_cases, 1):
        marks = int(case["m"])
        desc = case["desc"]
        try:
            lib = solution.DigitalLibraryManager()
            has_init_state = hasattr(lib, 'catalog')
            if not has_init_state: lib.catalog = {}

            p_ok = False
            if idx == 1: 
                p_ok = has_init_state and isinstance(lib.catalog, dict)
            elif idx == 2: 
                lib.add_book("Book1", "Tech")
                p_ok = ("Book1" in lib.catalog)
            elif idx == 3: 
                lib.catalog["Book1"] = _setup_book(solution, "Book1", "Tech", True, 0)
                p_ok = (lib.borrow_book("Book1") == "Borrowed Book1" and lib.catalog["Book1"].is_available == False)
            elif idx == 4: 
                lib.catalog["Book1"] = _setup_book(solution, "Book1", "Tech", False, 0)
                p_ok = (lib.pass_time("Book1", 10) == "Days tracked for Book1: 10")
            elif idx == 5: 
                lib.catalog["Book1"] = _setup_book(solution, "Book1", "Tech", False, 20)
                p_ok = (lib.get_fine("Book1") == 30.0)
            elif idx == 6: 
                lib.catalog = {"Book1": _setup_book(solution, "Book1", "Tech", True, 0)}
                p_ok = (lib.available_in_category("Tech") == ["Book1"])
            elif idx == 7: 
                lib.catalog["Book1"] = _setup_book(solution, "Book1", "Tech", False, 20)
                p_ok = ("Fine Due: $30.0" in lib.return_book("Book1"))

            if p_ok: 
                total_score += marks
                print(f"PASS TC{idx} [{desc}] ({marks}/{marks})")
            else: 
                print(f"FAIL TC{idx} [{desc}] (0/{marks})")
        except Exception as e:
            print(f"FAIL TC{idx} [{desc}] (0/{marks}) | Error: {e}")

    print(f"\nSCORE: {total_score}/20 (Visible) | {total_score}/20 (Total)")

if __name__ == "__main__":
    sol_file = sys.argv[1] if len(sys.argv) > 1 else None
    run_tests(sol_file)
