import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = 'https://accident.knia.or.kr/myaccident-content?chartNo=%EC%B0%A81-2&chartType=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as res:
        html = res.read().decode('euc-kr', errors='replace')
        with open('debug_1_2_html.txt', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Successfully downloaded HTML.")
except Exception as e:
    print(f"Error: {e}")
