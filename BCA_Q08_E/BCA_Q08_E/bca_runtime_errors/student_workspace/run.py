import subprocess
import sys
import os

def ensure_git_repo():
    ws = os.path.dirname(os.path.abspath(__file__))
    res = subprocess.run(["git", "log", "-n", "1"], cwd=ws, capture_output=True, text=True)
    if res.returncode != 0 or "fatal" in res.stderr.lower():
        print("[SYSTEM] Initializing Git repository and commit history...")
        subprocess.run(["git", "init"], cwd=ws, capture_output=True)
        
        # Commit 1 by dev_bob
        subprocess.run(["git", "config", "user.name", "dev_bob"], cwd=ws, capture_output=True)
        subprocess.run(["git", "config", "user.email", "dev_bob@company.com"], cwd=ws, capture_output=True)
        app_js = os.path.join(ws, "app.js")
        if not os.path.exists(app_js):
            with open(app_js, "w", encoding="utf-8") as f:
                f.write("// User registration baseline\nfunction signup(user) {\n  return true;\n}\n")
        subprocess.run(["git", "add", "."], cwd=ws, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit: signup baseline"], cwd=ws, capture_output=True)
        
        # Commit 2 by dev_alice (Target Commit)
        subprocess.run(["git", "config", "user.name", "dev_alice"], cwd=ws, capture_output=True)
        subprocess.run(["git", "config", "user.email", "dev_alice@company.com"], cwd=ws, capture_output=True)
        if os.path.exists(app_js):
            with open(app_js, "w", encoding="utf-8") as f:
                f.write("// User registration logic\nfunction signup(user) {\n  if (!user.email || !user.password) return false;\n  return true;\n}\n")
        subprocess.run(["git", "add", "."], cwd=ws, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Fix: modified signup validation rule"], cwd=ws, capture_output=True)
        print("[SYSTEM] Git repository initialized successfully!")

def main():
    ensure_git_repo()
    print("[SYSTEM] Running local tests...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    if not os.path.exists(driver_path):
        print(f"[ERROR] Driver not found at: {driver_path}")
        sys.exit(1)
    
    result = subprocess.run([sys.executable, driver_path], capture_output=False, text=True)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()