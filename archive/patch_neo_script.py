import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('function initNeoView()')
if start_idx == -1:
    print("Could not find initNeoView()")
    sys.exit(1)

# The new JS code for the neo view
new_neo_code = '''function initNeoView() {
    const container = document.getElementById('neo-tree-container');
    if (!container) return;
    container.innerHTML = '';
    
    // Add Header Row
    const headerRow = document.createElement('div');
    headerRow.style.display = 'grid';
    headerRow.style.gridTemplateColumns = '250px 1fr 1fr';
    headerRow.style.padding = '12px 16px';
    headerRow.style.borderTop = '2px solid #334155';
    headerRow.style.borderBottom = '1px solid #cbd5e1';
    headerRow.style.fontWeight = 'bold';
    headerRow.style.color = '#334155';
    headerRow.style.backgroundColor = '#f8fafc';
    headerRow.style.fontSize = '14px';
    
    headerRow.innerHTML = `
        <div>코드</div>
        <div>한글명</div>
        <div>영문명</div>
    `;
    container.appendChild(headerRow);
    
    // Create rows
    if (NEO_DATA && NEO_DATA.length > 0) {
        NEO_DATA.forEach(node => {
            renderNeoTableRow(node, container, 0);
        });
    }
}

function renderNeoTableRow(node, container, depth) {
    const hasChildren = node.children && node.children.length > 0;
    
    const row = document.createElement('div');
    row.style.display = 'grid';
    row.style.gridTemplateColumns = '250px 1fr 1fr';
    row.style.padding = '12px 16px';
    row.style.borderBottom = '1px solid #e2e8f0';
    row.style.alignItems = 'center';
    row.style.fontSize = '14px';
    row.style.cursor = hasChildren ? 'pointer' : 'default';
    
    if (depth > 0) {
        row.style.backgroundColor = '#ffffff';
    } else {
        row.style.backgroundColor = '#fcfcfc';
    }
    
    row.addEventListener('mouseenter', () => row.style.backgroundColor = '#f1f5f9');
    row.addEventListener('mouseleave', () => row.style.backgroundColor = depth > 0 ? '#ffffff' : '#fcfcfc');
    
    const codeCol = document.createElement('div');
    codeCol.style.display = 'flex';
    codeCol.style.alignItems = 'center';
    codeCol.style.paddingLeft = `${depth * 24}px`;
    
    const iconBtn = document.createElement('span');
    iconBtn.style.display = 'inline-flex';
    iconBtn.style.alignItems = 'center';
    iconBtn.style.justifyContent = 'center';
    iconBtn.style.width = '16px';
    iconBtn.style.height = '16px';
    iconBtn.style.marginRight = '8px';
    iconBtn.style.fontSize = '14px';
    iconBtn.style.color = 'white';
    iconBtn.style.backgroundColor = '#2563eb'; // Blue + button
    iconBtn.style.borderRadius = '2px';
    iconBtn.style.fontWeight = 'bold';
    
    if (hasChildren) {
        iconBtn.innerText = '+';
        codeCol.appendChild(iconBtn);
    } else {
        const dot = document.createElement('span');
        dot.style.display = 'inline-block';
        dot.style.width = '16px';
        dot.style.marginRight = '8px';
        codeCol.appendChild(dot);
    }
    
    const codeText = document.createElement('span');
    codeText.innerText = node.code || '';
    codeText.style.color = '#3b82f6'; // Light blue text for code
    codeText.style.fontWeight = '500';
    codeCol.appendChild(codeText);
    
    const nameCol = document.createElement('div');
    nameCol.innerText = node.name || '';
    nameCol.style.color = '#334155';
    
    const engCol = document.createElement('div');
    engCol.innerText = node.eng || '';
    engCol.style.color = '#94a3b8';
    
    row.appendChild(codeCol);
    row.appendChild(nameCol);
    row.appendChild(engCol);
    
    container.appendChild(row);
    
    if (hasChildren) {
        const childrenContainer = document.createElement('div');
        childrenContainer.style.display = 'none';
        container.appendChild(childrenContainer);
        
        node.children.forEach(child => {
            renderNeoTableRow(child, childrenContainer, depth + 1);
        });
        
        row.addEventListener('click', () => {
            if (childrenContainer.style.display === 'none') {
                childrenContainer.style.display = 'block';
                iconBtn.innerText = '-';
            } else {
                childrenContainer.style.display = 'none';
                iconBtn.innerText = '+';
            }
        });
    }
}

function filterNeo() {
    const q = document.getElementById('neo-search-input').value.trim().toLowerCase();
    const resultsContainer = document.getElementById('neo-search-results');
    const treeContainer = document.getElementById('neo-tree-container');
    
    if (q.length < 2) {
        resultsContainer.style.display = 'none';
        treeContainer.style.display = 'block';
        return;
    }
    
    treeContainer.style.display = 'none';
    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = '';
    
    let matches = [];
    
    function searchNode(node, rootName) {
        const code = (node.code || '').toLowerCase();
        const name = (node.name || '').toLowerCase();
        const eng = (node.eng || '').toLowerCase();
        
        if(code.includes(q) || name.includes(q) || eng.includes(q)) {
            matches.push({...node, rootName});
        }
        
        if(node.children) {
            node.children.forEach(child => searchNode(child, rootName));
        }
    }
    
    if (NEO_DATA) {
        NEO_DATA.forEach(root => searchNode(root, root.name));
    }
    
    if (matches.length === 0) {
        resultsContainer.innerHTML = '<p style="padding: 24px; text-align: center; color: #64748b;">검색 결과가 없습니다.</p>';
        return;
    }
    
    const headerRow = document.createElement('div');
    headerRow.style.display = 'grid';
    headerRow.style.gridTemplateColumns = '250px 1fr 1fr';
    headerRow.style.padding = '12px 16px';
    headerRow.style.borderTop = '2px solid #334155';
    headerRow.style.borderBottom = '1px solid #cbd5e1';
    headerRow.style.fontWeight = 'bold';
    headerRow.style.color = '#334155';
    headerRow.style.backgroundColor = '#f8fafc';
    headerRow.style.fontSize = '14px';
    headerRow.innerHTML = `<div>코드</div><div>한글명</div><div>영문명</div>`;
    resultsContainer.appendChild(headerRow);
    
    // limit matches to 100 for performance
    const maxMatches = Math.min(matches.length, 100);
    for(let i=0; i<maxMatches; i++) {
        // Render rows without children for search results
        renderNeoTableRow({...matches[i], children: []}, resultsContainer, 0);
    }
    
    if(matches.length > 100) {
        const moreDiv = document.createElement('div');
        moreDiv.style.padding = '16px';
        moreDiv.style.textAlign = 'center';
        moreDiv.style.color = '#94a3b8';
        moreDiv.style.fontSize = '14px';
        moreDiv.innerText = '... 결과가 너무 많습니다. 검색어를 더 상세히 입력해주세요 ...';
        resultsContainer.appendChild(moreDiv);
    }
}
'''

new_content = content[:start_idx] + new_neo_code

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Patched script.js successfully")
