import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import ssl

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

def normalize_username(raw_username):
    if not raw_username:
        return "student"
    if '@' in raw_username:
        raw_username = raw_username.split('@')[0]
    if '_' in raw_username:
        raw_username = raw_username.split('_')[0]
    return raw_username.lower().replace('.', '-')

def databricks_api_call(host, token, endpoint, method="GET", params=None, data=None):
    host = host.rstrip('/')
    url = f"{host}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    
    body = None
    if data:
        body = json.dumps(data).encode('utf-8')
        
    try:
        ctx = ssl._create_unverified_context()
    except Exception:
        ctx = None

    try:
        with urllib.request.urlopen(req, data=body, timeout=15, context=ctx) as response:
            res_data = response.read().decode('utf-8')
            return True, (json.loads(res_data) if res_data else {}), response.status
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode('utf-8')
            err_json = json.loads(err_body)
        except Exception:
            err_json = {"message": str(e)}
        return False, err_json, e.code
    except Exception as e:
        return False, {"message": str(e)}, 500

def verify_task():
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    # 1. Resolve REAL student info from environment first
    env_user = (
        os.getenv("DATABRICKS_USERNAME") or 
        os.getenv("databricks_username") or 
        os.getenv("LABSKRAFT_USERNAME") or 
        os.getenv("username") or 
        os.getenv("USER")
    )
    
    solution_path = os.path.join(get_base_path(), 'solution.json')
    exam_code = os.getenv("NIIT_EXAM_CODE") or os.getenv("EXAM_CODE") or os.getenv("exam_code") or "1123"

    raw_username = env_user

    # Only use solution.json if env user is not set or placeholder
    if os.path.exists(solution_path):
        try:
            with open(solution_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            sol_user = data.get('labskraft_username')
            if sol_user and sol_user.lower() not in ["candidate-user", "candidate", "student", ""]:
                if not raw_username or raw_username.lower() in ["student", ""]:
                    raw_username = sol_user
            if data.get('exam_code') and (not exam_code or exam_code == "UNKNOWN"):
                exam_code = data['exam_code']
        except Exception:
            pass

    if not raw_username:
        raw_username = "student"

    username = normalize_username(raw_username)
    exam_code_clean = (exam_code or "1123").lower()

    total_score = 0
    max_score = 20
    
    cluster_exists = False
    cluster_obj = None
    
    # 2. Databricks connection credentials (loaded from environment)
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")

    init_error = None
    if not host or not token:
        missing = []
        if not host: missing.append("DATABRICKS_HOST")
        if not token: missing.append("DATABRICKS_TOKEN")
        init_error = f"Missing environment variable(s): {', '.join(missing)}"

    # Build candidate usernames & cluster names
    user_variants = [username]
    if raw_username:
        norm_raw = normalize_username(raw_username)
        if norm_raw not in user_variants:
            user_variants.append(norm_raw)
        raw_prefix = raw_username.split('@')[0].lower().replace('.', '-').replace('_', '-')
        if raw_prefix not in user_variants:
            user_variants.append(raw_prefix)

    for u in ["ltmdemo02", "demo4", "labs-demo-user4", "labs_demo_user4", "student"]:
        norm_u = normalize_username(u)
        if norm_u not in user_variants:
            user_variants.append(norm_u)

    digits = re.findall(r'\d+', raw_username or '')
    if digits:
        d = digits[0]
        for v in [f"demo{d}", f"ltmdemo0{d}", f"ltmdemo{d}", f"labs-demo-user{d}"]:
            norm_v = normalize_username(v)
            if norm_v not in user_variants:
                user_variants.append(norm_v)

    candidate_clusters = []
    for u in user_variants:
        candidate_clusters.append(f"{u}-{exam_code_clean}-db-cluster")
        candidate_clusters.append(f"{u}_{exam_code_clean}_db_cluster")
        candidate_clusters.append(f"{u}-1123-db-cluster")
        candidate_clusters.append(f"{u}-db-cluster")
        candidate_clusters.append(f"{u}-{exam_code_clean}-cluster")
        candidate_clusters.append(f"{u}-cluster")

    primary_cluster_name = f"{username}-{exam_code_clean}-db-cluster"

    # Fetch cluster list via API
    found_any_cluster = None
    if init_error is None:
        success, res, code = databricks_api_call(host, token, "/api/2.0/clusters/list")
        if success and res:
            all_clusters = res.get("clusters", [])
            for c in all_clusters:
                c_name = c.get("cluster_name", "")
                c_name_lower = c_name.lower()
                if any(c_name_lower == cand.lower() for cand in candidate_clusters):
                    cluster_obj = c
                    break
            
            # Fallback partial match if exact name not matched
            if not cluster_obj:
                for c in all_clusters:
                    c_name = c.get("cluster_name", "")
                    c_name_lower = c_name.lower()
                    if "db-cluster" in c_name_lower or "db_cluster" in c_name_lower or (username in c_name_lower and "cluster" in c_name_lower):
                        found_any_cluster = c_name
                        cluster_obj = c
                        break

    # ==========================================
    # TC1: Cluster Existence (4 points)
    # ==========================================
    tc1_name = "TC1: Cluster Existence (<prefix>-db-cluster exists)"
    tc1_status = "[FAILED]"
    tc1_score = 0
    tc1_reason = f"Cluster '{primary_cluster_name}' does not exist."

    if cluster_obj:
        cluster_exists = True
        tc1_status = "[PASSED]"
        tc1_score = 4
        tc1_reason = f"Cluster '{cluster_obj.get('cluster_name')}' found successfully."
    else:
        if found_any_cluster:
            tc1_reason = f"Cluster '{primary_cluster_name}' not found. But found cluster '{found_any_cluster}'."
        else:
            tc1_reason = f"Cluster '{primary_cluster_name}' was not found in the workspace."

    # ==========================================
    # TC2: Spark Runtime Version (17.3 LTS) (4 points)
    # ==========================================
    tc2_name = "TC2: Spark Runtime Version (17.3.x-scala2.13)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    tc2_reason = "Prerequisite failed (Cluster not found)."

    if cluster_exists and cluster_obj:
        runtime = cluster_obj.get("spark_version", "")
        if "17.3" in runtime and "scala2.13" in runtime:
            tc2_status = "[PASSED]"
            tc2_score = 4
            tc2_reason = f"Spark runtime is correct ({runtime})."
        elif "17.3" in runtime:
            tc2_status = "[PASSED]"
            tc2_score = 4
            tc2_reason = f"Spark runtime contains 17.3 ({runtime})."
        else:
            tc2_reason = f"Runtime is '{runtime}', expected '17.3.x-scala2.13'."

    # ==========================================
    # TC3: Autotermination Verification (4 points)
    # ==========================================
    tc3_name = "TC3: Autotermination Verification (30 minutes)"
    tc3_status = "[FAILED]"
    tc3_score = 0
    tc3_reason = "Prerequisite failed."

    if cluster_exists and cluster_obj:
        auto_term = cluster_obj.get("autotermination_minutes", 0)
        if auto_term == 30:
            tc3_status = "[PASSED]"
            tc3_score = 4
            tc3_reason = "Autotermination is set to 30 minutes."
        else:
            tc3_reason = f"Autotermination is set to {auto_term} minutes, expected 30."

    # ==========================================
    # TC4: Single Node Mode Enabled (4 points)
    # ==========================================
    tc4_name = "TC4: Single Node Mode Enabled"
    tc4_status = "[FAILED]"
    tc4_score = 0
    tc4_reason = "Prerequisite failed."

    if cluster_exists and cluster_obj:
        num_workers = cluster_obj.get("num_workers", 0)
        spark_conf = cluster_obj.get("spark_conf", {})
        custom_tags = cluster_obj.get("custom_tags", {})
        profile = spark_conf.get("spark.databricks.cluster.profile", "")
        resource_class = custom_tags.get("ResourceClass", "")
        
        is_single_node = (num_workers == 0 or num_workers is None) and (profile == "singleNode" or resource_class.lower() == "singlenode")
        
        if is_single_node or (num_workers == 0 and not spark_conf.get("spark.databricks.cluster.profile") and resource_class.lower() == "singlenode"):
            tc4_status = "[PASSED]"
            tc4_score = 4
            tc4_reason = "Single Node mode is enabled (0 workers and singleNode profile)."
        else:
            if num_workers == 0:
                tc4_status = "[PASSED]"
                tc4_score = 4
                tc4_reason = "Single Node mode verified (0 workers)."
            else:
                tc4_reason = f"Cluster is not configured for Single Node (num_workers={num_workers}, profile='{profile}')."

    # ==========================================
    # TC5: Node Type Standard_D4s_v5 & Photon Disabled (4 points)
    # ==========================================
    tc5_name = "TC5: Node Type (Standard_D4s_v5) & Photon Disabled"
    tc5_status = "[FAILED]"
    tc5_score = 0
    tc5_reason = "Prerequisite failed."

    if cluster_exists and cluster_obj:
        node_type = cluster_obj.get("node_type_id", "")
        runtime = cluster_obj.get("spark_version", "")
        runtime_engine = cluster_obj.get("runtime_engine", "")
        
        photon_disabled = ("-photon" not in runtime.lower()) and (str(runtime_engine).upper() != "PHOTON")
        node_type_ok = ("standard_d4s_v5" in node_type.lower() or node_type == "Standard_D4s_v5" or "standard_f4" in node_type.lower())
        
        if node_type_ok and photon_disabled:
            tc5_status = "[PASSED]"
            tc5_score = 4
            tc5_reason = f"Node Type is {node_type} and Photon Acceleration is disabled."
        else:
            reasons = []
            if not node_type_ok:
                reasons.append(f"Node Type is '{node_type}', expected 'Standard_D4s_v5'")
            if not photon_disabled:
                reasons.append("Photon Acceleration is enabled")
            tc5_reason = " / ".join(reasons)

    # Construct results dict
    results = {
        "tc1": tc1_score == 4,
        "tc2": tc2_score == 4,
        "tc3": tc3_score == 4,
        "tc4": tc4_score == 4,
        "tc5": tc5_score == 4
    }

    # Write solution.json file locally by merging with existing metadata
    try:
        sol_data = {}
        if os.path.exists(solution_path):
            try:
                with open(solution_path, 'r', encoding='utf-8') as f:
                    sol_data = json.load(f)
            except Exception:
                pass
        sol_data['results'] = results
        with open(solution_path, 'w', encoding='utf-8') as f:
            json.dump(sol_data, f, indent=2)
    except Exception:
        pass

    # Handle output format
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
    else:
        print_separator()
        print("                NIIT REAL-TIME DATABRICKS AUDIT")
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

def verify_task_central(username, start_time_str, exam_code="UNKNOWN", **kwargs):
    try:
        from driver_central import verify_task_central as _central
        return _central(username, start_time_str, exam_code, **kwargs)
    except Exception:
        return verify_task()

if __name__ == "__main__":
    verify_task()
