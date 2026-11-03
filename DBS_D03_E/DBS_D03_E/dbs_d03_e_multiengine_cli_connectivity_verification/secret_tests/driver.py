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
    user = None
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            user = arg
            break
    if not user:
        user = os.getenv('NIIT_USERNAME') or os.getenv('USER') or os.getenv('USERNAME') or 'student'
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
    tc1_reason, tc2_reason, tc3_reason = "PostgreSQL table missing", "MySQL database missing", "Prerequisite failed"

    tc1_name = "TC1: PostgreSQL psql Connection & <prefix>_cli_audit Table Creation"
    tc2_name = "TC2: MySQL CLI Connection & <prefix>_cli_audit_db Database Creation"
    tc3_name = "TC3: Sign-Off Record Insertion & Verification across Engines"

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)

    # 1. Check Postgres table
    pg_conn = get_pg_connection()
    found_pg_table = None
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            for p in prefixes:
                tbl = f"{p}_cli_audit"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                row = cur.fetchone()
                if row:
                    found_pg_table = row[0]
                    break
            
            if not found_pg_table:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_cli_audit' OR table_name='cli_audit')")
                row = cur.fetchone()
                if row:
                    found_pg_table = row[0]
            
            if found_pg_table:
                tc1_score = 4
                tc1_status = "[PASSED]"
                tc1_reason = f"Audit table '{found_pg_table}' verified in PostgreSQL."
            else:
                tc1_reason = "Table '<prefix>_cli_audit' not found in PostgreSQL."
        except Exception as e:
            tc1_reason = f"PostgreSQL error: {e}"
    else:
        tc1_reason = "PostgreSQL service unavailable on localhost:5432."

    # 2. Check MySQL database
    my_conn = get_mysql_connection("mysql")
    found_my_db = None
    if my_conn:
        try:
            cur = my_conn.cursor()
            for p in prefixes:
                db_name = f"{p}_cli_audit_db"
                cur.execute("SELECT schema_name FROM information_schema.schemata WHERE lower(schema_name)=lower(%s)", (db_name,))
                row = cur.fetchone()
                if row:
                    found_my_db = row[0]
                    break
            
            if not found_my_db:
                cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE '%_cli_audit_db%' OR schema_name LIKE '%_cli_audit%'")
                row = cur.fetchone()
                if row:
                    found_my_db = row[0]
            
            if found_my_db:
                tc2_score = 3
                tc2_status = "[PASSED]"
                tc2_reason = f"Database '{found_my_db}' verified in MySQL."
            else:
                tc2_reason = "Database '<prefix>_cli_audit_db' not found in MySQL."
        except Exception as e:
            tc2_reason = f"MySQL error: {e}"
    else:
        tc2_reason = "MySQL service unavailable on localhost:3306."

    # 3. Check records across engines (PostgreSQL table & MySQL table)
    pg_rows = []
    if found_pg_table and pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute(f"SELECT * FROM \"{found_pg_table}\"")
            pg_rows = cur.fetchall()
        except Exception:
            pass

    my_rows = []
    if found_my_db and my_conn:
        try:
            cur = my_conn.cursor()
            cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{found_my_db}'")
            tables = [r[0] for r in cur.fetchall()]
            for tbl in tables:
                cur.execute(f"SELECT * FROM `{found_my_db}`.`{tbl}`")
                my_rows.extend(cur.fetchall())
        except Exception:
            pass

    if len(pg_rows) >= 1 or len(my_rows) >= 1:
        tc3_score = 3
        tc3_status = "[PASSED]"
        tc3_reason = f"Verified {len(pg_rows)} sign-off records in PostgreSQL and {len(my_rows)} in MySQL."
    else:
        tc3_reason = "No sign-off records found in PostgreSQL table or MySQL database."

    if pg_conn: pg_conn.close()
    if my_conn: my_conn.close()

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
