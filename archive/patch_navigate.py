import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_str = "if (viewId === 'view-neo' && typeof loadNeoData === 'function') {"
insert_str = "    if (viewId === 'view-accident') {\n        if(typeof initAccidentView === 'function') initAccidentView();\n    }\n\n    "

if "view-accident" not in content[:content.find(target_str) + 200] and target_str in content:
    new_content = content.replace(target_str, insert_str + target_str)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched script.js navigateTo")
else:
    print("Already patched or target not found.")
