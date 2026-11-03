import pandas as pd
import os
import sys
import importlib.util


def _write_report(report_path, lines):
    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def test_student_code(solution_path):
    """Run visible test cases for Course Engagement Analytics."""
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    # Clear previous report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("")

    # Load student solution module
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        err = f"IMPORT/SYNTAX ERROR: {type(e).__name__}: {e}"
        print(err)
        _write_report(report_path, [err])
        return

    print("Running Tests for: Course Engagement Analytics\n")
    report_lines = ["Running Tests for: Course Engagement Analytics\n"]

    # locate dataset
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    csv_path = os.path.join(data_dir, 'course_activity.csv')

    # Read dataset
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError as e:
        msg = f"DATA ERROR: {e}"
        print(msg)
        _write_report(report_path, [msg])
        return

    test_cases = [
        {
            'id': 'TC1',
            'desc': 'Completion % calculation',
            'call': lambda: solution.completion_percentage(df),
            'check': lambda res: isinstance(res, dict) and res.get('S03-C102') == 100.0,
            'expected': "S03-C102: 100.0",
            'marks': 4
        },
        {
            'id': 'TC2',
            'desc': 'Most engaged course',
            'call': lambda: solution.most_engaged_course(df),
            'check': lambda res: res == 'C102',
            'expected': "Most Engaged Course: C102",
            'marks': 4
        },
        {
            'id': 'TC3',
            'desc': 'Detect inactive students',
            'call': lambda: solution.inactive_students(df),
            'check': lambda res: isinstance(res, list) and res == ['S02', 'S04'],
            'expected': "Inactive Students: S02, S04",
            'marks': 4
        },
        {
            'id': 'TC4',
            'desc': 'Duplicate record detection',
            'call': lambda: solution.duplicate_records(df),
            'check': lambda res: isinstance(res, int) and res == 1,
            'expected': "Duplicate Records Found: 1",
            'marks': 4
        },
        {
            'id': 'TC5',
            'desc': 'Student ranking',
            'call': lambda: solution.rank_students(df),
            'check': lambda res: isinstance(res, list) and res[:3] == ['S03', 'S06', 'S05'],
            'expected': "1: S03\n2: S06\n3: S05",
            'marks': 4
        }
    ]

    total = 0
    max_total = 0
    for idx, tc in enumerate(test_cases, 1):
        marks = tc['marks']
        max_total += marks
        try:
            out = tc['call']()
            passed = tc['check'](out)
            if passed:
                msg = f"PASS {tc['id']} [{tc['desc']}] ({marks}/{marks})"
                total += marks
            else:
                msg = f"FAIL {tc['id']} [{tc['desc']}]: Expected {tc['expected']}, Got: {repr(out)}"
            print(msg)
            report_lines.append(msg)
        except Exception as e:
            msg = f"ERROR {tc['id']} [{tc['desc']}]: {type(e).__name__}: {e}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total}/{max_total} (Visible)"
    print(score_line)
    report_lines.append(score_line)
    _write_report(report_path, report_lines)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
