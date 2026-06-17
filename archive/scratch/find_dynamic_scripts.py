import re

def search_dynamic_js():
    with open("script.js", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Search for anything matching .js in double or single quotes
    matches = re.findall(r'[\'"]([a-zA-Z0-9_]+\.js[^\'\"]*)[\'"]', content)
    for m in set(matches):
        print(f"Dynamically loaded or referenced script: {m}")

if __name__ == '__main__':
    search_dynamic_js()
