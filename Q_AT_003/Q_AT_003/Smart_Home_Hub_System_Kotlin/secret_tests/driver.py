import os
import shutil
import subprocess
import re

def test_student_code(solution_path):
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(os.path.dirname(solution_path), "report.txt")
    
    # Target directory for the build (src/main/kotlin/Solution.kt)
    build_dest = os.path.join(base_dir, "src", "main", "kotlin", "Solution.kt")
    os.makedirs(os.path.dirname(build_dest), exist_ok=True)
    
    # 2. Preparation: Copy student code to the testable location
    shutil.copy(solution_path, build_dest)
    
    print("Running Tests for: Smart Home Hub (Intermediate LLD)\n")
    report_lines = ["Running Tests for: Smart Home Hub (Intermediate LLD)\n"]
    
    # 3. Execution: Run Gradle
    try:
        print("Warming up Gradle... (Initial run may take several minutes to download dependencies)\n")
        # Run gradle test (dynamically resolve based on OS and availability)
        if os.name == 'nt':
            local_gradle_c = r"C:\gradle-9.4.1\bin\gradle.bat"
            user_home = os.path.expanduser("~")
            local_gradle_user = os.path.join(user_home, "gradle-9.4.1", "bin", "gradle.bat")
            
            if os.path.exists(local_gradle_c):
                gradle_cmd = [local_gradle_c, "cleanTest", "test"]
            elif os.path.exists(local_gradle_user):
                gradle_cmd = [local_gradle_user, "cleanTest", "test"]
            else:
                # Try to download and install Gradle 9.4.1 in user home automatically
                try:
                    import urllib.request
                    import zipfile
                    
                    zip_path = os.path.join(user_home, "gradle-9.4.1-bin.zip")
                    dest_dir = os.path.join(user_home, "gradle-9.4.1")
                    
                    if not os.path.exists(dest_dir):
                        print(f"[SYSTEM] Local Gradle not found. Downloading Gradle 9.4.1 to {zip_path}...")
                        url = "https://services.gradle.org/distributions/gradle-9.4.1-bin.zip"
                        
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req) as response:
                            total_size = int(response.headers.get('content-length', 0))
                            block_size = 1024 * 64
                            downloaded = 0
                            with open(zip_path, 'wb') as out_file:
                                while True:
                                    chunk = response.read(block_size)
                                    if not chunk:
                                        break
                                    out_file.write(chunk)
                                    downloaded += len(chunk)
                                    if total_size > 0:
                                        percent = min(100, int(downloaded * 100 / total_size))
                                        print(f"\rDownloading Gradle: {percent}% completed", end="")
                        
                        print("\n[SYSTEM] Download finished. Extracting to user home...")
                        
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(user_home)
                            
                        if os.path.exists(zip_path):
                            os.remove(zip_path)
                            
                        print("[SYSTEM] Gradle extraction complete!")
                    
                    gradle_cmd = [local_gradle_user, "cleanTest", "test"]
                except Exception as ex:
                    print(f"[WARNING] Failed to auto-install Gradle: {ex}")
                    gradle_cmd = "gradle cleanTest test"
            use_shell = True
        else:
            gradle_cmd = ["gradle", "cleanTest", "test"]
            use_shell = False
            
        # Ensure JAVA_HOME is correctly set (not pointing to bin subfolder)
        env = os.environ.copy()
        if 'JAVA_HOME' in env:
            java_home = env['JAVA_HOME'].strip()
            if java_home.lower().endswith('bin') or java_home.lower().endswith('bin\\') or java_home.lower().endswith('bin/'):
                java_home = os.path.dirname(java_home.rstrip('\\/'))
                env['JAVA_HOME'] = java_home
            
        result = subprocess.run(gradle_cmd, capture_output=True, text=True, shell=use_shell, cwd=base_dir, env=env)
        
        # 4. Parsing (More granular parsing for 7 Test Cases)
        total_score = 0.0
        
        # Mapping markers from JUnit output
        results_text = result.stdout + result.stderr
        
        # DEBUG: If everything fails, print the output to see what's wrong
        if "PASSED" not in results_text:
            print("--- GRADLE DEBUG OUTPUT ---")
            print(results_text)
            print("--- END DEBUG OUTPUT ---")
        
        test_mapping = {
            "testAddDevice": ("TC2 [Device Registration Logic]", 1.0),
            "testToggleDevice": ("TC3 [State Toggle Logic]", 2.0),
            "testScheduleTimer": ("TC4 [Scheduling with Constraints]", 3.0),
            "testGetDeviceHistory": ("TC5 [Audit Trail Retrieval]", 1.0),
            "testTotalPowerConsumption": ("TC6 [Network Power Summation]", 1.0),
            "testTurnOffAllDevices": ("TC7 [Bulk Power Sweep]", 2.0)
        }
        
        for method, (tc_name, marks) in test_mapping.items():
            # Check if the method name appears in the "passed" list of Gradle output
            if f" > {method}() PASSED" in results_text:
                msg = f"PASS {tc_name} ({marks}/{marks})"
                total_score += marks
            else:
                msg = f"FAIL {tc_name} (0/{marks})"
            
            print(msg)
            report_lines.append(msg)
        
        score_line = f"\nTOTAL SCORE: {total_score}/10.0"
        print(score_line)
        report_lines.append(score_line)
        
        # 5. Output report
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
            
    except Exception as e:
        print(f"Error during evaluation: {e}")

if __name__ == "__main__":
    # Point to the student's solution.kt
    sol_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "student_workspace", "solution.kt")
    test_student_code(sol_file)
