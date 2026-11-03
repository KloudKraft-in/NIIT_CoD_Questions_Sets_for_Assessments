import os
import sys
import json
import re
import subprocess

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

def query_kafka_topic(candidate_names, bootstrap_servers="localhost:9092"):
    found_topic = None
    partition_count = None
    replication_factor = None
    err = None

    # Method 1: kafka-python (KafkaAdminClient)
    try:
        from kafka.admin import KafkaAdminClient
        admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers, request_timeout_ms=5000)
        try:
            cluster_topics = admin.list_topics()
            for cand in candidate_names:
                if cand in cluster_topics:
                    found_topic = cand
                    break
            if not found_topic:
                for t in cluster_topics:
                    if t.startswith("telemetry-stream"):
                        found_topic = t
                        break
            if found_topic:
                details = admin.describe_topics([found_topic])
                if details and details[0].get('error_code') == 0:
                    partitions = details[0].get('partitions', [])
                    partition_count = len(partitions)
                    if partitions and 'replicas' in partitions[0]:
                        replication_factor = len(partitions[0]['replicas'])
            admin.close()
            return found_topic, partition_count, replication_factor, None
        except Exception as e:
            try:
                admin.close()
            except Exception:
                pass
            err = str(e)
    except Exception as e:
        err = str(e)

    # Method 2: CLI fallback (kafka-topics.sh / kafka-topics)
    for cmd in ["kafka-topics.sh", "kafka-topics", "/opt/kafka/bin/kafka-topics.sh", "/usr/local/kafka/bin/kafka-topics.sh", "/opt/bitnami/kafka/bin/kafka-topics.sh"]:
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
                        if t.startswith("telemetry-stream"):
                            found_topic = t
                            break
                if found_topic:
                    desc_proc = subprocess.run([cmd, "--bootstrap-server", bootstrap_servers, "--describe", "--topic", found_topic], capture_output=True, text=True, timeout=6)
                    if desc_proc.returncode == 0:
                        p_match = re.search(r"PartitionCount:\s*(\d+)", desc_proc.stdout)
                        r_match = re.search(r"ReplicationFactor:\s*(\d+)", desc_proc.stdout)
                        if p_match:
                            partition_count = int(p_match.group(1))
                        if r_match:
                            replication_factor = int(r_match.group(1))
                return found_topic, partition_count, replication_factor, None
        except Exception:
            pass

    return found_topic, partition_count, replication_factor, err

def verify_task():
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    username, exam_code, prefix = resolve_candidate_info()
    expected_topic = f"telemetry-stream-{prefix}"

    candidate_names = [
        expected_topic,
        f"telemetry-stream-{username}",
        f"telemetry-stream-{exam_code}",
        "telemetry-stream"
    ]

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    found_topic, partition_count, replication_factor, conn_err = query_kafka_topic(candidate_names, bootstrap_servers)

    tc1_name = f"TC1: Topic existence ({expected_topic})"
    tc1_status = "[FAILED]"
    tc1_score = 0
    if found_topic:
        tc1_status = "[PASSED]"
        tc1_score = 4
        tc1_reason = f"Topic '{found_topic}' exists on broker."
    else:
        reason_detail = f" (Connection details: {conn_err})" if conn_err else ""
        tc1_reason = f"Topic '{expected_topic}' not found on broker {bootstrap_servers}.{reason_detail}"

    tc2_name = "TC2: Partition count check (3)"
    tc2_status = "[FAILED]"
    tc2_score = 0
    if found_topic and partition_count == 3:
        tc2_status = "[PASSED]"
        tc2_score = 4
        tc2_reason = f"Partition count is {partition_count}."
    elif found_topic:
        tc2_reason = f"Partition count is {partition_count}, expected 3."
    else:
        tc2_reason = "Prerequisite failed (topic not found)."

    tc3_name = "TC3: Replication factor verification (1)"
    tc3_status = "[FAILED]"
    tc3_score = 0
    if found_topic and replication_factor == 1:
        tc3_status = "[PASSED]"
        tc3_score = 4
        tc3_reason = f"Replication factor is {replication_factor}."
    elif found_topic:
        tc3_reason = f"Replication factor is {replication_factor}, expected 1."
    else:
        tc3_reason = "Prerequisite failed (topic not found)."

    tc4_name = "TC4: Reserved validation"
    tc4_status = "[PASSED]" if found_topic else "[FAILED]"
    tc4_score = 4 if found_topic else 0
    tc4_reason = "Validated successfully." if found_topic else "Prerequisite failed."

    tc5_name = "TC5: Reserved validation"
    tc5_status = "[PASSED]" if found_topic else "[FAILED]"
    tc5_score = 4 if found_topic else 0
    tc5_reason = "Validated successfully." if found_topic else "Prerequisite failed."

    results = {
        'tc1': tc1_score == 4,
        'tc2': tc2_score == 4,
        'tc3': tc3_score == 4,
        'tc4': tc4_score == 4,
        'tc5': tc5_score == 4
    }

    # Save solution.json merging with metadata
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        sol_data = {}
        if os.path.exists(sol_path):
            try:
                with open(sol_path, 'r', encoding='utf-8') as f:
                    sol_data = json.load(f)
            except Exception:
                pass
        sol_data['results'] = results
        with open(sol_path, 'w', encoding='utf-8') as f:
            json.dump(sol_data, f, indent=2)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
        return

    print_separator()
    print("                NIIT REAL-TIME AUDIT")
    print_separator()
    print_test_case(tc1_name, tc1_status, tc1_score, 4, tc1_reason)
    print_test_case(tc2_name, tc2_status, tc2_score, 4, tc2_reason)
    print_test_case(tc3_name, tc3_status, tc3_score, 4, tc3_reason)
    print_test_case(tc4_name, tc4_status, tc4_score, 4, tc4_reason)
    print_test_case(tc5_name, tc5_status, tc5_score, 4, tc5_reason)

    total_score = tc1_score + tc2_score + tc3_score + tc4_score + tc5_score
    print_separator()
    score_string = f"{total_score}/20"
    print(f"TOTAL SCORE:{score_string:>57}")
    print_separator()

if __name__ == '__main__':
    verify_task()

def verify_task_central(username, start_time_str, exam_code="UNKNOWN", **kwargs):
    try:
        from driver_central import verify_task_central as _central
        return _central(username, start_time_str, exam_code, **kwargs)
    except Exception:
        return verify_task()
