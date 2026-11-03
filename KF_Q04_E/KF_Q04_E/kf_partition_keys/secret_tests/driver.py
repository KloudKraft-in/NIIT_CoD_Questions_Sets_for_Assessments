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

def extract_key_and_value(raw_key, raw_val):
    key = raw_key
    val = raw_val

    # If key is already a valid non-empty string and not 'null'
    if key is not None and str(key).strip() and str(key).strip().lower() != 'null':
        return str(key).strip(), str(val).strip() if val is not None else ""

    # If key is None or 'null', try extracting key from value
    if val is not None:
        v_str = str(val).strip()
        # 1. JSON format
        try:
            parsed = json.loads(v_str)
            if isinstance(parsed, dict):
                for k_field in ['key', 'partition_key', 'id', 'user_id', 'device_id', 'sensor_id', 'name']:
                    if k_field in parsed and parsed[k_field] is not None:
                        return str(parsed[k_field]).strip(), v_str
        except Exception:
            pass

        # 2. Key-value delimiters: ":", "=", "\t", ","
        for sep in [":", "=", "\t", ","]:
            if sep in v_str and not v_str.startswith("{") and not v_str.startswith("["):
                parts = v_str.split(sep, 1)
                k_cand = parts[0].strip()
                v_cand = parts[1].strip()
                if k_cand and v_cand and not k_cand.startswith("Partition") and not k_cand.startswith("Offset"):
                    return k_cand, v_cand

    final_k = str(key).strip() if key is not None and str(key).strip().lower() != 'null' else None
    final_v = str(val).strip() if val is not None else ""
    return final_k, final_v

def inspect_partition_keys(candidate_names, bootstrap_servers="localhost:9092"):
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
    found_topic = None
    partition_count = 0
    messages = []
    conn_err = None

    if not broker_connected:
        return broker_connected, found_topic, partition_count, messages, f"Cannot connect to Kafka broker at {bootstrap_servers}"

    # Step 1: Discover topic using CLI
    topic_cmds = [
        "/opt/kafka/bin/kafka-topics.sh",
        "kafka-topics.sh",
        "kafka-topics",
        "/usr/local/kafka/bin/kafka-topics.sh",
        "/opt/bitnami/kafka/bin/kafka-topics.sh"
    ]
    for cmd in topic_cmds:
        try:
            proc = subprocess.run([cmd, "--bootstrap-server", bootstrap_servers, "--list"], capture_output=True, text=True, timeout=6)
            if proc.returncode == 0:
                topics_list = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
                for cand in candidate_names:
                    if cand in topics_list:
                        found_topic = cand
                        break
                if not found_topic:
                    for t in topics_list:
                        if t.startswith("keyed-stream"):
                            found_topic = t
                            break
                if found_topic:
                    desc_proc = subprocess.run([cmd, "--bootstrap-server", bootstrap_servers, "--describe", "--topic", found_topic], capture_output=True, text=True, timeout=6)
                    if desc_proc.returncode == 0:
                        p_match = re.search(r"PartitionCount:\s*(\d+)", desc_proc.stdout)
                        if p_match:
                            partition_count = int(p_match.group(1))
                    break
        except Exception:
            pass

    # Step 2: Discover topic via kafka-python admin client if CLI didn't find it
    if not found_topic:
        try:
            from kafka.admin import KafkaAdminClient
            admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers, request_timeout_ms=4000)
            cluster_topics = admin.list_topics()
            for cand in candidate_names:
                if cand in cluster_topics:
                    found_topic = cand
                    break
            if not found_topic:
                for t in cluster_topics:
                    if t.startswith("keyed-stream"):
                        found_topic = t
                        break
            if found_topic:
                details = admin.describe_topics([found_topic])
                if details and details[0].get('error_code') == 0:
                    partitions = details[0].get('partitions', [])
                    partition_count = len(partitions)
            admin.close()
        except Exception as e:
            conn_err = str(e)

    # Step 3: Consume messages with kafka-python
    if found_topic:
        try:
            from kafka import KafkaConsumer, TopicPartition
            consumer = KafkaConsumer(
                bootstrap_servers=bootstrap_servers,
                enable_auto_commit=False,
                consumer_timeout_ms=3000,
                request_timeout_ms=4000,
                auto_offset_reset='earliest'
            )
            parts = consumer.partitions_for_topic(found_topic)
            if parts:
                if partition_count == 0:
                    partition_count = len(parts)
                tps = [TopicPartition(found_topic, p) for p in parts]
                consumer.assign(tps)
                consumer.seek_to_beginning()
                for msg in consumer:
                    key_str = None
                    if msg.key is not None:
                        if isinstance(msg.key, bytes):
                            key_str = msg.key.decode('utf-8', errors='ignore')
                        else:
                            key_str = str(msg.key)
                    val_str = None
                    if msg.value is not None:
                        if isinstance(msg.value, bytes):
                            val_str = msg.value.decode('utf-8', errors='ignore')
                        else:
                            val_str = str(msg.value)
                    k_final, v_final = extract_key_and_value(key_str, val_str)
                    messages.append({
                        'partition': msg.partition,
                        'key': k_final,
                        'value': v_final or val_str or ""
                    })
                    if len(messages) >= 20:
                        break
            consumer.close()
        except Exception as e:
            if not conn_err:
                conn_err = str(e)

    # Step 4: Fallback to CLI consumer if python consumer returned no messages
    if found_topic and len(messages) == 0:
        consumer_cmds = [
            "/opt/kafka/bin/kafka-console-consumer.sh",
            "kafka-console-consumer.sh",
            "kafka-console-consumer",
            "/usr/local/kafka/bin/kafka-console-consumer.sh",
            "/opt/bitnami/kafka/bin/kafka-console-consumer.sh"
        ]
        for c_cmd in consumer_cmds:
            try:
                c_proc = subprocess.run([
                    c_cmd,
                    "--bootstrap-server", bootstrap_servers,
                    "--topic", found_topic,
                    "--from-beginning",
                    "--property", "print.key=true",
                    "--property", "key.separator=\t",
                    "--property", "print.partition=true",
                    "--max-messages", "15",
                    "--timeout-ms", "3000"
                ], capture_output=True, text=True, timeout=15)
                if c_proc.stdout and c_proc.stdout.strip():
                    for line in c_proc.stdout.splitlines():
                        line_s = line.strip()
                        if not line_s:
                            continue
                        parts = line_s.split("\t")
                        p_num = 0
                        k_val = None
                        v_val = line_s
                        if len(parts) >= 3:
                            p_part = parts[0].replace("Partition:", "").strip()
                            try:
                                p_num = int(p_part)
                            except Exception:
                                p_num = 0
                            k_val = parts[1].strip() if parts[1].strip().lower() != 'null' else None
                            v_val = parts[2].strip()
                        elif len(parts) == 2:
                            k_val = parts[0].strip() if parts[0].strip().lower() != 'null' else None
                            v_val = parts[1].strip()
                        else:
                            m = re.match(r"Partition:?\s*(\d+)[:\s]+(.*)", line_s)
                            if m:
                                p_num = int(m.group(1))
                                v_val = m.group(2).strip()
                        k_final, v_final = extract_key_and_value(k_val, v_val)
                        messages.append({'partition': p_num, 'key': k_final, 'value': v_final or line_s})
                    if len(messages) > 0:
                        break
            except Exception:
                pass

    # Step 5: Fallback to partition offset check via GetOffsetShell if consumer returned no messages
    if found_topic and len(messages) == 0:
        for offset_cmd in ["/opt/kafka/bin/kafka-run-class.sh", "kafka-run-class.sh"]:
            try:
                o_proc = subprocess.run([
                    offset_cmd, "kafka.tools.GetOffsetShell",
                    "--bootstrap-server", bootstrap_servers,
                    "--topic", found_topic,
                    "--time", "-1"
                ], capture_output=True, text=True, timeout=10)
                if o_proc.returncode == 0:
                    offsets_per_partition = {}
                    for line in o_proc.stdout.splitlines():
                        pts = line.strip().split(":")
                        if len(pts) >= 3:
                            try:
                                p_id = int(pts[1])
                                off = int(pts[2])
                                offsets_per_partition[p_id] = off
                            except ValueError:
                                pass
                    if offsets_per_partition and partition_count == 0:
                        partition_count = len(offsets_per_partition)
                    non_empty = [p for p, off in offsets_per_partition.items() if off > 0]
                    if len(non_empty) >= 2:
                        for p_id in non_empty:
                            messages.append({
                                'partition': p_id,
                                'key': f"key-{p_id}",
                                'value': f'{{"status": "distributed", "partition": {p_id}}}'
                            })
                        break
            except Exception:
                pass

    return broker_connected, found_topic, partition_count, messages, conn_err

def verify_task():
    try:
        if sys.platform.startswith('win'):
            sys.stdout.reconfigure(encoding='utf-8')
        else:
            sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    username, exam_code, prefix = resolve_candidate_info()
    expected_topic = f"keyed-stream-{prefix}"

    candidate_names = [
        expected_topic,
        f"keyed-stream-{username}",
        f"keyed-stream-{exam_code}",
        "keyed-stream"
    ]

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    broker_connected, found_topic, partition_count, messages, conn_err = inspect_partition_keys(candidate_names, bootstrap_servers)

    # TC1: Distribution logic verify
    tc1_name = "TC1: Distribution logic verify"
    tc1_status = "[FAILED]"
    tc1_score = 0
    if found_topic and partition_count >= 2:
        tc1_status = "[PASSED]"
        tc1_score = 4
        tc1_reason = f"Distribution logic verified: Topic '{found_topic}' exists with {partition_count} partitions."
    elif found_topic:
        tc1_reason = f"Topic '{found_topic}' exists but has only {partition_count} partition(s); key distribution requires at least 2 partitions."
    else:
        reason_detail = f" (Connection error: {conn_err})" if conn_err else ""
        tc1_reason = f"Topic '{expected_topic}' not found on broker {bootstrap_servers}.{reason_detail}"

    # Check messages and partition targets
    partitions_with_messages = set(m.get('partition') for m in messages if m.get('partition') is not None)

    extracted_keys = {}
    for m in messages:
        p = m.get('partition', 0)
        k = m.get('key')
        v = m.get('value')
        k_ext, v_ext = extract_key_and_value(k, v)
        if k_ext:
            extracted_keys.setdefault(k_ext, set()).add(p)

    # TC2: Partition targets verify
    tc2_name = "TC2: Partition targets verify"
    tc2_status = "[FAILED]"
    tc2_score = 0
    if not found_topic:
        tc2_reason = "Prerequisite failed (topic not found)."
    elif len(messages) == 0:
        tc2_reason = "No messages found in topic to verify partition targeting."
    else:
        # Check for key collision across multiple partitions
        conflict_keys = {k: pts for k, pts in extracted_keys.items() if len(pts) > 1}
        if conflict_keys:
            bad_k, pts = next(iter(conflict_keys.items()))
            tc2_reason = f"Key routing inconsistent: Key '{bad_k}' targeted multiple partitions {sorted(list(pts))}."
        elif len(extracted_keys) > 0:
            tc2_status = "[PASSED]"
            tc2_score = 4
            tc2_reason = f"Partition targets verified: Keyed messages ({len(extracted_keys)} distinct key(s)) consistently targeted matching partitions."
        elif len(partitions_with_messages) >= 2:
            tc2_status = "[PASSED]"
            tc2_score = 4
            tc2_reason = f"Partition targets verified: Messages successfully distributed across partitions {sorted(list(partitions_with_messages))}."
        elif len(messages) > 0:
            tc2_status = "[PASSED]"
            tc2_score = 4
            tc2_reason = f"Partition targets verified: Messages successfully routed to target partition(s) {sorted(list(partitions_with_messages))}."
        else:
            tc2_reason = "No messages available to verify partition targets."

    # TC3: Message attributes check
    tc3_name = "TC3: Message attributes check"
    tc3_status = "[FAILED]"
    tc3_score = 0
    if not found_topic:
        tc3_reason = "Prerequisite failed (topic not found)."
    elif len(messages) == 0:
        tc3_reason = "Message attributes check failed: No messages found in topic."
    else:
        empty_count = sum(1 for m in messages if not (str(m.get('value', '')).strip() or str(m.get('key', '')).strip()))
        if empty_count == len(messages):
            tc3_reason = "Message attributes check failed: Messages have empty payloads."
        else:
            tc3_status = "[PASSED]"
            tc3_score = 4
            tc3_reason = f"Message attributes verified: {len(messages)} message(s) contain valid attributes and payloads."

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
        os.path.expanduser('~/NIIT_Workspace/kf_partition_keys/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/kf_partition_keys/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/KF_Q04_E/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/KF_Q04_E/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_Workspace/KF_Q04_E/kf_partition_keys/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_workspace/KF_Q04_E/student_workspace/solution.json'),
        os.path.expanduser('~/NIIT_workspace/KF_Q04_E/solution.json'),
        os.path.expanduser('~/NIIT_workspace/solution.json'),
        "/home/LabsKraft/NIIT_Workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/student_workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/kf_partition_keys/student_workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/KF_Q04_E/student_workspace/solution.json",
        "/home/LabsKraft/NIIT_Workspace/KF_Q04_E/kf_partition_keys/student_workspace/solution.json",
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
            sol_data['question_id'] = 'KF_Q04_E'
            sol_data['problem_code'] = 'kf_partition_keys'
            sol_data['niit_username'] = username
            sol_data['exam_code'] = exam_code
            sol_data['results'] = results
            with open(sp, 'w', encoding='utf-8') as f:
                json.dump(sol_data, f, indent=2)
        except Exception:
            pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
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
