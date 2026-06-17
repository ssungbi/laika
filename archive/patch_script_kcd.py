import sys

# Read original script
with open('script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False

# We will inject the new KCD logic
new_kcd_logic = """
let KCD_DATA = [];
let currentKcdChapter = null;
let isKcdLoaded = false;

async function loadKcdData() {
    if (isKcdLoaded) return;
    try {
        const response = await fetch('kcd_data.json');
        if (!response.ok) throw new Error('Network response was not ok');
        KCD_DATA = await response.json();
        isKcdLoaded = true;
        initKcdView();
    } catch (error) {
        console.error('KCD 데이터를 로드하는데 실패했습니다:', error);
        document.getElementById('kcd-chapters-container').innerHTML = '<p>데이터를 로드하는데 실패했습니다.</p>';
    }
}

// Search helper (Chosung)
function getChosung2(str) {
    const cho = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
    let result = "";
    for(let i=0; i<str.length; i++) {
        const code = str.charCodeAt(i) - 44032;
        if(code > -1 && code < 11172) result += cho[Math.floor(code / 588)];
        else result += str.charAt(i);
    }
    return result;
}

function initKcdView() {
    const chaptersContainer = document.getElementById('kcd-chapters-container');
    if(!chaptersContainer) return;
    
    // Clear
    chaptersContainer.innerHTML = '';
    
    // Create 4x6 grid of chapter buttons
    KCD_DATA.forEach(chapter => {
        const btn = document.createElement('button');
        btn.className = 'tool-card-new tc-blue';
        btn.style.display = 'flex';
        btn.style.flexDirection = 'column';
        btn.style.alignItems = 'center';
        btn.style.justifyContent = 'center';
        btn.style.padding = '15px 10px';
        btn.style.border = '1px solid #cbd5e1';
        btn.style.borderRadius = '8px';
        btn.style.background = '#f8fafc';
        btn.style.cursor = 'pointer';
        btn.style.fontSize = '14px';
        btn.style.fontWeight = '600';
        btn.style.color = '#334155';
        btn.style.textAlign = 'center';
        btn.style.transition = 'all 0.2s';
        
        // On hover
        btn.onmouseover = () => { btn.style.background = '#eff6ff'; btn.style.borderColor = '#3b82f6'; };
        btn.onmouseout = () => { btn.style.background = '#f8fafc'; btn.style.borderColor = '#cbd5e1'; };
        
        let shortName = chapter.name;
        let codeRange = '';
        if(chapter.name && chapter.name.includes(' (')) {
            const parts = chapter.name.split(' (');
            shortName = parts[0];
            codeRange = parts[1].replace(')', '');
        }
        
        btn.innerHTML = `<span style="font-size: 15px; font-weight: 700; color: #2563eb; margin-bottom: 6px; letter-spacing: 0.5px; background: #e0e7ff; padding: 4px 8px; border-radius: 4px;">${codeRange}</span><span style="font-size: 13px; color: #475569; word-break: keep-all; line-height: 1.4;">${shortName}</span>`;
        btn.style.boxShadow = '0 2px 4px rgba(0,0,0,0.05)';
        
        btn.onclick = () => {
            // Remove active style from all
            Array.from(chaptersContainer.children).forEach(c => {
                c.style.background = '#f8fafc'; c.style.borderColor = '#cbd5e1';
                c.onmouseout = () => { c.style.background = '#f8fafc'; c.style.borderColor = '#cbd5e1'; };
            });
            // Set active style for this
            btn.style.background = '#eff6ff'; btn.style.borderColor = '#3b82f6';
            btn.onmouseout = () => { btn.style.background = '#eff6ff'; btn.style.borderColor = '#3b82f6'; };
            
            renderKcdTree(chapter.id || chapter.code || chapter.name);
        };
        chaptersContainer.appendChild(btn);
    });
}

function renderKcdTree(chapterId) {
    const treeContainer = document.getElementById('kcd-tree-container');
    treeContainer.style.display = 'block';
    treeContainer.innerHTML = '';
    
    const chapter = KCD_DATA.find(c => (c.id == chapterId) || (c.code == chapterId) || (c.name == chapterId));
    if(!chapter) return;
    
    // Extract code range and name
    let shortName = chapter.name;
    let codeRange = '';
    if(chapter.name && chapter.name.includes(' (')) {
        const parts = chapter.name.split(' (');
        shortName = parts[0];
        codeRange = parts[1].replace(')', '');
    }
    
    const title = document.createElement('h3');
    title.style.margin = '30px 0 20px 0';
    title.style.color = '#1e293b';
    title.style.borderBottom = '3px solid #3b82f6';
    title.style.paddingBottom = '10px';
    title.style.fontSize = '22px';
    title.style.display = 'flex';
    title.style.alignItems = 'center';
    title.style.gap = '12px';
    title.innerHTML = `<span style="background: #3b82f6; color: white; padding: 4px 12px; border-radius: 20px; font-size: 16px;">${codeRange}</span> ${shortName}`;
    treeContainer.appendChild(title);
    
    if(!chapter.children || chapter.children.length === 0) {
        treeContainer.innerHTML += '<p style="color:#64748b;">하위 항목이 없습니다.</p>';
        return;
    }
    
    chapter.children.forEach(c3 => {
        const item = createKcdAccordionNode(c3, 1);
        treeContainer.appendChild(item);
    });
    
    // Scroll to tree
    treeContainer.scrollIntoView({behavior: 'smooth', block: 'start'});
}

function createKcdAccordionNode(node, depth) {
    const wrapper = document.createElement('div');
    wrapper.className = 'accordion-item kcd-acc-item';
    wrapper.style.border = 'none';
    wrapper.style.borderBottom = '1px solid #e2e8f0';
    wrapper.style.marginBottom = '0';
    wrapper.style.borderRadius = '0';
    
    const header = document.createElement('button');
    header.className = 'accordion-header kcd-acc-header';
    header.style.display = 'flex';
    header.style.alignItems = 'center';
    header.style.justifyContent = 'space-between';
    header.style.width = '100%';
    header.style.padding = '12px 16px';
    header.style.border = 'none';
    header.style.textAlign = 'left';
    header.style.cursor = 'pointer';
    header.style.transition = 'background 0.2s';
    
    // Depth styling
    let paddingLeft = 16 + (depth - 1) * 24;
    header.style.paddingLeft = paddingLeft + 'px';
    
    if(depth === 1) {
        header.style.background = '#f8fafc'; // Very light gray/blue
        header.style.fontWeight = '700';
        header.style.color = '#0f172a';
    } else if (depth === 2) {
        header.style.background = '#ffffff';
        header.style.fontWeight = '600';
        header.style.color = '#334155';
    } else {
        header.style.background = '#ffffff';
        header.style.fontWeight = '400';
        header.style.color = '#475569';
    }
    
    // Hover effect
    header.onmouseover = () => { header.style.background = '#f1f5f9'; };
    header.onmouseout = () => { 
        if(!header.classList.contains('active')) {
            header.style.background = depth === 1 ? '#f8fafc' : '#ffffff'; 
        }
    };
    
    const titleSpan = document.createElement('span');
    titleSpan.style.flex = '1';
    
    const codeText = node.code ? `<strong style="color:#2563eb; display:inline-block; width:60px;">[${node.code}]</strong> ` : '';
    const engText = node.eng ? `<span style="font-size:12px; color:#94a3b8; margin-left:8px; font-weight:normal;">${node.eng}</span>` : '';
    titleSpan.innerHTML = `${codeText}${node.name} ${engText}`;
    
    const iconSpan = document.createElement('span');
    iconSpan.className = 'material-icons-round accordion-icon';
    iconSpan.innerText = 'expand_more';
    iconSpan.style.color = '#94a3b8';
    iconSpan.style.transition = 'transform 0.3s';
    
    header.appendChild(titleSpan);
    if(node.children && node.children.length > 0) {
        header.appendChild(iconSpan);
    } else {
        iconSpan.style.opacity = '0';
        header.appendChild(iconSpan);
    }
    
    const content = document.createElement('div');
    content.className = 'accordion-content';
    content.style.padding = '0';
    content.style.maxHeight = '0';
    content.style.overflow = 'hidden';
    content.style.transition = 'max-height 0.3s ease-out';
    content.style.background = '#ffffff';
    
    header.onclick = () => {
        if(!node.children || node.children.length === 0) return;
        
        const isOpen = header.classList.contains('active');
        if(isOpen) {
            header.classList.remove('active');
            header.style.background = depth === 1 ? '#f8fafc' : '#ffffff';
            content.style.maxHeight = '0';
            iconSpan.style.transform = 'rotate(0deg)';
        } else {
            header.classList.add('active');
            header.style.background = '#eff6ff';
            
            // If content is empty, render children first
            if(content.innerHTML === '') {
                node.children.forEach(child => {
                    content.appendChild(createKcdAccordionNode(child, depth + 1));
                });
            }
            content.style.maxHeight = content.scrollHeight + 5000 + "px"; // Hack for deeply nested
            iconSpan.style.transform = 'rotate(180deg)';
            
            // Adjust parent heights
            let parentContent = wrapper.closest('.accordion-content');
            while(parentContent) {
                parentContent.style.maxHeight = parseInt(parentContent.style.maxHeight || 0) + content.scrollHeight + 5000 + "px";
                parentContent = parentContent.parentElement.closest('.accordion-content');
            }
        }
    };
    
    wrapper.appendChild(header);
    wrapper.appendChild(content);
    return wrapper;
}

function filterKcd() {
    const q = document.getElementById('kcd-search-input').value.trim().toLowerCase();
    const qCho = getChosung2(q);
    const resultsContainer = document.getElementById('kcd-search-results');
    const treeContainer = document.getElementById('kcd-tree-container');
    const chaptersContainer = document.getElementById('kcd-chapters-container');
    
    if(q.length < 2) {
        resultsContainer.style.display = 'none';
        chaptersContainer.style.display = 'grid';
        treeContainer.style.display = 'block'; // Or none depending on state
        return;
    }
    
    chaptersContainer.style.display = 'none';
    treeContainer.style.display = 'none';
    resultsContainer.style.display = 'block';
    
    let matches = [];
    
    // Recursive search
    function searchNode(node, chapterName) {
        const code = (node.code || '').toLowerCase();
        const name = (node.name || '').toLowerCase();
        const eng = (node.eng || '').toLowerCase();
        
        if(code.includes(q) || name.includes(q) || getChosung2(name).includes(qCho) || eng.includes(q)) {
            matches.push({...node, chapterName});
        }
        
        if(node.children) {
            node.children.forEach(child => searchNode(child, chapterName));
        }
    }
    
    KCD_DATA.forEach(chapter => {
        if(chapter.children) {
            chapter.children.forEach(c3 => searchNode(c3, chapter.name));
        }
    });
    
    resultsContainer.innerHTML = `<h3 style="margin-bottom:15px; color:#1e293b; font-size:18px;">검색 결과 (${matches.length}건)</h3>`;
    if(matches.length === 0) {
        resultsContainer.innerHTML += '<p style="color:#64748b; padding:20px; text-align:center; background:#f8fafc; border-radius:8px;">검색 결과가 없습니다.</p>';
        return;
    }
    
    const limit = Math.min(matches.length, 100);
    
    const listWrapper = document.createElement('div');
    listWrapper.style.border = '1px solid #e2e8f0';
    listWrapper.style.borderRadius = '8px';
    listWrapper.style.overflow = 'hidden';
    
    for(let i=0; i<limit; i++) {
        const m = matches[i];
        const item = document.createElement('div');
        item.style.padding = '12px 16px';
        item.style.borderBottom = i === limit-1 ? 'none' : '1px solid #e2e8f0';
        item.style.background = i % 2 === 0 ? '#ffffff' : '#f8fafc';
        
        const codeText = m.code ? `<strong style="color:#2563eb; width:60px; display:inline-block;">[${m.code}]</strong>` : '';
        item.innerHTML = `
            <div style="font-size:12px; color:#64748b; margin-bottom:4px;">${m.chapterName}</div>
            <div>
                ${codeText}
                <span style="font-weight:600; color:#1e293b;">${m.name}</span>
                <span style="font-size:12px; color:#94a3b8; margin-left:8px;">${m.eng || ''}</span>
            </div>
        `;
        listWrapper.appendChild(item);
    }
    resultsContainer.appendChild(listWrapper);
    
    if(matches.length > 100) {
        const msg = document.createElement('div');
        msg.style.padding = '16px';
        msg.style.color = '#ef4444';
        msg.style.textAlign = 'center';
        msg.style.fontWeight = '500';
        msg.innerText = `결과가 너무 많습니다. 검색어를 더 구체적으로 입력하세요. (최대 100건 표시)`;
        resultsContainer.appendChild(msg);
    }
}
"""

in_kcd_data = False
in_old_kcd_logic = False
for line in lines:
    if line.startswith('const KCD_DATA = ['):
        in_kcd_data = True
        continue
    
    if in_kcd_data:
        if line.startswith('];'):
            in_kcd_data = False
            # Wait, directly after this was let currentKcdChapter = null; etc.
            # So we start skipping the old kcd logic here too.
            in_old_kcd_logic = True
            new_lines.append(new_kcd_logic)
        continue
        
    if in_old_kcd_logic:
        # Stop skipping if we hit the end of the file or another recognizable block
        # Actually, old KCD logic goes until the end of the file, except maybe DOMContentLoaded.
        # We replace EVERYTHING from KCD_DATA to the end.
        pass
    else:
        new_lines.append(line)

with open('script.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Patch applied.")
