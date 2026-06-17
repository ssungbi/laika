import os

html_file = r'c:\Users\SB\Desktop\연습용\index.html'
css_file = r'c:\Users\SB\Desktop\연습용\styles.css'
js_file = r'c:\Users\SB\Desktop\연습용\script.js'

# --- 1. index.html ---
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

old_cta = '<div class="quick-start-card main-cta">'
new_cta = '<div class="quick-start-card main-cta" onclick="navigateTo(\'view-insurance-portal\');" style="cursor:pointer;">'
if old_cta in html_content:
    html_content = html_content.replace(old_cta, new_cta)

new_view = '''
        <!-- 4. Insurance Portal View -->
        <div id="view-insurance-portal" class="page-view hidden">
            <div class="content-wrapper">
                <div class="sub-header">
                    <button class="back-btn" onclick="navigateTo('view-main')">
                        <span class="material-icons-round">arrow_back</span>
                    </button>
                    <h2 class="sub-header-title">보험회사 전산실</h2>
                </div>
                
                <div class="disability-container">
                    <p class="disability-desc">각 보험회사의 청구 팩스, 등기우편 주소, 약관 및 청구양식을 확인하세요.</p>
                    
                    <div class="insurance-grid" id="insurance-list-container">
                        <!-- JS로 렌더링 -->
                    </div>
                </div>
            </div>
        </div>
'''
if 'id="view-insurance-portal"' not in html_content:
    html_content = html_content.replace('</main>', new_view + '\n        </main>')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)


# --- 2. styles.css ---
with open(css_file, 'r', encoding='utf-8') as f:
    css_content = f.read()

new_css = '''
/* Insurance Portal Styles */
.insurance-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 20px;
    margin-top: 16px;
}
.ins-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    display: flex;
    flex-direction: column;
}
.ins-header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
    border-bottom: 1px solid #f3f4f6;
    padding-bottom: 12px;
}
.ins-name {
    font-size: 18px;
    font-weight: 700;
    color: #111827;
}
.ins-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
}
.ins-info-row {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.ins-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 600;
}
.ins-value {
    font-size: 15px;
    color: #374151;
}
.ins-btn-small {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    color: #4b5563;
    cursor: pointer;
    font-weight: 600;
}
.ins-btn-small:hover {
    background: #e5e7eb;
}
.ins-address {
    display: block;
    margin-top: 8px;
    background: #f8fafc;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    color: #374151;
    border-left: 3px solid #3b82f6;
}
.ins-footer {
    display: flex;
    gap: 8px;
}
.ins-btn-outline {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 10px;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    color: #3b82f6;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s;
}
.ins-btn-outline:hover {
    background: #eff6ff;
}
.ins-btn-outline .material-icons-round {
    font-size: 18px;
}
'''

if 'Insurance Portal Styles' not in css_content:
    with open(css_file, 'a', encoding='utf-8') as f:
        f.write('\n' + new_css)

# --- 3. script.js ---
with open(js_file, 'r', encoding='utf-8') as f:
    js_content = f.read()

new_js = '''
// Insurance Portal Data & Logic
const insuranceCompanies = [
    {
        name: "삼성화재",
        fax: "0505-168-4114",
        address: "우)07995 서울특별시 양천구 목동동로 233-3, 14층 삼성화재 장기보험접수팀",
        termsUrl: "#",
        formUrl: "#"
    },
    {
        name: "현대해상",
        fax: "0507-774-6060",
        address: "우)07328 서울특별시 영등포구 국회대로 543, 7층 현대해상 장기손사지원부",
        termsUrl: "#",
        formUrl: "#"
    },
    {
        name: "DB손해보험",
        fax: "0505-181-4861",
        address: "우)54966 전북 전주시 완산구 서원로 99, DB손해보험 신사옥 3층 사고접수팀",
        termsUrl: "#",
        formUrl: "#"
    },
    {
        name: "KB손해보험",
        fax: "0505-136-6500",
        address: "우)04027 서울특별시 마포구 양화로 19, KB손해보험 합정빌딩 19층",
        termsUrl: "#",
        formUrl: "#"
    },
    {
        name: "메리츠화재",
        fax: "0505-021-3400",
        address: "우)14623 경기도 부천시 원미구 송내대로 80, 메리츠화재빌딩 6층 접수센터",
        termsUrl: "#",
        formUrl: "#"
    },
    {
        name: "한화손해보험",
        fax: "0502-779-1004",
        address: "우)07326 서울특별시 영등포구 여의대로 56, 한화증권빌딩 12층",
        termsUrl: "#",
        formUrl: "#"
    },
    {
        name: "롯데손해보험",
        fax: "0505-013-1004",
        address: "우)04528 서울특별시 중구 소월로 3, 롯데손해보험빌딩 10층 장기보상팀",
        termsUrl: "#",
        formUrl: "#"
    },
    {
        name: "흥국화재",
        fax: "0505-999-1688",
        address: "우)03184 서울특별시 종로구 새문안로 68, 흥국생명빌딩 11층",
        termsUrl: "#",
        formUrl: "#"
    }
];

function toggleAddress(btn) {
    const addressSpan = btn.nextElementSibling;
    if (addressSpan.classList.contains('hidden')) {
        addressSpan.classList.remove('hidden');
        btn.textContent = '주소닫기';
    } else {
        addressSpan.classList.add('hidden');
        btn.textContent = '주소보기';
    }
}

function renderInsuranceList() {
    const container = document.getElementById('insurance-list-container');
    if (!container) return;
    
    container.innerHTML = insuranceCompanies.map(ins => `
        <div class="ins-card">
            <div class="ins-header">
                <div class="ins-name">${ins.name}</div>
            </div>
            <div class="ins-body">
                <div class="ins-info-row">
                    <span class="ins-label">청구팩스</span>
                    <span class="ins-value">${ins.fax}</span>
                </div>
                <div class="ins-info-row">
                    <span class="ins-label">등기우편</span>
                    <div class="ins-value">
                        <button class="ins-btn-small" onclick="toggleAddress(this)">주소보기</button>
                        <span class="ins-address hidden">${ins.address}</span>
                    </div>
                </div>
            </div>
            <div class="ins-footer">
                <a href="${ins.termsUrl}" class="ins-btn-outline"><span class="material-icons-round">description</span> 약관</a>
                <a href="${ins.formUrl}" class="ins-btn-outline"><span class="material-icons-round">download</span> 청구양식</a>
            </div>
        </div>
    `).join('');
}

// init
document.addEventListener('DOMContentLoaded', () => {
    // try render if container exists
    setTimeout(renderInsuranceList, 100);
});
'''

if 'renderInsuranceList' not in js_content:
    with open(js_file, 'a', encoding='utf-8') as f:
        f.write('\n' + new_js)

print('All files patched successfully.')
