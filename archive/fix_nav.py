import sys

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# The navigateTo function in script.js currently has:
# if (viewId === 'view-kcd' && typeof loadKcdData === 'function') {
#     loadKcdData();
# }

old_nav = "if (viewId === 'view-kcd' && typeof loadKcdData === 'function') {"
new_nav = "if (viewId === 'view-neo' && typeof loadNeoData === 'function') {\n        loadNeoData();\n    }\n    if (viewId === 'view-kcd' && typeof loadKcdData === 'function') {"

if old_nav in js and 'view-neo' not in js.split(old_nav)[0]:
    js = js.replace(old_nav, new_nav, 1)
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched navigateTo perfectly.")
else:
    print("Could not find the target string in script.js or it's already patched.")
    
# Let's verify if view-neo is really there
if 'loadNeoData();' in js:
    print("loadNeoData() is inside script.js!")
