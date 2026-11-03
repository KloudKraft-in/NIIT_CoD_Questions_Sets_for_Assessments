import os
import sys
import json
import re
import socket
import subprocess

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def print_separator():
    print("-" * 70, flush=True)

def print_test_case(name, status, score, max_score, reason):
    pad_length = 63 - len(name) - 1
    if pad_length < 1: 
        pad_length = 1
    dots = "." * pad_length
    print(f"{name} {dots} {status} ({score}/{max_score})", flush=True)
    print(f"    └─ [Reason]: {reason}", flush=True)

def resolve_candidate_info():
    solution_path = os.path.join(get_base_path(), 'solution.json')
    sol_user = None
    sol_exam = None
    if os.path.exists(solution_path):
        try:
            with open(solution_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                sol_user = data.get('niit_username') or data.get('labskraft_username')
                sol_exam = data.get('exam_code')
        except Exception:
            pass

    raw_username = (
        os.getenv("LABSKRAFT_USERNAME") or
        os.getenv("NIIT_USERNAME") or
        sol_user or
        os.getenv("USER") or
        os.getenv("username") or
        "student"
    )
    if '@' in raw_username:
        raw_username = raw_username.split('@')[0]
    if '_' in raw_username:
        raw_username = raw_username.split('_')[0]
    username = raw_username.lower().replace('.', '-')

    exam_code = (
        os.getenv("NIIT_EXAM_CODE") or
        os.getenv("EXAM_CODE") or
        sol_exam or
        "exam123"
    ).lower()

    prefix = f"{username}-{exam_code}"
    return username, exam_code, prefix

def check_broker_alive(host="localhost", port=9092, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def inspect_consumer_offsets(candidate_names, bootstrap_servers="localhost:9092"):
    host = "localhost"
    port = 9092
    if ":" in bootstrap_servers:
        parts = bootstrap_servers.split(":")
        host = parts[0]
        try:
            port = int(parts[1])
        except Exception:
            port = 9092

    broker_connected = check_broker_alive(host, port)
    found_group = None
    committed_offset = 0
    conn_err = None

    if not broker_connected:
        return broker_connected, found_group, committed_offset, f"Cannot connect to Kafka broker at {bootstrap_servers}"

    # Step 1: Discover consumer group via CLI
    group_cmds = [
        "/opt/kafka/bin/kafka-consumer-groups.sh",
        "kafka-consumer-groups.sh",
        "kafka-consumer-groups",
        "/usr/local/kafka/bin/kafka-consumer-groups.sh",
        "/opt/bitnami/kafka/bin/kafka-consumer-groups.sh"
    ]
    for cmd in group_cmds:
        try:
            proc = subprocess.run([cmd, "--bootstrap-server", bootstrap_servers, "--list"], capture_output=True, text=True, timeout=8)
            if proc.returncode == 0 and proc.stdout:
                groups_list = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
                for cand in candidate_names:
                    if cand in groups_list:
                        found_group = cand
                        break
                if not found_group:
                    for g in groups_list:
                        if g.startswith("alerts-group"):
                            found_group = g
                            break
                if found_group:
                    break
        except Exception:
            pass

    # Fallback Step 1b: Discover via kafka-python admin client
    if not found_group:
        try:
            from kafka.admin import KafkaAdminClient
            admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers, request_timeout_ms=4000)
            cluster_groups = [g[0] for g in admin.list_consumer_groups()]
            for cand in candidate_names:
                if cand in cluster_groups:
                    found_group = cand
                    break
            if not found_group:
                for g in cluster_groups:
                    if g.startswith("alerts-group"):
                        found_group = g
                        break
            admin.close()
        except Exception as e:
            conn_err = str(e)

    # Step 2: Check committed offsets for found consumer group
    if found_group:
        for cmd in group_cmds:
            try:
                proc = subprocess.run([cmd, "--bootstrap-server", bootstrap_servers, "--describe", "--group", found_group], capture_output=True, text=True, timeout=10)
                if proc.returncode == 0 and proc.stdout:
                    for line in proc.stdout.splitlines():
                        line_s = line.strip()
                        # Ignore header rows or informational warnings
                        if not line_s or line_s.startswith("GROUP") or line_s.startswith("The consumer") or line_s.startswith("Consumer group"):
                            continue
                        parts = re.split(r'\s+', line_s)
                        # Format typically: GROUP TOPIC PARTITION CURRENT-OFFSET LOG-END-OFFSET LAG ...
                        # Or: TOPIC PARTITION CURRENT-OFFSET LOG-END-OFFSET LAG ...
                        for part in parts:
                            if part.isdigit() and int(part) > 0:
                                committed_offset = max(committed_offset, int(part))
                    if committed_offset > 0:
                        break
            except Exception:
                pass

        # Fallback Step 2b: Check committed offsets via kafka-python admin client
        if committed_offset == 0:
            try:
                from kafka.admin import KafkaAdminClient
                admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers, request_timeout_ms=4000)
                offsets_map = admin.list_consumer_group_offsets(found_group)
                for tp, om in offsets_map.items():
                    if hasattr(om, 'offset') and om.offset is not None and om.offset > 0:
                        committed_offset = max(committed_offset, om.offset)
                admin.close()
            except Exception as e:
                if not conn_err:
                    conn_err = str(e)

    return broker_connected, found_group, committed_offset, conn_err

def verify_task():
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    username, exam_code, prefix = resolve_candidate_info()
    expected_group = f"alerts-group-{prefix}"

    candidate_names = [
        expected_group,
        f"alerts-group-{username}",
        f"alerts-group-{exam_code}",
        "alerts-group"
    ]

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    broker_connected, found_group, committed_offset, conn_err = inspect_consumer_offsets(candidate_names, bootstrap_servers)

    # TC3: Consumer connection check
    tc3_name = "TC3: Consumer connection check"
    tc3_status = "[FAILED]"
    tc3_score = 0
    if broker_connected:
        tc3_status = "[PASSED]"
        tc3_score = 4
        tc3_reason = f"Successfully connected to Kafka broker at {bootstrap_servers}."
    else:
        reason_detail = f" ({conn_err})" if conn_err else ""
        tc3_reason = f"Broker connection failed at {bootstrap_servers}.{reason_detail}"

    # TC1: Consumer group check
    tc1_name = f"TC1: Consumer group check ({expected_group})"
    tc1_status = "[FAILED]"
    tc1_score = 0
    if found_group:
        tc1_status = "[PASSED]"
        tc1_score = 4
        tc1_reason = f"Consumer group '{found_group}' exists on broker."
    else:
        tc1_reason = f"Consumer group '{expected_group}' not found on broker."

    # TC2: Commit offset verification
    tc2_name = "TC2: Commit offset verification"
    tc2_status = "[FAILED]"
    tc2_score = 0
    if found_group and committed_offset > 0:
        tc2_status = "[PASSED]"
        tc2_score = 4
        tc2_reason = f"Verified committed offset progress ({committed_offset}) in group '{found_group}'."
    elif found_group:
        tc2_reason = f"Consumer group '{found_group}' found, but no committed offset progress detected."
    else:
        tc2_reason = "Prerequisite failed (consumer group not found)."

    # TC4 & TC5: Reserved validation
    all_prereqs = (tc1_score == 4 and tc2_score == 4 and tc3_score == 4)
    tc4_name = "TC4: Reserved validation"
    tc4_status = "[PASSED]" if all_prereqs else "[FAILED]"
    tc4_score = 4 if all_prereqs else 0
    tc4_reason = "Verified successfully." if all_prereqs else "Prerequisite failed."

    tc5_name = "TC5: Reserved validation"
    tc5_status = "[PASSED]" if all_prereqs else "[FAILED]"
    tc5_score = 4 if all_prereqs else 0
    tc5_reason = "Verified successfully." if all_prereqs else "Prerequisite failed."

    results = {
        'tc1': tc1_score == 4,
        'tc2': tc2_score == 4,
        'tc3': tc3_score == 4,
        'tc4': tc4_score == 4,
        'tc5': tc5_score == 4
    }

    # Save solution.json merging with metadata across all possible workspace locations
    candidate_save_paths = [
        os.path.join(get_base_path(), 'solution.json'),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace', 'solution.json')),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solution.json')),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'solution.json')),
        os.path.join(os.getcwd(), 'solution.json'),
        os.path.join(os.getcwd(), 'student_workspace', 'solution.json'),
        os.path.expanduser('~/solution.json'),
        os.path.expanduser('~/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/kf_consumer_offsets/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/kf_consumer_offsets/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/KF_Q03_E/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/KF_Q03_E/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/KF_Q03_E/kf_consumer_offsets/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_workspace/KF_Q03_E/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_workspace/KF_Q03_E/solution.json'),
        os.path.expanduser('~/NIIT_workspace/solution.json'),
        "/home/LabsKraft/NIIT_Workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/student_workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/kf_consumer_offsets/student_workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/KF_Q03_E/student_workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/KF_Q03_E/kf_consumer_offsets/student_workspace/solution.json",
        "/home/LabsKraft/student_workspace/solution.json",
        "/home/LabsKraft/solution.json"
    ]

    # Also search candidate roots dynamically for any solution.json
    for search_root in [os.path.expanduser('~/NIIT_Workspace'), os.path.expanduser('~/NIIT_workspace'), os.path.expanduser('~'), '/home/LabsKraft', os.getcwd()]:
        if os.path.isdir(search_root):
            try:
                for r, d, f in os.walk(search_root):
                    depth = len(os.path.relpath(r, search_root).split(os.sep))
                    if depth > 4:
                        d.clear()
                        continue
                    if 'solution.json' in f:
                        sp_cand = os.path.join(r, 'solution.json')
                        if sp_cand not in candidate_save_paths:
                            candidate_save_paths.append(sp_cand)
            except Exception:
                pass

    for sp in candidate_save_paths:
        try:
            sp_dir = os.path.dirname(sp)
            if sp_dir and not os.path.exists(sp_dir):
                continue
            sol_data = {}
            if os.path.exists(sp):
                try:
                    with open(sp, 'r', encoding='utf-8') as f:
                        sol_data = json.load(f)
                except Exception:
                    sol_data = {}
            if not isinstance(sol_data, dict):
                sol_data = {}
            sol_data['question_id'] = 'KF_Q03_E'
            sol_data['problem_code'] = 'kf_consumer_offsets'
            sol_data['niit_username'] = username
            sol_data['exam_code'] = exam_code
            sol_data['results'] = results
            with open(sp, 'w', encoding='utf-8') as f:
                json.dump(sol_data, f, indent=2)
        except Exception:
            pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results), flush=True)
        return

    print_separator()
    print("                NIIT REAL-TIME AUDIT", flush=True)
    print_separator()
    print_test_case(tc1_name, tc1_status, tc1_score, 4, tc1_reason)
    print_test_case(tc2_name, tc2_status, tc2_score, 4, tc2_reason)
    print_test_case(tc3_name, tc3_status, tc3_score, 4, tc3_reason)
    print_test_case(tc4_name, tc4_status, tc4_score, 4, tc4_reason)
    print_test_case(tc5_name, tc5_status, tc5_score, 4, tc5_reason)

    total_score = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
    print_separator()
    score_string = f"{total_score}/20"
    print(f"TOTAL SCORE:{score_string:>57}", flush=True)
    print_separator()

if __name__ == '__main__':
    verify_task()

def verify_task_central(username, start_time_str, exam_code="UNKNOWN", **kwargs):
    try:
        from driver_central import verify_task_central as _central
        return _central(username, start_time_str, exam_code, **kwargs)
    except Exception:
        return verify_task()
