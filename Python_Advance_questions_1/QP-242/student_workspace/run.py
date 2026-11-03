import os
import sys
import json
from datetime import datetime
from unittest.mock import MagicMock

# Ensure we don't write bytecode
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Path injection
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Mock the requests library before importing the solution
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    def json(self):
        return self.json_data

mock_requests = MagicMock()
sys.modules['requests'] = mock_requests

try:
    from solution import APIHandler, APIError
except ImportError as e:
    print(f"Error: Could not import classes from solution.py. {e}")
    sys.exit(1)

def run_tests():
    print("-" * 85)
    print("TESTING SOLUTION: solution.py")
    print("-" * 85)
    
    results = []
    total_marks = 0
    handler = APIHandler("http://api.test")
    
    # TC1: Initialization
    try:
        results.append(("TC1", "Initialization", "Passed", 0))
    except Exception as e:
        results.append(("TC1", "Initialization", f"Failed ({e})", 0))

    # TC2: Successful GET (5 Marks)
    try:
        mock_requests.get.return_value = MockResponse({"id": 1, "name": "Test"}, 200)
        data = handler.fetch_data("/users/1")
        if data["id"] == 1:
            results.append(("TC2", "GET Logic (200)", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "GET Logic (200)", "Failed", 0))
    except Exception as e:
        results.append(("TC2", "GET Logic (200)", f"Failed ({e})", 0))

    # TC3: Handling 404 error (5 Marks)
    try:
        mock_requests.get.return_value = MockResponse({}, 404)
        try:
             handler.fetch_data("/users/99")
             results.append(("TC3", "GET Handling (404)", "Failed (No APIError raised)", 0))
        except APIError as e:
             if hasattr(e, 'status_code') and e.status_code == 404:
                 results.append(("TC3", "GET Handling (404)", "Passed", 5))
                 total_marks += 5
             else:
                  results.append(("TC3", "GET Handling (404)", f"Failed (Wrong status: {getattr(e, 'status_code', 'None')})", 0))
    except Exception as e:
        results.append(("TC3", "GET Handling (404)", f"Failed ({e})", 0))

    # TC4: Successful POST (5 Marks)
    try:
        mock_requests.post.return_value = MockResponse({}, 201)
        msg = handler.submit_data("/users", {"name": "Test"})
        if msg == "Created":
            results.append(("TC4", "POST Logic (201)", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "POST Logic (201)", "Failed", 0))
    except Exception as e:
        results.append(("TC4", "POST Logic (201)", f"Failed ({e})", 0))

    # TC5: Handling 400 error (5 Marks)
    try:
        mock_requests.post.return_value = MockResponse({}, 400)
        msg = handler.submit_data("/users", {})
        if msg == "Bad Request":
            results.append(("TC5", "POST Handling (400)", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC5", "POST Handling (400)", "Failed", 0))
    except Exception as e:
        results.append(("TC5", "POST Handling (400)", f"Failed ({e})", 0))

    # TC6: Field Extraction (5 Marks)
    try:
        mock_requests.get.return_value = MockResponse({"id": 1, "email": "test@hcl.com"}, 200)
        email = handler.get_user_email(1)
        if email == "test@hcl.com":
            results.append(("TC6", "JSON Field Extraction", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC6", "JSON Field Extraction", "Failed", 0))
    except Exception as e:
        results.append(("TC6", "JSON Field Extraction", f"Failed ({e})", 0))

    # TC7: Chained logic for Not Found (5 Marks)
    try:
        mock_requests.get.return_value = MockResponse({}, 404)
        msg = handler.get_user_email(99)
        if msg == "User Not Found":
            results.append(("TC7", "User Not Found logic", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC7", "User Not Found logic", "Failed", 0))
    except Exception as e:
        results.append(("TC7", "User Not Found logic", f"Failed ({e})", 0))

    # Display Results
    print(f"{'TC ID':<10} | {'Description':<25} | {'Status':<30} | {'Marks':<10}")
    print("-" * 85)
    for tcid, desc, status, marks in results:
        print(f"{tcid:<10} | {desc:<25} | {status:<30} | {marks:<10}")
    print("-" * 85)
    print(f"TOTAL SCORE: {total_marks} / 30")
    print("-" * 85)

    # Generate Report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.abspath(os.path.join(current_dir, "..", "reports"))
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"report_{timestamp}.txt"
    report_path = os.path.join(report_dir, report_filename)
    
    with open(report_path, "w") as f:
        f.write(f"API Request Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
