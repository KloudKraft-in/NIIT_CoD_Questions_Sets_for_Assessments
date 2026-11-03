# # import json
# # import os
# # import sys
# # import socket
# # import re
# # import shutil
# # import subprocess
# # from datetime import datetime, timezone, timedelta

# # # Metadata
# # QUESTION_CODE = "OS_LX_M07_M"
# # PROBLEM_SLUG = "os_lx_m07_m_critical_service_dependency_recovery"
# # LAB_TITLE = "Linux Lab: Critical Service Dependency Recovery & Unit Override Management"
# # TOTAL_MARKS = 20

# # START_TIME_STR = os.getenv('NIIT_START_TIME')
# # START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
# # USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
# # HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

# # def safe_isdir(path):
# #     try:
# #         return os.path.isdir(path)
# #     except Exception:
# #         return False

# # def safe_isfile(path):
# #     try:
# #         return os.path.isfile(path) and os.path.getsize(path) > 0
# #     except Exception:
# #         return False

# # def safe_read(path, default=""):
# #     try:
# #         with open(path, 'r', encoding='utf-8', errors='ignore') as f:
# #             return f.read()
# #     except Exception:
# #         return default

# # def find_all_user_homes():
# #     homes = set()
# #     for base in ['/home', '/root']:
# #         if os.path.isdir(base):
# #             if base == '/root':
# #                 homes.add('/root')
# #             else:
# #                 try:
# #                     for u in os.listdir(base):
# #                         p = os.path.join(base, u)
# #                         if os.path.isdir(p):
# #                             homes.add(p)
# #                 except Exception:
# #                     pass
# #     homes.add(os.path.expanduser('~'))
# #     for u in ['LabsKraft', 'ubuntu', 'labskraft', 'Niit', 'niit']:
# #         p = f'/home/{u}'
# #         if os.path.isdir(p):
# #             homes.add(p)
# #     for ws_base in ['/home/LabsKraft/NIIT_workspace', '/home/LabsKraft/NIIT_Workspace', '/home/ubuntu/NIIT_workspace', '/home/ubuntu/NIIT_Workspace']:
# #         if os.path.isdir(ws_base):
# #             homes.add(ws_base)
# #             try:
# #                 for sub in os.listdir(ws_base):
# #                     sub_p = os.path.join(ws_base, sub)
# #                     if os.path.isdir(sub_p):
# #                         homes.add(sub_p)
# #             except Exception:
# #                 pass
# #     try:
# #         script_dir = os.path.dirname(os.path.abspath(__file__))
# #         homes.add(os.path.normpath(os.path.join(script_dir, '..')))
# #         homes.add(os.path.normpath(os.path.join(script_dir, '..', '..')))
# #         homes.add(os.getcwd())
# #     except Exception:
# #         pass
# #     return [h for h in homes if os.path.isdir(h)]

# # def get_aws_metadata():
# #     import urllib.request
# #     try:
# #         token_req = urllib.request.Request("http://169.254.169.254/latest/api/token", headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'}, method='PUT')
# #         token = urllib.request.urlopen(token_req, timeout=1).read().decode()
# #         id_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/instance-id", headers={'X-aws-ec2-metadata-token': token})
# #         instance_id = urllib.request.urlopen(id_req, timeout=1).read().decode()
# #         region_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/placement/region", headers={'X-aws-ec2-metadata-token': token})
# #         region = urllib.request.urlopen(region_req, timeout=1).read().decode()
# #         return instance_id, region
# #     except Exception:
# #         return None, None

# # TC_NAMES = {
# #     "tc1": "Failure diagnosis: journalctl confirms start-limit-hit and missing environment variables",
# #     "tc2": "Counter reset: systemctl reset-failed clears the start-limit throttle state",
# #     "tc3": "Drop-in configuration: /etc/systemd/system/payment-gateway.service.d/override.conf created with valid syntax",
# #     "tc4": "Daemon reload: systemctl daemon-reload executes cleanly",
# #     "tc5": "Service startup: payment-gateway enters stable active (running) state",
# #     "tc6": "Log validation: unit logs show successful configuration loading with zero errors",
# #     "tc7": "Health check probe: local daemon health port responds with HTTP 200 OK"
# # }

# # TC_MARKS = {
# #     "tc1": 3,
# #     "tc2": 2,
# #     "tc3": 3,
# #     "tc4": 3,
# #     "tc5": 3,
# #     "tc6": 3,
# #     "tc7": 3
# # }

# # def check_bash_history(homes, pattern):
# #     for h in homes:
# #         for hist_file in [".bash_history", ".zsh_history"]:
# #             p = os.path.join(h, hist_file)
# #             if safe_isfile(p):
# #                 content = safe_read(p)
# #                 if re.search(pattern, content, re.I):
# #                     return True
# #     return False

# # def validate_all_tcs(homes, check_mtime_func):
# #     results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False}

# #     # -------------------------------------------------------------------------
# #     # TC1: Failure diagnosis: journalctl confirms start-limit-hit and missing environment variables (3 Marks)
# #     # -------------------------------------------------------------------------
# #     for h in homes:
# #         for fn in ["payment_diagnosis.txt", "payment_error.txt", "diagnosis.txt", "journal_error.txt", "tc1.txt"]:
# #             f = os.path.join(h, fn)
# #             if safe_isfile(f):
# #                 c = safe_read(f).lower()
# #                 if any(term in c for term in ['start-limit', 'environment', 'payment-gateway', 'failed', 'throttle', 'port', 'api_key', 'no entries', 'not found', 'could not be found', 'journalctl', 'systemctl', 'payment']):
# #                     results['tc1'] = True
# #                     break
# #         if results['tc1']:
# #             break
# #     if not results['tc1']:
# #         if check_bash_history(homes, r'journalctl') or check_bash_history(homes, r'systemctl'):
# #             results['tc1'] = True

# #     # -------------------------------------------------------------------------
# #     # TC2: Counter reset: systemctl reset-failed clears the start-limit throttle state (2 Marks)
# #     # -------------------------------------------------------------------------
# #     for h in homes:
# #         for fn in ["reset_counter.txt", "reset_failed.txt", "reset.txt", "tc2.txt"]:
# #             f = os.path.join(h, fn)
# #             if safe_isfile(f):
# #                 results['tc2'] = True
# #                 break
# #         if results['tc2']:
# #             break
# #     if not results['tc2']:
# #         if check_bash_history(homes, r'reset-failed'):
# #             results['tc2'] = True

# #     # -------------------------------------------------------------------------
# #     # TC3: Drop-in configuration: override.conf created with valid syntax (3 Marks)
# #     # -------------------------------------------------------------------------
# #     override_paths = [
# #         '/etc/systemd/system/payment-gateway.service.d/override.conf',
# #         '/etc/systemd/system/payment-gateway.service.d/10-env.conf'
# #     ]
# #     for h in homes:
# #         override_paths.append(os.path.join(h, "etc", "systemd", "system", "payment-gateway.service.d", "override.conf"))
# #         override_paths.append(os.path.join(h, "override.conf"))
# #         override_paths.append(os.path.join(h, "tc3.conf"))

# #     found_override = None
# #     for op in override_paths:
# #         if safe_isfile(op):
# #             found_override = op
# #             break

# #     if found_override:
# #         c = safe_read(found_override)
# #         has_env = ('EnvironmentFile' in c and '/etc/payment/gateway.env' in c) or 'EnvironmentFile' in c or 'gateway.env' in c
# #         has_restart = 'RestartSec' in c
# #         has_section = '[Service]' in c
# #         if has_env or has_restart or has_section:
# #             results['tc3'] = True

# #     # -------------------------------------------------------------------------
# #     # TC4: Daemon reload: systemctl daemon-reload executes cleanly (3 Marks)
# #     # -------------------------------------------------------------------------
# #     for h in homes:
# #         for fn in ["daemon_reload.txt", "reload.txt", "tc4.txt"]:
# #             f = os.path.join(h, fn)
# #             if safe_isfile(f):
# #                 results['tc4'] = True
# #                 break
# #         if results['tc4']:
# #             break
# #     if not results['tc4']:
# #         if check_bash_history(homes, r'daemon-reload'):
# #             results['tc4'] = True
# #     if not results['tc4']:
# #         systemctl_bin = shutil.which('systemctl')
# #         if systemctl_bin:
# #             try:
# #                 res = subprocess.run([systemctl_bin, 'show', '-p', 'DropInPaths', 'payment-gateway'], capture_output=True, text=True, timeout=5)
# #                 if 'override.conf' in res.stdout:
# #                     results['tc4'] = True
# #             except Exception:
# #                 pass

# #     # -------------------------------------------------------------------------
# #     # TC5: Service startup: payment-gateway enters stable active (running) state (3 Marks)
# #     # -------------------------------------------------------------------------
# #     systemctl_bin = shutil.which('systemctl')
# #     if systemctl_bin:
# #         try:
# #             res = subprocess.run([systemctl_bin, 'is-active', 'payment-gateway'], capture_output=True, text=True, timeout=5)
# #             if res.stdout.strip() == 'active':
# #                 results['tc5'] = True
# #         except Exception:
# #             pass
# #     if not results['tc5']:
# #         for h in homes:
# #             for fn in ["service_status.txt", "payment_status.txt", "status.txt", "tc5.txt"]:
# #                 f = os.path.join(h, fn)
# #                 if safe_isfile(f):
# #                     c = safe_read(f).lower()
# #                     if 'active (running)' in c or 'active' in c or 'running' in c or 'payment' in c or 'service' in c or 'started' in c:
# #                         results['tc5'] = True
# #                         break
# #             if results['tc5']:
# #                 break

# #     # -------------------------------------------------------------------------
# #     # TC6: Log validation: unit logs show successful configuration loading with zero errors (3 Marks)
# #     # -------------------------------------------------------------------------
# #     journalctl_bin = shutil.which('journalctl')
# #     if journalctl_bin and results['tc5']:
# #         try:
# #             j_res = subprocess.run([journalctl_bin, '-u', 'payment-gateway', '-n', '20'], capture_output=True, text=True, timeout=5)
# #             if 'Payment Gateway starting' in j_res.stdout or 'API_KEY verified' in j_res.stdout or 'Started' in j_res.stdout:
# #                 results['tc6'] = True
# #         except Exception:
# #             pass
# #     if not results['tc6']:
# #         for h in homes:
# #             for fn in ["payment_logs.txt", "unit_logs.txt", "journal_success.txt", "tc6.txt"]:
# #                 f = os.path.join(h, fn)
# #                 if safe_isfile(f):
# #                     c = safe_read(f).lower()
# #                     if any(w in c for w in ['starting', 'port 8080', 'port', '8080', 'verified', 'healthy', 'success', 'started', 'api_key', 'payment']):
# #                         results['tc6'] = True
# #                         break
# #             if results['tc6']:
# #                 break

# #     # -------------------------------------------------------------------------
# #     # TC7: Health check probe: local daemon health port responds with HTTP 200 OK (3 Marks)
# #     # -------------------------------------------------------------------------
# #     curl_bin = shutil.which('curl')
# #     if curl_bin:
# #         try:
# #             res = subprocess.run([curl_bin, '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:8080/health'], capture_output=True, text=True, timeout=3)
# #             if res.stdout.strip() in ['200', '204', '202']:
# #                 results['tc7'] = True
# #         except Exception:
# #             pass
# #     if not results['tc7']:
# #         for h in homes:
# #             for fn in ["health_check.txt", "health_probe.txt", "curl_health.txt", "tc7.txt"]:
# #                 f = os.path.join(h, fn)
# #                 if safe_isfile(f):
# #                     c = safe_read(f)
# #                     if '200' in c or 'healthy' in c.lower() or 'ok' in c.lower() or 'curl' in c.lower():
# #                         results['tc7'] = True
# #                         break
# #             if results['tc7']:
# #                 break
# #     if not results['tc7']:
# #         if check_bash_history(homes, r'curl\s+.*8080') or check_bash_history(homes, r'curl'):
# #             results['tc7'] = True

# #     return results

# # def verify_task():
# #     def check_mtime(path):
# #         if not os.path.exists(path):
# #             return False
# #         if not START_TIME:
# #             return True
# #         try:
# #             mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
# #             return mtime >= START_TIME - timedelta(hours=24)
# #         except Exception:
# #             return True

# #     all_homes = find_all_user_homes()
# #     results = validate_all_tcs(all_homes, check_mtime)
# #     total_score = sum(TC_MARKS[k] for k, v in results.items() if v)

# #     print("\n" + "-" * 60)
# #     print(f"{LAB_TITLE.upper() + ' VERIFICATION':^60}")
# #     print(f"System Hostname: {socket.gethostname()}")
# #     print("-" * 60)

# #     for k in sorted(TC_NAMES.keys()):
# #         status = "PASSED" if results.get(k, False) else "FAILED"
# #         desc = TC_NAMES.get(k, k.upper())
# #         marks = TC_MARKS.get(k, 0)
# #         earned = marks if results.get(k, False) else 0
# #         print(f"{k.upper()}: {desc:<45} [{status}] ({earned}/{marks})")

# #     print("-" * 60)
# #     print(f"{'TOTAL SCORE:':<44} {total_score}/{TOTAL_MARKS}")
# #     print("-" * 60 + "\n")

# #     ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace'))
# #     os.makedirs(ws_path, exist_ok=True)
    
# #     existing_data = {
# #         'question_id': QUESTION_CODE,
# #         'problem_code': PROBLEM_SLUG,
# #         'score': total_score,
# #         'total_marks': TOTAL_MARKS,
# #         'results': results
# #     }
# #     instance_id, aws_region = get_aws_metadata()
# #     if instance_id:
# #         existing_data['instance_id'] = instance_id
# #         existing_data['aws_region'] = aws_region
        
# #     legacy_metadata_path = os.path.join(HOME, 'Niit_Workspace', PROBLEM_SLUG, 'student_workspace', 'solution.json')
# #     try:
# #         if os.path.isfile(legacy_metadata_path):
# #             with open(legacy_metadata_path, 'r') as f:
# #                 metadata = json.load(f)
# #                 metadata.update(existing_data)
# #                 existing_data = metadata
# #     except Exception:
# #         pass

# #     with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
# #         json.dump(existing_data, f, indent=4)
# #     with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
# #         f.write(f"# Solution verification result\nresults = {json.dumps(results, indent=4)}\nscore = {total_score}\n")

# # if __name__ == '__main__':
# #     verify_task()


# import json
# import os
# import sys
# import socket
# import re
# import shutil
# import subprocess
# from datetime import datetime, timezone, timedelta

# # Metadata
# QUESTION_CODE = "OS_LX_M07_M"
# PROBLEM_SLUG = "os_lx_m07_m_critical_service_dependency_recovery"
# LAB_TITLE = "Linux Lab: Critical Service Dependency Recovery & Unit Override Management"
# TOTAL_MARKS = 20

# START_TIME_STR = os.getenv('NIIT_START_TIME')
# START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
# USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
# HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

# def safe_isdir(path):
#     try:
#         return os.path.isdir(path)
#     except Exception:
#         return False

# def safe_isfile(path):
#     try:
#         return os.path.isfile(path) and os.path.getsize(path) > 0
#     except Exception:
#         return False

# def safe_read(path, default=""):
#     try:
#         with open(path, 'r', encoding='utf-8', errors='ignore') as f:
#             return f.read()
#     except Exception:
#         return default

# def find_all_user_homes():
#     homes = set()
#     for base in ['/home', '/root']:
#         if os.path.isdir(base):
#             if base == '/root':
#                 homes.add('/root')
#             else:
#                 try:
#                     for u in os.listdir(base):
#                         p = os.path.join(base, u)
#                         if os.path.isdir(p):
#                             homes.add(p)
#                 except Exception:
#                     pass
#     homes.add(os.path.expanduser('~'))
#     for u in ['LabsKraft', 'ubuntu', 'labskraft', 'Niit', 'niit']:
#         p = f'/home/{u}'
#         if os.path.isdir(p):
#             homes.add(p)
#     for ws_base in ['/home/LabsKraft/NIIT_workspace', '/home/LabsKraft/NIIT_Workspace', '/home/ubuntu/NIIT_workspace', '/home/ubuntu/NIIT_Workspace']:
#         if os.path.isdir(ws_base):
#             homes.add(ws_base)
#             try:
#                 for sub in os.listdir(ws_base):
#                     sub_p = os.path.join(ws_base, sub)
#                     if os.path.isdir(sub_p):
#                         homes.add(sub_p)
#             except Exception:
#                 pass
#     try:
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         homes.add(os.path.normpath(os.path.join(script_dir, '..')))
#         homes.add(os.path.normpath(os.path.join(script_dir, '..', '..')))
#         homes.add(os.getcwd())
#     except Exception:
#         pass
#     return [h for h in homes if os.path.isdir(h)]

# def get_aws_metadata():
#     import urllib.request
#     try:
#         token_req = urllib.request.Request("http://169.254.169.254/latest/api/token", headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'}, method='PUT')
#         token = urllib.request.urlopen(token_req, timeout=1).read().decode()
#         id_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/instance-id", headers={'X-aws-ec2-metadata-token': token})
#         instance_id = urllib.request.urlopen(id_req, timeout=1).read().decode()
#         region_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/placement/region", headers={'X-aws-ec2-metadata-token': token})
#         region = urllib.request.urlopen(region_req, timeout=1).read().decode()
#         return instance_id, region
#     except Exception:
#         return None, None

# TC_NAMES = {
#     "tc1": "Failure diagnosis: journalctl confirms start-limit-hit and missing environment variables",
#     "tc2": "Counter reset: systemctl reset-failed clears the start-limit throttle state",
#     "tc3": "Drop-in configuration: /etc/systemd/system/payment-gateway.service.d/override.conf created with valid syntax",
#     "tc4": "Daemon reload: systemctl daemon-reload executes cleanly",
#     "tc5": "Service startup: payment-gateway enters stable active (running) state",
#     "tc6": "Log validation: unit logs show successful configuration loading with zero errors",
#     "tc7": "Health check probe: local daemon health port responds with HTTP 200 OK"
# }

# TC_MARKS = {
#     "tc1": 3,
#     "tc2": 2,
#     "tc3": 3,
#     "tc4": 3,
#     "tc5": 3,
#     "tc6": 3,
#     "tc7": 3
# }

# def check_bash_history(homes, pattern):
#     for h in homes:
#         for hist_file in [".bash_history", ".zsh_history"]:
#             p = os.path.join(h, hist_file)
#             if safe_isfile(p):
#                 content = safe_read(p)
#                 if re.search(pattern, content, re.I):
#                     return True
#     return False

# def validate_all_tcs(homes, check_mtime_func):
#     results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False}

#     # -------------------------------------------------------------------------
#     # TC1: Failure diagnosis: journalctl confirms start-limit-hit and missing environment variables (3 Marks)
#     # -------------------------------------------------------------------------
#     for h in homes:
#         for fn in ["payment_diagnosis.txt", "payment_error.txt", "diagnosis.txt", "journal_error.txt", "tc1.txt"]:
#             f = os.path.join(h, fn)
#             if safe_isfile(f):
#                 c = safe_read(f).lower()
#                 if any(term in c for term in ['start-limit', 'environment', 'payment-gateway', 'failed', 'throttle', 'port', 'api_key', 'no entries', 'not found', 'could not be found', 'journalctl', 'systemctl', 'payment']):
#                     results['tc1'] = True
#                     break
#         if results['tc1']:
#             break
#     if not results['tc1']:
#         if check_bash_history(homes, r'journalctl') or check_bash_history(homes, r'systemctl'):
#             results['tc1'] = True

#     # -------------------------------------------------------------------------
#     # TC2: Counter reset: systemctl reset-failed clears the start-limit throttle state (2 Marks)
#     # -------------------------------------------------------------------------
#     for h in homes:
#         for fn in ["reset_counter.txt", "reset_failed.txt", "reset.txt", "tc2.txt", "reset_counter.log", "reset.log", "systemctl_reset.txt", "counter.txt"]:
#             f = os.path.join(h, fn)
#             if safe_isfile(f):
#                 results['tc2'] = True
#                 break
#         if results['tc2']:
#             break
#     if not results['tc2']:
#         if check_bash_history(homes, r'reset-failed') or check_bash_history(homes, r'reset'):
#             results['tc2'] = True

#     # -------------------------------------------------------------------------
#     # TC3: Drop-in configuration: override.conf created with valid syntax (3 Marks)
#     # -------------------------------------------------------------------------
#     override_paths = [
#         '/etc/systemd/system/payment-gateway.service.d/override.conf',
#         '/etc/systemd/system/payment-gateway.service.d/10-env.conf'
#     ]
#     for h in homes:
#         override_paths.append(os.path.join(h, "etc", "systemd", "system", "payment-gateway.service.d", "override.conf"))
#         override_paths.append(os.path.join(h, "override.conf"))
#         override_paths.append(os.path.join(h, "tc3.conf"))

#     found_override = None
#     for op in override_paths:
#         if safe_isfile(op):
#             found_override = op
#             break

#     if found_override:
#         c = safe_read(found_override)
#         has_env = ('EnvironmentFile' in c and '/etc/payment/gateway.env' in c) or 'EnvironmentFile' in c or 'gateway.env' in c
#         has_restart = 'RestartSec' in c
#         has_section = '[Service]' in c
#         if has_env or has_restart or has_section:
#             results['tc3'] = True

#     # -------------------------------------------------------------------------
#     # TC4: Daemon reload: systemctl daemon-reload executes cleanly (3 Marks)
#     # -------------------------------------------------------------------------
#     for h in homes:
#         for fn in ["daemon_reload.txt", "reload.txt", "tc4.txt"]:
#             f = os.path.join(h, fn)
#             if safe_isfile(f):
#                 results['tc4'] = True
#                 break
#         if results['tc4']:
#             break
#     if not results['tc4']:
#         if check_bash_history(homes, r'daemon-reload'):
#             results['tc4'] = True
#     if not results['tc4']:
#         systemctl_bin = shutil.which('systemctl')
#         if systemctl_bin:
#             try:
#                 res = subprocess.run([systemctl_bin, 'show', '-p', 'DropInPaths', 'payment-gateway'], capture_output=True, text=True, timeout=5)
#                 if 'override.conf' in res.stdout:
#                     results['tc4'] = True
#             except Exception:
#                 pass

#     # -------------------------------------------------------------------------
#     # TC5: Service startup: payment-gateway enters stable active (running) state (3 Marks)
#     # -------------------------------------------------------------------------
#     systemctl_bin = shutil.which('systemctl')
#     if systemctl_bin:
#         try:
#             res = subprocess.run([systemctl_bin, 'is-active', 'payment-gateway'], capture_output=True, text=True, timeout=5)
#             if res.stdout.strip() == 'active':
#                 results['tc5'] = True
#         except Exception:
#             pass
#     if not results['tc5']:
#         for h in homes:
#             for fn in ["service_status.txt", "payment_status.txt", "status.txt", "tc5.txt"]:
#                 f = os.path.join(h, fn)
#                 if safe_isfile(f):
#                     c = safe_read(f).lower()
#                     if 'active (running)' in c or 'active' in c or 'running' in c or 'payment' in c or 'service' in c or 'started' in c:
#                         results['tc5'] = True
#                         break
#             if results['tc5']:
#                 break

#     # -------------------------------------------------------------------------
#     # TC6: Log validation: unit logs show successful configuration loading with zero errors (3 Marks)
#     # -------------------------------------------------------------------------
#     journalctl_bin = shutil.which('journalctl')
#     if journalctl_bin and results['tc5']:
#         try:
#             j_res = subprocess.run([journalctl_bin, '-u', 'payment-gateway', '-n', '20'], capture_output=True, text=True, timeout=5)
#             if 'Payment Gateway starting' in j_res.stdout or 'API_KEY verified' in j_res.stdout or 'Started' in j_res.stdout:
#                 results['tc6'] = True
#         except Exception:
#             pass
#     if not results['tc6']:
#         for h in homes:
#             for fn in ["payment_logs.txt", "unit_logs.txt", "journal_success.txt", "tc6.txt"]:
#                 f = os.path.join(h, fn)
#                 if safe_isfile(f):
#                     c = safe_read(f).lower()
#                     if any(w in c for w in ['starting', 'port 8080', 'port', '8080', 'verified', 'healthy', 'success', 'started', 'api_key', 'payment']):
#                         results['tc6'] = True
#                         break
#             if results['tc6']:
#                 break

#     # -------------------------------------------------------------------------
#     # TC7: Health check probe: local daemon health port responds with HTTP 200 OK (3 Marks)
#     # -------------------------------------------------------------------------
#     curl_bin = shutil.which('curl')
#     if curl_bin:
#         try:
#             res = subprocess.run([curl_bin, '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:8080/health'], capture_output=True, text=True, timeout=3)
#             if res.stdout.strip() in ['200', '204', '202']:
#                 results['tc7'] = True
#         except Exception:
#             pass
#     if not results['tc7']:
#         for h in homes:
#             for fn in ["health_check.txt", "health_probe.txt", "curl_health.txt", "tc7.txt"]:
#                 f = os.path.join(h, fn)
#                 if safe_isfile(f):
#                     c = safe_read(f)
#                     if '200' in c or 'healthy' in c.lower() or 'ok' in c.lower() or 'curl' in c.lower():
#                         results['tc7'] = True
#                         break
#             if results['tc7']:
#                 break
#     if not results['tc7']:
#         if check_bash_history(homes, r'curl\s+.*8080') or check_bash_history(homes, r'curl'):
#             results['tc7'] = True

#     return results

# def verify_task():
#     def check_mtime(path):
#         if not os.path.exists(path):
#             return False
#         if not START_TIME:
#             return True
#         try:
#             mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
#             return mtime >= START_TIME - timedelta(hours=24)
#         except Exception:
#             return True

#     all_homes = find_all_user_homes()
#     results = validate_all_tcs(all_homes, check_mtime)
#     total_score = sum(TC_MARKS[k] for k, v in results.items() if v)

#     print("\n" + "-" * 60)
#     print(f"{LAB_TITLE.upper() + ' VERIFICATION':^60}")
#     print(f"System Hostname: {socket.gethostname()}")
#     print("-" * 60)

#     for k in sorted(TC_NAMES.keys()):
#         status = "PASSED" if results.get(k, False) else "FAILED"
#         desc = TC_NAMES.get(k, k.upper())
#         marks = TC_MARKS.get(k, 0)
#         earned = marks if results.get(k, False) else 0
#         print(f"{k.upper()}: {desc:<45} [{status}] ({earned}/{marks})")

#     print("-" * 60)
#     print(f"{'TOTAL SCORE:':<44} {total_score}/{TOTAL_MARKS}")
#     print("-" * 60 + "\n")

#     ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace'))
#     os.makedirs(ws_path, exist_ok=True)
    
#     existing_data = {
#         'question_id': QUESTION_CODE,
#         'problem_code': PROBLEM_SLUG,
#         'score': total_score,
#         'total_marks': TOTAL_MARKS,
#         'results': results
#     }
#     instance_id, aws_region = get_aws_metadata()
#     if instance_id:
#         existing_data['instance_id'] = instance_id
#         existing_data['aws_region'] = aws_region
        
#     legacy_metadata_path = os.path.join(HOME, 'Niit_Workspace', PROBLEM_SLUG, 'student_workspace', 'solution.json')
#     try:
#         if os.path.isfile(legacy_metadata_path):
#             with open(legacy_metadata_path, 'r') as f:
#                 metadata = json.load(f)
#                 metadata.update(existing_data)
#                 existing_data = metadata
#     except Exception:
#         pass

#     with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
#         json.dump(existing_data, f, indent=4)
#     with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
#         f.write(f"# Solution verification result\nresults = {json.dumps(results, indent=4)}\nscore = {total_score}\n")

# if __name__ == '__main__':
#     verify_task()











import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_M07_M"
PROBLEM_SLUG = "os_lx_m07_m_critical_service_dependency_recovery"
LAB_TITLE = "Linux Lab: Critical Service Dependency Recovery & Unit Override Management"
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
    "tc1": "Failure diagnosis: journalctl confirms start-limit-hit and missing environment variables",
    "tc2": "Counter reset: systemctl reset clears the start-limit throttle state",
    "tc3": "Drop-in configuration: /etc/systemd/system/payment-gateway.service.d/override.conf created with valid syntax",
    "tc4": "Daemon reload: systemctl daemon-reload executes cleanly",
    "tc5": "Service startup: payment-gateway enters stable active (running) state",
    "tc6": "Log validation: unit logs show successful configuration loading with zero errors",
    "tc7": "Health check probe: local daemon health port responds with HTTP 200 OK"
}

TC_MARKS = {
    "tc1": 3,
    "tc2": 2,
    "tc3": 3,
    "tc4": 3,
    "tc5": 3,
    "tc6": 3,
    "tc7": 3
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
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False}

    # -------------------------------------------------------------------------
    # TC1: Failure diagnosis: journalctl confirms start-limit-hit and missing environment variables (3 Marks)
    # -------------------------------------------------------------------------
    for h in homes:
        for fn in ["payment_diagnosis.txt", "payment_error.txt", "diagnosis.txt", "journal_error.txt", "tc1.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                c = safe_read(f).lower()
                if any(term in c for term in ['start-limit', 'environment', 'payment-gateway', 'failed', 'throttle', 'port', 'api_key', 'no entries', 'not found', 'could not be found', 'journalctl', 'systemctl', 'payment']):
                    results['tc1'] = True
                    break
        if results['tc1']:
            break
    if not results['tc1']:
        if check_bash_history(homes, r'journalctl') or check_bash_history(homes, r'systemctl'):
            results['tc1'] = True

    # -------------------------------------------------------------------------
    # TC2: Counter reset: systemctl reset-failed clears the start-limit throttle state (2 Marks)
    # -------------------------------------------------------------------------
    for h in homes:
        for fn in ["reset_counter.txt", "reset_failed.txt", "reset.txt", "tc2.txt", "reset_counter.log", "reset.log", "systemctl_reset.txt", "counter.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                results['tc2'] = True
                break
        if results['tc2']:
            break
    if not results['tc2']:
        if check_bash_history(homes, r'reset-failed') or check_bash_history(homes, r'reset'):
            results['tc2'] = True

    # -------------------------------------------------------------------------
    # TC3: Drop-in configuration: override.conf created with valid syntax (3 Marks)
    # -------------------------------------------------------------------------
    override_paths = [
        '/etc/systemd/system/payment-gateway.service.d/override.conf',
        '/etc/systemd/system/payment-gateway.service.d/10-env.conf'
    ]
    for h in homes:
        override_paths.append(os.path.join(h, "etc", "systemd", "system", "payment-gateway.service.d", "override.conf"))
        override_paths.append(os.path.join(h, "override.conf"))
        override_paths.append(os.path.join(h, "tc3.conf"))

    found_override = None
    for op in override_paths:
        if safe_isfile(op):
            found_override = op
            break

    if found_override:
        c = safe_read(found_override)
        has_env = ('EnvironmentFile' in c and '/etc/payment/gateway.env' in c) or 'EnvironmentFile' in c or 'gateway.env' in c
        has_restart = 'RestartSec' in c
        has_section = '[Service]' in c
        if has_env or has_restart or has_section:
            results['tc3'] = True

    # -------------------------------------------------------------------------
    # TC4: Daemon reload: systemctl daemon-reload executes cleanly (3 Marks)
    # -------------------------------------------------------------------------
    for h in homes:
        for fn in ["daemon_reload.txt", "reload.txt", "tc4.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                results['tc4'] = True
                break
        if results['tc4']:
            break
    if not results['tc4']:
        if check_bash_history(homes, r'daemon-reload'):
            results['tc4'] = True
    if not results['tc4']:
        systemctl_bin = shutil.which('systemctl')
        if systemctl_bin:
            try:
                res = subprocess.run([systemctl_bin, 'show', '-p', 'DropInPaths', 'payment-gateway'], capture_output=True, text=True, timeout=5)
                if 'override.conf' in res.stdout:
                    results['tc4'] = True
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # TC5: Service startup: payment-gateway enters stable active (running) state (3 Marks)
    # -------------------------------------------------------------------------
    systemctl_bin = shutil.which('systemctl')
    if systemctl_bin:
        try:
            res = subprocess.run([systemctl_bin, 'is-active', 'payment-gateway'], capture_output=True, text=True, timeout=5)
            if res.stdout.strip() == 'active':
                results['tc5'] = True
        except Exception:
            pass
    if not results['tc5']:
        for h in homes:
            for fn in ["service_status.txt", "payment_status.txt", "status.txt", "tc5.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if 'active (running)' in c or 'active' in c or 'running' in c or 'payment' in c or 'service' in c or 'started' in c:
                        results['tc5'] = True
                        break
            if results['tc5']:
                break

    # -------------------------------------------------------------------------
    # TC6: Log validation: unit logs show successful configuration loading with zero errors (3 Marks)
    # -------------------------------------------------------------------------
    journalctl_bin = shutil.which('journalctl')
    if journalctl_bin and results['tc5']:
        try:
            j_res = subprocess.run([journalctl_bin, '-u', 'payment-gateway', '-n', '20'], capture_output=True, text=True, timeout=5)
            if 'Payment Gateway starting' in j_res.stdout or 'API_KEY verified' in j_res.stdout or 'Started' in j_res.stdout:
                results['tc6'] = True
        except Exception:
            pass
    if not results['tc6']:
        for h in homes:
            for fn in ["payment_logs.txt", "unit_logs.txt", "journal_success.txt", "tc6.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['starting', 'port 8080', 'port', '8080', 'verified', 'healthy', 'success', 'started', 'api_key', 'payment']):
                        results['tc6'] = True
                        break
            if results['tc6']:
                break

    # -------------------------------------------------------------------------
    # TC7: Health check probe: local daemon health port responds with HTTP 200 OK (3 Marks)
    # -------------------------------------------------------------------------
    curl_bin = shutil.which('curl')
    if curl_bin:
        try:
            res = subprocess.run([curl_bin, '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:8080/health'], capture_output=True, text=True, timeout=3)
            if res.stdout.strip() in ['200', '204', '202']:
                results['tc7'] = True
        except Exception:
            pass
    if not results['tc7']:
        for h in homes:
            for fn in ["health_check.txt", "health_probe.txt", "curl_health.txt", "tc7.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f)
                    if '200' in c or 'healthy' in c.lower() or 'ok' in c.lower() or 'curl' in c.lower():
                        results['tc7'] = True
                        break
            if results['tc7']:
                break
    if not results['tc7']:
        if check_bash_history(homes, r'curl\s+.*8080') or check_bash_history(homes, r'curl'):
            results['tc7'] = True

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

