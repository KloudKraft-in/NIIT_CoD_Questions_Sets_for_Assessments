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
    taskflow_decorators_used = False
    func1_prints_correct = False
    func2_prints_correct = False
    
    tc1_reason = "No Python DAG files found in workspace."
    tc2_reason = "DAG file failed syntax check."
    tc3_reason = "DAG file failed parsing check."
    tc4_reason = "Function 1 output verification failed."
    tc5_reason = "Function 2 output verification failed."

    base_path = get_base_path()
    dag_file = None
    
    # 1. Find the student's DAG file
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
            # Verify valid syntax
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

    if syntax_ok:
        try:
            # Attempt to use Airflow DagBag to parse
            from airflow.models import DagBag
            os.environ['AIRFLOW__DATABASE__SQL_ALCHEMY_CONN'] = 'sqlite:////tmp/airflow.db'
            dagbag = DagBag(dag_folder=os.path.dirname(dag_file), include_examples=False)
            
            if dagbag.import_errors:
                err_msg = list(dagbag.import_errors.values())[0].replace('\n', ' ')
                tc2_reason = f"Airflow import errors: {err_msg}"
            elif len(dagbag.dags) > 0:
                dag_loaded = True
                tc2_status = "[PASSED]"
                tc2_score = 4
                tc2_reason = f"DAG successfully loaded by Airflow DagBag. DAG ID: {list(dagbag.dags.keys())[0]}"
            else:
                # Fallback AST parsing
                tree = ast.parse(code_content)
                has_dag = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == 'DAG':
                            has_dag = True
                        elif isinstance(node.func, ast.Attribute) and node.func.attr == 'DAG':
                            has_dag = True
                    elif isinstance(node, ast.Decorator):
                        if isinstance(node.decorator, ast.Name) and node.decorator.id == 'dag':
                            has_dag = True
                        elif isinstance(node.decorator, ast.Call) and isinstance(node.decorator.func, ast.Name) and node.decorator.func.id == 'dag':
                            has_dag = True
                
                if has_dag:
                    dag_loaded = True
                    tc2_status = "[PASSED]"
                    tc2_score = 4
                    tc2_reason = "DAG verified via AST structure check (Static Import Mode)."
                else:
                    tc2_reason = "No DAG object or @dag decorator found in Python code."
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
                    elif isinstance(node, ast.FunctionDef):
                        for dec in node.decorator_list:
                            if isinstance(dec, ast.Name) and dec.id == 'dag':
                                has_dag = True
                            elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name) and dec.func.id == 'dag':
                                has_dag = True
                if has_dag:
                    dag_loaded = True
                    tc2_status = "[PASSED]"
                    tc2_score = 4
                    tc2_reason = "DAG verified via fallback AST syntax analysis (Airflow not installed locally)."
                else:
                    tc2_reason = "Failed to load DAG and no DAG definition/decorator detected in AST."
            except Exception as ast_err:
                tc2_reason = f"Failed to parse DAG script: {ast_err}"

    # ==========================================
    # TC3: TaskFlow Decorator API Verification (4 points)
    # ==========================================
    tc3_name = "TC3: TaskFlow Decorator API Verification"
    tc3_status = "[FAILED]"
    tc3_score = 0

    if dag_loaded:
        try:
            tree = ast.parse(code_content)
            has_dag_decorator = False
            has_task_decorator = False
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for dec in node.decorator_list:
                        if isinstance(dec, ast.Name) and dec.id == 'dag':
                            has_dag_decorator = True
                        elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name) and dec.func.id == 'dag':
                            has_dag_decorator = True
                        elif isinstance(dec, ast.Name) and dec.id == 'task':
                            has_task_decorator = True
                        elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name) and dec.func.id == 'task':
                            has_task_decorator = True
                            
            if has_dag_decorator or has_task_decorator:
                taskflow_decorators_used = True
                tc3_status = "[PASSED]"
                tc3_score = 4
                tc3_reason = "Verified use of `@dag` or `@task` TaskFlow decorator syntax."
            else:
                tc3_reason = "DAG is not defined using TaskFlow decorators (e.g. @dag, @task)."
        except Exception as e:
            tc3_reason = f"Error performing AST check for decorators: {e}"

    # Analyze function prints using AST for TC4 and TC5
    if dag_loaded:
        try:
            tree = ast.parse(code_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name) and subnode.func.id == 'print':
                            for arg in subnode.args:
                                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                                    val = arg.value
                                    if "welcome orchestrator" in val.lower():
                                        func1_prints_correct = True
                                    if "login time" in val.lower():
                                        func2_prints_correct = True
                                elif isinstance(arg, ast.JoinedStr):
                                    f_str_text = ""
                                    for value in arg.values:
                                        if isinstance(value, ast.Constant):
                                            f_str_text += str(value.value)
                                    if "login time" in f_str_text.lower():
                                        func2_prints_correct = True
                                    if "welcome orchestrator" in f_str_text.lower():
                                        func1_prints_correct = True
        except Exception:
            pass

    # ==========================================
    # TC4: Task 1 Content Verification (4 points)
    # ==========================================
    tc4_name = "TC4: Task 1 Content Verification (Welcome orchestrator)"
    tc4_status = "[FAILED]"
    tc4_score = 0
    if dag_loaded:
        if func1_prints_correct:
            tc4_status = "[PASSED]"
            tc4_score = 4
            tc4_reason = "Task function correctly prints 'Welcome orchestrator'."
        else:
            tc4_reason = "Could not find a task function printing 'Welcome orchestrator'."

    # ==========================================
    # TC5: Task 2 Content Verification (4 points)
    # ==========================================
    tc5_name = "TC5: Task 2 Content Verification (Login time)"
    tc5_status = "[FAILED]"
    tc5_score = 0
    if dag_loaded:
        if func2_prints_correct:
            tc5_status = "[PASSED]"
            tc5_score = 4
            tc5_reason = "Task function correctly prints 'Login time'."
        else:
            tc5_reason = "Could not find a task function printing 'Login time'."

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
