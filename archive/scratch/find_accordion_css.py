import os

def find_accordion():
    with open("styles.css", "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        if "accordion" in line.lower():
            print(f"Line {idx+1}: {line.strip()}")
            # Print a few lines after
            for i in range(1, 15):
                if idx + i < len(lines):
                    print(f"  +{i}: {lines[idx+i].strip()}")
            print("-" * 40)

if __name__ == '__main__':
    find_accordion()
