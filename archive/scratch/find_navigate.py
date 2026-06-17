import os

def find_navigate():
    with open("script.js", "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "navigateTo" in line:
                print(f"Line {idx+1}: {line.strip()}")

if __name__ == '__main__':
    find_navigate()
