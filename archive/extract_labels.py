import urllib.request, ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = 'https://accident.knia.or.kr/myaccident-content?chartNo=%EC%B0%A81-1&chartType=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as res:
    html = res.read().decode('euc-kr', errors='replace')
soup = BeautifulSoup(html, 'html.parser')

with open('debug_html.txt', 'w', encoding='utf-8') as f:
    cb = soup.select_one('.checkbox')
    if cb:
        parent = cb.find_parent('div', class_='tbl_scroll') or cb.find_parent('table')
        if not parent:
            parent = cb.find_parent('div')
        f.write(parent.prettify())
