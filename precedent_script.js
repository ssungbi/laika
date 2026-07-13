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

// 검색어 지우기 함수
function clearPrecedentSearch(type) {
    const input = document.getElementById(`${type}-search-input`);
    if (input) {
        input.value = '';
        filterPrecedents(type);
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
    
    renderPrecedents(type, results, query);
}

// 태그 클릭 검색 기능
function searchTag(type, tag) {
    const input = document.getElementById(`${type}-search-input`);
    if (input) {
        input.value = tag;
        filterPrecedents(type);
    }
}

// 텍스트 매칭 하이라이트 헬퍼
function highlightText(text, query) {
    if (!text || !query || query.trim() === '') return text;
    const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    try {
        const regex = new RegExp(`(${escapedQuery})(?![^<>]*>)`, 'gi');
        return text.replace(regex, '<mark style="background-color: #ffe066; color: inherit; font-weight: bold; padding: 0 2px; border-radius: 2px;">$1</mark>');
    } catch (e) {
        return text;
    }
}

// 리스트 렌더링 헬퍼
function buildListHtml(title, items, color, query) {
    if (!items || items.length === 0) return '';
    const listItems = Array.isArray(items) ? items : [items];
    const lis = listItems.map(i => {
        const highlighted = highlightText(i, query);
        return `<li style="margin-bottom: 6px;">${highlighted}</li>`;
    }).join('');
    return `
        <div style="margin-bottom: 18px;">
            <strong style="color: ${color}; display: block; margin-bottom: 6px; font-size: 15px;">${title}</strong>
            <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #475569; line-height: 1.6;">
                ${lis}
            </ul>
        </div>
    `;
}

function buildTextHtml(title, text, color, query) {
    if (!text) return '';
    const highlighted = highlightText(text.replace(/\\n/g, '<br>'), query);
    return `
        <div style="margin-bottom: 18px;">
            <strong style="color: ${color}; display: block; margin-bottom: 6px; font-size: 15px;">${title}</strong>
            <div style="margin-top: 5px; font-size: 14px; color: #475569; line-height: 1.6;">${highlighted}</div>
        </div>
    `;
}

// 렌더링 함수
function renderPrecedents(type, data, query = '') {
    const container = document.getElementById(`${type}-results-container`);
    if (!container) return;
    
    container.innerHTML = '';
    
    if (data.length === 0) {
        container.innerHTML = `
            <div style="padding: 60px 20px; text-align: center; color: #94a3b8; font-size: 15px;">
                <span class="material-icons-round" style="font-size: 48px; color: #cbd5e1; display: block; margin-bottom: 12px;">find_in_page</span>
                검색 결과가 없습니다. 다른 검색어를 입력해보세요.
            </div>
        `;
        return;
    }
    
    data.forEach(item => {
        const card = document.createElement('div');
        card.className = 'precedent-card';
        
        let tagsHtml = '';
        if (item.keywords && item.keywords.length > 0) {
            tagsHtml = '<div style="margin-top: 15px; display: flex; flex-wrap: wrap; gap: 6px;">' + 
                item.keywords.map(k => {
                    const highlightedTag = highlightText(k, query);
                    return `<span class="tag-badge" onclick="searchTag('${type}', '${k}')">#${highlightedTag}</span>`;
                }).join('') + 
                '</div>';
        }
        
        // 새 스키마 호환 처리
        const mainSummary = item.core_issue || item.summary || '내용 없음';
        const subInfo = [item.court, item.case_no, item.case_type].filter(Boolean).join(' | ');
        
        let consumerBadge = '';
        if (item.consumer_result) {
            let badgeBg = '#f1f5f9';
            let badgeColor = '#475569';
            if (item.consumer_result === '유리') { badgeBg = '#dcfce7'; badgeColor = '#166534'; }
            else if (item.consumer_result === '불리') { badgeBg = '#fee2e2'; badgeColor = '#991b1b'; }
            else if (item.consumer_result === '중립') { badgeBg = '#fef9c3'; badgeColor = '#854d0e'; }
            
            consumerBadge = `<span style="display: inline-block; margin-left: 8px; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; background-color: ${badgeBg}; color: ${badgeColor}; vertical-align: middle;">${item.consumer_result}</span>`;
        }
        
        const subInfoHtml = subInfo ? `<div style="display: flex; align-items: center; margin-bottom: 8px;"><div style="font-size: 13px; color: #e67e22; font-weight: 600;">[${highlightText(subInfo, query)}]</div>${consumerBadge}</div>` : '';
        
        // 디테일 영역 구성 (신/구 데이터 모두 대응)
        let detailsHtml = '';
        if (item.decision || item.rationale) {
            // 과거 데이터
            detailsHtml += buildTextHtml('결정/판결 내용', item.decision, '#2980b9', query);
            detailsHtml += buildTextHtml('주요 근거', item.rationale, '#27ae60', query);
        } else {
            // 신규 데이터
            detailsHtml += buildListHtml('✅ 인정 요건', item.acceptance_criteria, '#27ae60', query);
            detailsHtml += buildListHtml('❌ 배척 요건 또는 한계', item.rejection_criteria, '#e74c3c', query);
            detailsHtml += buildListHtml('📋 사실관계 요약', item.fact_summary, '#34495e', query);
            detailsHtml += buildListHtml('⚖️ 법원/금감원의 판단', item.court_decision, '#2980b9', query);
            detailsHtml += buildListHtml('💡 실무 적용 포인트', item.practical_points, '#8e44ad', query);
            detailsHtml += buildListHtml('🛡️ 보험사 예상 반론', item.expected_rebuttals, '#d35400', query);
            detailsHtml += buildListHtml('⚔️ 반박 논리', item.counter_logic, '#16a085', query);
        }

        const dateStr = item.date ? `<div style="font-size: 13px; color: #94a3b8; margin-bottom: 6px;">${item.date}</div>` : '';
        const titleStr = highlightText(item.title, query);
        const mainSummaryStr = highlightText(mainSummary, query);

        card.innerHTML = `
            ${dateStr}
            ${subInfoHtml}
            <h3>${titleStr}</h3>
            <div class="core-issue-box">
                <strong>핵심 쟁점:</strong> ${mainSummaryStr}
            </div>
            <div style="display: flex; gap: 10px;">
                <button class="btn-details-toggle" onclick="toggleDetails(this)">
                    상세보기 <span class="material-icons-round" style="font-size: 18px; vertical-align: middle;">expand_more</span>
                </button>
            </div>
            <div class="precedent-details" style="display: none;">
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
        btn.innerHTML = '접기 <span class="material-icons-round" style="font-size: 18px; vertical-align: middle;">expand_less</span>';
        btn.style.background = '#e2e8f0';
    } else {
        details.style.display = 'none';
        btn.innerHTML = '상세보기 <span class="material-icons-round" style="font-size: 18px; vertical-align: middle;">expand_more</span>';
        btn.style.background = '#f1f5f9';
    }
}

// DOM Load 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 혹시 script.js 등 다른 곳에서 navigateTo 호출로 렌더링이 안될 수 있으므로
    // 0.5초 딜레이 후 초기화 (페이지 로딩 훅)
    setTimeout(initPrecedents, 500);
});

async function syncObsidianData() {
    const btn = document.getElementById('sync-obsidian-btn');
    const icon = btn.querySelector('.sync-icon');
    
    // Add spinning animation style if not exists
    if (!document.getElementById('sync-spin-style')) {
        const style = document.createElement('style');
        style.id = 'sync-spin-style';
        style.innerHTML = `
            @keyframes spin { 100% { transform: rotate(360deg); } }
            .spinning { animation: spin 1s linear infinite; }
        `;
        document.head.appendChild(style);
    }
    
    // Set loading state
    icon.classList.add('spinning');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<span class="material-icons-round sync-icon spinning" style="font-size: 18px;">sync</span> 동기화 중...`;
    btn.disabled = true;

    try {
        const response = await fetch('http://localhost:3123/api/sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            alert(`동기화 성공! 총 ${result.count}개의 판례가 확인되었습니다.\n${result.changed ? '새로운 변경사항이 GitHub에 푸시되었습니다.' : '새로운 변경사항이 없습니다.'}`);
            sessionStorage.setItem('activeTab', 'view-precedent-court');
            window.location.reload(); // Reload to fetch the updated JS file
        } else {
            alert('동기화 실패: ' + (result.error || '알 수 없는 오류'));
        }
    } catch (e) {
        alert('서버 연결 실패: 로컬 동기화 서버(server.js)가 실행 중인지 확인해주세요.\n실행 방법: cmd에서 start_server.bat 실행');
        console.error(e);
    } finally {
        // Restore button state
        btn.innerHTML = originalText;
        btn.disabled = false;
        btn.querySelector('.sync-icon').classList.remove('spinning');
    }
}
