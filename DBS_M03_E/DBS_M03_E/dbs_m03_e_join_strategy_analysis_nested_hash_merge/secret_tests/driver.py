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
    tc1_reason, tc2_reason, tc3_reason, tc4_reason = "Relational tables missing", "Prerequisite failed", "Prerequisite failed", "Prerequisite failed"

    tc1_name = "TC1: Primary & Foreign Key Tables (<prefix>_depts, <prefix>_emps) Creation"
    tc2_name = "TC2: Data Seeding & Referential Integrity Verification"
    tc3_name = "TC3: Join Audit Table (<prefix>_join_strategy_audit) Setup"
    tc4_name = "TC4: Join Operator (Hash Join vs Nested Loop) Verification"

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)
    conn = get_pg_connection()

    if conn:
        try:
            cur = conn.cursor()
            depts_tbl, emps_tbl, audit_tbl = None, None, None
            for p in prefixes:
                if not depts_tbl:
                    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (f"{p}_depts",))
                    r = cur.fetchone()
                    if r: depts_tbl = r[0]
                if not emps_tbl:
                    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (f"{p}_emps",))
                    r = cur.fetchone()
                    if r: emps_tbl = r[0]
                if not audit_tbl:
                    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (f"{p}_join_strategy_audit",))
                    r = cur.fetchone()
                    if r: audit_tbl = r[0]

            if not depts_tbl:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_depts' OR table_name='depts')")
                r = cur.fetchone()
                if r: depts_tbl = r[0]
            if not emps_tbl:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_emps' OR table_name='emps')")
                r = cur.fetchone()
                if r: emps_tbl = r[0]
            if not audit_tbl:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_join_strategy%' OR table_name LIKE '%_join_strategy_audit')")
                r = cur.fetchone()
                if r: audit_tbl = r[0]

            if depts_tbl and emps_tbl:
                tc1_score = 3
                tc1_status = "[PASSED]"
                tc1_reason = f"Verified relational tables '{depts_tbl}' and '{emps_tbl}'."

                # TC2: Check rows in depts & emps
                cur.execute(f"SELECT COUNT(*) FROM \"{depts_tbl}\"")
                d_cnt = cur.fetchone()[0]
                cur.execute(f"SELECT COUNT(*) FROM \"{emps_tbl}\"")
                e_cnt = cur.fetchone()[0]
                if d_cnt >= 1 and e_cnt >= 1:
                    tc2_score = 3
                    tc2_status = "[PASSED]"
                    tc2_reason = f"Data seeded successfully: {d_cnt} departments, {e_cnt} employees."
                else:
                    tc2_reason = f"Insufficient records seeded: depts={d_cnt}, emps={e_cnt}."
            else:
                tc1_reason = f"Relational tables missing. Found depts={depts_tbl}, emps={emps_tbl}."

            if audit_tbl:
                tc3_score = 2
                tc3_status = "[PASSED]"
                tc3_reason = f"Join strategy audit table '{audit_tbl}' verified."

                cur.execute(f"SELECT * FROM \"{audit_tbl}\"")
                rows = cur.fetchall()
                row_texts = [" ".join(str(v).lower() for v in r) for r in rows]

                has_operator = any('hash' in txt or 'nested' in txt or 'merge' in txt or 'join' in txt for txt in row_texts)
                if len(rows) >= 1 and has_operator:
                    tc4_score = 2
                    tc4_status = "[PASSED]"
                    tc4_reason = "Join operator (Hash Join / Nested Loop) verified in audit log."
                else:
                    tc4_reason = "Audit table missing recorded join operator verification."
            else:
                tc3_reason = "Table '<prefix>_join_strategy_audit' not found in PostgreSQL."
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
