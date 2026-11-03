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
    tc1_reason, tc2_reason, tc3_reason = "MySQL database missing", "replica_telemetry table missing", "Telemetry rows missing"

    tc1_name = "TC1: MySQL Monitoring Database (<prefix>_rep_monitor) Creation"
    tc2_name = "TC2: Replication Log Table (replica_telemetry) Schema Definition"
    tc3_name = "TC3: Telemetry Heartbeat Data & Status Population"

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)
    conn = get_mysql_connection("mysql")

    found_db = None
    if conn:
        try:
            cur = conn.cursor()
            for p in prefixes:
                db_name = f"{p}_rep_monitor"
                cur.execute("SELECT schema_name FROM information_schema.schemata WHERE lower(schema_name)=lower(%s)", (db_name,))
                r = cur.fetchone()
                if r:
                    found_db = r[0]
                    break
            if not found_db:
                cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE '%_rep_monitor%' OR schema_name='rep_monitor'")
                r = cur.fetchone()
                if r:
                    found_db = r[0]

            if found_db:
                tc1_score = 4
                tc1_status = "[PASSED]"
                tc1_reason = f"Monitoring database '{found_db}' verified in MySQL."

                # Check table replica_telemetry
                cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{found_db}' AND lower(table_name)='replica_telemetry'")
                tbl_row = cur.fetchone()
                if not tbl_row:
                    cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{found_db}'")
                    tbl_row = cur.fetchone()

                if tbl_row:
                    tbl_name = tbl_row[0]
                    tc2_score = 3
                    tc2_status = "[PASSED]"
                    tc2_reason = f"Table '{tbl_name}' created in database '{found_db}'."

                    # TC3: Check rows
                    cur.execute(f"SELECT COUNT(*) FROM `{found_db}`.`{tbl_name}`")
                    cnt = cur.fetchone()[0]
                    if cnt >= 1:
                        tc3_score = 3
                        tc3_status = "[PASSED]"
                        tc3_reason = f"Verified {cnt} replication telemetry log entries."
                    else:
                        tc3_reason = f"Table '{tbl_name}' is empty. Telemetry records required."
                else:
                    tc2_reason = f"Table 'replica_telemetry' not found in database '{found_db}'."
            else:
                tc1_reason = "Database '<prefix>_rep_monitor' not found in MySQL."
            conn.close()
        except Exception as e:
            tc1_reason = f"MySQL query error: {e}"
    else:
        tc1_reason = "MySQL service offline on localhost:3306."

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
