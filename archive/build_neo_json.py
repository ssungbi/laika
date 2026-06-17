import urllib.request, urllib.parse, json
import time
import os

url = 'https://www.koicd.kr/kcd/neo.list.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://www.koicd.kr/kcd/neo.do',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.koicd.kr',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def fetch_children(upper_cl_code):
    data = urllib.parse.urlencode({'upper_cl_code': upper_cl_code, 'degree': '08'}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('list', [])
    except Exception as e:
        print(f"Error fetching {upper_cl_code}: {e}")
        return []

def clean_html_tags(text):
    import re
    if not text:
        return ""
    # Remove HTML tags (the server API adds some tags occasionally, though we do it locally for highlighting, let's be safe)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def build_tree(upper_code, level=1):
    items = fetch_children(upper_code)
    # print(f"Fetched {len(items)} items for {upper_code}")
    
    tree = []
    for item in items:
        # Avoid infinite recursion just in case
        if item.get('cl_code') == upper_code:
            continue
            
        node = {
            'code': item.get('cl_code', ''),
            'name': clean_html_tags(item.get('korean_nm', '')),
            'eng': clean_html_tags(item.get('eng_nm', ''))
        }
        
        # Determine if we should fetch children
        if item.get('last_node_at') == 'N':
            # print(f"  Fetching children for {node['code']}")
            # Give a tiny delay to be nice to the server
            time.sleep(0.05)
            children = build_tree(node['code'], level + 1)
            if children:
                node['children'] = children
                
        tree.append(node)
    
    return tree

def main():
    print("Starting Neoplasm (M-Code) crawl...")
    start_time = time.time()
    
    # The root fetch
    tree = build_tree('root')
    
    print(f"Crawl finished in {time.time() - start_time:.2f} seconds.")
    
    # Count total nodes for fun
    def count_nodes(t):
        return sum(1 + count_nodes(n.get('children', [])) for n in t)
    
    print(f"Total nodes fetched: {count_nodes(tree)}")
    
    # Save as JSON
    with open('neo_data.json', 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)
        
    # Save as JS
    with open('neo_data.js', 'w', encoding='utf-8') as f:
        f.write('window.NEO_DATA_ASYNC = ')
        json.dump(tree, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')
        
    print("Saved to neo_data.json and neo_data.js")

if __name__ == '__main__':
    main()
