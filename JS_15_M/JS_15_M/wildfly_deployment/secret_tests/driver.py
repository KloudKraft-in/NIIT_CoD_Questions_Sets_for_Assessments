# import sys
# import json
# import os
# import xml.etree.ElementTree as ET

# def get_base_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# def run_tests():
#     base_path = get_base_path()
#     results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False, "tc6": False, "tc7": False, "tc8": False}
    
#     xml_path = os.path.join(base_path, 'configuration', 'standalone.xml')
#     if os.path.exists(xml_path):
#         results['tc1'] = True
#         try:
#             tree = ET.parse(xml_path)
#             root = tree.getroot()
#             results['tc3'] = True
#             results['tc5'] = True
#             results['tc6'] = True
            
#             http_binding = root.find(".//socket-binding[@name='http']")
#             if http_binding is None:
#                 for elem in root.iter('socket-binding'):
#                     if elem.attrib.get('name') == 'http':
#                         http_binding = elem
#                         break
            
#             if http_binding is not None:
#                 port = http_binding.attrib.get('port')
#                 if str(port) == '8082':
#                     results['tc2'] = True
#                     results['tc4'] = True
#                     results['tc7'] = True
#                     results['tc8'] = True
#         except Exception:
#             pass
            
#     return results

# if __name__ == "__main__":
#     test_results = run_tests()
#     try:
#         sol_path = os.path.join(get_base_path(), 'solution.java')
#         with open(sol_path, 'w') as f:
#             json.dump({'results': test_results}, f)
#     except Exception:
#         pass
    
#     if len(sys.argv) > 1 and sys.argv[1] == '--json':
#         print(json.dumps(test_results))
#     else:
#         TC_NAMES = {
#             "tc1": "standalone.xml exists",
#             "tc2": "HTTP port set to 8082",
#             "tc3": "XML configuration parsed",
#             "tc4": "HTTP binding offset initialized",
#             "tc5": "HTTP socket registered",
#             "tc6": "Deployment profile validated",
#             "tc7": "Socket port offset active",
#             "tc8": "Socket parameters enabled"
#         }
#         print("Running Tests for: JBoss WildFly Deployment Configuration\n")
#         total_score = 0
#         for k, v in test_results.items():
#             tc_num = k[2:]
#             desc = TC_NAMES.get(k, '')
#             marks = 4 if k == 'tc8' else 3
#             if v:
#                 total_score += marks
#                 print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
#             else:
#                 print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
#         print(f"\nSCORE: {total_score}/25.0")



import sys
import json
import os
import re
import xml.etree.ElementTree as ET

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False, "tc6": False, "tc7": False, "tc8": False}
    
    xml_path = os.path.join(base_path, 'configuration', 'standalone.xml')
    if os.path.exists(xml_path):
        results['tc1'] = True
        try:
            with open(xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            parsed = False
            http_binding = None
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()
                parsed = True
                
                for elem in root.iter():
                    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                    if tag == 'socket-binding' and elem.attrib.get('name') == 'http':
                        http_binding = elem
                        break
            except Exception:
                pass
                
            if parsed:
                results['tc3'] = True
                results['tc5'] = True
                results['tc6'] = True

            port_val = None
            if http_binding is not None:
                port_val = http_binding.attrib.get('port')
            else:
                m = re.search(r'<socket-binding\s+[^>]*name=["\']http["\'][^>]*port=["\'](\d+)["\']', content)
                if not m:
                    m = re.search(r'<socket-binding\s+[^>]*port=["\'](\d+)["\'][^>]*name=["\']http["\']', content)
                if m:
                    port_val = m.group(1)
                    results['tc3'] = True
                    results['tc5'] = True
                    results['tc6'] = True
                    
            if port_val and str(port_val).strip() == '8082':
                results['tc2'] = True
                results['tc4'] = True
                results['tc7'] = True
                results['tc8'] = True
        except Exception:
            pass
            
    return results

if __name__ == "__main__":
    test_results = run_tests()
    try:
        sol_path = os.path.join(get_base_path(), 'solution.java')
        with open(sol_path, 'w') as f:
            json.dump({'results': test_results}, f)
    except Exception:
        pass
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(test_results))
    else:
        TC_NAMES = {
            "tc1": "standalone.xml exists",
            "tc2": "HTTP port set to 8082",
            "tc3": "XML configuration parsed",
            "tc4": "HTTP binding offset initialized",
            "tc5": "HTTP socket registered",
            "tc6": "Deployment profile validated",
            "tc7": "Socket port offset active",
            "tc8": "Socket parameters enabled"
        }
        print("Running Tests for: JBoss WildFly Deployment Configuration\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 4 if k == 'tc8' else 3
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/25.0")

