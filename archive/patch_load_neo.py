import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('function loadNeoData() {')
if start_idx == -1:
    print('Not found')
    sys.exit(1)

end_idx = content.find('function initNeoView()', start_idx)

new_func = '''function loadNeoData() {
    if (isNeoLoaded) return;
    
    const container = document.getElementById('neo-tree-container');
    if (container) {
        container.innerHTML = '<p style="text-align:center; padding:40px; color:#64748b; font-size:16px;">데이터를 로딩 중입니다. 잠시만 기다려주세요...</p>';
    }

    const script = document.createElement('script');
    script.src = 'neo_data_all.js?v=1';
    script.onload = () => {
        if (window.NEO_DATA_ALL_ASYNC) {
            window.NEO_DATA_ALL = window.NEO_DATA_ALL_ASYNC;
            const select = document.getElementById('neo-degree-select');
            const degree = select ? select.value : '08';
            NEO_DATA = window.NEO_DATA_ALL[degree] || [];
            isNeoLoaded = true;
            initNeoView();
        } else {
            if (container) container.innerHTML = '<p style="color:#ef4444;">데이터 로드 오류: NEO_DATA_ALL_ASYNC를 찾을 수 없습니다.</p>';
        }
    };
    script.onerror = () => {
        if (container) container.innerHTML = '<p style="color:#ef4444;">데이터 스크립트를 로드하는데 실패했습니다.</p>';
    };
    document.body.appendChild(script);
}

window.changeNeoDegree = function(degree) {
    if (!window.NEO_DATA_ALL) return;
    NEO_DATA = window.NEO_DATA_ALL[degree] || [];
    initNeoView();
    const searchInput = document.getElementById('neo-search-input');
    if (searchInput) searchInput.value = '';
    const resultsContainer = document.getElementById('neo-search-results');
    if (resultsContainer) resultsContainer.style.display = 'none';
    const treeContainer = document.getElementById('neo-tree-container');
    if (treeContainer) treeContainer.style.display = 'block';
};

'''

new_content = content[:start_idx] + new_func + content[end_idx:]

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Successfully patched script.js')
