import sys
import re

# 1. Update index.html
html_path = r'c:\Users\SB\Desktop\연습용\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<div style="font-size: 18px; font-weight: 800;">우회전</div>', '<div id="acc-header-car-a" style="font-size: 18px; font-weight: 800;">우회전</div>')
html = html.replace('<div style="font-size: 18px; font-weight: 800;">직진(녹색)</div>', '<div id="acc-header-car-b" style="font-size: 18px; font-weight: 800;">직진(녹색)</div>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")

# 2. Update script.js
js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# remove the bug causing tab overwrite
js = js.replace("document.getElementById('acc-detail-situation').innerHTML = detail.situation || '상황 설명이 없습니다.';\n", "")
# add header update logic
header_logic = """
    // Update headers
    const headerA = document.getElementById('acc-header-car-a');
    if(headerA) headerA.innerText = detail.car_a_text || '우회전';
    
    const headerB = document.getElementById('acc-header-car-b');
    if(headerB) headerB.innerText = detail.car_b_text || '직진(녹색)';
    
    // Initialize tabs
    switchAccidentDetailTab('situation');"""

js = js.replace("// Initialize tabs\n    switchAccidentDetailTab('situation');", header_logic)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated script.js")

# 3. Update build_accident_data.py
py_path = r'c:\Users\SB\Desktop\연습용\build_accident_data.py'
with open(py_path, 'r', encoding='utf-8') as f:
    py = f.read()

target_py = """    # Extract tabs
    tab_situation = soup.select_one('#caracdsittn')"""

new_py = """    # Extract headers
    a_con = soup.select_one('#case1 .cont_l .con')
    if a_con: detail['car_a_text'] = a_con.get_text(strip=True)
    b_con = soup.select_one('#case1 .cont_r .con')
    if b_con: detail['car_b_text'] = b_con.get_text(strip=True)

    # Extract tabs
    tab_situation = soup.select_one('#caracdsittn')"""

if target_py in py:
    py = py.replace(target_py, new_py)
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(py)
    print("Updated build_accident_data.py")
else:
    print("Failed to update build_accident_data.py")
