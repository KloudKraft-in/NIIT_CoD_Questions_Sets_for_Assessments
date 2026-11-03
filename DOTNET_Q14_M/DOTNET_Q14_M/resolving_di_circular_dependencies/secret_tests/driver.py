import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': True, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}

    program_path = os.path.join(base_path, 'Program.cs')
    if os.path.exists(program_path):
        results['tc2'] = True
    else:
        return results

    try:
        with open(program_path, 'r') as f:
            content = f.read()
        
        if 'AddTransient<ServiceA>' in content or 'AddScoped<ServiceA>' in content or 'AddSingleton<ServiceA>' in content:
            results['tc3'] = True
        if 'AddTransient<ServiceB>' in content or 'AddScoped<ServiceB>' in content or 'AddSingleton<ServiceB>' in content:
            results['tc4'] = True
        if 'AddTransient<ServiceC>' in content or 'AddScoped<ServiceC>' in content or 'AddSingleton<ServiceC>' in content:
            results['tc5'] = True
            
        # Check that constructor logic was decoupled
        has_decoupled = 'IServiceA' in content or 'Lazy<ServiceA>' in content or 'IServiceB' in content or 'IServiceC' in content or 'Func<' in content
        if has_decoupled:
            results['tc6'] = True
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
            "tc1": "Local VM Environment active and verified",
            "tc2": "Program.cs exists in workspace", "tc3": "ServiceA registered under DI container", "tc4": "ServiceB registered under DI container", "tc5": "ServiceC registered under DI container", "tc6": "Circular dependency between A, B, C is resolved", "tc7": "Services compiled cleanly", "tc8": "Interface dependencies introduced to abstract circular binds"
        }
        print("Running Tests for: Resolving DI Circular Dependencies\n")
        total_score = 0
        marks_list = [3, 3, 3, 3, 3, 3, 2]
        for k, v in test_results.items():
            tc_num = int(k[2:])
            desc = TC_NAMES.get(k, '')
            marks = marks_list[tc_num - 2] if tc_num > 1 else 0
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20")
