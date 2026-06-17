import os

def find_text():
    with open("index.html", "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if "동시감정" in line:
            print(f"Line {idx+1}: {line.strip()}")
            for i in range(1, 10):
                if idx + i < len(lines):
                    print(f"  +{i}: {lines[idx+i].strip()}")
            print("-" * 40)

if __name__ == '__main__':
    find_text()
