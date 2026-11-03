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
    tc1_reason, tc2_reason, tc3_reason = "Backup directory missing", "pg_dump file missing or empty", "Audit table missing"

    tc1_name = "TC1: Backup Directory & Target Path Configuration"
    tc2_name = "TC2: pg_dump Schema Backup File Generation on Disk"
    tc3_name = "TC3: Database Backup Audit Table & Sign-Off Record"

    raw_prefix = get_candidate_prefix()
    prefixes = get_safe_prefixes(raw_prefix)

    # Search potential backup directory locations
    potential_dirs = []
    for p in prefixes:
        potential_dirs.append(f"/var/backups/db/{p}_backup")
        potential_dirs.append(os.path.expanduser(f"~/backups/{p}_backup"))
        potential_dirs.append(os.path.expanduser(f"~/{p}_backup"))
    potential_dirs.extend([
        "/var/backups/db",
        os.path.expanduser("~/backups"),
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'backups')),
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    ])
    # Add any subdirectories in /var/backups/db or ~/backups
    for parent in ["/var/backups/db", os.path.expanduser("~/backups"), os.path.expanduser("~")]:
        if os.path.isdir(parent):
            try:
                for entry in os.listdir(parent):
                    full = os.path.join(parent, entry)
                    if os.path.isdir(full) and 'backup' in entry.lower():
                        potential_dirs.append(full)
            except Exception:
                pass

    found_dir = None
    backup_file = None
    for d in potential_dirs:
        if os.path.isdir(d):
            found_dir = d
            cand = os.path.join(d, 'postgres_schema.sql')
            if os.path.isfile(cand) and os.path.getsize(cand) > 100:
                backup_file = cand
                break

    if found_dir:
        tc1_score = 4
        tc1_status = "[PASSED]"
        tc1_reason = f"Backup directory verified at: {found_dir}"
    else:
        tc1_reason = "Backup directory not found. Expected under /var/backups/db/<prefix>_backup/ or ~/backups/."

    if backup_file and os.path.getsize(backup_file) > 100:
        tc2_score = 3
        tc2_status = "[PASSED]"
        tc2_reason = f"Schema backup file verified ({os.path.getsize(backup_file)} bytes) at {backup_file}."
    else:
        # Check if any .sql file is present
        if found_dir:
            sql_files = [f for f in os.listdir(found_dir) if f.endswith('.sql')]
            if sql_files and os.path.getsize(os.path.join(found_dir, sql_files[0])) > 100:
                tc2_score = 3
                tc2_status = "[PASSED]"
                tc2_reason = f"Backup file '{sql_files[0]}' verified ({os.path.getsize(os.path.join(found_dir, sql_files[0]))} bytes)."
            else:
                tc2_reason = "No valid postgres_schema.sql dump file (>100 bytes) found in backup directory."
        else:
            tc2_reason = "Backup directory not found; cannot verify dump file."

    # TC3: PostgreSQL backup audit table
    conn = get_pg_connection()
    if conn:
        try:
            cur = conn.cursor()
            found_table = None
            for p in prefixes:
                tbl = f"{p}_backup_audit"
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND lower(table_name)=lower(%s)", (tbl,))
                row = cur.fetchone()
                if row:
                    found_table = row[0]
                    break
            if not found_table:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%_backup_audit' OR table_name='backup_audit')")
                row = cur.fetchone()
                if row:
                    found_table = row[0]

            if found_table:
                cur.execute(f"SELECT COUNT(*) FROM \"{found_table}\"")
                cnt = cur.fetchone()[0]
                if cnt >= 1:
                    tc3_score = 3
                    tc3_status = "[PASSED]"
                    tc3_reason = f"Audit table '{found_table}' contains {cnt} logged backup run records."
                else:
                    tc3_reason = f"Audit table '{found_table}' is empty. Must contain sign-off record."
            else:
                tc3_reason = "Table '<prefix>_backup_audit' not found in PostgreSQL."
            conn.close()
        except Exception as e:
            tc3_reason = f"Audit table query error: {e}"
    else:
        tc3_reason = "PostgreSQL service offline on localhost:5432."

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
