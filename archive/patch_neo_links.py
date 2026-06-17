import sys

with open('index.html', 'r', encoding='cp949', errors='ignore') as f:
    lines = f.readlines()

new_lines = []
skip_until = None

for i, line in enumerate(lines):
    # Fix the tc-pink card onclick
    if '<a href="#" class="tool-card-new tc-pink">' in line:
        line = line.replace('<a href="#" class="tool-card-new tc-pink">', '<a href="#" class="tool-card-new tc-pink" onclick="navigateTo(\'view-neo\'); return false;">')
    
    # Add sidebar link right after KCD sidebar link (line 71 ends the KCD link)
    new_lines.append(line)
    if '<span class="text">KCD 질병분류표</span>' in line or '<span class="text">KCD 질병분류' in line:
        # Check next line to see if it's </a>
        pass
    if '</a>' in line and ('KCD 질병분류' in lines[i-1]):
        # Inject the Neoplasm sidebar link
        neo_sidebar = '''                    <a href="#" class="nav-item" onclick="navigateTo('view-neo'); return false;">
                        <span class="nav-icon-box">신생물</span>
                        <span class="text">신생물 형태분류</span>
                    </a>\n'''
        if neo_sidebar not in ''.join(lines):
            new_lines.append(neo_sidebar)

with open('index.html', 'w', encoding='cp949') as f:
    f.writelines(new_lines)

print("index.html patched with correct navigation events.")
