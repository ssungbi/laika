import subprocess
import os

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Result code {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    return result.returncode == 0

def main():
    git_path = r"C:\Program Files\Git\cmd\git.exe"
    if not os.path.exists(git_path):
        print(f"Git executable not found at {git_path}")
        return
        
    # 1. Untrack the archive folder (git rm -r --cached archive/)
    run_cmd([git_path, "rm", "-r", "--cached", "archive/"])
    
    # 2. Stage changes (git add .)
    run_cmd([git_path, "add", "."])
    
    # 3. Commit changes (git commit -m "Ignore and remove archive folder from index")
    run_cmd([git_path, "commit", "-m", "Ignore and remove archive folder from index"])

if __name__ == '__main__':
    main()
