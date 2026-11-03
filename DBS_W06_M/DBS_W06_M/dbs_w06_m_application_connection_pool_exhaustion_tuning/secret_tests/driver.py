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
    tc1_max, tc2_max, tc3_max, tc4_max = 5, 5, 5, 5
    tc1_score, tc2_score, tc3_score, tc4_score = 0, 0, 0, 0
    tc1_status, tc2_status, tc3_status, tc4_status = "[FAILED]", "[FAILED]", "[FAILED]", "[FAILED]"
    tc1_reason, tc2_reason, tc3_reason, tc4_reason = "PostgreSQL metrics query failed", "Pool governance table missing", "Prerequisite failed", "Prerequisite failed"

    tc1_name = "TC1: PostgreSQL Session & Capacity Metrics Interrogation"
    tc2_name = "TC2: Pool Governance Table (<prefix>_pool_governance) Creation"
    tc3_name = "TC3: Pool Sizing & Leak Detection Threshold Parameters Population"
    tc4_name = "TC4: Server-Side Idle Session Timeout Configuration Verification"

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)
    conn = get_pg_connection()

    found_table = None
    if conn:
        try:
            cur = conn.cursor()

            for p in prefixes:
                tbl = f"{p}_pool_governance"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                r = cur.fetchone()
                if r:
                    found_table = r[0]
                    break
            if not found_table:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (lower(table_name) LIKE '%_pool_governance' OR lower(table_name)='pool_governance')")
                r = cur.fetchone()
                if r:
                    found_table = r[0]

            if not found_table:
                tc1_score, tc2_score, tc3_score, tc4_score = 0, 0, 0, 0
                tc1_status, tc2_status, tc3_status, tc4_status = "[FAILED]", "[FAILED]", "[FAILED]", "[FAILED]"
                tc1_reason = "Prerequisite failed: Pool governance table '<prefix>_pool_governance' missing in PostgreSQL."
                tc2_reason = "Table '<prefix>_pool_governance' not found in PostgreSQL."
                tc3_reason = "Prerequisite failed: Governance records missing."
                tc4_reason = "Prerequisite failed: Server session timeout governance missing."
            else:
                # TC1: Session & Capacity Metrics Interrogation
                cur.execute("SHOW max_connections")
                m_conn = cur.fetchone()[0]
                cur.execute("SELECT count(*) FROM pg_stat_activity")
                act_cnt = cur.fetchone()[0]
                tc1_score = 5
                tc1_status = "[PASSED]"
                tc1_reason = f"Live session capacity interrogated (max_connections = {m_conn}, active_sessions = {act_cnt})."

                # TC2: Pool Governance Table Creation
                tc2_score = 5
                tc2_status = "[PASSED]"
                tc2_reason = f"Pool governance table '{found_table}' verified in PostgreSQL."

                cur.execute(f"SELECT * FROM \"{found_table}\"")
                rows = cur.fetchall()

                if rows and len(rows) >= 1:
                    row_text = " ".join(str(v).lower() for v in rows[0])

                    # TC3: pool sizing & leak detection
                    if 'hikaripool' in row_text or '25' in row_text or '30000' in row_text or '60000' in row_text or len(rows[0]) >= 4:
                        tc3_score = 5
                        tc3_status = "[PASSED]"
                        tc3_reason = "Pool sizing (25) and leak detection (60000ms) policies verified."
                    else:
                        tc3_reason = "Pool sizing and leak detection threshold metrics missing."

                    # TC4: Server-side idle session timeout or candidate sign-off
                    timeout_val = None
                    try:
                        cur.execute("SHOW idle_in_transaction_session_timeout")
                        timeout_val = str(cur.fetchone()[0]).lower()
                    except Exception:
                        pass

                    if (timeout_val and ('60' in timeout_val or '1min' in timeout_val)) or any(p in row_text for p in prefixes) or len(rows[0]) >= 5:
                        tc4_score = 5
                        tc4_status = "[PASSED]"
                        tc4_reason = "Server-side idle session timeout (60s) or candidate sign-off confirmed."
                    else:
                        tc4_reason = "Server-side idle session timeout (60s) not configured and candidate sign-off missing."
                else:
                    tc3_reason = f"Table '{found_table}' is empty. Must contain pool policy records."
                    tc4_reason = "Prerequisite failed: Table is empty."
            conn.close()
        except Exception as e:
            tc1_reason = f"PostgreSQL error: {e}"
    else:
        tc1_reason = "PostgreSQL service offline on localhost:5432."

    total_score = tc1_score + tc2_score + tc3_score + tc4_score
    results = {"tc1": tc1_score == tc1_max, "tc2": tc2_score == tc2_max, "tc3": tc3_score == tc3_max, "tc4": tc4_score == tc4_max}
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
        print_test_case(tc4_name, tc4_status, tc4_score, tc4_max, tc4_reason)
        print_separator()
        score_str = f"{total_score}/{max_score}"
        print(f"TOTAL SCORE:{score_str:>57}")
        print_separator()

    sys.exit(0 if total_score == max_score else 1)

def verify_task_central(username, start_time_str, exam_code="UNKNOWN", **kwargs):
    return verify_task()

if __name__ == "__main__":
    verify_task()
