import importlib.util
import os
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(student_module)
    except SyntaxError as e:
        error_msg = f"SYNTAX ERROR: {str(e)}"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return

    print("Running Tests for: Task Registry Manager\n")
    report_lines = ["Running Tests for: Task Registry Manager\n"]

    # Test cases - each with independent setup to ensure test isolation
    test_cases = [
        {
            "desc": "Add task and verify [P] prefix",
            "func": "add_task",
            "setup": lambda: (student_module.TaskRegistry(), lambda obj: obj.add_task("Buy Milk")),
            "call": lambda obj, setup_fn: (setup_fn(obj), obj.get_all())[1],
            "check": lambda result: isinstance(result, list) and "[P] Buy Milk" in result,
            "marks": 2.0
        },
        {
            "desc": "Complete task and verify [D] prefix",
            "func": "complete_task",
            "setup": lambda: (student_module.TaskRegistry(), lambda obj: (obj.add_task("Buy Milk"), obj.complete_task("Buy Milk"))),
            "call": lambda obj, setup_fn: (setup_fn(obj), obj.get_all())[1],
            "check": lambda result: isinstance(result, list) and "[D] Buy Milk" in result and "[P] Buy Milk" not in result,
            "marks": 2.0
        },
        {
            "desc": "Get count of pending tasks",
            "func": "get_count",
            "setup": lambda: (student_module.TaskRegistry(), lambda obj: (obj.add_task("Task 1"), obj.add_task("Task 2"), obj.add_task("Task 3"))),
            "call": lambda obj, setup_fn: (setup_fn(obj), obj.get_count("P"))[1],
            "check": lambda result: isinstance(result, int) and result == 3,
            "marks": 2.0
        },
        {
            "desc": "Complete task returns True and get count of done tasks",
            "func": "complete_task & get_count",
            "setup": lambda: (student_module.TaskRegistry(), lambda obj: (obj.add_task("Task 1"), obj.add_task("Task 2"), obj.complete_task("Task 1"))),
            "call": lambda obj, setup_fn: (setup_fn(obj), obj.get_count("D"))[1],
            "check": lambda result: isinstance(result, int) and result == 1,
            "marks": 2.0
        },
        {
            "desc": "Delete task and verify removal",
            "func": "delete_task",
            "setup": lambda: (student_module.TaskRegistry(), lambda obj: (obj.add_task("Task 1"), obj.add_task("Task 2"), obj.delete_task("Task 1"))),
            "call": lambda obj, setup_fn: (setup_fn(obj), obj.get_all())[1],
            "check": lambda result: isinstance(result, list) and "[P] Task 1" not in result and "[P] Task 2" in result,
            "marks": 2.0
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2.0)
        max_score += marks
        
        try:
            # Create fresh instance for each test
            registry = case["setup"]()[0]
            setup_fn = case["setup"]()[1]
            
            # Execute setup and call
            result = case["call"](registry, setup_fn)
            
            # Check result
            passed = case["check"](result)
            
            if passed:
                msg = f"PASS TC{idx} [{case['desc']}]"
                total_score += marks
            else:
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: True (check condition satisfied)\n"
                msg += f"  Got: {repr(result)}"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
