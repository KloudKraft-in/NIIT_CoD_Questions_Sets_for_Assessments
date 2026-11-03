import importlib.util
import os
import sys
import random

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    print("Running Tests for: Retail Inventory System (Independence & Unique Methods Mode)\n")
    report_lines = ["Running Tests for: Retail Inventory System (Independence & Unique Methods Mode)\n"]

    if not hasattr(solution, "RetailInventorySystem"):
        print("ERROR: RetailInventorySystem class not found"); return
    
    SystemClass = solution.RetailInventorySystem
    
    tc_configs = [
        ("Initialize retail store structure", 0),
        ("Register a new product", 5),
        ("Update stock for existing item", 5),
        ("Process a sale with stock check", 5),
        ("Calculate total inventory value", 5),
        ("Retrieve individual product details", 5),
        ("Remove product from the catalog", 5)
    ]

    random.seed(None)

    total_score = 0
    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, current_obj, data_params):
                name, price, stock = data_params
                if idx == 1: 
                    t1 = SystemClass()
                    if not hasattr(t1, 'inventory'): return "MISSING_ATTR"
                    return t1.inventory
                
                if idx == 2: return current_obj.register_product(name, price, stock)
                if idx == 3: current_obj.inventory[name] = {'price': price, 'stock': stock}; return current_obj.restock_item(name, 10)
                if idx == 4: current_obj.inventory[name] = {'price': price, 'stock': stock}; return current_obj.complete_sale(name, 2)
                if idx == 5: current_obj.inventory[name] = {'price': price, 'stock': stock}; return current_obj.inventory_report()
                if idx == 6: current_obj.inventory[name] = {'price': price, 'stock': stock}; return current_obj.get_product_info(name)
                if idx == 7: current_obj.inventory[name] = {'price': price, 'stock': stock}; return current_obj.remove_product(name)
                return None

            p_ok, h_det, none_ret = False, False, False
            actual_res = None
            expected_res = None

            if i == 1:
                actual_res = run_t(i, None, ("", 0, 0))
                expected_res = {}
                p_ok = (actual_res == expected_res)
            else:
                # DUAL RUN
                rv, rp = random.randint(10, 80), float(random.randint(155, 455))
                
                # RUN 1
                obj1 = SystemClass(); obj1.inventory = {}
                res1 = run_t(idx=i, current_obj=obj1, data_params=("TestX", 100.0, 10))
                
                # RUN 2
                obj2 = SystemClass(); obj2.inventory = {}
                res2 = run_t(idx=i, current_obj=obj2, data_params=("TestX", rp, rv))
                
                actual_res = res2
                if i == 2: expected_res = "Product TestX registered."
                elif i == 3: expected_res = f"Restocked TestX. Now: {rv + 10}"
                elif i == 4: expected_res = f"Bill: ${rp * 2}"
                elif i == 5: expected_res = float(rp * rv)
                elif i == 6: expected_res = {'price': rp, 'stock': rv}
                elif i == 7: expected_res = "Removed TestX from catalog."

                if actual_res == expected_res:
                    p_ok = True
                elif actual_res is None:
                    none_ret = True
                elif res1 == res2:
                    h_det = True

            if p_ok:
                total_score += marks
                msg = f"PASS TC{i} [{desc}] ({marks}/{marks})"
            elif none_ret:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Method not implemented / No return value"
            elif h_det:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Hardcoded. Dynamic check failed."
            else:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output. Expected: {expected_res}"
        except Exception as e: msg = f"FAIL TC{i} [{desc}] | Error: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/30.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    import sys
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
