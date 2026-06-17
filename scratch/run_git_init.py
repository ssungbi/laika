import subprocess
import os

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Failed with return code {result.returncode}")
        print(result.stderr)
    return result.returncode == 0

def main():
    git_path = r"C:\Program Files\Git\cmd\git.exe"
    if not os.path.exists(git_path):
        print(f"Git executable not found at {git_path}")
        return
        
    # 1. git init
    if not run_cmd([git_path, "init"]):
        return
        
    # 2. git add .
    if not run_cmd([git_path, "add", "."]):
        return
        
    # 3. git commit -m "Initialize project"
    if not run_cmd([git_path, "commit", "-m", "Initialize project"]):
        # It's possible name/email configuration is missing.
        # Let's try to set temporary config if it fails
        print("Configuring temporary user name and email...")
        run_cmd([git_path, "config", "user.name", "InsuranceCalculatorUser"])
        run_cmd([git_path, "config", "user.email", "calculator@example.com"])
        
        # Retry commit
        run_cmd([git_path, "commit", "-m", "Initialize project"])
        
    # 4. git branch -M main
    run_cmd([git_path, "branch", "-M", "main"])

if __name__ == '__main__':
    main()
