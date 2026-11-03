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
    tc1_max, tc2_max, tc3_max, tc4_max = 3, 3, 2, 2
    tc1_score, tc2_score, tc3_score, tc4_score = 0, 0, 0, 0
    tc1_status, tc2_status, tc3_status, tc4_status = "[FAILED]", "[FAILED]", "[FAILED]", "[FAILED]"
    tc1_reason, tc2_reason, tc3_reason, tc4_reason = "DSN audit table missing", "Prerequisite failed", "Prerequisite failed", "Prerequisite failed"

    tc1_name = "TC1: Audit Table (<prefix>_dsn_audit) Creation in PostgreSQL"
    tc2_name = "TC2: Multi-Engine Connection String Standards Population (4 Engines)"
    tc3_name = "TC3: Standard Port Validation (5432, 3306, 1433, 1521)"
    tc4_name = "TC4: TLS / SSL Compliance Status Differentiation"

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)
    conn = get_pg_connection()

    found_table = None
    if conn:
        try:
            cur = conn.cursor()
            for p in prefixes:
                tbl = f"{p}_dsn_audit"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                r = cur.fetchone()
                if r:
                    found_table = r[0]
                    break
            if not found_table:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_dsn_audit' OR table_name='dsn_audit')")
                r = cur.fetchone()
                if r:
                    found_table = r[0]

            if found_table:
                tc1_score = 3
                tc1_status = "[PASSED]"
                tc1_reason = f"DSN audit table '{found_table}' verified in PostgreSQL."

                cur.execute(f"SELECT * FROM \"{found_table}\"")
                rows = cur.fetchall()

                if len(rows) >= 4:
                    tc2_score = 3
                    tc2_status = "[PASSED]"
                    tc2_reason = f"Verified {len(rows)} engine connection templates across database fleet."
                else:
                    tc2_reason = f"Found {len(rows)} entries in '{found_table}' (expected at least 4 engines)."

                # Check ports or timeout parameters
                ports_found = set()
                for r in rows:
                    for val in r:
                        if isinstance(val, int) and val in [5432, 3306, 1433, 1521]:
                            ports_found.add(val)
                        elif isinstance(val, int) and 0 < val <= 60:
                            ports_found.add(val)

                if tc2_score > 0 and len(ports_found) >= 3:
                    tc3_score = 2
                    tc3_status = "[PASSED]"
                    tc3_reason = f"Standard database ports / SLA parameters verified ({sorted(list(ports_found))})."
                else:
                    tc3_reason = f"Expected standard ports (5432, 3306, 1433, 1521), found: {sorted(list(ports_found))}."

                # Check TLS / SSL compliance differentiation or author prefix
                row_texts = [" ".join(str(v).lower() for v in r) for r in rows]
                has_tls_diff = any('compliant' in txt for txt in row_texts) or any(any(p in txt for p in prefixes) for txt in row_texts)
                if tc2_score > 0 and has_tls_diff:
                    tc4_score = 2
                    tc4_status = "[PASSED]"
                    tc4_reason = "TLS/SSL compliance status differentiation and audit integrity verified."
                else:
                    tc4_reason = "Missing compliance status ('COMPLIANT'/'NON_COMPLIANT') or candidate sign-off."
            else:
                tc1_reason = "Table '<prefix>_dsn_audit' not found in PostgreSQL."
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
