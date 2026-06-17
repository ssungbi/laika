import sys

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_load_logic = """async function loadKcdData() {
    if (isKcdLoaded) return;
    try {
        const response = await fetch('kcd_data.json');
        if (!response.ok) throw new Error('Network response was not ok');
        KCD_DATA = await response.json();
        isKcdLoaded = true;
        initKcdView();
    } catch (error) {
        console.error('KCD 데이터를 로드하는데 실패했습니다:', error);
        document.getElementById('kcd-chapters-container').innerHTML = '<p>데이터를 로드하는데 실패했습니다.</p>';
    }
}"""

new_load_logic = """function loadKcdData() {
    if (isKcdLoaded) return;
    
    const chaptersContainer = document.getElementById('kcd-chapters-container');
    if (chaptersContainer) {
        chaptersContainer.innerHTML = '<p style="text-align:center; padding:40px; color:#64748b; font-size:16px;">데이터를 로딩 중입니다. 잠시만 기다려주세요...</p>';
    }

    const script = document.createElement('script');
    script.src = 'kcd_data.js';
    script.onload = () => {
        if (window.KCD_DATA_ASYNC) {
            KCD_DATA = window.KCD_DATA_ASYNC;
            isKcdLoaded = true;
            initKcdView();
        } else {
            if (chaptersContainer) chaptersContainer.innerHTML = '<p style="color:#ef4444;">데이터 로드 오류: KCD_DATA_ASYNC를 찾을 수 없습니다.</p>';
        }
    };
    script.onerror = () => {
        if (chaptersContainer) chaptersContainer.innerHTML = '<p style="color:#ef4444;">데이터 스크립트를 로드하는데 실패했습니다.</p>';
    };
    document.body.appendChild(script);
}"""

if old_load_logic in js:
    js = js.replace(old_load_logic, new_load_logic)
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched loadKcdData for JSONP.")
else:
    print("Could not find old_load_logic in script.js")
