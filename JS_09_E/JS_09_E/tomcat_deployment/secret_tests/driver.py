import sys
import json
import os
import xml.etree.ElementTree as ET

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False}
    
    xml_path = os.path.join(base_path, 'conf', 'tomcat-users.xml')
    if os.path.exists(xml_path):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            results['tc1'] = True
            
            roles = [r.attrib.get('rolename') for r in root.findall('role')]
            if 'manager-gui' in roles:
                results['tc2'] = True
                
            user = root.find(".//user[@username='admin']")
            if user is not None:
                results['tc3'] = True
                if user.attrib.get('password') == 'secrettomcat':
                    results['tc4'] = True
                user_roles = [r.strip() for r in user.attrib.get('roles', '').split(',')]
                if 'manager-gui' in user_roles:
                    results['tc5'] = True
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
            "tc1": "tomcat-users.xml is valid XML",
            "tc2": "manager-gui role is defined",
            "tc3": "admin user is defined",
            "tc4": "admin password is correct",
            "tc5": "admin has manager-gui role"
        }
        print("Running Tests for: Tomcat Standalone App Server Deployment\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if v:
                total_score += 2
                print(f"PASS TC{tc_num} [{desc}] (2/2)")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/2)")
        print(f"\nSCORE: {total_score}/10.0")
