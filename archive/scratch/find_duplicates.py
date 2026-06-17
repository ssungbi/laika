import os

def find_duplicates():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find all occurrences of "종 수술" or similar
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        if "종 수술" in line or "수술" in line:
            print(f"Line {idx+1}: {line.strip()}")

if __name__ == '__main__':
    find_duplicates()
