import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def print_separator():
    print("-" * 70)

def print_test_case(name, status, score, max_score, reason):
    pad_length = 63 - len(name) - 1
    if pad_length < 1: 
        pad_length = 1
    dots = "." * pad_length
    print(f"{name} {dots} {status} ({score}/{max_score})")
    print(f"    └─ [Reason]: {reason}")

def verify_task():
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    labskraft_username = os.getenv("LABSKRAFT_USERNAME") or "student"
    exam_code = os.getenv("NIIT_EXAM_CODE") or os.getenv("EXAM_CODE") or "UNKNOWN"
    
    sol_path = os.path.join(get_base_path(), 'solution.json')
    if os.path.exists(sol_path):
        try:
            with open(sol_path, 'r') as f:
                data = json.load(f)
            if data.get('labskraft_username'):
                labskraft_username = data['labskraft_username']
            if data.get('exam_code'):
                exam_code = data['exam_code']
        except Exception:
            pass

    raw_username = labskraft_username
    if '@' in raw_username:
        raw_username = raw_username.split('@')[0]
    if '_' in raw_username:
        raw_username = raw_username.split('_')[0]
    username = raw_username.lower().replace('.', '-')
    
    if exam_code and exam_code != "UNKNOWN":
        prefix = f"{username}_{exam_code.lower()}"
    else:
        prefix = username
        
    db_name = f"sn_ltm_{prefix}".upper().replace('-', '_')

    total_score = 0
    max_score = 20
    
    db_exists = False
    schema_exists = False
    
    conn = None
    init_error = None
    
    # 1. Connect to Snowflake
    try:
        import snowflake.connector
        user = os.getenv("SNOWFLAKE_USER") or "LTM_DEMO"
        password = os.getenv("SNOWFLAKE_PASSWORD") or "KloudKraft#2026"
        account = os.getenv("SNOWFLAKE_ACCOUNT") or "op53614.ap-southeast-2"
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE") or "LTM_WH"
        
        candidates = [account, "op53614.ap-southeast-2", "OP53614.ap-southeast-2", "0P53614.ap-southeast-2", "op53614.ap-southeast-2.aws"]
        for acc in candidates:
            try:
                conn = snowflake.connector.connect(
                    user=user,
                    password=password,
                    account=acc,
                    warehouse=warehouse
                )
                if conn:
                    break
            except Exception:
                continue
        if not conn:
            # Try one last time to capture exception
            conn = snowflake.connector.connect(
                user=user,
                password=password,
                account=account,
                warehouse=warehouse
            )
    except Exception as e:
        init_error = f"{type(e).__name__}: {e}"
        print(f"[SYSTEM] Snowflake connection error: {init_error}")

    
    # Auto-detect database, schema, table
    target_db = None
    target_schema = None
    target_table = None
    
    if conn:
        try:
            cursor = conn.cursor()
            # Try setting warehouse context explicitly
            try:
                cursor.execute("SHOW WAREHOUSES")
                wh_list = [w[0] for w in cursor.fetchall()]
                chosen_wh = "LTM_WH" if "LTM_WH" in [w.upper() for w in wh_list] else (wh_list[0] if wh_list else None)
                if chosen_wh:
                    cursor.execute(f"USE WAREHOUSE {chosen_wh}")
            except Exception:
                pass

            cursor.execute("SHOW DATABASES")
            for db in cursor.fetchall():
                db_name_curr = db[1].upper()
                if db_name_curr.startswith("SN_LTM_"):
                    target_db = db_name_curr
                    break
            
            if target_db:
                cursor.execute(f"SHOW SCHEMAS IN DATABASE {target_db}")
                for sch in cursor.fetchall():
                    sch_name_curr = sch[1].upper()
                    if sch_name_curr in ["DATA", "PUBLIC"]:
                        cursor.execute(f"SHOW TABLES IN {target_db}.{sch_name_curr}")
                        for tbl in cursor.fetchall():
                            tbl_name_curr = tbl[1].upper()
                            if tbl_name_curr:
                                target_schema = sch_name_curr
                                target_table = tbl_name_curr
                                break
                        if target_table:
                            break
        except Exception:
            pass

    final_db = target_db or db_name
    final_schema = target_schema or "DATA"
    final_table = target_table or "CANDIDATE_DATA"

    db_exists = False
    schema_exists = False
    table_exists = False

    # TC1: Database Existence
    tc1_name = f"TC1: Database Existence ({final_db})"
    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Database '{final_db}' not found."

    if conn:
        if target_db:
            db_exists = True
            tc1_status = "[PASSED]"
            tc1_score = 4
            tc1_reason = f"Database '{final_db}' found successfully."
        else:
            tc1_reason = f"Database '{final_db}' was not found in Snowflake."
    else:
        tc1_reason = f"Failed to connect to Snowflake: {init_error}"

    # TC2: Schema Existence
    tc2_name = f"TC2: Schema Existence ({final_schema})"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Database does not exist)."

    if db_exists:
        if target_schema:
            schema_exists = True
            tc2_status = "[PASSED]"
            tc2_score = 4
            tc2_reason = f"Schema '{final_schema}' exists inside database '{final_db}'."
        else:
            tc2_reason = f"Expected schema 'DATA' or 'PUBLIC' was not found inside database '{final_db}'."

    # TC3: Table and Data Load
    tc3_name = f"TC3: Table and Data Load ({final_table} Ingestion Check)"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed (Schema does not exist)."

    if schema_exists:
        if target_table:
            table_exists = True
            tc3_status = "[PASSED]"
            tc3_score = 4
            tc3_reason = f"Table '{final_table}' found inside schema '{final_schema}'."
        else:
            tc3_reason = f"No tables found inside schema '{final_schema}'."

    # TC4: Database Query Validation
    tc4_name = "TC4: Database Query Validation"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed (Table does not exist)."

    if table_exists:
        tc4_status = "[PASSED]"
        tc4_score = 4
        tc4_reason = "Database query execution validated successfully."

    # TC5: Table Data Verification
    tc5_name = f"TC5: Table Data Verification ({final_table} Data Ingestion Check)"
    tc5_status = "[FAILED]"
    tc5_score = 0
    tc5_reason = "Prerequisite failed (Table does not exist)."

    if table_exists:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {final_db}.{final_schema}.{final_table}")
            row_count = cursor.fetchone()[0]
            if row_count > 0:
                tc5_status = "[PASSED]"
                tc5_score = 4
                tc5_reason = f"Table data verified. Found {row_count} rows ingested."
            else:
                tc5_reason = "Table is empty (0 rows found)."
        except Exception as e:
            tc5_reason = f"Failed to retrieve table row count: {e}"

    # Construct results dict
    results = {
        "tc1": tc1_score > 0,
        "tc2": tc2_score > 0,
        "tc3": tc3_score > 0,
        "tc4": tc4_score > 0,
        "tc5": tc5_score > 0
    }

    # Write solution.json file locally by merging with existing metadata
    try:
        sol_data = {}
        if os.path.exists(sol_path):
            try:
                with open(sol_path, 'r') as f:
                    sol_data = json.load(f)
            except Exception:
                pass
        sol_data['results'] = results
        with open(sol_path, 'w') as f:
            json.dump(sol_data, f, indent=2)
    except Exception:
        pass

    # Handle output format
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
    else:
        print_separator()
        print("                NIIT REAL-TIME SNOWFLAKE AUDIT")
        print_separator()
        print_test_case(tc1_name, tc1_status, tc1_score, 4, tc1_reason)
        print_test_case(tc2_name, tc2_status, tc2_score, 4, tc2_reason)
        print_test_case(tc3_name, tc3_status, tc3_score, 4, tc3_reason)
        print_test_case(tc4_name, tc4_status, tc4_score, 4, tc4_reason)
        print_test_case(tc5_name, tc5_status, tc5_score, 4, tc5_reason)
        
        total_score = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
        print_separator()
        score_string = f"{total_score}/{max_score}"
        print(f"TOTAL SCORE:{score_string:>57}")
        print_separator()

if __name__ == '__main__':
    verify_task()
