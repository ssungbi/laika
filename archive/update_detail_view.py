import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update showAccidentChart
target = """    if(detail.imageUrl) {
        document.getElementById('acc-detail-image').innerHTML = `<img src="${detail.imageUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;
    } else {
        document.getElementById('acc-detail-image').innerHTML = `<span style="color: #94a3b8;">도표 이미지가 없습니다.</span>`;
    }"""

new_target = """    // Keep detail in window for tab switching
    window.currentAccidentDetail = detail;

    if(detail.videoUrl) {
        document.getElementById('acc-detail-image').innerHTML = `
            <video width="100%" controls autoplay loop style="max-height: 100%; max-width: 100%; object-fit: contain; border-radius: 8px;">
                <source src="${detail.videoUrl}" type="video/mp4">
            </video>
        `;
    } else if(detail.imageUrl) {
        document.getElementById('acc-detail-image').innerHTML = `<img src="${detail.imageUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 8px;">`;
    } else {
        document.getElementById('acc-detail-image').innerHTML = `<span style="color: #94a3b8;">도표 컨텐츠가 없습니다.</span>`;
    }
    
    // Initialize tabs
    switchAccidentDetailTab('situation');"""

if target in content:
    content = content.replace(target, new_target)
    print("Replaced showAccidentChart image logic")
else:
    print("Could not find showAccidentChart image logic")

# Update switchAccidentDetailTab
target2 = """function switchAccidentDetailTab(tab) {
    const tabs = document.querySelectorAll('.dt-tab');
    // We only want the tabs inside the accident detail view
    // A better way is to scope it to the container
    const container = document.getElementById('accident-detail-container');
    const tabBtns = container.querySelectorAll('.dt-tab');
    
    tabBtns.forEach(t => t.classList.remove('active'));
    
    if (tab === 'situation') tabBtns[0].classList.add('active');
    if (tab === 'apply') tabBtns[1].classList.add('active');
    if (tab === 'explain') tabBtns[2].classList.add('active');
}"""

new_target2 = """function switchAccidentDetailTab(tab) {
    const container = document.getElementById('accident-detail-container');
    const tabBtns = container.querySelectorAll('.dt-tab');
    const contentDiv = document.getElementById('acc-detail-tab-content');
    
    tabBtns.forEach(t => t.classList.remove('active'));
    
    let detail = window.currentAccidentDetail;
    if(!detail) return;
    
    let htmlContent = '내용이 없습니다.';
    
    if (tab === 'situation') {
        tabBtns[0].classList.add('active');
        htmlContent = detail.tab_situation || '사고 상황 내용이 없습니다.';
    }
    if (tab === 'apply') {
        tabBtns[1].classList.add('active');
        htmlContent = detail.tab_apply || '적용 내용이 없습니다.';
    }
    if (tab === 'explain') {
        tabBtns[2].classList.add('active');
        htmlContent = detail.tab_explain || '해설 내용이 없습니다.';
    }
    
    contentDiv.innerHTML = htmlContent;
}"""

if target2 in content:
    content = content.replace(target2, new_target2)
    print("Replaced switchAccidentDetailTab logic")
else:
    print("Could not find switchAccidentDetailTab logic")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
