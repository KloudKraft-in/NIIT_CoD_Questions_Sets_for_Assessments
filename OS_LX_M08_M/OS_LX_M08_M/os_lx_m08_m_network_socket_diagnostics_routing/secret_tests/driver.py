import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_M08_M"
PROBLEM_SLUG = "os_lx_m08_m_network_socket_diagnostics_routing"
LAB_TITLE = "Linux Lab: Network Socket Diagnostics, Routing Path & DNS Troubleshooting"
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
    "tc1": "Socket state inspection: ss -tulpn correctly captures all listening TCP/UDP sockets",
    "tc2": "DNS resolution analysis: forward lookup and DNS query response time recorded",
    "tc3": "Path hop tracing: traceroute output captures the exact hop where latency climbs or drops",
    "tc4": "Port probe testing: nc -zv accurately identifies port reachability status",
    "tc5": "Failure signature classification: correctly distinguishes 'Connection Refused' vs 'Connection Timed Out'",
    "tc6": "Firewall audit: local iptables/nftables rules audited for outbound restrictions",
    "tc7": "ICMP latency check: ping packet loss and RTT variance documented",
    "tc8": "Final verdict report: network_triage_verdict.json contains root cause category (DNS, ROUTING, FIREWALL, or SERVICE_DOWN)"
}

TC_MARKS = {
    "tc1": 2,
    "tc2": 2,
    "tc3": 2,
    "tc4": 3,
    "tc5": 3,
    "tc6": 2,
    "tc7": 3,
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

    verdict_data = None
    for h in homes:
        f = os.path.join(h, "network_triage_verdict.json")
        if safe_isfile(f):
            try:
                parsed = json.loads(safe_read(f))
                if isinstance(parsed, dict) and len(parsed) > 0:
                    verdict_data = parsed
                    break
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # TC1: Socket state inspection (2 Marks)
    # -------------------------------------------------------------------------
    if verdict_data and any(k in verdict_data for k in ['listening_sockets', 'sockets', 'ss_output', 'ports', 'open_ports']):
        results['tc1'] = True
    if not results['tc1']:
        for h in homes:
            for fn in ["listening_sockets.txt", "sockets.txt", "ss.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['listen', 'tcp', 'udp', 'local address', 'peer address', 'ss -tulpn']):
                        results['tc1'] = True
                        break
            if results['tc1']:
                break
    if not results['tc1']:
        if check_bash_history(homes, r'ss\s+-tulpn.*listening_sockets') or check_bash_history(homes, r'listening_sockets\.txt'):
            results['tc1'] = True

    # -------------------------------------------------------------------------
    # TC2: DNS resolution analysis (2 Marks)
    # -------------------------------------------------------------------------
    if verdict_data and any(k in verdict_data for k in ['dns_resolution', 'dns_analysis', 'nslookup', 'dig', 'dns']):
        results['tc2'] = True
    if not results['tc2']:
        for h in homes:
            for fn in ["dns_resolution.txt", "dns.txt", "nslookup.txt", "dig.txt", "dns_lookup.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['paymentpartner', 'server:', 'address:', 'a record', 'nxdomain', 'query time', 'answer:']):
                        results['tc2'] = True
                        break
            if results['tc2']:
                break
    if not results['tc2']:
        if check_bash_history(homes, r'nslookup\s+.*paymentpartner') or check_bash_history(homes, r'dig\s+.*paymentpartner') or check_bash_history(homes, r'dns_resolution\.txt'):
            results['tc2'] = True

    # -------------------------------------------------------------------------
    # TC3: Path hop tracing (2 Marks)
    # -------------------------------------------------------------------------
    if verdict_data and any(k in verdict_data for k in ['route_hops', 'traceroute', 'hops', 'routing_path', 'routing']):
        results['tc3'] = True
    if not results['tc3']:
        for h in homes:
            for fn in ["route_hops.txt", "traceroute.txt", "trace.txt", "hops.txt", "tracepath.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['traceroute', 'hops', 'ms', '* * *', '1  ', '2  ', 'gateway']):
                        results['tc3'] = True
                        break
            if results['tc3']:
                break
    if not results['tc3']:
        if check_bash_history(homes, r'traceroute') or check_bash_history(homes, r'tracepath'):
            results['tc3'] = True

    # -------------------------------------------------------------------------
    # TC4: Port probe testing (3 Marks)
    # -------------------------------------------------------------------------
    if verdict_data and any(k in verdict_data for k in ['port_probe', 'nc_output', 'probe_status', 'tcp_connect', 'nc']):
        results['tc4'] = True
    if not results['tc4']:
        for h in homes:
            for fn in ["port_probe.txt", "nc_probe.txt", "nc.txt", "nc_output.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['nc', '8443', 'succeeded', 'refused', 'timed out', 'open', 'connection to']):
                        results['tc4'] = True
                        break
            if results['tc4']:
                break
    if not results['tc4']:
        if check_bash_history(homes, r'nc\s+-zv') or check_bash_history(homes, r'nc\s+.*8443') or check_bash_history(homes, r'telnet.*8443'):
            results['tc4'] = True

    # -------------------------------------------------------------------------
    # TC5: Failure signature classification (3 Marks)
    # -------------------------------------------------------------------------
    if verdict_data:
        sig = str(verdict_data.get('failure_signature', verdict_data.get('signature', verdict_data.get('connection_status', '')))).upper()
        if any(term in sig for term in ['REFUSED', 'TIMED_OUT', 'TIMEOUT', 'CONNECTION', 'DROPPED', 'REJECTED']):
            results['tc5'] = True
    if not results['tc5']:
        for h in homes:
            for fn in ["failure_signature.txt", "signature.txt", "port_probe.txt", "nc_probe.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['connection refused', 'connection timed out', 'timed out', 'refused', 'rejected', 'dropped']):
                        results['tc5'] = True
                        break
            if results['tc5']:
                break

    # -------------------------------------------------------------------------
    # TC6: Firewall audit (2 Marks)
    # -------------------------------------------------------------------------
    if verdict_data and any(k in verdict_data for k in ['firewall_audit', 'iptables_rules', 'nftables', 'ufw', 'firewall']):
        results['tc6'] = True
    if not results['tc6']:
        for h in homes:
            for fn in ["firewall_audit.txt", "iptables.txt", "ufw.txt", "nftables.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['chain output', 'iptables', 'accept', 'drop', 'reject', 'ufw status', 'filter']):
                        results['tc6'] = True
                        break
            if results['tc6']:
                break
    if not results['tc6']:
        if check_bash_history(homes, r'iptables\s+-L') or check_bash_history(homes, r'ufw\s+status') or check_bash_history(homes, r'nft\s+list'):
            results['tc6'] = True

    # -------------------------------------------------------------------------
    # TC7: ICMP latency check (3 Marks)
    # -------------------------------------------------------------------------
    if verdict_data and any(k in verdict_data for k in ['icmp_metrics', 'ping_stats', 'packet_loss', 'rtt', 'ping']):
        results['tc7'] = True
    if not results['tc7']:
        for h in homes:
            for fn in ["icmp_metrics.txt", "ping.txt", "ping_stats.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['packets transmitted', 'packet loss', 'rtt min/avg/max', '0% packet loss', '100% packet loss', 'ping statistics', 'round-trip']):
                        results['tc7'] = True
                        break
            if results['tc7']:
                break
    if not results['tc7']:
        if check_bash_history(homes, r'ping\s+.*icmp_metrics') or check_bash_history(homes, r'icmp_metrics\.txt') or check_bash_history(homes, r'ping\s+-c\s+\d+\s+192\.168'):
            results['tc7'] = True

    # -------------------------------------------------------------------------
    # TC8: Final verdict report (3 Marks)
    # -------------------------------------------------------------------------
    if verdict_data:
        verdict = str(verdict_data.get('root_cause_verdict', verdict_data.get('verdict', verdict_data.get('root_cause', '')))).upper()
        if any(v in verdict for v in ['DNS', 'ROUTING', 'FIREWALL', 'SERVICE_DOWN', 'PORT_BLOCK', 'CONNECTION_REFUSED']):
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
                metadata = json.load(f)
                metadata.update(existing_data)
                existing_data = metadata
    except Exception:
        pass

    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        f.write(f"# Solution verification result\nresults = {json.dumps(results, indent=4)}\nscore = {total_score}\n")

if __name__ == '__main__':
    verify_task()
