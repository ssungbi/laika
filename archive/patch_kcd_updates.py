import sys

def patch_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Update placeholder
    old_placeholder = '질병명 또는 코드를 입력하세요 (초성 검색 가능, 예: A00, 콜레라, ㅋㄹㄹ)'
    new_placeholder = '질병명 또는 코드를 입력하세요 (예: A00, 콜레라)'
    html = html.replace(old_placeholder, new_placeholder)
    
    # 2. Update max-width specifically in the KCD section
    # Let's split by KCD section
    if 'id="view-kcd"' in html:
        parts = html.split('id="view-kcd"')
        if len(parts) == 2:
            # Replace max-width:800px to max-width:1100px in the second part
            parts[1] = parts[1].replace('max-width:800px;', 'max-width:1100px;', 1)
            html = 'id="view-kcd"'.join(parts)
            
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched index.html")

def patch_script():
    with open('script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # Replace the searchNode logic
    old_search = """function searchNode(node, chapterName) {
        const code = (node.code || '').toLowerCase();
        const name = (node.name || '').toLowerCase();
        const eng = (node.eng || '').toLowerCase();
        
        if(code.includes(q) || name.includes(q) || getChosung2(name).includes(qCho) || eng.includes(q)) {
            matches.push({...node, chapterName});
        }
        
        if(node.children) {
            node.children.forEach(child => searchNode(child, chapterName));
        }
    }"""
    
    new_search = """function searchNode(node, chapterName) {
        const code = (node.code || '').toLowerCase();
        const name = (node.name || '').toLowerCase();
        const eng = (node.eng || '').toLowerCase();
        
        if(code.includes(q) || name.includes(q) || eng.includes(q)) {
            matches.push({...node, chapterName});
        }
        
        if(node.children) {
            node.children.forEach(child => searchNode(child, chapterName));
        }
    }"""
    
    js = js.replace(old_search, new_search)
    
    # Remove qCho definition
    js = js.replace("const qCho = getChosung2(q);", "")
    
    # Also remove getChosung2 function completely if it exists
    # We can just leave it there in case it's used elsewhere, but user requested to remove chosung logic from search. 
    # That is handled by replacing `getChosung2(name).includes(qCho)` above.
    
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched script.js")

if __name__ == '__main__':
    patch_index()
    patch_script()
