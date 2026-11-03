import subprocess
import sys
import os

def ensure_git_setup():
    ws = os.path.dirname(os.path.abspath(__file__))
    setup_script = os.path.join(ws, "setup_git.py")
    if os.path.exists(setup_script):
        subprocess.run([sys.executable, setup_script], cwd=ws, capture_output=True)
    else:
        auth_js = os.path.join(ws, "auth.js")
        if not os.path.exists(auth_js):
            with open(auth_js, "w", encoding="utf-8") as f:
                f.write("<<<<<<< HEAD\nconst AUTH_TIMEOUT = 3000;\n=======\nconst AUTH_TIMEOUT = 5000;\n>>>>>>> feature/login\n")

def main():
    ensure_git_setup()
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
