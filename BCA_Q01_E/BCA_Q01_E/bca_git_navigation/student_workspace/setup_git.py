import subprocess
import sys
import os

def setup_git_repo():
    ws = os.path.dirname(os.path.abspath(__file__))
    dot_git = os.path.join(ws, ".git")
    
    print("[SYSTEM] Initializing Git repository...")
    subprocess.run(["git", "init"], cwd=ws, capture_output=True)
    
    # Commit 1 by dev_bob
    subprocess.run(["git", "config", "user.name", "dev_bob"], cwd=ws, capture_output=True)
    subprocess.run(["git", "config", "user.email", "dev_bob@company.com"], cwd=ws, capture_output=True)
    
    app_js = os.path.join(ws, "app.js")
    with open(app_js, "w", encoding="utf-8") as f:
        f.write("// User registration baseline\nfunction signup(user) {\n  return true;\n}\n")
    
    subprocess.run(["git", "add", "app.js"], cwd=ws, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit: signup baseline"], cwd=ws, capture_output=True)
    
    # Commit 2 by dev_alice (Target Commit)
    subprocess.run(["git", "config", "user.name", "dev_alice"], cwd=ws, capture_output=True)
    subprocess.run(["git", "config", "user.email", "dev_alice@company.com"], cwd=ws, capture_output=True)
    
    with open(app_js, "w", encoding="utf-8") as f:
        f.write("// User registration logic\nfunction signup(user) {\n  if (!user.email || !user.password) return false;\n  return true;\n}\n")
    
    subprocess.run(["git", "add", "app.js"], cwd=ws, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Fix: modified signup validation rule"], cwd=ws, capture_output=True)
    
    print("[SUCCESS] Git repository initialized! You can now run git commands in your terminal.")

if __name__ == "__main__":
    setup_git_repo()
