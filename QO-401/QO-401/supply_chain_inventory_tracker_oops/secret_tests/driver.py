import importlib.util
import os
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Supply Chain Inventory Tracker\n")
    report_lines = ["Running Tests for: Supply Chain Inventory Tracker\n"]

    test_cases = [
        {
            "desc": "Add a new product to inventory",
            "func": "add_product",
            "setup": lambda: student_module.SupplyChainInventory(),
            "call": lambda obj: obj.add_product("PRD101", 50),
            "check": lambda result: isinstance(result, dict) and result.get("PRD101") == 50,
            "marks": 2.5
        },
        {
            "desc": "Fulfill an order by deducting stock",
            "func": "fulfill_order",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc)[0],
            "call": lambda obj: obj.fulfill_order("PRD101", 10),
            "check": lambda result: isinstance(result, dict) and result.get("PRD101") == 40,
            "marks": 2.5
        },
        {
            "desc": "Restock returned goods back into inventory",
            "func": "restock_return",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc.fulfill_order("PRD101", 10), sc)[0],
            "call": lambda obj: obj.restock_return("PRD101", 5),
            "check": lambda result: isinstance(result, dict) and result.get("PRD101") == 45,
            "marks": 2.5
        },
        {
            "desc": "List products with available stock",
            "func": "list_available_products",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc.add_product("PRD102", 0), sc)[0],
            "call": lambda obj: obj.list_available_products(),
            "check": lambda result: isinstance(result, list) and "PRD101" in result and "PRD102" not in result,
            "marks": 2.5
        },
        {
            "desc": "Update product stock when already exists",
            "func": "add_product",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc)[0],
            "call": lambda obj: obj.add_product("PRD101", 25),
            "check": lambda result: isinstance(result, dict) and result.get("PRD101") == 75,
            "marks": 2.5
        },
        {
            "desc": "Fulfill order with insufficient stock raises error",
            "func": "fulfill_order",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 10), sc)[0],
            "call": lambda obj: obj.fulfill_order("PRD101", 20),
            "check": lambda result: False,  # Should raise error
            "should_raise": ValueError,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Products with zero stock not listed",
            "func": "list_available_products",
            "setup": lambda: (sc := student_module.SupplyChainInventory(), sc.add_product("PRD101", 50), sc.add_product("PRD102", 10), sc.fulfill_order("PRD102", 10), sc)[0],
            "call": lambda obj: obj.list_available_products(),
            "check": lambda result: isinstance(result, list) and "PRD101" in result and "PRD102" not in result,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Restock return for non-existent product creates entry",
            "func": "restock_return",
            "setup": lambda: student_module.SupplyChainInventory(),
            "call": lambda obj: obj.restock_return("PRD999", 15),
            "check": lambda result: isinstance(result, dict) and result.get("PRD999") == 15,
            "marks": 2.5,
            "is_hidden": True
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2.5)
        is_hidden = case.get("is_hidden", False)
        
        if not is_hidden:
            max_score += marks
        
        try:
            obj = case["setup"]()
            
            # Check for pass-only implementation
            func = getattr(obj, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()
            if 'pass' in src and len(src) < 80:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue
            
            # Execute test
            try:
                result = case["call"](obj)
                
                if case.get("should_raise"):
                    test_type = "Hidden" if is_hidden else "Visible"
                    msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Expected {case['should_raise'].__name__} but no error raised"
                    print(msg)
                    report_lines.append(msg)
                else:
                    passed = case["check"](result)
                    if passed:
                        test_type = "Hidden" if is_hidden else "Visible"
                        msg = f"PASS {test_type} Test Case {idx} Passed: {case['desc']}"
                        if not is_hidden:
                            total_score += marks
                    else:
                        test_type = "Hidden" if is_hidden else "Visible"
                        msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"
                    
                    print(msg)
                    report_lines.append(msg)
            
            except Exception as e:
                if case.get("should_raise") and isinstance(e, case.get("should_raise")):
                    test_type = "Hidden" if is_hidden else "Visible"
                    msg = f"PASS {test_type} Test Case {idx} Passed: {case['desc']}"
                    if not is_hidden:
                        total_score += marks
                    print(msg)
                    report_lines.append(msg)
                else:
                    test_type = "Hidden" if is_hidden else "Visible"
                    msg = f"FAIL {test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"
                    print(msg)
                    report_lines.append(msg)
        
        except Exception as e:
            test_type = "Hidden" if is_hidden else "Visible"
            msg = f"FAIL {test_type} Test Case {idx} Setup Error: {case['desc']} | Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/12.5 (Visible) | Total: 20 (Visible: 12.5 + Hidden: 7.5)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
