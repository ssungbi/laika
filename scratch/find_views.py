import re

def find_views():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    views = re.findall(r'id=["\'](view-[a-zA-Z0-9_-]+)["\']', content)
    for v in set(views):
        print(f"Page view container ID: {v}")

if __name__ == '__main__':
    find_views()
