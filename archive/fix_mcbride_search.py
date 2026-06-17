import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """        // If user is typing in Wizard mode, automatically switch to List mode
        switchMcBrideMode('list');
        
        if (!query) {
            resultsContainer.style.display = 'none';
            listContainer.style.display = 'block';
            return;
        }
        
        resultsContainer.style.display = 'block';
        listContainer.style.display = 'none';"""

new_target = """        if (!query) {
            switchMcBrideTab('list');
            return;
        }
        
        switchMcBrideTab('search');"""

if target in content:
    content = content.replace(target, new_target)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed setupMcBrideSearch in script.js")
else:
    print("Target not found")
