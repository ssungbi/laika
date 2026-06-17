import sys
import re

html_file = r'c:\Users\SB\Desktop\연습용\index.html'
css_file = r'c:\Users\SB\Desktop\연습용\styles.css'
js_file = r'c:\Users\SB\Desktop\연습용\script.js'

# ==========================================
# 1. Update index.html
# ==========================================
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Add search bar inside disability-container of view-insurance-portal
search_bar_html = '''
                    <p class="disability-desc">각 보험회사의 청구 팩스, 등기우편 주소, 약관 및 청구양식을 확인하세요.</p>
                    
                    <div class="insurance-search-container">
                        <span class="material-icons-round search-icon">search</span>
                        <input type="text" id="ins-search-input" placeholder="보험사를 검색하세요 (초성 검색 가능, 예: ㅅㅅㅎㅈ)" onkeyup="filterInsurance()">
                    </div>
'''
# Replace the desc with desc + search bar
if 'id="ins-search-input"' not in html_content:
    html_content = html_content.replace(
        '<p class="disability-desc">각 보험회사의 청구 팩스, 등기우편 주소, 약관 및 청구양식을 확인하세요.</p>',
        search_bar_html
    )

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)


# ==========================================
# 2. Update styles.css
# ==========================================
with open(css_file, 'r', encoding='utf-8') as f:
    css_content = f.read()

new_css = '''
.insurance-search-container {
    position: relative;
    margin-bottom: 24px;
    max-width: 500px;
}
.insurance-search-container .search-icon {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #9ca3af;
    font-size: 20px;
}
#ins-search-input {
    width: 100%;
    padding: 14px 16px 14px 44px;
    font-size: 15px;
    border: 1px solid #d1d5db;
    border-radius: 12px;
    background: #fff;
    color: #111827;
    transition: all 0.2s;
    font-family: inherit;
}
#ins-search-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
.ins-address-visible {
    display: block;
    margin-top: 4px;
    background: #f8fafc;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    color: #374151;
    border-left: 3px solid #3b82f6;
    line-height: 1.4;
}
'''
if 'insurance-search-container' not in css_content:
    with open(css_file, 'a', encoding='utf-8') as f:
        f.write('\n' + new_css)


# ==========================================
# 3. Update script.js
# ==========================================
with open(js_file, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace the existing Insurance Portal Data & Logic
# We'll use regex to remove the old section if it exists, and append the new one.
start_marker = '// Insurance Portal Data & Logic'
if start_marker in js_content:
    js_content = js_content[:js_content.find(start_marker)]

new_js = '''// Insurance Portal Data & Logic
const CHO_HANGUL = [
  'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ',
  'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
  'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ',
  'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
];
const HANGUL_START_CHARCODE = 0xAC00;
const HANGUL_END_CHARCODE = 0xD7A3;

function getChosung(str) {
  let result = "";
  for (let i = 0; i < str.length; i++) {
    const code = str.charCodeAt(i);
    if (code >= HANGUL_START_CHARCODE && code <= HANGUL_END_CHARCODE) {
      const choIndex = Math.floor((code - HANGUL_START_CHARCODE) / 588);
      result += CHO_HANGUL[choIndex];
    } else {
      result += str.charAt(i); // 숫자, 영문 등 그대로
    }
  }
  return result;
}

const insuranceCompanies = [
    // --- 생명보험 (22개) ---
    { name: "삼성생명", fax: "0505-111-1111", address: "서울 서초구 서초대로74길 11 삼성생명", termsUrl: "#", formUrl: "#" },
    { name: "한화생명", fax: "0505-222-2222", address: "서울 영등포구 63로 50 한화생명", termsUrl: "#", formUrl: "#" },
    { name: "교보생명", fax: "0505-333-3333", address: "서울 종로구 종로 1 교보생명", termsUrl: "#", formUrl: "#" },
    { name: "신한라이프", fax: "0505-444-4444", address: "서울 중구 삼일대로 358 신한라이프", termsUrl: "#", formUrl: "#" },
    { name: "NH농협생명", fax: "0505-555-5555", address: "서울 서대문구 통일로 87 NH농협생명", termsUrl: "#", formUrl: "#" },
    { name: "미래에셋생명", fax: "0505-666-6666", address: "서울 영등포구 국제금융로 56 미래에셋생명", termsUrl: "#", formUrl: "#" },
    { name: "동양생명", fax: "0505-777-7777", address: "서울 종로구 청진동 동양생명", termsUrl: "#", formUrl: "#" },
    { name: "흥국생명", fax: "0505-888-8888", address: "서울 종로구 새문안로 68 흥국생명", termsUrl: "#", formUrl: "#" },
    { name: "DB생명", fax: "0505-999-9999", address: "서울 강남구 테헤란로 432 DB생명", termsUrl: "#", formUrl: "#" },
    { name: "KDB생명", fax: "0505-000-0001", address: "서울 용산구 한강대로 210 KDB생명", termsUrl: "#", formUrl: "#" },
    { name: "KB라이프생명", fax: "0505-000-0002", address: "서울 강남구 강남대로 298 KB라이프생명", termsUrl: "#", formUrl: "#" },
    { name: "ABL생명", fax: "0505-000-0003", address: "서울 영등포구 의사당대로 147 ABL생명", termsUrl: "#", formUrl: "#" },
    { name: "라이나생명", fax: "0505-000-0004", address: "서울 종로구 삼봉로 48 라이나생명", termsUrl: "#", formUrl: "#" },
    { name: "AIA생명", fax: "0505-000-0005", address: "서울 중구 통일로 2 AIA생명", termsUrl: "#", formUrl: "#" },
    { name: "메트라이프생명", fax: "0505-000-0006", address: "서울 강남구 테헤란로 316 메트라이프생명", termsUrl: "#", formUrl: "#" },
    { name: "처브라이프생명", fax: "0505-000-0007", address: "서울 종로구 종로 33 처브라이프생명", termsUrl: "#", formUrl: "#" },
    { name: "푸본현대생명", fax: "0505-000-0008", address: "서울 영등포구 여의나루로 50 푸본현대생명", termsUrl: "#", formUrl: "#" },
    { name: "DGB생명", fax: "0505-000-0009", address: "대구 북구 옥산로 111 DGB생명", termsUrl: "#", formUrl: "#" },
    { name: "하나생명", fax: "0505-000-0010", address: "서울 중구 을지로 66 하나생명", termsUrl: "#", formUrl: "#" },
    { name: "교보라이프플래닛", fax: "0505-000-0011", address: "서울 영등포구 국제금융로 10 교보라이프플래닛", termsUrl: "#", formUrl: "#" },
    { name: "BNP파리바카디프생명", fax: "0505-000-0012", address: "서울 중구 세종대로 93 BNP파리바카디프생명", termsUrl: "#", formUrl: "#" },
    { name: "IBK연금보험", fax: "0505-000-0013", address: "서울 중구 을지로 79 IBK연금보험", termsUrl: "#", formUrl: "#" },

    // --- 손해보험 (22개) ---
    { name: "삼성화재", fax: "0505-168-4114", address: "서울 양천구 목동동로 233-3 삼성화재", termsUrl: "#", formUrl: "#" },
    { name: "현대해상", fax: "0507-774-6060", address: "서울 영등포구 국회대로 543 현대해상", termsUrl: "#", formUrl: "#" },
    { name: "DB손해보험", fax: "0505-181-4861", address: "전북 전주시 완산구 서원로 99 DB손해보험", termsUrl: "#", formUrl: "#" },
    { name: "KB손해보험", fax: "0505-136-6500", address: "서울 마포구 양화로 19 KB손해보험", termsUrl: "#", formUrl: "#" },
    { name: "메리츠화재", fax: "0505-021-3400", address: "경기 부천시 원미구 송내대로 80 메리츠화재", termsUrl: "#", formUrl: "#" },
    { name: "한화손해보험", fax: "0502-779-1004", address: "서울 영등포구 여의대로 56 한화손해보험", termsUrl: "#", formUrl: "#" },
    { name: "롯데손해보험", fax: "0505-013-1004", address: "서울 중구 소월로 3 롯데손해보험", termsUrl: "#", formUrl: "#" },
    { name: "흥국화재", fax: "0505-999-1688", address: "서울 종로구 새문안로 68 흥국화재", termsUrl: "#", formUrl: "#" },
    { name: "MG손해보험", fax: "0505-000-1001", address: "서울 강남구 테헤란로 134 MG손해보험", termsUrl: "#", formUrl: "#" },
    { name: "NH농협손해보험", fax: "0505-000-1002", address: "서울 서대문구 충정로 60 NH농협손해보험", termsUrl: "#", formUrl: "#" },
    { name: "하나손해보험", fax: "0505-000-1003", address: "서울 종로구 창경궁로 117 하나손해보험", termsUrl: "#", formUrl: "#" },
    { name: "악사손해보험", fax: "0505-000-1004", address: "서울 용산구 한강대로 71 악사손해보험", termsUrl: "#", formUrl: "#" },
    { name: "에이아이지손해보험", fax: "0505-000-1005", address: "서울 영등포구 국제금융로 10 AIG손해보험", termsUrl: "#", formUrl: "#" },
    { name: "에이스손해보험", fax: "0505-000-1006", address: "서울 종로구 종로 33 에이스손해보험", termsUrl: "#", formUrl: "#" },
    { name: "캐롯손해보험", fax: "0505-000-1007", address: "서울 중구 을지로 100 캐롯손해보험", termsUrl: "#", formUrl: "#" },
    { name: "신한EZ손해보험", fax: "0505-000-1008", address: "서울 중구 남대문로 113 신한EZ손해보험", termsUrl: "#", formUrl: "#" },
    { name: "카카오페이손해보험", fax: "0505-000-1009", address: "경기 성남시 분당구 판교역로 166 카카오페이손해보험", termsUrl: "#", formUrl: "#" },
    { name: "SGI서울보증", fax: "0505-000-1010", address: "서울 종로구 김상옥로 29 SGI서울보증", termsUrl: "#", formUrl: "#" },
    { name: "코리안리", fax: "0505-000-1011", address: "서울 종로구 수송동 코리안리", termsUrl: "#", formUrl: "#" },
    { name: "신협공제", fax: "0505-000-1012", address: "대전 서구 둔산대로 117 신협공제", termsUrl: "#", formUrl: "#" },
    { name: "새마을금고공제", fax: "0505-000-1013", address: "서울 강남구 삼성로 93 새마을금고공제", termsUrl: "#", formUrl: "#" },
    { name: "우체국보험", fax: "0505-000-1014", address: "서울 종로구 종로 6 우체국보험", termsUrl: "#", formUrl: "#" }
];

// Pre-calculate chosung for performance
insuranceCompanies.forEach(ins => {
    ins.chosung = getChosung(ins.name);
});

function renderInsuranceList(list) {
    const container = document.getElementById('insurance-list-container');
    if (!container) return;
    
    container.innerHTML = list.map(ins => `
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
                    <span class="ins-address-visible">${ins.address}</span>
                </div>
            </div>
            <div class="ins-footer">
                <a href="${ins.termsUrl}" class="ins-btn-outline"><span class="material-icons-round">description</span> 약관</a>
                <a href="${ins.formUrl}" class="ins-btn-outline"><span class="material-icons-round">download</span> 청구양식</a>
            </div>
        </div>
    `).join('');
}

function filterInsurance() {
    const input = document.getElementById('ins-search-input').value.trim();
    if (!input) {
        renderInsuranceList(insuranceCompanies);
        return;
    }
    
    // Check if input contains only chosung or english/numbers
    const isChosungSearch = /^[ㄱ-ㅎa-zA-Z0-9\s]+$/.test(input);
    const lowerInput = input.toLowerCase();
    
    const filtered = insuranceCompanies.filter(ins => {
        if (isChosungSearch) {
            return ins.chosung.includes(input) || ins.name.toLowerCase().includes(lowerInput);
        } else {
            return ins.name.toLowerCase().includes(lowerInput);
        }
    });
    
    renderInsuranceList(filtered);
}

// init
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => renderInsuranceList(insuranceCompanies), 100);
});
'''

with open(js_file, 'w', encoding='utf-8') as f:
    f.write(js_content + '\n' + new_js)

print("Updates applied successfully.")
