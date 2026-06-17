import sys

# 1. Update index.html
html_path = r'c:\Users\SB\Desktop\연습용\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

target_html = """                                  <!-- Detail Tabs (Static Mockup) -->
                                  <div style="display: flex; border-bottom: 1px solid #cbd5e1; border-top: 1px solid #cbd5e1; background: #f8fafc; font-size: 14px;">
                                      <div style="padding: 12px; flex: 1; text-align: center; border-right: 1px solid #cbd5e1; font-weight: bold; color: #0f766e;">사고 상황</div>
                                      <div style="padding: 12px; flex: 1; text-align: center; border-right: 1px solid #cbd5e1; color: #64748b;">적용(비적용)</div>
                                      <div style="padding: 12px; flex: 1; text-align: center; color: #64748b;">기본과실 해설</div>
                                  </div>
                                  
                                  <div id="acc-detail-situation" style="padding: 16px; font-size: 14px; color: #475569; line-height: 1.6; min-height: 100px; background: #fff;">
                                      사고 상황 설명이 이곳에 표시됩니다.
                                  </div>"""

new_html = """                                  <!-- Detail Tabs -->
                                  <div style="display: flex; border-bottom: 1px solid #cbd5e1; border-top: 1px solid #cbd5e1; background: #f8fafc; font-size: 14px;">
                                      <button id="acc-tab-situation" onclick="switchAccidentDetailTab('situation')" style="padding: 12px; flex: 1; text-align: center; border: none; border-right: 1px solid #cbd5e1; font-weight: bold; color: #0f766e; background: #fff; cursor: pointer;">사고 상황</button>
                                      <button id="acc-tab-apply" onclick="switchAccidentDetailTab('apply')" style="padding: 12px; flex: 1; text-align: center; border: none; border-right: 1px solid #cbd5e1; color: #64748b; background: transparent; cursor: pointer;">적용(비적용)</button>
                                      <button id="acc-tab-explain" onclick="switchAccidentDetailTab('explain')" style="padding: 12px; flex: 1; text-align: center; border: none; color: #64748b; background: transparent; cursor: pointer;">기본과실 해설</button>
                                  </div>
                                  
                                  <div id="acc-detail-situation" style="padding: 16px; font-size: 14px; color: #475569; line-height: 1.6; min-height: 100px; background: #fff;">
                                      사고 상황 설명이 이곳에 표시됩니다.
                                  </div>"""

if target_html in html:
    html = html.replace(target_html, new_html)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed index.html tabs")
else:
    print("Target HTML not found. Trying regex.")
    import re
    html = re.sub(r'<!-- Detail Tabs \(Static Mockup\).*?</div>\s*</div>', new_html, html, flags=re.DOTALL)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed index.html tabs via regex")

# 2. Update script.js
js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Append switchAccidentDetailTab if it's missing
if 'function switchAccidentDetailTab' not in js:
    js += """
function switchAccidentDetailTab(tab) {
    const btnSituation = document.getElementById('acc-tab-situation');
    const btnApply = document.getElementById('acc-tab-apply');
    const btnExplain = document.getElementById('acc-tab-explain');
    const contentDiv = document.getElementById('acc-detail-situation');
    
    if(!btnSituation || !btnApply || !btnExplain) return;
    
    // Reset buttons
    btnSituation.style.fontWeight = 'normal'; btnSituation.style.color = '#64748b'; btnSituation.style.background = 'transparent';
    btnApply.style.fontWeight = 'normal'; btnApply.style.color = '#64748b'; btnApply.style.background = 'transparent';
    btnExplain.style.fontWeight = 'normal'; btnExplain.style.color = '#64748b'; btnExplain.style.background = 'transparent';
    
    let detail = window.currentAccidentDetail;
    let htmlContent = '내용이 없습니다.';
    
    if (tab === 'situation') {
        btnSituation.style.fontWeight = 'bold'; btnSituation.style.color = '#0f766e'; btnSituation.style.background = '#fff';
        htmlContent = detail && detail.tab_situation ? detail.tab_situation : (detail && detail.situation ? detail.situation : '사고 상황 내용이 없습니다.');
    } else if (tab === 'apply') {
        btnApply.style.fontWeight = 'bold'; btnApply.style.color = '#0f766e'; btnApply.style.background = '#fff';
        htmlContent = detail && detail.tab_apply ? detail.tab_apply : '적용 내용이 없습니다.';
    } else if (tab === 'explain') {
        btnExplain.style.fontWeight = 'bold'; btnExplain.style.color = '#0f766e'; btnExplain.style.background = '#fff';
        htmlContent = detail && detail.tab_explain ? detail.tab_explain : '해설 내용이 없습니다.';
    }
    
    contentDiv.innerHTML = htmlContent;
}
"""
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Appended switchAccidentDetailTab")
else:
    print("switchAccidentDetailTab already exists")
