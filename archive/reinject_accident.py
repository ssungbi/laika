import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

accident_logic = """
// --- Auto Accident Logic ---
let currentAccidentPath = [];
let accidentTree = null;
let accidentDetails = null;

function initAccidentView() {
    const navContainer = document.getElementById('accident-nav-container');
    const detailContainer = document.getElementById('accident-detail-container');
    
    if(!navContainer) return;
    
    if(window.ACCIDENT_DATA_ASYNC) {
        accidentTree = window.ACCIDENT_DATA_ASYNC.tree1;
        accidentDetails = window.ACCIDENT_DATA_ASYNC.details;
    }
    
    // Reset to top level
    currentAccidentPath = [];
    detailContainer.style.display = 'none';
    navContainer.style.display = 'block';
    
    renderAccidentLevel(accidentTree);
}

function renderAccidentLevel(nodes, parentName = '자동차와 자동차의 사고') {
    const navContainer = document.getElementById('accident-nav-container');
    const detailContainer = document.getElementById('accident-detail-container');
    
    navContainer.innerHTML = '';
    
    // Top Level Hardcode if current path is empty
    if(currentAccidentPath.length === 0) {
        navContainer.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 40px;">
                <button class="tool-card-new tc-blue" onclick="drillDownAccident('tree1', '자동차와 자동차의 사고')" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #fff; cursor: pointer; height: 200px;">
                    <img src="https://accident.knia.or.kr/images/main/banner_carvscar.png" style="max-height: 80px; margin-bottom: 20px;" alt="차대차">
                    <div style="font-size: 20px; font-weight: bold; color: #1e293b;">자동차와 자동차의 사고</div>
                    <div style="font-size: 14px; color: #64748b; margin-top: 8px;">(이륜차 포함)</div>
                </button>
                <button class="tool-card-new tc-green" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; cursor: not-allowed; height: 200px; opacity: 0.7;">
                    <img src="https://accident.knia.or.kr/images/main/banner_carvsman_off.png" style="max-height: 80px; margin-bottom: 20px;" alt="차대사람">
                    <div style="font-size: 20px; font-weight: bold; color: #64748b;">자동차와 보행자의 사고</div>
                    <div style="font-size: 14px; color: #94a3b8; margin-top: 8px;">(준비중)</div>
                </button>
                <button class="tool-card-new tc-purple" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; cursor: not-allowed; height: 200px; opacity: 0.7;">
                    <img src="https://accident.knia.or.kr/images/main/banner_carvsbicycle_off.png" style="max-height: 80px; margin-bottom: 20px;" alt="차대자전거">
                    <div style="font-size: 20px; font-weight: bold; color: #64748b;">자동차와 자전거의 사고</div>
                    <div style="font-size: 14px; color: #94a3b8; margin-top: 8px;">(준비중)</div>
                </button>
            </div>
        `;
        return;
    }
    
    // Breadcrumbs / Back button
    let headerHtml = `
        <div style="display: flex; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;">
            <button onclick="goBackAccident()" style="background: none; border: none; cursor: pointer; color: #287df3; display: flex; align-items: center; font-weight: bold; margin-right: 16px; padding: 8px;">
                <span class="material-icons-round" style="margin-right: 4px;">arrow_back</span> 이전으로
            </button>
            <div style="font-size: 18px; font-weight: bold; color: #334155;">
                ${parentName}
            </div>
        </div>
    `;
    
    let gridHtml = `<div style="display: flex; flex-direction: column; gap: 12px;">`;
    
    nodes.forEach((node, index) => {
        if(node.type === 'category') {
            gridHtml += `
                <button onclick="drillDownAccident(${index}, '${node.text}')" style="display:flex; justify-content: space-between; align-items:center; padding: 16px 24px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; color: #1e293b; text-align: left; transition: all 0.2s;" onmouseover="this.style.background='#e2e8f0'" onmouseout="this.style.background='#f8fafc'">
                    ${node.text}
                    <span class="material-icons-round" style="color: #94a3b8;">chevron_right</span>
                </button>
            `;
        } else if (node.type === 'chart') {
            gridHtml += `
                <button onclick="showAccidentChart('${node.chartNo}')" style="display:flex; align-items:center; padding: 16px 24px; background: #fff; border: 1px solid #cbd5e1; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 500; color: #3b82f6; text-align: left; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" onmouseover="this.style.borderColor='#3b82f6'; this.style.boxShadow='0 2px 4px rgba(59,130,246,0.2)'" onmouseout="this.style.borderColor='#cbd5e1'; this.style.boxShadow='0 1px 2px rgba(0,0,0,0.05)'">
                    <span style="display: inline-block; padding: 4px 12px; background: #3b82f6; color: white; border-radius: 12px; font-size: 13px; font-weight: bold; margin-right: 16px;">${node.chartNo}</span>
                    ${node.text}
                </button>
            `;
        }
    });
    
    gridHtml += `</div>`;
    navContainer.innerHTML = headerHtml + gridHtml;
}

function drillDownAccident(indexOrKey, name) {
    if(indexOrKey === 'tree1') {
        currentAccidentPath.push({nodes: accidentTree, name: name});
        renderAccidentLevel(accidentTree, name);
    } else {
        const currentNodeList = currentAccidentPath[currentAccidentPath.length - 1].nodes;
        const targetNode = currentNodeList[indexOrKey];
        if(targetNode && targetNode.children) {
            currentAccidentPath.push({nodes: targetNode.children, name: name});
            renderAccidentLevel(targetNode.children, name);
        }
    }
}

function goBackAccident() {
    if(currentAccidentPath.length > 1) {
        currentAccidentPath.pop();
        const prev = currentAccidentPath[currentAccidentPath.length - 1];
        renderAccidentLevel(prev.nodes, prev.name);
    } else {
        currentAccidentPath = [];
        renderAccidentLevel([]);
    }
}

let currentBaseRatioA = 0;
let currentBaseRatioB = 0;

function showAccidentChart(chartNo) {
    const navContainer = document.getElementById('accident-nav-container');
    const detailContainer = document.getElementById('accident-detail-container');
    
    navContainer.style.display = 'none';
    detailContainer.style.display = 'block';
    
    const detail = accidentDetails ? accidentDetails[chartNo] : null;
    if(!detail) {
        document.getElementById('acc-detail-situation').innerHTML = '상세 데이터를 불러올 수 없습니다. (' + chartNo + ')';
        return;
    }
    
    document.getElementById('acc-detail-chart-no').innerText = detail.chartNo || chartNo;
    
    if(detail.imageUrl) {
        document.getElementById('acc-detail-image').innerHTML = `<img src="${detail.imageUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;
    } else {
        document.getElementById('acc-detail-image').innerHTML = `<span style="color: #94a3b8;">도표 이미지가 없습니다.</span>`;
    }
    
    document.getElementById('acc-detail-situation').innerHTML = detail.situation || '상황 설명이 없습니다.';
    
    currentBaseRatioA = parseInt(detail.ratio_a) || 0;
    currentBaseRatioB = parseInt(detail.ratio_b) || 0;
    updateAccidentRatioUI(currentBaseRatioA, currentBaseRatioB);
    
    // Render Factors
    const factorsContainer = document.getElementById('acc-factors-container');
    factorsContainer.innerHTML = '';
    
    if(detail.factors && detail.factors.length > 0) {
        detail.factors.forEach((f, idx) => {
            const valAStr = f.val_a > 0 ? '+' + f.val_a : (f.val_a < 0 ? f.val_a : '0');
            const valBStr = f.val_b > 0 ? '+' + f.val_b : (f.val_b < 0 ? f.val_b : '0');
            const aColor = f.val_a !== 0 ? '#ef4444' : '#94a3b8';
            const bColor = f.val_b !== 0 ? '#f59e0b' : '#94a3b8';
            
            // Temporary fix for missing labels from scraper: fallback names
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
        factorsContainer.innerHTML = '<div style="padding: 20px; color: #94a3b8;">적용 가능한 가감요소가 없습니다.</div>';
    }
}

function recalculateAccidentRatio() {
    let finalA = currentBaseRatioA;
    let finalB = currentBaseRatioB;
    
    const checkboxes = document.querySelectorAll('.acc-factor-cb');
    checkboxes.forEach(cb => {
        if(cb.checked) {
            finalA += parseInt(cb.getAttribute('data-a')) || 0;
            finalB += parseInt(cb.getAttribute('data-b')) || 0;
        }
    });
    
    // Bounds check
    if(finalA < 0) finalA = 0;
    if(finalB < 0) finalB = 0;
    if(finalA > 100) { finalA = 100; finalB = 0; }
    if(finalB > 100) { finalB = 100; finalA = 0; }
    
    updateAccidentRatioUI(finalA, finalB);
}

function updateAccidentRatioUI(a, b) {
    document.getElementById('acc-ratio-a').innerText = a;
    document.getElementById('acc-ratio-b').innerText = b;
    document.getElementById('acc-bar-a').style.width = a + '%';
    document.getElementById('acc-bar-b').style.width = b + '%';
}
"""

if "function initAccidentView" not in content:
    with open(js_path, 'a', encoding='utf-8') as f:
        f.write("\n" + accident_logic + "\n")
    print("Injected accident logic into script.js")
else:
    print("Logic already exists.")

