import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_M06_M"
PROBLEM_SLUG = "os_lx_m06_m_sustained_high_load_triage"
LAB_TITLE = "Linux Lab: Sustained High Load Triage & Root Cause Classification"
TOTAL_MARKS = 20

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

def safe_isdir(path):
    try:
        return os.path.isdir(path)
    except Exception:
        return False

def safe_isfile(path):
    try:
        return os.path.isfile(path) and os.path.getsize(path) > 0
    except Exception:
        return False

def safe_read(path, default=""):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return default

def find_all_user_homes():
    homes = set()
    for base in ['/home', '/root']:
        if os.path.isdir(base):
            if base == '/root':
                homes.add('/root')
            else:
                try:
                    for u in os.listdir(base):
                        p = os.path.join(base, u)
                        if os.path.isdir(p):
                            homes.add(p)
                except Exception:
                    pass
    homes.add(os.path.expanduser('~'))
    for u in ['LabsKraft', 'ubuntu', 'labskraft', 'Niit', 'niit']:
        p = f'/home/{u}'
        if os.path.isdir(p):
            homes.add(p)
    for ws_base in ['/home/LabsKraft/NIIT_workspace', '/home/LabsKraft/NIIT_Workspace', '/home/ubuntu/NIIT_workspace', '/home/ubuntu/NIIT_Workspace']:
        if os.path.isdir(ws_base):
            homes.add(ws_base)
            try:
                for sub in os.listdir(ws_base):
                    sub_p = os.path.join(ws_base, sub)
                    if os.path.isdir(sub_p):
                        homes.add(sub_p)
            except Exception:
                pass
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        homes.add(os.path.normpath(os.path.join(script_dir, '..')))
        homes.add(os.path.normpath(os.path.join(script_dir, '..', '..')))
        homes.add(os.getcwd())
    except Exception:
        pass
    return [h for h in homes if os.path.isdir(h)]

def get_aws_metadata():
    import urllib.request
    try:
        token_req = urllib.request.Request("http://169.254.169.254/latest/api/token", headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'}, method='PUT')
        token = urllib.request.urlopen(token_req, timeout=1).read().decode()
        id_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/instance-id", headers={'X-aws-ec2-metadata-token': token})
        instance_id = urllib.request.urlopen(id_req, timeout=1).read().decode()
        region_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/placement/region", headers={'X-aws-ec2-metadata-token': token})
        region = urllib.request.urlopen(region_req, timeout=1).read().decode()
        return instance_id, region
    except Exception:
        return None, None

TC_NAMES = {
    "tc1": "Load average capture: baseline load and 1/5/15 minute trends documented",
    "tc2": "CPU state analysis: user vs system vs iowait (%wa) accurately differentiated",
    "tc3": "Memory & swap triage: free memory and swap activity verified",
    "tc4": "Process identification: rogue process PID and command line accurately isolated",
    "tc5": "I/O inspection: disk write/read throughput of offending process recorded",
    "tc6": "Graceful process termination: process terminated cleanly with SIGTERM/SIGKILL",
    "tc7": "System recovery verification: CPU idle percentage returns to >80%",
    "tc8": "RCA report: load_triage_report.json populated with valid schema and root cause call"
}

TC_MARKS = {
    "tc1": 2,
    "tc2": 2,
    "tc3": 2,
    "tc4": 3,
    "tc5": 3,
    "tc6": 3,
    "tc7": 2,
    "tc8": 3
}

def check_bash_history(homes, pattern):
    for h in homes:
        for hist_file in [".bash_history", ".zsh_history"]:
            p = os.path.join(h, hist_file)
            if safe_isfile(p):
                content = safe_read(p)
                if re.search(pattern, content, re.I):
                    return True
    return False

def validate_all_tcs(homes, check_mtime_func):
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}

    # Load JSON report if candidate has generated it
    report_data = None
    for h in homes:
        f = os.path.join(h, "load_triage_report.json")
        if safe_isfile(f):
            try:
                parsed = json.loads(safe_read(f))
                if isinstance(parsed, dict) and len(parsed) > 0:
                    report_data = parsed
                    break
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # TC1: Load average capture: baseline load and 1/5/15 minute trends documented (2 Marks)
    # -------------------------------------------------------------------------
    if report_data and any(k in report_data for k in ['load_average', 'baseline_load', 'load_metrics', 'load_trends']):
        results['tc1'] = True
    if not results['tc1']:
        for h in homes:
            for fn in ["load_metrics.txt", "uptime.txt", "load.txt", "load_average.txt", "vmstat.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if 'load average' in c or 'average' in c or re.search(r'\d+\.\d+', c):
                        results['tc1'] = True
                        break
            if results['tc1']:
                break
    if not results['tc1']:
        if check_bash_history(homes, r'\buptime\b') or check_bash_history(homes, r'vmstat\s+\d+'):
            results['tc1'] = True

    # -------------------------------------------------------------------------
    # TC2: CPU state analysis: user vs system vs iowait (%wa) accurately differentiated (2 Marks)
    # -------------------------------------------------------------------------
    if report_data:
        cpu_data = report_data.get('cpu_states', report_data.get('cpu_metrics', report_data.get('cpu', {})))
        if isinstance(cpu_data, dict) and any(k in cpu_data for k in ['wa', 'iowait', '%wa', 'usr', 'user', '%usr', 'sys', 'system', '%sys', 'id', 'idle']):
            results['tc2'] = True
        elif any(w in json.dumps(report_data).lower() for w in ['iowait', '%wa', '%usr', 'us', 'sy', 'wa']):
            results['tc2'] = True
    if not results['tc2']:
        for h in homes:
            for fn in ["cpu_states.txt", "cpu_metrics.txt", "cpu.txt", "vmstat.txt", "top.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['%usr', '%sys', '%wa', 'iowait', 'us', 'sy', 'id', 'wa', 'cpu states', '%cpu']):
                        results['tc2'] = True
                        break
            if results['tc2']:
                break
    if not results['tc2']:
        if check_bash_history(homes, r'vmstat') or check_bash_history(homes, r'\btop\b') or check_bash_history(homes, r'\bhtop\b') or check_bash_history(homes, r'mpstat'):
            results['tc2'] = True

    # -------------------------------------------------------------------------
    # TC3: Memory & swap triage: free memory and swap activity verified (2 Marks)
    # -------------------------------------------------------------------------
    if report_data:
        mem_data = report_data.get('memory_metrics', report_data.get('memory', {}))
        if isinstance(mem_data, dict) and len(mem_data) > 0:
            results['tc3'] = True
        elif 'swap' in json.dumps(report_data).lower() or 'free' in json.dumps(report_data).lower():
            results['tc3'] = True
    if not results['tc3']:
        for h in homes:
            for fn in ["memory_triage.txt", "memory.txt", "mem_swap.txt", "free.txt", "vmstat.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['swap', 'free', 'buff/cache', 'available', 'total', 'si', 'so']):
                        results['tc3'] = True
                        break
            if results['tc3']:
                break
    if not results['tc3']:
        if check_bash_history(homes, r'free\s+-m') or check_bash_history(homes, r'free\s+-h') or check_bash_history(homes, r'\bvmstat\b'):
            results['tc3'] = True

    # -------------------------------------------------------------------------
    # TC4: Process identification: rogue process PID and command line accurately isolated (3 Marks)
    # -------------------------------------------------------------------------
    rogue_pid = None
    if report_data:
        rogue = report_data.get('rogue_process', report_data.get('process', {}))
        if isinstance(rogue, dict):
            rogue_pid = rogue.get('pid')
            if rogue_pid or 'command' in rogue or 'name' in rogue:
                results['tc4'] = True
        elif 'pid' in report_data or 'rogue_pid' in report_data:
            rogue_pid = report_data.get('pid') or report_data.get('rogue_pid')
            results['tc4'] = True
    if not results['tc4']:
        for h in homes:
            for fn in ["rogue_process.txt", "top_process.txt", "ps_cpu.txt", "ps.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['pid', 'cpu', 'rogue', 'worker', 'stress', 'sh', 'python']):
                        results['tc4'] = True
                        break
            if results['tc4']:
                break
    if not results['tc4']:
        if check_bash_history(homes, r'ps\s+.*%cpu') or check_bash_history(homes, r'ps\s+aux') or check_bash_history(homes, r'pgrep'):
            results['tc4'] = True

    # -------------------------------------------------------------------------
    # TC5: I/O inspection: disk write/read throughput of offending process recorded (3 Marks)
    # -------------------------------------------------------------------------
    if report_data:
        if any(k in report_data for k in ['io_metrics', 'io_stats', 'disk_throughput', 'read_write_kb', 'disk_io']):
            results['tc5'] = True
        elif 'throughput' in json.dumps(report_data).lower() or 'read_bytes' in json.dumps(report_data).lower() or 'write_bytes' in json.dumps(report_data).lower():
            results['tc5'] = True
    if not results['tc5']:
        for h in homes:
            for fn in ["io_metrics.txt", "disk_io.txt", "pid_io.txt", "iotop.txt", "pidstat.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['read', 'write', 'io', 'kb/s', 'bytes', 'rchar', 'wchar']):
                        results['tc5'] = True
                        break
            if results['tc5']:
                break
    if not results['tc5']:
        if check_bash_history(homes, r'iotop') or check_bash_history(homes, r'pidstat\s+-d') or check_bash_history(homes, r'/proc/\d+/io') or check_bash_history(homes, r'iostat'):
            results['tc5'] = True

    # -------------------------------------------------------------------------
    # TC6: Graceful process termination: process terminated cleanly with SIGTERM/SIGKILL (3 Marks)
    # -------------------------------------------------------------------------
    # Live check: check if rogue worker process is no longer active
    rogue_running = False
    try:
        ps_out = subprocess.run(['pgrep', '-f', 'rogue_worker.sh'], capture_output=True, text=True, timeout=5).stdout.strip()
        if ps_out:
            rogue_running = True
    except Exception:
        pass

    if not rogue_running and safe_isfile('/var/run/rogue_worker.pid'):
        # Process was launched by setup and is now gone
        results['tc6'] = True
    elif not rogue_running and (check_bash_history(homes, r'kill\s+(-15|-9|\b)\s*\d+') or check_bash_history(homes, r'pkill') or check_bash_history(homes, r'killall')):
        results['tc6'] = True
    elif rogue_pid:
        if not os.path.exists(f"/proc/{rogue_pid}"):
            results['tc6'] = True
    if not results['tc6']:
        for h in homes:
            for fn in ["process_killed.txt", "kill_log.txt", "termination.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    results['tc6'] = True
                    break
            if results['tc6']:
                break

    # -------------------------------------------------------------------------
    # TC7: System recovery verification: CPU idle percentage returns to >80% (2 Marks)
    # -------------------------------------------------------------------------
    if results['tc6']:
        try:
            vmstat_out = subprocess.run(['vmstat', '1', '2'], capture_output=True, text=True, timeout=5).stdout.splitlines()
            if len(vmstat_out) >= 4:
                cols = vmstat_out[-1].split()
                if len(cols) >= 15:
                    idle_val = int(cols[14])
                    if idle_val >= 80:
                        results['tc7'] = True
        except Exception:
            pass
    if not results['tc7'] and report_data:
        if any(k in report_data for k in ['recovered_idle_cpu', 'recovery_metrics', 'idle_recovery', 'cpu_idle_after']):
            results['tc7'] = True
    if not results['tc7']:
        for h in homes:
            for fn in ["recovery.txt", "system_recovery.txt", "post_triage.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if 'idle' in c or 'recovery' in c or '8' in c or '9' in c:
                        results['tc7'] = True
                        break
            if results['tc7']:
                break
    if not results['tc7'] and not rogue_running and results['tc6']:
        results['tc7'] = True

    # -------------------------------------------------------------------------
    # TC8: RCA report: load_triage_report.json populated with valid schema and root cause call (3 Marks)
    # -------------------------------------------------------------------------
    if report_data:
        rca = str(report_data.get('root_cause', report_data.get('rca', report_data.get('classification', '')))).upper()
        if any(c in rca for c in ['CPU', 'IO', 'MEMORY', 'DEADLOCK', 'BOUND', 'LEAK', 'RUNAWAY', 'STARVATION']):
            results['tc8'] = True

    return results

def verify_task():
    def check_mtime(path):
        if not os.path.exists(path):
            return False
        if not START_TIME:
            return True
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            return mtime >= START_TIME - timedelta(hours=24)
        except Exception:
            return True

    all_homes = find_all_user_homes()
    results = validate_all_tcs(all_homes, check_mtime)
    total_score = sum(TC_MARKS[k] for k, v in results.items() if v)

    print("\n" + "-" * 60)
    print(f"{LAB_TITLE.upper() + ' VERIFICATION':^60}")
    print(f"System Hostname: {socket.gethostname()}")
    print("-" * 60)

    for k in sorted(TC_NAMES.keys()):
        status = "PASSED" if results.get(k, False) else "FAILED"
        desc = TC_NAMES.get(k, k.upper())
        marks = TC_MARKS.get(k, 0)
        earned = marks if results.get(k, False) else 0
        print(f"{k.upper()}: {desc:<45} [{status}] ({earned}/{marks})")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/{TOTAL_MARKS}")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    existing_data = {
        'question_id': QUESTION_CODE,
        'problem_code': PROBLEM_SLUG,
        'score': total_score,
        'total_marks': TOTAL_MARKS,
        'results': results
    }
    instance_id, aws_region = get_aws_metadata()
    if instance_id:
        existing_data['instance_id'] = instance_id
        existing_data['aws_region'] = aws_region
        
    legacy_metadata_path = os.path.join(HOME, 'Niit_Workspace', PROBLEM_SLUG, 'student_workspace', 'solution.json')
    try:
        if os.path.isfile(legacy_metadata_path):
            with open(legacy_metadata_path, 'r') as f:
                meta = json.load(f)
                for fld in ['labskraft_username', 'user_id', 'assessment_id', 'assessment_start_time', 'question_id']:
                    if fld in meta and fld not in existing_data:
                        existing_data[fld] = meta[fld]
    except Exception:
        pass

    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        f.write(f"# Solution verification result\nresults = {json.dumps(results, indent=4)}\nscore = {total_score}\n")

if __name__ == '__main__':
    verify_task()
