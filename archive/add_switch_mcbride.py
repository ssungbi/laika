import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """
function switchMcBrideTab(tab) {
    const btnSearch = document.getElementById('mcbride-tab-search');
    const btnList = document.getElementById('mcbride-tab-list');
    const containerSearch = document.getElementById('mcbride-search-results');
    const containerList = document.getElementById('mcbride-list-container');
    
    if(!btnSearch || !btnList) return;
    
    if (tab === 'search') {
        btnSearch.style.background = '#2563eb';
        btnSearch.style.color = '#fff';
        btnList.style.background = '#e2e8f0';
        btnList.style.color = '#475569';
        if(containerSearch) containerSearch.style.display = 'block';
        if(containerList) containerList.style.display = 'none';
    } else {
        btnSearch.style.background = '#e2e8f0';
        btnSearch.style.color = '#475569';
        btnList.style.background = '#2563eb';
        btnList.style.color = '#fff';
        if(containerSearch) containerSearch.style.display = 'none';
        if(containerList) containerList.style.display = 'block';
    }
}
"""

if 'function switchMcBrideTab' not in content:
    with open(js_path, 'a', encoding='utf-8') as f:
        f.write(new_func)
    print("Appended switchMcBrideTab to script.js")
else:
    print("Already exists")
