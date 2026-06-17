import json

def get_behavior_code(code):
    if not code or '/' not in code:
        return None
    b = code.split('/')[1].strip()
    return b

def restructure_neo():
    with open('neo_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    leaf_nodes = []
    def extract_leaves(nodes):
        for node in nodes:
            if 'children' in node and node['children']:
                extract_leaves(node['children'])
            else:
                leaf_nodes.append(node)

    extract_leaves(data)

    behavior_groups = {
        '0': {'code': '/0', 'name': '양성', 'eng': 'Benign', 'children': []},
        '1': {'code': '/1', 'name': '양성인지 악성인지 불확실한 또는 알 수 없는', 'eng': 'Uncertain whether benign or malignant', 'children': []},
        '2': {'code': '/2', 'name': '상피내의', 'eng': 'In situ', 'children': []},
        '3': {'code': '/3', 'name': '악성, 원발부위', 'eng': 'Malignant, primary site', 'children': []},
        '6': {'code': '/6', 'name': '악성, 전이부위', 'eng': 'Malignant, metastatic site', 'children': []},
        '9': {'code': '/9', 'name': '악성, 원발부위인지 전이부위인지 불확실한', 'eng': 'Malignant, uncertain whether primary or metastatic site', 'children': []}
    }

    # Remove duplicates based on code
    seen = set()
    unique_leaves = []
    for leaf in leaf_nodes:
        code = leaf.get('code')
        if not code: continue
        if code not in seen:
            seen.add(code)
            unique_leaves.append(leaf)

    for leaf in unique_leaves:
        b = get_behavior_code(leaf['code'])
        if b in behavior_groups:
            behavior_groups[b]['children'].append(leaf)

    tree = [
        behavior_groups['0'],
        behavior_groups['1'],
        behavior_groups['2'],
        behavior_groups['3'],
        behavior_groups['6'],
        behavior_groups['9']
    ]

    # Filter out empty behaviors if needed, but KOICD shows them even if empty or small. Let's keep all 6.

    # Sort children by code
    for g in tree:
        g['children'] = sorted(g['children'], key=lambda x: x['code'])

    # Save as JSON
    with open('neo_data.json', 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)
        
    # Save as JS
    with open('neo_data.js', 'w', encoding='utf-8') as f:
        f.write('window.NEO_DATA_ASYNC = ')
        json.dump(tree, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')

    print(f"Restructured neo data into behavior categories.")

if __name__ == '__main__':
    restructure_neo()
