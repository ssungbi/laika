import json

try:
    with open('kcd_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f'Total roots: {len(data)}')
        if len(data) > 0:
            print(f'First root keys: {list(data[0].keys())}')
            print(f'First root code: {data[0].get("code")}')
            print(f'First root name: {data[0].get("name")}')
            if 'children' in data[0] and data[0]['children']:
                print(f'First child keys: {list(data[0]["children"][0].keys())}')
                print(f'First child code: {data[0]["children"][0].get("code")}')
                print(f'First child name: {data[0]["children"][0].get("name")}')
except Exception as e:
    print(f"Error: {e}")
