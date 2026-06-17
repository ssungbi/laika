import urllib.request, urllib.parse, json
import time

url = 'https://www.koicd.kr/kcd/neo.list.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://www.koicd.kr/kcd/neo.do',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.koicd.kr',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def fetch_children(upper_cl_code, degree):
    data = urllib.parse.urlencode({'upper_cl_code': upper_cl_code, 'degree': degree}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('list', [])
    except Exception as e:
        print(f"Error fetching {upper_cl_code} for degree {degree}: {e}")
        return []

def clean_html_tags(text):
    import re
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def build_tree(upper_code, degree, level=1):
    items = fetch_children(upper_code, degree)
    
    tree = []
    for item in items:
        if item.get('cl_code') == upper_code:
            continue
            
        node = {
            'code': item.get('cl_code', ''),
            'name': clean_html_tags(item.get('korean_nm', '')),
            'eng': clean_html_tags(item.get('eng_nm', ''))
        }
        
        if item.get('last_node_at') == 'N':
            time.sleep(0.02)
            children = build_tree(node['code'], degree, level + 1)
            if children:
                node['children'] = children
                
        tree.append(node)
    
    return tree

def main():
    degrees = ['08', '07', '06', '05', '04', '03', '02']
    all_data = {}
    
    start_time = time.time()
    
    for degree in degrees:
        print(f"Fetching degree {degree}...")
        tree = build_tree('root', degree)
        all_data[degree] = tree
        
        def count_nodes(t):
            return sum(1 + count_nodes(n.get('children', [])) for n in t)
        
        print(f"  -> Fetched {count_nodes(tree)} nodes for degree {degree}")

    print(f"Crawl finished in {time.time() - start_time:.2f} seconds.")
    
    # Save as JS
    with open('neo_data_all.js', 'w', encoding='utf-8') as f:
        f.write('window.NEO_DATA_ALL_ASYNC = ')
        json.dump(all_data, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')
        
    print("Saved to neo_data_all.js")

if __name__ == '__main__':
    main()
