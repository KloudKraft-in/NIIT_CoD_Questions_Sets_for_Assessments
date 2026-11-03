import os
import shutil
import subprocess

def test_student_code(solution_path):
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(os.path.dirname(solution_path), "report.txt")
    
    # Target directory for the build (src/main/kotlin/GreetingFormatter.kt)
    build_dest = os.path.join(base_dir, "src", "main", "kotlin", "GreetingFormatter.kt")
    os.makedirs(os.path.dirname(build_dest), exist_ok=True)
    
    # 2. Preparation: Copy student code to the testable location
    shutil.copy(solution_path, build_dest)
    
    print("Running Tests for: Greeting Formatter (Basic Level)\n")
    report_lines = ["Running Tests for: Greeting Formatter (Basic Level)\n"]
    
    # 3. Execution: Run Gradle
    try:
        # Run gradle test
        result = subprocess.run(["gradle", "test"], capture_output=True, text=True, shell=True, cwd=base_dir)
        
        # 4. Parsing
        if result.returncode == 0:
            msg = "PASS TC1 [Greeting Formatter Output] (10/10)"
            total_score = 10.0
        else:
            msg = "FAIL TC1 [Greeting Formatter Output] (0/10) - Tests failed or Compilation Error"
            print("\n--- GRADLE STDOUT ---")
            print(result.stdout)
            print("\n--- GRADLE STDERR ---")
            print(result.stderr)
            total_score = 0.0
            
        print(msg)
        report_lines.append(msg)
        
        score_line = f"\nSCORE: {total_score}/10.0"
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
