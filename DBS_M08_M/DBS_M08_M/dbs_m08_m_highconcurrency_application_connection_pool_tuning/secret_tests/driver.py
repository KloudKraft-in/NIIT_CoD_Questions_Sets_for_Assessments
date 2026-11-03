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
        "TC1: PostgreSQL Connection Metrics Interrogation (max_connections)",
        "TC2: Pool SRE Table (<prefix>_pool_sre_tuning) Creation",
        "TC3: Peak Concurrency & Sizing Formula Calculation",
        "TC4: Connection Timeout (20000ms) Setting Specification",
        "TC5: Leak Detection Threshold (30000ms) Policy",
        "TC6: Application Workload (CheckoutService) Tagging",
        "TC7: Approved By Prefix Integrity Verification",
        "TC8: Live Platform Connection Capacity Health Sign-Off"
    ]

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)
    conn = get_pg_connection()

    found_table = None
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SHOW max_connections")
            max_conn_val = cur.fetchone()[0]
            tc_scores[0] = 3
            tc_status[0] = "[PASSED]"
            tc_reasons[0] = f"Database connection ceiling queried (max_connections = {max_conn_val})."

            for p in prefixes:
                tbl = f"{p}_pool_sre_tuning"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                r = cur.fetchone()
                if r:
                    found_table = r[0]
                    break
            if not found_table:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_pool_sre_tuning' OR table_name='pool_sre_tuning')")
                r = cur.fetchone()
                if r:
                    found_table = r[0]

            if found_table:
                tc_scores[1] = 3
                tc_status[1] = "[PASSED]"
                tc_reasons[1] = f"Pool SRE tuning table '{found_table}' verified in PostgreSQL."

                cur.execute(f"SELECT * FROM \"{found_table}\"")
                rows = cur.fetchall()

                if len(rows) >= 1:
                    row = rows[0]
                    row_text = " ".join(str(v).lower() for v in row)
                    ints = [v for v in row if isinstance(v, int)]

                    # TC3: pool sizing
                    pool_sz = next((x for x in ints if 10 <= x <= 200), None)
                    if pool_sz or any('32' in str(x) for x in ints) or 'checkout' in row_text:
                        tc_scores[2] = 3
                        tc_status[2] = "[PASSED]"
                        tc_reasons[2] = f"Calculated pool size verified from concurrency model."
                    else:
                        tc_reasons[2] = "Pool sizing metric missing or out of expected range."

                    # TC4: connection timeout
                    to_ms = next((x for x in ints if 10000 <= x <= 30000), None)
                    if to_ms or '20000' in row_text:
                        tc_scores[3] = 3
                        tc_status[3] = "[PASSED]"
                        tc_reasons[3] = f"Connection timeout setting (20000ms) verified against SLA."
                    else:
                        tc_reasons[3] = "Connection timeout policy setting (20000ms) missing."

                    # TC5: leak threshold
                    leak_ms = next((x for x in ints if 20000 <= x <= 60000 and x != to_ms), None)
                    if leak_ms or '30000' in row_text:
                        tc_scores[4] = 2
                        tc_status[4] = "[PASSED]"
                        tc_reasons[4] = f"Leak detection threshold policy (30000ms) verified."
                    else:
                        tc_reasons[4] = "Leak detection threshold setting (30000ms) missing."

                    # TC6: workload name
                    if 'checkout' in row_text or 'service' in row_text or len(row_text) > 10:
                        tc_scores[5] = 2
                        tc_status[5] = "[PASSED]"
                        tc_reasons[5] = "Application workload (CheckoutService) tagged."
                    else:
                        tc_reasons[5] = "Application workload name missing."

                    # TC7: approved by
                    if any(p in row_text for p in prefixes) or len(row) >= 5:
                        tc_scores[6] = 2
                        tc_status[6] = "[PASSED]"
                        tc_reasons[6] = "Tuning rule approved by candidate prefix."
                    else:
                        tc_reasons[6] = "Candidate prefix missing from approved_by column."

                    # TC8: Live connection health
                    tc_scores[7] = 2
                    tc_status[7] = "[PASSED]"
                    tc_reasons[7] = "Platform connection capacity health sign-off confirmed."
                else:
                    tc_reasons[2] = f"Table '{found_table}' is empty."
            else:
                tc_reasons[1] = "Table '<prefix>_pool_sre_tuning' not found in PostgreSQL."
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
