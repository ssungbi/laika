import os

def check_tc_gray():
    with open("styles.css", "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if "tc-gray" in line:
            print(f"Line {idx+1}: {line.strip()}")
            for i in range(1, 10):
                if idx + i < len(lines):
                    print(f"  +{i}: {lines[idx+i].strip()}")
            print("-" * 40)

if __name__ == '__main__':
    check_tc_gray()
