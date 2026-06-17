import re

def find_script_src():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    scripts = re.findall(r'<script\s+src=["\']([^"\']+)["\']', content)
    for src in scripts:
        print(f"Loaded script: {src}")

if __name__ == '__main__':
    find_script_src()
