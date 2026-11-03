# secret_tests/driver.py

import os
import importlib.util
from pathlib import Path
import datetime

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"report_{timestamp}.txt")

    os.makedirs(report_dir, exist_ok=True)

    print("🧪 Running Tests for: Library Management System (OOPs)\n")
    report_lines = ["🧪 Running Tests for: Library Management System (OOPs)\n"]
    total_score = 0
    max_score = 20
    idx = 1

    try:
        spec = importlib.util.spec_from_file_location("student_solution", solution_path)
        student_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_module)
        Library = student_module.Library
    except Exception as e:
        msg = f"❌ Failed to load solution.py: {e}"
        print(msg)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join([msg]) + "\n")
        return

    print(f"=== Test Run at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    report_lines.append(f"=== Test Run at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    # TC1: Initialization
    try:
        lib = Library()
        if isinstance(lib.books, dict) and isinstance(lib.history, list):
            msg = f"✅ Visible Test Case {idx} Passed: Initialize empty library"
            total_score += 3
        else:
            msg = f"❌ Visible Test Case {idx} Failed: Incorrect data structures"
    except Exception as e:
        msg = f"❌ Visible Test Case {idx} Crashed: {str(e)}"
    print(msg); report_lines.append(msg)
    idx += 1

    # TC2: Add Book
    try:
        lib = Library()
        lib.add_book("Python 101", "Guido")
        if "Python 101" in lib.books and lib.books["Python 101"]["author"] == "Guido":
            msg = f"✅ Visible Test Case {idx} Passed: Add book correctly"
            total_score += 3
        else:
            msg = f"❌ Visible Test Case {idx} Failed: Book not added properly"
    except Exception as e:
        msg = f"❌ Visible Test Case {idx} Crashed: {str(e)}"
    print(msg); report_lines.append(msg)
    idx += 1

    # TC3: Borrow Book (setup book manually)
    try:
        lib = Library()
        lib.books = {"Python 101": {"author": "Guido", "available": True}}
        result = lib.borrow_book("Python 101", "Alice")
        if result.lower().startswith("borrowed"):
            msg = f"✅ Visible Test Case {idx} Passed: Borrow available book"
            total_score += 3
        else:
            msg = f"❌ Visible Test Case {idx} Failed: Incorrect return message"
    except Exception as e:
        msg = f"❌ Visible Test Case {idx} Crashed: {str(e)}"
    print(msg); report_lines.append(msg)
    idx += 1

    # TC4: Return Book (setup book manually as unavailable)
    try:
        lib = Library()
        lib.books = {"Python 101": {"author": "Guido", "available": False}}
        result = lib.return_book("Python 101", "Alice")
        if result.lower().startswith("returned") and lib.books["Python 101"]["available"]:
            msg = f"✅ Visible Test Case {idx} Passed: Return borrowed book"
            total_score += 3
        else:
            msg = f"❌ Visible Test Case {idx} Failed: Book not marked as available"
    except Exception as e:
        msg = f"❌ Visible Test Case {idx} Crashed: {str(e)}"
    print(msg); report_lines.append(msg)
    idx += 1

    # TC5: Search Book
    try:
        lib = Library()
        lib.books = {"Python 101": {"author": "Guido", "available": True}}
        found = lib.search_book("Python 101")
        missing = lib.search_book("Nonexistent Book")
        if found is True and missing is False:
            msg = f"✅ Visible Test Case {idx} Passed: Search existing & missing book"
            total_score += 4
        else:
            msg = f"❌ Visible Test Case {idx} Failed: Incorrect search result"
    except Exception as e:
        msg = f"❌ Visible Test Case {idx} Crashed: {str(e)}"
    print(msg); report_lines.append(msg)
    idx += 1

    # TC6: View History (setup manually)
    try:
        lib = Library()
        lib.history = [
            "Added: 'Python 101' by Guido",
            "Borrowed: 'Python 101' by Alice",
            "Returned: 'Python 101' by Alice"
        ]
        history = lib.view_history()
        if isinstance(history, list) and len(history) == 3:
            msg = f"✅ Visible Test Case {idx} Passed: View all transactions"
            total_score += 4
        else:
            msg = f"❌ Visible Test Case {idx} Failed: History not tracked correctly"
    except Exception as e:
        msg = f"❌ Visible Test Case {idx} Crashed: {str(e)}"
    print(msg); report_lines.append(msg)

    # Final Summary
    print("\n✔️ Tests complete.")
    report_lines.append("\n✔️ Tests complete.")
    score_line = f"\n🎯 TOTAL SCORE: {total_score}/{max_score}\n"
    print(score_line); report_lines.append(score_line)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
