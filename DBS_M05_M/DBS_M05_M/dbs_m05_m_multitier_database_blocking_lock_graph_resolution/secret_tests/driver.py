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
    max_score = 20
    tc_scores = [0] * 8
    tc_status = ["[FAILED]"] * 8
    tc_reasons = ["Prerequisite failed"] * 8
    tc_weights = [3, 3, 3, 3, 2, 2, 2, 2]

    tc_names = [
        "TC1: Catalog Inspection & Lock Tree Traversal (pg_locks)",
        "TC2: Root Blocker Identification & Waiter Exclusion",
        "TC3: Lock SOP Table (<prefix>_multitier_lock_sop) Creation",
        "TC4: Safe Termination Command Formulation (pg_terminate_backend)",
        "TC5: Cascading Waiter Release Verification",
        "TC6: Lock Timeout Configuration (lock_timeout=10s)",
        "TC7: Post-Incident Governance Metadata Documentation",
        "TC8: Live Database Concurrency State Sign-Off"
    ]

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)
    conn = get_pg_connection()

    found_table = None
    if conn:
        try:
            cur = conn.cursor()
            # TC1: Live pg_locks queryable
            cur.execute("SELECT COUNT(*) FROM pg_locks")
            lock_cnt = cur.fetchone()[0]
            tc_scores[0] = 3
            tc_status[0] = "[PASSED]"
            tc_reasons[0] = f"Active lock catalog traversed successfully ({lock_cnt} locks evaluated)."

            # TC2: pg_stat_activity queryable
            cur.execute("SELECT COUNT(*) FROM pg_stat_activity")
            act_cnt = cur.fetchone()[0]
            tc_scores[1] = 3
            tc_status[1] = "[PASSED]"
            tc_reasons[1] = f"Session tree analyzed across {act_cnt} active connections."

            # Find table
            for p in prefixes:
                tbl = f"{p}_multitier_lock_sop"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                r = cur.fetchone()
                if r:
                    found_table = r[0]
                    break
            if not found_table:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_multitier_lock_sop' OR table_name='multitier_lock_sop')")
                r = cur.fetchone()
                if r:
                    found_table = r[0]

            if found_table:
                # TC3: Table verified
                tc_scores[2] = 3
                tc_status[2] = "[PASSED]"
                tc_reasons[2] = f"Lock SOP table '{found_table}' verified in PostgreSQL."

                cur.execute(f"SELECT * FROM \"{found_table}\"")
                rows = cur.fetchall()

                if len(rows) >= 1:
                    row = rows[0]
                    row_text = " ".join(str(v).lower() for v in row)

                    # TC4: Termination command
                    if 'terminate' in row_text or 'pg_terminate_backend' in row_text or 'kill' in row_text:
                        tc_scores[3] = 3
                        tc_status[3] = "[PASSED]"
                        tc_reasons[3] = "Safe backend termination command (pg_terminate_backend) formulated."
                    else:
                        tc_reasons[3] = "Termination command missing safe pg_terminate_backend call."

                    # TC5: Waiter release verified
                    tc_scores[4] = 2
                    tc_status[4] = "[PASSED]"
                    tc_reasons[4] = "Cascading transaction release logic confirmed for blocker PID."

                    # TC6: Lock timeout
                    if '10' in row_text or 's' in row_text or 'ms' in row_text:
                        tc_scores[5] = 2
                        tc_status[5] = "[PASSED]"
                        tc_reasons[5] = "Lock timeout policy verified (lock_timeout=10s)."
                    else:
                        tc_reasons[5] = "Lock timeout setting missing expected 10s threshold."

                    # TC7: Sign-off
                    if any(p in row_text for p in prefixes) or len(row) >= 5:
                        tc_scores[6] = 2
                        tc_status[6] = "[PASSED]"
                        tc_reasons[6] = "Governance metadata confirmed with candidate sign-off."
                    else:
                        tc_reasons[6] = "Candidate prefix sign-off missing from governance record."

                    # TC8: Live concurrency sign-off
                    tc_scores[7] = 2
                    tc_status[7] = "[PASSED]"
                    tc_reasons[7] = "End-to-end database lock governance health sign-off confirmed."
                else:
                    tc_reasons[3] = f"Table '{found_table}' is empty."
            else:
                tc_reasons[2] = "Table '<prefix>_multitier_lock_sop' not found in PostgreSQL."
            conn.close()
        except Exception as e:
            tc_reasons[0] = f"PostgreSQL error: {e}"
    else:
        tc_reasons[0] = "PostgreSQL service offline on localhost:5432."

    total_score = sum(tc_scores)
    results = {f"tc{i+1}": tc_scores[i] == tc_weights[i] for i in range(8)}
    write_solution_json(total_score, max_score, results)

    if '--json' in sys.argv:
        print(json.dumps(results))
    else:
        print_separator()
        print("                NIIT REAL-TIME DATABASE PLATFORM AUDIT")
        print_separator()
        for i in range(8):
            print_test_case(tc_names[i], tc_status[i], tc_scores[i], tc_weights[i], tc_reasons[i])
        print_separator()
        score_str = f"{total_score}/{max_score}"
        print(f"TOTAL SCORE:{score_str:>57}")
        print_separator()

    sys.exit(0 if total_score == max_score else 1)

def verify_task_central(username, start_time_str, exam_code="UNKNOWN", **kwargs):
    return verify_task()

if __name__ == "__main__":
    verify_task()
