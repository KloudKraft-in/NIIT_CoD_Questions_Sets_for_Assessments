# driver.py (secret_tests)
import numpy as np
import os
import importlib.util

def load_solution_module():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    solution_path = os.path.abspath(os.path.join(current_dir, '..', 'student_workspace', 'solution.py'))

    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solution)
    return solution

def write_report(lines):
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))
    os.makedirs(reports_dir, exist_ok=True)

    existing_reports = [f for f in os.listdir(reports_dir) if f.startswith("report_")]
    report_number = len(existing_reports) + 1
    report_path = os.path.join(reports_dir, f"report_{report_number}.txt")

    # 🛠️ Use UTF-8 encoding to support emojis and special characters
    with open(report_path, 'w', encoding='utf-8') as report_file:
        for line in lines:
            print(line)
            report_file.write(line + "\n")


def test_student_code():
    sol = load_solution_module()
    results = []
    score = 0

    # Initialize results log
    results = []
    results.append("🧪 Running Tests for: Simplevotingsystem\n")

    # Test Case 1: create_vote_array
    try:
        result = sol.create_vote_array([1, 2, 3])
        if isinstance(result, np.ndarray) and np.array_equal(result, np.array([1, 2, 3])):
            results.append("✅ Visible Test Case 1 Passed: create_vote_array() - Converts list to numpy array")
            score += 2.5
        else:
            results.append("❌ Visible Test Case 1 Failed: create_vote_array() - Incorrect array conversion")
    except Exception as e:
        results.append(f"❌ Visible Test Case 1 Error: create_vote_array() - Exception: {e}")

    # Test Case 2: count_votes_per_candidate
    try:
        arr = np.array([1, 2, 2, 3])
        result = sol.count_votes_per_candidate(arr)
        if isinstance(result, np.ndarray) and np.array_equal(result, np.array([1, 2, 1])):
            results.append("✅ Visible Test Case 2 Passed: count_votes_per_candidate() - Correct vote counts")
            score += 2.5
        else:
            results.append("❌ Visible Test Case 2 Failed: count_votes_per_candidate() - Incorrect vote counts")
    except Exception as e:
        results.append(f"❌ Visible Test Case 2 Error: count_votes_per_candidate() - Exception: {e}")

    # Test Case 3: determine_winner
    try:
        arr = np.array([1, 2, 2, 3])
        result = sol.determine_winner(arr)
        if result == 2:
            results.append("✅ Visible Test Case 3 Passed: determine_winner() - Correct winner returned")
            score += 2.5
        else:
            results.append(f"❌ Visible Test Case 3 Failed: determine_winner() - Expected 2 but got {result}")
    except Exception as e:
        results.append(f"❌ Visible Test Case 3 Error: determine_winner() - Exception: {e}")

    # Test Case 4: validate_vote_array
    try:
        arr = np.array([1, 3, 5])
        result = sol.validate_vote_array(arr)
        if result is True:
            results.append("✅ Visible Test Case 4 Passed: validate_vote_array() - All votes valid")
            score += 2.5
        else:
            results.append("❌ Visible Test Case 4 Failed: validate_vote_array() - Expected True but got False")
    except Exception as e:
        results.append(f"❌ Visible Test Case 4 Error: validate_vote_array() - Exception: {e}")


    # Hidden Test Case 1: winner with tie
    try:
        arr = np.array([1, 2, 1, 2])
        result = sol.determine_winner(arr)
        if result in (1, 2):
            results.append("✅ Hidden Test Case 1 Passed: determine_winner() - Tie-break handled")
            score += 2.5
        else:
            results.append(f"❌ Hidden Test Case 1 Failed: determine_winner() - Unexpected winner: {result}")
    except Exception as e:
        results.append(f"❌ Hidden Test Case 1 Error: determine_winner() - Exception: {e}")

    # Hidden Test Case 2: validation fails
    try:
        arr = np.array([0, 6, 2])
        result = sol.validate_vote_array(arr)
        if result is False:
            results.append("✅ Hidden Test Case 2 Passed: validate_vote_array() - Out of range votes detected")
            score += 2.5
        else:
            results.append("❌ Hidden Test Case 2 Failed: validate_vote_array() - Expected False for invalid values")
    except Exception as e:
        results.append(f"❌ Hidden Test Case 2 Error: validate_vote_array() - Exception: {e}")

    results.append(f"\n🎯 TOTAL SCORE: {int(score)}/15")
    write_report(results)
