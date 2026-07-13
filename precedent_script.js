// Fuse.js 인스턴스
let courtFuse, fssFuse;

// 초기화 함수
function initPrecedents() {
    const fuseOptions = {
        keys: [
            'title', 'summary', 'keywords', 'decision', 'rationale',
            'case_no', 'court', 'case_type', 'core_issue', 'fact_summary'
        ],
        threshold: 0.3,
        ignoreLocation: true
    };
    
    // court_precedents 와 fss_precedents 는 해당 _data.js 파일에서 로드됨
    if (typeof court_precedents !== 'undefined') {
        courtFuse = new Fuse(court_precedents, fuseOptions);
        renderPrecedents('court', court_precedents);
    }
    
    if (typeof fss_precedents !== 'undefined') {
        fssFuse = new Fuse(fss_precedents, fuseOptions);
        renderPrecedents('fss', fss_precedents);
    }
}

// 필터링 함수
function filterPrecedents(type) {
    const query = document.getElementById(`${type}-search-input`).value;
    let results = [];
    
    if (query.trim() === '') {
        results = type === 'court' ? court_precedents : fss_precedents;
    } else {
        const fuse = type === 'court' ? courtFuse : fssFuse;
        const searchResults = fuse.search(query);
        results = searchResults.map(res => res.item);
    }
    
    renderPrecedents(type, results);
}

// 리스트 렌더링 헬퍼
function buildListHtml(title, items, color) {
    if (!items || items.length === 0) return '';
    const listItems = Array.isArray(items) ? items : [items];
    const lis = listItems.map(i => `<li style="margin-bottom: 4px;">${i}</li>`).join('');
    return `
        <div style="margin-bottom: 15px;">
            <strong style="color: ${color}; display: block; margin-bottom: 6px;">${title}</strong>
            <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #555; line-height: 1.6;">
                ${lis}
            </ul>
        </div>
    `;
}

function buildTextHtml(title, text, color) {
    if (!text) return '';
    return `
        <div style="margin-bottom: 15px;">
            <strong style="color: ${color}; display: block; margin-bottom: 6px;">${title}</strong>
            <div style="margin-top: 5px; font-size: 14px; color: #555; line-height: 1.6;">${text.replace(/\\n/g, '<br>')}</div>
        </div>
    `;
}

// 렌더링 함수
function renderPrecedents(type, data) {
    const container = document.getElementById(`${type}-results-container`);
    if (!container) return;
    
    container.innerHTML = '';
    
    if (data.length === 0) {
        container.innerHTML = '<div style="padding: 40px; text-align: center; color: #7f8c8d;">검색 결과가 없습니다.</div>';
        return;
    }
    
    data.forEach(item => {
        const card = document.createElement('div');
        card.className = 'precedent-card';
        card.style.cssText = 'background: white; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee;';
        
        let tagsHtml = '';
        if (item.keywords && item.keywords.length > 0) {
            tagsHtml = '<div style="margin-top: 10px;">' + 
                item.keywords.map(k => `<span style="display: inline-block; background: #eef2f5; color: #34495e; padding: 4px 10px; border-radius: 20px; font-size: 13px; margin-right: 8px; margin-bottom: 8px;">#${k}</span>`).join('') + 
                '</div>';
        }
        
        // 새 스키마 호환 처리
        const mainSummary = item.core_issue || item.summary || '내용 없음';
        const subInfo = [item.court, item.case_no, item.case_type].filter(Boolean).join(' | ');
        const subInfoHtml = subInfo ? `<div style="font-size: 13px; color: #e67e22; margin-bottom: 8px; font-weight: 600;">[${subInfo}]</div>` : '';
        
        // 디테일 영역 구성 (신/구 데이터 모두 대응)
        let detailsHtml = '';
        if (item.decision || item.rationale) {
            // 과거 데이터
            detailsHtml += buildTextHtml('결정/판결 내용:', item.decision, '#2980b9');
            detailsHtml += buildTextHtml('주요 근거:', item.rationale, '#27ae60');
        } else {
            // 신규 데이터
            detailsHtml += buildListHtml('✅ 인정 요건', item.acceptance_criteria, '#27ae60');
            detailsHtml += buildListHtml('❌ 배척 요건 또는 한계', item.rejection_criteria, '#e74c3c');
            detailsHtml += buildListHtml('📋 사실관계 요약', item.fact_summary, '#34495e');
            detailsHtml += buildListHtml('⚖️ 법원/금감원의 판단', item.court_decision, '#2980b9');
            detailsHtml += buildListHtml('💡 실무 적용 포인트', item.practical_points, '#8e44ad');
            detailsHtml += buildListHtml('🛡️ 보험사 예상 반론', item.expected_rebuttals, '#d35400');
            detailsHtml += buildListHtml('⚔️ 반박 논리', item.counter_logic, '#16a085');
        }

        card.innerHTML = `
            <div style="font-size: 14px; color: #95a5a6; margin-bottom: 8px;">${item.date || ''}</div>
            ${subInfoHtml}
            <h3 style="margin: 0 0 15px 0; font-size: 18px; color: #2c3e50;">${item.title}</h3>
            <div style="font-size: 15px; color: #34495e; line-height: 1.6; margin-bottom: 15px; background: #f8f9fa; padding: 12px; border-left: 4px solid #3498db; border-radius: 4px;">
                <strong>핵심 쟁점:</strong> ${mainSummary}
            </div>
            <div style="display: flex; gap: 10px;">
                <button onclick="toggleDetails(this)" style="background: none; border: 1px solid #bdc3c7; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; color: #7f8c8d; transition: all 0.2s;">
                    상세보기 ▼
                </button>
            </div>
            <div class="precedent-details" style="display: none; margin-top: 20px; padding-top: 20px; border-top: 1px dashed #ecf0f1;">
                ${detailsHtml}
            </div>
            ${tagsHtml}
        `;
        container.appendChild(card);
    });
}

function toggleDetails(btn) {
    const details = btn.parentElement.nextElementSibling;
    if (details.style.display === 'none') {
        details.style.display = 'block';
        btn.innerText = '접기 ▲';
        btn.style.background = '#f8f9fa';
    } else {
        details.style.display = 'none';
        btn.innerText = '상세보기 ▼';
        btn.style.background = 'none';
    }
}

// DOM Load 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 혹시 script.js 등 다른 곳에서 navigateTo 될 때 렌더링이 안될 수 있으니
    // 0.5초 딜레이 후 초기화 (데이터 로딩 대기)
    setTimeout(initPrecedents, 500);
});
