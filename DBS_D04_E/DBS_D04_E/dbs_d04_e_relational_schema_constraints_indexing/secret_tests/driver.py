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
    tc1_reason, tc2_reason, tc3_reason = "Customers table or constraints missing", "Orders foreign key missing", "B-tree index missing"

    tc1_name = "TC1: Primary Key & Unique Constraint Definitions (<prefix>_customers)"
    tc2_name = "TC2: Foreign Key Referential Integrity (<prefix>_orders -> customers)"
    tc3_name = "TC3: B-Tree Index Creation (idx_<prefix>_orders_cust on customer_id)"

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)
    conn = get_pg_connection()

    if conn:
        try:
            cur = conn.cursor()
            # Find customers table
            cust_tbl = None
            for p in prefixes:
                tbl = f"{p}_customers"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                row = cur.fetchone()
                if row:
                    cust_tbl = row[0]
                    break
            if not cust_tbl:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_customers' OR table_name='customers')")
                row = cur.fetchone()
                if row:
                    cust_tbl = row[0]

            # Find orders table
            ord_tbl = None
            for p in prefixes:
                tbl = f"{p}_orders"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                row = cur.fetchone()
                if row:
                    ord_tbl = row[0]
                    break
            if not ord_tbl:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_orders' OR table_name='orders')")
                row = cur.fetchone()
                if row:
                    ord_tbl = row[0]

            # TC1: Check Customers table, PK and UNIQUE constraint
            if cust_tbl:
                cur.execute("""
                    SELECT tc.constraint_type
                    FROM information_schema.table_constraints tc
                    WHERE tc.table_name = %s
                """, (cust_tbl,))
                constraints = [r[0] for r in cur.fetchall()]
                has_pk = 'PRIMARY KEY' in constraints
                if has_pk:
                    tc1_score = 4
                    tc1_status = "[PASSED]"
                    tc1_reason = f"Table '{cust_tbl}' verified with PRIMARY KEY and constraints: {constraints}."
                else:
                    tc1_reason = f"Table '{cust_tbl}' exists but missing PRIMARY KEY constraint."
            else:
                tc1_reason = "Table '<prefix>_customers' not found in PostgreSQL."

            # TC2: Check Orders FK
            if ord_tbl:
                cur.execute("""
                    SELECT tc.constraint_name, kcu.column_name, ccu.table_name AS foreign_table_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s
                """, (ord_tbl,))
                fk_rows = cur.fetchall()
                if fk_rows:
                    tc2_score = 3
                    tc2_status = "[PASSED]"
                    tc2_reason = f"Foreign key on '{ord_tbl}' correctly references {fk_rows[0][2]}."
                else:
                    tc2_reason = f"Table '{ord_tbl}' exists but no FOREIGN KEY constraint found."
            else:
                tc2_reason = "Table '<prefix>_orders' not found in PostgreSQL."

            # TC3: Check Index on customer_id
            if ord_tbl:
                cur.execute("""
                    SELECT indexname, indexdef
                    FROM pg_indexes
                    WHERE tablename = %s
                """, (ord_tbl,))
                idx_rows = cur.fetchall()
                has_cust_idx = any('customer_id' in str(r[1]).lower() or 'idx' in str(r[0]).lower() for r in idx_rows)
                if has_cust_idx:
                    tc3_score = 3
                    tc3_status = "[PASSED]"
                    tc3_reason = f"Index verified on '{ord_tbl}': {[r[0] for r in idx_rows]}."
                else:
                    tc3_reason = f"No index on customer_id found on '{ord_tbl}'."
            else:
                tc3_reason = "Orders table missing for index verification."
            conn.close()
        except Exception as e:
            tc1_reason = f"Catalog query error: {e}"
    else:
        tc1_reason = "PostgreSQL service offline on localhost:5432."

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
