import urllib.request, urllib.parse, json

url = 'https://www.koicd.kr/kcd/neo.list.json'
data = urllib.parse.urlencode({'upper_cl_code': 'root', 'degree': '08'}).encode('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://www.koicd.kr/kcd/neo.do',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.koicd.kr',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

req = urllib.request.Request(url, data=data, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"Total items: {len(result.get('list', []))}")
        for i, item in enumerate(result.get('list', [])[:5]):
            print(item)
except Exception as e:
    print(f"Error: {e}")
