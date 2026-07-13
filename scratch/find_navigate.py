with open("script.js", "r", encoding="utf-8") as f:
    lines = f.readlines()
for idx, line in enumerate(lines):
    if "window.navigateTo" in line or "function navigateTo" in line:
        print(f"Line {idx+1}: {line.strip()}")
        for i in range(1, 40):
            if idx+i < len(lines):
                print(f"  +{i}: {lines[idx+i].strip()}")
        break
