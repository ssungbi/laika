import re

with open('c:/Users/SB/Desktop/연습용/build_accident_data.py', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('def main():')

new_main = """def main():
    data = { 'details': {} }
    charts_to_fetch = []
    
    def find_charts(nodes):
        for n in nodes:
            if n['type'] == 'chart':
                charts_to_fetch.append(n)
            elif 'children' in n:
                find_charts(n['children'])
    
    # Mapping KNIA URL index to UI tree name and category name
    # 1: Car vs Car -> tree1
    # 2: Highway -> append to tree1
    # 3: Car vs Pedestrian -> tree2
    # 4: Car vs Two-Wheeler -> tree3
    # 5: Car vs Bicycle -> tree4
    knia_mapping = {
        1: ("tree1", "자동차 vs 자동차"),
        2: ("tree_highway", "고속도로"),
        3: ("tree2", "자동차 vs 보행자"),
        4: ("tree3", "자동차 vs 이륜차"),
        5: ("tree4", "자동차 vs 자전거")
    }

    for knia_idx, (tree_key, name) in knia_mapping.items():
        print(f"Scraping {name} (myaccident{knia_idx})...")
        html = fetch_url(f'https://accident.knia.or.kr/myaccident{knia_idx}')
        if not html:
            print(f"Failed to fetch myaccident{knia_idx}")
            data[tree_key] = []
            continue
        tree = parse_tree_from_html(html, knia_idx)
        data[tree_key] = tree

    # Merge Highway into tree1
    if 'tree_highway' in data and data['tree_highway']:
        if 'tree1' not in data: data['tree1'] = []
        highway_node = {'id': 'highway_merged', 'text': '고속도로/자동차전용도로', 'children': data['tree_highway'], 'type': 'category'}
        data['tree1'].append(highway_node)
        del data['tree_highway']
    
    # Collect all charts
    for tree_key in ['tree1', 'tree2', 'tree3', 'tree4']:
        if tree_key in data:
            find_charts(data[tree_key])

    total_charts = len(charts_to_fetch)
    print(f"Found a total of {total_charts} charts.")
    
    for i, c in enumerate(charts_to_fetch):
        print(f"Fetching detail for {c['chartNo']} ({i+1}/{total_charts})...")
        detail = extract_chart_detail(c['chartNo'], c['chartType'])
        if detail:
            data['details'][c['chartNo']] = detail
        delay = random.uniform(1.0, 2.0)
        print(f"Waiting {delay:.2f} seconds to avoid IP block...")
        time.sleep(delay)
        
    with open('accident_data.js', 'w', encoding='utf-8') as f:
        f.write('window.ACCIDENT_DATA_ASYNC = ')
        json.dump(data, f, ensure_ascii=False)
        f.write(';\\n')
        
    print("Scraping complete. Saved to accident_data.js")

if __name__ == "__main__":
    main()
"""

new_text = text[:start_idx] + new_main

with open('c:/Users/SB/Desktop/연습용/build_accident_data.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("build_accident_data.py updated with correct category mapping.")
