import os
import sys
import json
import ast

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

    total_score = 0
    max_score = 20
    
    syntax_ok = False
    dag_loaded = False
    bash_operators_used = False
    has_echo = False
    has_date = False
    
    tc1_reason = "No Python DAG files found in workspace."
    tc2_reason = "DAG file failed syntax check."
    tc3_reason = "DAG file failed parsing check."
    tc4_reason = "Echo command verification failed."
    tc5_reason = "Date command verification failed."

    base_path = get_base_path()
    dag_file = None
    
    for root, dirs, files in os.walk(base_path):
        for f in files:
            if f.endswith('.py') and f != 'run.py':
                dag_file = os.path.join(root, f)
                break
        if dag_file:
            break

    # ==========================================
    # TC1: DAG File Syntax & Parsing (4 points)
    # ==========================================
    tc1_name = "TC1: Airflow DAG Python Syntax Check"
    tc1_status = "[FAILED]"
    tc1_score = 0

    if dag_file:
        try:
            with open(dag_file, 'r', encoding='utf-8') as fh:
                code_content = fh.read()
            compile(code_content, dag_file, 'exec')
            syntax_ok = True
            tc1_status = "[PASSED]"
            tc1_score = 4
            tc1_reason = f"Valid Python file found and compiled successfully: {os.path.basename(dag_file)}"
        except Exception as e:
            tc1_reason = f"Syntax error in Python script: {e}"
    else:
        tc1_reason = "No Python files (other than run.py) found in student_workspace."

    # ==========================================
    # TC2: DAG Import and DagBag Loading (4 points)
    # ==========================================
    tc2_name = "TC2: DAG Import and DagBag Loading"
    tc2_status = "[FAILED]"
    tc2_score = 0

    dag_obj = None
    if syntax_ok:
        try:
            from airflow.models import DagBag
            os.environ['AIRFLOW__DATABASE__SQL_ALCHEMY_CONN'] = 'sqlite:////tmp/airflow.db'
            dagbag = DagBag(dag_folder=os.path.dirname(dag_file), include_examples=False)
            
            if dagbag.import_errors:
                err_msg = list(dagbag.import_errors.values())[0].replace('\n', ' ')
                tc2_reason = f"Airflow import errors: {err_msg}"
            elif len(dagbag.dags) > 0:
                dag_loaded = True
                dag_obj = list(dagbag.dags.values())[0]
                tc2_status = "[PASSED]"
                tc2_score = 4
                tc2_reason = f"DAG successfully loaded by Airflow DagBag. DAG ID: {dag_obj.dag_id}"
            else:
                # Fallback to static parser check
                tree = ast.parse(code_content)
                has_dag = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == 'DAG':
                            has_dag = True
                        elif isinstance(node.func, ast.Attribute) and node.func.attr == 'DAG':
                            has_dag = True
                if has_dag:
                    dag_loaded = True
                    tc2_status = "[PASSED]"
                    tc2_score = 4
                    tc2_reason = "DAG verified via AST structure check."
                else:
                    tc2_reason = "No DAG definition found in Python code."
        except Exception as e:
            # Fallback if apache-airflow package is missing entirely
            try:
                tree = ast.parse(code_content)
                has_dag = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == 'DAG':
                            has_dag = True
                        elif isinstance(node.func, ast.Attribute) and node.func.attr == 'DAG':
                            has_dag = True
                if has_dag:
                    dag_loaded = True
                    tc2_status = "[PASSED]"
                    tc2_score = 4
                    tc2_reason = "DAG verified via fallback AST structure (Airflow not installed locally)."
                else:
                    tc2_reason = "Failed to load DAG and no DAG definition detected in AST."
            except Exception as ast_err:
                tc2_reason = f"Failed to parse DAG script: {ast_err}"

    # ==========================================
    # TC3: BashOperator Tasks Class Check (4 points)
    # ==========================================
    tc3_name = "TC3: BashOperator Tasks Class Check"
    tc3_status = "[FAILED]"
    tc3_score = 0

    if dag_loaded:
        if dag_obj:
            try:
                from airflow.operators.bash import BashOperator
                bash_tasks = [t for t in dag_obj.tasks if isinstance(t, BashOperator)]
                if len(bash_tasks) >= 2:
                    bash_operators_used = True
                    tc3_status = "[PASSED]"
                    tc3_score = 4
                    tc3_reason = f"Verified {len(bash_tasks)} task(s) of class 'BashOperator' in loaded DAG."
                else:
                    tc3_reason = f"Found {len(bash_tasks)} BashOperator task(s), but expected at least 2."
            except Exception as e:
                # Fallback to AST verification
                tree = ast.parse(code_content)
                bash_operator_calls = 0
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == 'BashOperator':
                            bash_operator_calls += 1
                if bash_operator_calls >= 2:
                    bash_operators_used = True
                    tc3_status = "[PASSED]"
                    tc3_score = 4
                    tc3_reason = f"Verified {bash_operator_calls} BashOperator instantiation(s) in AST."
                else:
                    tc3_reason = f"AST inspection found {bash_operator_calls} BashOperator instantiations, expected 2."
        else:
            # Fallback to AST
            tree = ast.parse(code_content)
            bash_operator_calls = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'BashOperator':
                        bash_operator_calls += 1
            if bash_operator_calls >= 2:
                bash_operators_used = True
                tc3_status = "[PASSED]"
                tc3_score = 4
                tc3_reason = f"Verified {bash_operator_calls} BashOperator instantiation(s) via fallback AST check."
            else:
                tc3_reason = f"AST search found {bash_operator_calls} BashOperator instantiations, expected 2."

    # Analyze commands using AST for TC4 and TC5
    if bash_operators_used:
        try:
            tree = ast.parse(code_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'BashOperator':
                        for kw in node.keywords:
                            if kw.arg == 'bash_command':
                                if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                                    cmd = kw.value.value.strip()
                                    if 'echo' in cmd and 'welcome to airflow' in cmd.lower():
                                        has_echo = True
                                    if cmd == 'date' or 'date' in cmd.split():
                                        has_date = True
        except Exception:
            pass

    # ==========================================
    # TC4: Task 1 Command Verification (4 points)
    # ==========================================
    tc4_name = "TC4: Task 1 Command Verification"
    tc4_status = "[FAILED]"
    tc4_score = 0
    if bash_operators_used:
        if has_echo:
            tc4_status = "[PASSED]"
            tc4_score = 4
            tc4_reason = "Verified presence of 'echo \"Welcome to Airflow\"' in BashOperator task."
        else:
            tc4_reason = "Missing echo command in BashOperator tasks."

    # ==========================================
    # TC5: Task 2 Command Verification (4 points)
    # ==========================================
    tc5_name = "TC5: Task 2 Command Verification"
    tc5_status = "[FAILED]"
    tc5_score = 0
    if bash_operators_used:
        if has_date:
            tc5_status = "[PASSED]"
            tc5_score = 4
            tc5_reason = "Verified presence of 'date' command in BashOperator task."
        else:
            tc5_reason = "Missing date command in BashOperator tasks."

    # Construct results
    results = {
        "tc1": tc1_score == 4,
        "tc2": tc2_score == 4,
        "tc3": tc3_score == 4,
        "tc4": tc4_score == 4,
        "tc5": tc5_score == 4
    }

    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        with open(sol_path, 'w') as f:
            json.dump({'results': results}, f)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
    else:
        print_separator()
        print("                NIIT REAL-TIME AIRFLOW AUDIT")
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

if __name__ == "__main__":
    verify_task()
