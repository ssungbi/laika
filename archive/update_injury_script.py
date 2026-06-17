import os

script_path = r"C:\Users\SB\Desktop\연습용\script.js"

with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace navigateTo
old_nav = """    if (viewId === 'view-kcd' && typeof loadKcdData === 'function') {
        loadKcdData();
    }
}"""
new_nav = """    if (viewId === 'view-kcd' && typeof loadKcdData === 'function') {
        loadKcdData();
    }
    if (viewId === 'view-injury-class' && typeof renderInjuryData === 'function') {
        renderInjuryData();
    }
}"""

content = content.replace(old_nav, new_nav)

# Append functions
new_funcs = """

let injuryRendered = false;

function renderInjuryData() {
    if (injuryRendered || typeof injuryData === 'undefined') return;
    
    // 1. 부상급수별 렌더링
    const viewClass = document.getElementById('injury-view-class');
    if (viewClass) {
        let classHtml = '';
        injuryData.classes.forEach((gradeItem, index) => {
            let listHtml = '';
            gradeItem.items.forEach(item => {
                listHtml += `
                    <li style="padding: 12px; border-bottom: 1px solid #f1f5f9;">
                        <div class="dis-desc" style="font-size: 15px; color: #334155; line-height: 1.5;">
                            <span style="font-weight:bold; color:#2563eb; margin-right:8px; display:inline-block; min-width:60px;">[${item.part}]</span>
                            ${item.desc}
                        </div>
                    </li>
                `;
            });
            
            classHtml += `
                <div class="accordion-item injury-acc-class" id="injury-acc-class-${index}">
                    <div class="accordion-header" onclick="document.getElementById('injury-acc-class-${index}').classList.toggle('open')">
                        <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
                            <span style="font-weight:bold; font-size:16px;">${gradeItem.grade}</span>
                            <span style="color:#ef4444; font-size:14px; margin-right:12px;">한도: <span style="font-weight:bold;">${gradeItem.amount}</span></span>
                        </div>
                        <span class="material-icons-round">expand_more</span>
                    </div>
                    <div class="accordion-body" style="padding:0;">
                        <ul class="disability-list" style="list-style:none; padding:0; margin:0;">
                            ${listHtml}
                        </ul>
                    </div>
                </div>
            `;
        });
        viewClass.innerHTML = classHtml;
    }

    // 2. 신체부위별 렌더링
    const viewPart = document.getElementById('injury-view-part');
    if (viewPart) {
        let partHtml = '';
        injuryData.parts.forEach((partItem, index) => {
            let listHtml = '';
            partItem.items.forEach(item => {
                listHtml += `
                    <li style="padding: 12px; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center;">
                        <div class="dis-desc" style="font-size: 15px; color: #334155; line-height: 1.5; flex: 1;">${item.desc}</div>
                        <div class="dis-rate" style="font-weight:700; color:#ef4444; margin-left: 16px; white-space: nowrap;">${item.grade}</div>
                    </li>
                `;
            });
            
            partHtml += `
                <div class="accordion-item injury-acc-part" id="injury-acc-part-${index}">
                    <div class="accordion-header" onclick="document.getElementById('injury-acc-part-${index}').classList.toggle('open')">
                        <span style="font-weight:bold; font-size:16px;">${partItem.part}</span>
                        <span class="material-icons-round">expand_more</span>
                    </div>
                    <div class="accordion-body" style="padding:0;">
                        <ul class="disability-list" style="list-style:none; padding:0; margin:0;">
                            ${listHtml}
                        </ul>
                    </div>
                </div>
            `;
        });
        viewPart.innerHTML = partHtml;
    }

    // 3. 영역별 세부지침 렌더링
    const viewGuide = document.getElementById('injury-view-guide');
    if (viewGuide) {
        let guideHtml = '';
        injuryData.guidelines.forEach((guideItem, index) => {
            let listHtml = '';
            guideItem.subcategories.forEach(sub => {
                let contentText = sub.content.replace(/\\n/g, '<br>');
                listHtml += `
                    <div style="margin-bottom:20px; background:#f8fafc; padding:16px; border-radius:8px;">
                        <div style="font-weight:bold; font-size:15px; color:#0f766e; margin-bottom:8px;">● ${sub.title}</div>
                        <div style="font-size:14px; color:#475569; line-height:1.6; padding-left:12px; border-left:3px solid #cbd5e1;">${contentText}</div>
                    </div>
                `;
            });
            
            guideHtml += `
                <div class="accordion-item injury-acc-guide" id="injury-acc-guide-${index}">
                    <div class="accordion-header" onclick="document.getElementById('injury-acc-guide-${index}').classList.toggle('open')">
                        <span style="font-weight:bold; font-size:16px;">▢ ${guideItem.category}</span>
                        <span class="material-icons-round">expand_more</span>
                    </div>
                    <div class="accordion-body" style="padding: 20px;">
                        ${listHtml}
                    </div>
                </div>
            `;
        });
        viewGuide.innerHTML = guideHtml;
    }
    
    injuryRendered = true;
}

function filterInjury() {
    const keyword = document.getElementById('injury-search-input').value.toLowerCase().trim();
    
    const filterGroup = (selector) => {
        const items = document.querySelectorAll(selector);
        items.forEach(acc => {
            // 본문 텍스트 검색
            const text = acc.textContent.toLowerCase();
            if (text.includes(keyword)) {
                acc.style.display = 'block';
                if(keyword) acc.classList.add('open');
                else acc.classList.remove('open');
                
                // 만약 키워드가 있다면 리스트 아이템 하이라이팅 처리 (선택사항)
                if(keyword) {
                    const lis = acc.querySelectorAll('li, .dis-desc, > div > div');
                    let foundAny = false;
                    lis.forEach(li => {
                        if (li.textContent.toLowerCase().includes(keyword)) {
                            // 강조 표시
                            li.style.background = '#fef08a'; // yellow-200
                            foundAny = true;
                        } else {
                            li.style.background = 'transparent';
                        }
                    });
                } else {
                    const lis = acc.querySelectorAll('li, .dis-desc, > div > div');
                    lis.forEach(li => li.style.background = 'transparent');
                }
            } else {
                acc.style.display = 'none';
            }
        });
    };

    filterGroup('.injury-acc-class');
    filterGroup('.injury-acc-part');
    filterGroup('.injury-acc-guide');
}
"""

if "function renderInjuryData" not in content:
    content += new_funcs

with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated script.js successfully")
