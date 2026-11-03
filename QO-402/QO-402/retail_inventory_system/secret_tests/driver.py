import importlib.util
import os

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Retail Inventory System\n")
    report_lines = ["Running Tests for: Retail Inventory System\n"]

    test_cases = [
        {
            "desc": "Initialize retail store structure",
            "func": "initialize",
            "setup": lambda: student_module.RetailStore(),
            "call": lambda obj: obj.inventory,
            "check": lambda result: isinstance(result, dict) and len(result) == 0,
            "marks": 5
        },
        {
            "desc": "Register a new product",
            "func": "register_product",
            "setup": lambda: student_module.RetailStore(),
            "call": lambda obj: (obj.register_product("Laptop", 1200.0, 10), obj.inventory.get("Laptop")),
            "check": lambda result: isinstance(result, tuple) and "Product Laptop registered." in result[0] and result[1] == {"price": 1200.0, "stock": 10},
            "marks": 5
        },
        {
            "desc": "Update stock for existing item",
            "func": "restock_item",
            "setup": lambda: _setup_restock(student_module),
            "call": lambda obj: (obj.restock_item("Laptop", 5), obj.inventory.get("Laptop", {}).get("stock")),
            "check": lambda result: isinstance(result, tuple) and "Restocked Laptop. Now: 15" in result[0] and result[1] == 15,
            "marks": 5
        },
        {
            "desc": "Process a sale with stock check",
            "func": "complete_sale",
            "setup": lambda: _setup_sale(student_module),
            "call": lambda obj: (obj.complete_sale("Laptop", 2), obj.inventory.get("Laptop", {}).get("stock")),
            "check": lambda result: isinstance(result, tuple) and "Bill: $2400.0" in result[0] and result[1] == 8,
            "marks": 5
        },
        {
            "desc": "Calculate total inventory value",
            "func": "inventory_report",
            "setup": lambda: _setup_inventory(student_module),
            "call": lambda obj: obj.inventory_report(),
            "check": lambda result: result == 13000.0,
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 5)
        
        max_score += marks
        
        try:
            obj = case["setup"]()
            
            # Execute test
            result = case["call"](obj)
            passed = case["check"](result)
            
            if passed:
                msg = f"PASS Visible Test Case {idx} Passed: {case['desc']}"
                total_score += marks
            else:
                msg = f"FAIL Visible Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL Visible Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/25.0 (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_restock(student_module):
    """Setup for restock test."""
    store = student_module.RetailStore()
    store.register_product("Laptop", 1200.0, 10)
    return store


def _setup_sale(student_module):
    """Setup for sale test."""
    store = student_module.RetailStore()
    store.register_product("Laptop", 1200.0, 10)
    return store


def _setup_inventory(student_module):
    """Setup for inventory report test."""
    store = student_module.RetailStore()
    store.register_product("Laptop", 1200.0, 10)
    store.register_product("Mouse", 50.0, 20)
    return store


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
