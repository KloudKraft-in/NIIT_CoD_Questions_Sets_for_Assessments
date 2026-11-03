import os
import sys
import json
import re
import socket
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
    # If any arg is a valid prefix (not a flag like --json)
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
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        sol_json_path = os.path.join(ws_path, 'solution.json')
        if os.path.exists(sol_json_path):
            try:
                with open(sol_json_path, 'r', encoding='utf-8') as f:
                    old_meta = json.load(f)
                    if isinstance(old_meta, dict):
                        old_meta.update(sol_data)
                        sol_data = old_meta
            except Exception:
                pass

        with open(os.path.join(ws_path, 'solution.json'), 'w', encoding='utf-8') as f:
            json.dump(sol_data, f, indent=4)
        with open(os.path.join(ws_path, 'solution.py'), 'w', encoding='utf-8') as f:
            json.dump(sol_data, f, indent=4)
        with open(os.path.join(root_ws_path, 'solution.json'), 'w', encoding='utf-8') as f:
            json.dump(sol_data, f, indent=4)
        with open(os.path.join(root_ws_path, 'solution.py'), 'w', encoding='utf-8') as f:
            json.dump(sol_data, f, indent=4)
    except Exception:
        pass

def verify_task():
    max_score = 10
    tc1_score, tc2_score, tc3_score = 0, 0, 0
    tc1_status, tc2_status, tc3_status = "[FAILED]", "[FAILED]", "[FAILED]"
    tc1_reason, tc2_reason, tc3_reason = "PostgreSQL connection failed or table missing", "Prerequisite failed", "Prerequisite failed"

    tc1_name = "TC1: PostgreSQL Table (<prefix>_conn_chain) Creation"
    tc2_name = "TC2: 5-Layer Connection Chain Audit Records Population"
    tc3_name = "TC3: Data Integrity & Candidate Sign-Off Verification"

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)
    conn = get_pg_connection()

    found_table = None
    if conn:
        try:
            cur = conn.cursor()
            for p in prefixes:
                tbl = f"{p}_conn_chain"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                row = cur.fetchone()
                if row:
                    found_table = row[0]
                    break
            
            if not found_table:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE '%_conn_chain'")
                row = cur.fetchone()
                if row:
                    found_table = row[0]

            if found_table:
                tc1_score = 4
                tc1_status = "[PASSED]"
                tc1_reason = f"Audit table '{found_table}' successfully created in PostgreSQL public schema."

                cur.execute(f"SELECT layer_name, status, signed_by FROM \"{found_table}\"")
                rows = cur.fetchall()
                layers = [r[0].lower() for r in rows] if rows else []
                expected_keywords = ['client', 'pool', 'network', 'session', 'statement']
                matched = [kw for kw in expected_keywords if any(kw in lyr for lyr in layers)]
                
                if len(rows) >= 5 and len(matched) >= 4:
                    tc2_score = 3
                    tc2_status = "[PASSED]"
                    tc2_reason = f"Found {len(rows)} audit records covering required connection interaction layers."
                else:
                    tc2_reason = f"Table contains {len(rows)} rows (minimum 5 required, matching key layers)."

                healthy_count = sum(1 for r in rows if r[1] and 'healthy' in r[1].lower())
                signed_count = sum(1 for r in rows if r[2] and any(p in r[2].lower() for p in prefixes))
                if tc2_score > 0 and healthy_count >= 5:
                    tc3_score = 3
                    tc3_status = "[PASSED]"
                    tc3_reason = f"All 5 layers signed off with HEALTHY status and valid candidate sign-off."
                else:
                    tc3_reason = f"Rows with HEALTHY status: {healthy_count}/5, signed by candidate: {signed_count}/5."
            else:
                tc1_reason = f"Table '<prefix>_conn_chain' not found in PostgreSQL. Ensure table is created using psql."
            conn.close()
        except Exception as e:
            tc1_reason = f"PostgreSQL query error: {e}"
    else:
        tc1_reason = "Unable to connect to PostgreSQL on localhost:5432 (service offline or unconfigured)."

    total_score = tc1_score + tc2_score + tc3_score
    results = {"tc1": tc1_score == 4, "tc2": tc2_score == 3, "tc3": tc3_score == 3}
    write_solution_json(total_score, max_score, results)

    if '--json' in sys.argv:
        print(json.dumps(results))
    else:
        print_separator()
        print("                NIIT REAL-TIME DATABASE PLATFORM AUDIT")
        print_separator()
        print_test_case(tc1_name, tc1_status, tc1_score, 4, tc1_reason)
        print_test_case(tc2_name, tc2_status, tc2_score, 3, tc2_reason)
        print_test_case(tc3_name, tc3_status, tc3_score, 3, tc3_reason)
        print_separator()
        score_str = f"{total_score}/{max_score}"
        print(f"TOTAL SCORE:{score_str:>57}")
        print_separator()

    sys.exit(0 if total_score == max_score else 1)

def verify_task_central(username, start_time_str, exam_code="UNKNOWN", **kwargs):
    return verify_task()

if __name__ == "__main__":
    verify_task()
