import os
import sys
import json
import re
import socket
import subprocess
from datetime import datetime, timezone, timedelta

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def print_separator():
    print("-" * 70)

def print_test_case(name, status, score, max_score, reason):
    pad_length = 63 - len(name) - 1
    if pad_length < 1: 
        pad_length = 1
    dots = "." * pad_length
    print(f"{name} {dots} {status} ({score}/{max_score})")
    print(f"    +- [Reason]: {reason}")

def get_candidate_prefix():
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            user = arg
            if '@' in user:
                user = user.split('@')[0]
            return user
    user = os.getenv('NIIT_USERNAME', 'student')
    if '@' in user:
        user = user.split('@')[0]
    return user

def get_safe_prefixes(raw_prefix):
    p_lower = raw_prefix.lower()
    p_safe = re.sub(r'[^a-zA-Z0-9_]', '_', p_lower)
    return list(dict.fromkeys([p_lower, p_safe, 'student']))

def get_pg_connection():
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="postgres",
            user="postgres",
            password="PostgresPassword123!",
            connect_timeout=3
        )
        return conn
    except Exception:
        return None

def get_mysql_connection(database="mysql"):
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            database=database,
            user="root",
            password="MySQLPassword123!",
            connection_timeout=3
        )
        return conn
    except Exception:
        return None

def write_solution_json(score, max_score, results):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ws_path = os.path.normpath(os.path.join(current_dir, '..', 'student_workspace'))
        root_ws_path = os.path.normpath(os.path.join(current_dir, '..'))
        os.makedirs(ws_path, exist_ok=True)
        sol_data = {
            "score": score,
            "total_marks": max_score,
            "results": results,
            "timestamp": "2026-11-01T00:00:00Z"
        }
        for p in [ws_path, root_ws_path]:
            for fname in ['solution.json', 'solution.py']:
                with open(os.path.join(p, fname), 'w', encoding='utf-8') as f:
                    json.dump(sol_data, f, indent=4)
    except Exception:
        pass


def verify_task():
    max_score = 10
    tc1_max, tc2_max, tc3_max = 4, 3, 3
    tc1_score, tc2_score, tc3_score = 0, 0, 0
    tc1_status, tc2_status, tc3_status = "[FAILED]", "[FAILED]", "[FAILED]"
    tc1_reason, tc2_reason, tc3_reason = "test_pg_dsn.py missing in student_workspace", "Prerequisite failed", "Prerequisite failed"

    tc1_name = "TC1: test_pg_dsn.py Creation & TCP Socket Verification"
    tc2_name = "TC2: PostgreSQL Live Driver Handshake on Port 5432"
    tc3_name = "TC3: Query Execution (current_database & version) Output"

    current_dir = os.path.dirname(os.path.abspath(__file__))
    ws_dir = os.path.normpath(os.path.join(current_dir, '..', 'student_workspace'))
    root_ws_dir = os.path.normpath(os.path.join(current_dir, '..'))

    script_path = os.path.join(ws_dir, 'test_pg_dsn.py')
    if not os.path.isfile(script_path) and os.path.isfile(os.path.join(root_ws_dir, 'test_pg_dsn.py')):
        script_path = os.path.join(root_ws_dir, 'test_pg_dsn.py')
        ws_dir = root_ws_dir

    if os.path.isfile(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            code_text = f.read().lower()

        # Check socket logic in script
        has_socket = ('socket' in code_text and '5432' in code_text) or ('connect' in code_text and '5432' in code_text)
        if has_socket:
            tc1_score = 4
            tc1_status = "[PASSED]"
            tc1_reason = "Script test_pg_dsn.py exists and includes port 5432 connectivity check."
        else:
            tc1_reason = "Script test_pg_dsn.py exists but does not test socket connectivity on 5432."

        # TC2 & TC3: Execute the script
        try:
            res = subprocess.run([sys.executable, script_path], cwd=ws_dir, capture_output=True, text=True, timeout=10)
            output = (res.stdout + " " + res.stderr).lower()
            if res.returncode == 0:
                tc2_score = 3
                tc2_status = "[PASSED]"
                tc2_reason = "Script executed cleanly with zero return code."

                if 'postgres' in output and ('version' in output or 'postgresql' in output or '14' in output or '15' in output or '16' in output):
                    tc3_score = 3
                    tc3_status = "[PASSED]"
                    tc3_reason = "Script output confirmed live query execution (database: postgres, PostgreSQL version)."
                else:
                    tc3_reason = f"Script ran but did not output expected database/version info. Output: {res.stdout[:100]}."
            else:
                tc2_reason = f"Script execution returned non-zero exit code ({res.returncode}): {res.stderr[:100]}"
        except Exception as e:
            tc2_reason = f"Failed to execute test_pg_dsn.py: {e}"
    else:
        tc1_reason = "Script test_pg_dsn.py does not exist in student_workspace/."

    total_score = tc1_score + tc2_score + tc3_score
    results = {"tc1": tc1_score == tc1_max, "tc2": tc2_score == tc2_max, "tc3": tc3_score == tc3_max}
    write_solution_json(total_score, max_score, results)

    if '--json' in sys.argv:
        print(json.dumps(results))
    else:
        print_separator()
        print("                NIIT REAL-TIME DATABASE PLATFORM AUDIT")
        print_separator()
        print_test_case(tc1_name, tc1_status, tc1_score, tc1_max, tc1_reason)
        print_test_case(tc2_name, tc2_status, tc2_score, tc2_max, tc2_reason)
        print_test_case(tc3_name, tc3_status, tc3_score, tc3_max, tc3_reason)
        print_separator()
        score_str = f"{total_score}/{max_score}"
        print(f"TOTAL SCORE:{score_str:>57}")
        print_separator()

    sys.exit(0 if total_score == max_score else 1)

def verify_task_central(username, start_time_str, exam_code="UNKNOWN", **kwargs):
    return verify_task()

if __name__ == "__main__":
    verify_task()
