# import os
# import sys
# import json

# def get_base_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# def run_tests():
#     import subprocess
#     base_path = get_base_path()
#     results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False}
#     # TC1: File fetcher.js exists
#     js_file = os.path.join(base_path, 'fetcher.js')
#     if os.path.exists(js_file):
#         results['tc1'] = True
#     else:
#         return results

#     try:
#         # Import method
#         sys.path.insert(0, base_path)
#         # We can run node to verify it exports fetchUrls and works
#         node_code = "const f = require('./fetcher'); console.log(typeof f.fetchUrls);"
#         process = subprocess.run(['node', '-e', node_code], cwd=base_path, capture_output=True, text=True)
#         if 'function' in process.stdout:
#             results['tc2'] = True

#         # Test output validation
#         test_run = "const f = require('./fetcher'); f.fetchUrls(['url1','url2']).then(r => { if (Array.isArray(r) && r.length === 2 && r.includes('Data from url1') && r.includes('Data from url2')) console.log('OK_JSON_VAL'); }).catch(e => {});"
#         p2 = subprocess.run(['node', '-e', test_run], cwd=base_path, capture_output=True, text=True)
#         if 'OK_JSON_VAL' in p2.stdout:
#             results['tc3'] = True

#         # Test execution duration (parallel should take ~100-150ms, sequential ~200ms)
#         perf_run = "const f = require('./fetcher'); const start = Date.now(); f.fetchUrls(['a','b','c']).then(() => console.log(Date.now() - start));"
#         p3 = subprocess.run(['node', '-e', perf_run], cwd=base_path, capture_output=True, text=True)
#         elapsed = int(p3.stdout.strip())
#         if elapsed < 180:
#             results['tc4'] = True

#         # Check Promise.all code text
#         with open(js_file, 'r') as f:
#             code = f.read()
#             if 'Promise.all' in code:
#                 results['tc5'] = True
#     except Exception:
#         pass
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
#             "tc1": "File fetcher.js exists in student workspace", "tc2": "Module compiles and exports fetchUrls method", "tc3": "Method fetchUrls correctly resolves array output data", "tc4": "Parallel execution reduces latency compared to sequential run", "tc5": "Code uses native Promise.all to achieve concurrency"
#         }
#         print("Running Tests for: Async/Await Parallel Processing Flow\n")
#         total_score = 0
#         for k, v in test_results.items():
#             tc_num = k[2:]
#             desc = TC_NAMES.get(k, '')
#             marks = 2
#             display_marks = int(marks) if marks % 1 == 0 else marks
#             if v:
#                 total_score += marks
#                 print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
#             else:
#                 print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")
#         display_score = int(total_score) if total_score % 1 == 0 else total_score
#         display_max = int(10) if 10 % 1 == 0 else 10
#         print(f"\nSCORE: {display_score}/{display_max}")



import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    import re
    base_path = get_base_path()
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False}
    # TC1: File fetcher.js exists
    js_file = os.path.join(base_path, 'fetcher.js')
    if os.path.exists(js_file):
        results['tc1'] = True
    else:
        return results

    try:
        # Import method
        sys.path.insert(0, base_path)
        # We can run node to verify it exports fetchUrls and works
        node_code = "const f = require('./fetcher'); console.log(typeof f.fetchUrls);"
        process = subprocess.run(['node', '-e', node_code], cwd=base_path, capture_output=True, text=True)
        if 'function' in process.stdout:
            results['tc2'] = True

        # Test output validation
        test_run = "const f = require('./fetcher'); f.fetchUrls(['url1','url2']).then(r => { if (Array.isArray(r) && r.length === 2 && r.includes('Data from url1') && r.includes('Data from url2')) console.log('OK_JSON_VAL'); }).catch(e => {});"
        p2 = subprocess.run(['node', '-e', test_run], cwd=base_path, capture_output=True, text=True)
        if 'OK_JSON_VAL' in p2.stdout:
            results['tc3'] = True

        # Test execution duration (parallel should take ~100-150ms, sequential ~200ms)
        perf_run = "const f = require('./fetcher'); const start = Date.now(); f.fetchUrls(['a','b','c']).then(() => console.log(Date.now() - start));"
        p3 = subprocess.run(['node', '-e', perf_run], cwd=base_path, capture_output=True, text=True)
        elapsed = int(p3.stdout.strip())
        if elapsed < 180:
            results['tc4'] = True

        # Check Promise.all code text
        with open(js_file, 'r') as f:
            code = f.read()
            clean_c = re.sub(r'//.*', '', code)
            clean_c = re.sub(r'/\*.*?\*/', '', clean_c, flags=re.DOTALL)
            if 'Promise.all' in clean_c:
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
            "tc1": "File fetcher.js exists in student workspace", "tc2": "Module compiles and exports fetchUrls method", "tc3": "Method fetchUrls correctly resolves array output data", "tc4": "Parallel execution reduces latency compared to sequential run", "tc5": "Code uses native Promise.all to achieve concurrency"
        }
        print("Running Tests for: Async/Await Parallel Processing Flow\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 2
            display_marks = int(marks) if marks % 1 == 0 else marks
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")
        display_score = int(total_score) if total_score % 1 == 0 else total_score
        display_max = int(10) if 10 % 1 == 0 else 10
        print(f"\nSCORE: {display_score}/{display_max}")
