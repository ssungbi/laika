import re

with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# We will replace showAccidentChart with a new implementation
start_idx = text.find('function showAccidentChart(chartNo) {')
end_idx = text.find('function recalculateAccidentRatio() {')

new_code = """function showAccidentChart(chartNo) {
    const navContainer = document.getElementById('accident-nav-container');
    const detailContainer = document.getElementById('accident-detail-container');
    
    navContainer.style.display = 'none';
    detailContainer.style.display = 'block';
    
    const detail = accidentDetails ? accidentDetails[chartNo] : null;
    if(!detail) {
        document.getElementById('acc-detail-situation').innerHTML = '데이터를 불러올 수 없습니다. (' + chartNo + ')';
        return;
    }
    
    document.getElementById('acc-detail-chart-no').innerText = detail.chartNo || chartNo;
    
    // Keep detail in window for tab switching
    window.currentAccidentDetail = detail;

    // Render case tabs if multiple cases exist
    const casesContainer = document.getElementById('acc-cases-container');
    const baseRatioLabel = document.getElementById('acc-base-ratio-label');
    if (detail.cases && detail.cases.length > 1) {
        casesContainer.style.display = 'flex';
        casesContainer.innerHTML = '';
        detail.cases.forEach((c, idx) => {
            const isSelected = idx === 0;
            const bg = isSelected ? '#fff' : '#f8fafc';
            const color = isSelected ? '#ef4444' : '#64748b';
            const border = isSelected ? 'border-top: 3px solid #ef4444; border-bottom: none;' : 'border-top: 3px solid transparent; border-bottom: 1px solid #e2e8f0;';
            casesContainer.innerHTML += `
                <button id="acc-case-tab-${idx}" onclick="switchAccidentCase(${idx})" style="padding: 12px 24px; font-weight: bold; font-size: 15px; cursor: pointer; border: none; border-right: 1px solid #e2e8f0; background: ${bg}; color: ${color}; ${border}">
                    ${c.label || '케이스 ' + (idx + 1)}
                </button>
            `;
        });
        baseRatioLabel.innerText = '기본과실';
    } else {
        casesContainer.style.display = 'none';
        baseRatioLabel.innerText = '기본과실';
    }

    // Default to case 0
    switchAccidentCase(0);
}

function switchAccidentCase(caseIdx) {
    const detail = window.currentAccidentDetail;
    if (!detail) return;
    
    // Update case tabs styling
    if (detail.cases && detail.cases.length > 1) {
        detail.cases.forEach((c, idx) => {
            const tab = document.getElementById(`acc-case-tab-${idx}`);
            if (tab) {
                if (idx === caseIdx) {
                    tab.style.background = '#fff';
                    tab.style.color = '#ef4444';
                    tab.style.borderTop = '3px solid #ef4444';
                    tab.style.borderBottom = 'none';
                } else {
                    tab.style.background = '#f8fafc';
                    tab.style.color = '#64748b';
                    tab.style.borderTop = '3px solid transparent';
                    tab.style.borderBottom = '1px solid #e2e8f0';
                }
            }
        });
        
        // Update labels
        const baseRatioLabel = document.getElementById('acc-base-ratio-label');
        if (baseRatioLabel) {
            baseRatioLabel.innerText = '기본과실' + (detail.cases[caseIdx].label || '');
        }
    }

    // Determine current case data
    let currentCase = detail; // fallback
    if (detail.cases && detail.cases.length > caseIdx) {
        currentCase = detail.cases[caseIdx];
    }
    
    // Video doesn't change per case, but keep logic in case it does
    if(detail.videoUrl) {
        document.getElementById('acc-detail-image').innerHTML = `
            <video width="100%" controls autoplay loop style="max-height: 100%; max-width: 100%; object-fit: contain; border-radius: 8px;">
                <source src="${detail.videoUrl}" type="video/mp4">
            </video>
        `;
    } else if(detail.imageUrl) {
        document.getElementById('acc-detail-image').innerHTML = `<img src="${detail.imageUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 8px;">`;
    } else {
        document.getElementById('acc-detail-image').innerHTML = `<span style="color: #94a3b8;">도표 이미지가 없습니다.</span>`;
    }
    
    // Update headers
    const headerA = document.getElementById('acc-header-car-a');
    if(headerA) headerA.innerText = currentCase.car_a_text || '자동차A';
    
    const headerB = document.getElementById('acc-header-car-b');
    if(headerB) headerB.innerText = currentCase.car_b_text || '자동차B';
    
    // Initialize bottom tabs
    switchAccidentDetailTab('situation');
    
    currentBaseRatioA = parseInt(currentCase.ratio_a) || 0;
    currentBaseRatioB = parseInt(currentCase.ratio_b) || 0;
    updateAccidentRatioUI(currentBaseRatioA, currentBaseRatioB);
    
    // Render Factors
    const factorsContainer = document.getElementById('acc-factors-container');
    factorsContainer.innerHTML = '';
    
    const factors = currentCase.factors || detail.factors;
    
    if(factors && factors.length > 0) {
        factors.forEach((f, idx) => {
            const valAStr = f.val_a > 0 ? '+' + f.val_a : (f.val_a < 0 ? f.val_a : '0');
            const valBStr = f.val_b > 0 ? '+' + f.val_b : (f.val_b < 0 ? f.val_b : '0');
            const aColor = f.val_a !== 0 ? '#ef4444' : '#94a3b8';
            const bColor = f.val_b !== 0 ? '#f59e0b' : '#94a3b8';
            
            const labelStr = f.label ? f.label : `가감요소 ${idx+1}`;
            
            factorsContainer.innerHTML += `
                <div style="display: flex; border-bottom: 1px solid #e2e8f0; align-items: center; transition: background 0.2s;" onmouseover="this.style.background='#f1f5f9'" onmouseout="this.style.background='transparent'">
                    <div style="flex: 2; padding: 12px; border-right: 1px solid #e2e8f0; display: flex; align-items: center; gap: 12px; text-align: left;">
                        <input type="checkbox" id="factor_${idx}" class="acc-factor-cb" data-a="${f.val_a}" data-b="${f.val_b}" onchange="recalculateAccidentRatio()" style="width: 18px; height: 18px; cursor: pointer;">
                        <label for="factor_${idx}" style="cursor: pointer; user-select: none; font-size: 14px; color: #334155;">${labelStr}</label>
                    </div>
                    <div style="flex: 1; padding: 12px; border-right: 1px solid #e2e8f0; color: ${aColor}; font-weight: bold; font-size: 15px;">
                        ${valAStr}
                    </div>
                    <div style="flex: 1; padding: 12px; color: ${bColor}; font-weight: bold; font-size: 15px;">
                        ${valBStr}
                    </div>
                </div>
            `;
        });
    } else {
        factorsContainer.innerHTML = '<div style="padding: 20px; color: #94a3b8;">가감요소가 없습니다.</div>';
    }
}

"""

new_text = text[:start_idx] + new_code + text[end_idx:]

with open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("script.js updated successfully.")
