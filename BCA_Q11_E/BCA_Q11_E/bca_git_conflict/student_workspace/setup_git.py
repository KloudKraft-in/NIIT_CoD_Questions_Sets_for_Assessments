import subprocess
import os

def setup_git_repo():
    ws = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["git", "init"], cwd=ws, capture_output=True)
    subprocess.run(["git", "config", "user.name", "dev_bob"], cwd=ws, capture_output=True)
    subprocess.run(["git", "config", "user.email", "dev_bob@company.com"], cwd=ws, capture_output=True)
    
    auth_js = os.path.join(ws, "auth.js")
    with open(auth_js, "w", encoding="utf-8") as f:
        f.write("<<<<<<< HEAD\nconst AUTH_TIMEOUT = 3000;\n=======\nconst AUTH_TIMEOUT = 5000;\n>>>>>>> feature/login\n")
    subprocess.run(["git", "add", "auth.js"], cwd=ws, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit with merge conflict markers"], cwd=ws, capture_output=True)
    print("[SUCCESS] Git repository initialized with conflict markers!")

if __name__ == "__main__":
    setup_git_repo()
