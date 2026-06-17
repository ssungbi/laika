import urllib.request, ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = 'https://accident.knia.or.kr/myaccident-content?chartNo=%EC%B0%A81-4&chartType=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as res:
    html = res.read().decode('euc-kr', errors='replace')
soup = BeautifulSoup(html, 'html.parser')

with open('debug_macont.txt', 'w', encoding='utf-8') as f:
    f.write('--- macont01 ---\n')
    m1 = soup.select_one('#macont01')
    if m1: f.write(m1.prettify())

    f.write('\n\n--- macont02 ---\n')
    m2 = soup.select_one('#macont02')
    if m2: f.write(m2.prettify())

    f.write('\n\n--- macont03 ---\n')
    m3 = soup.select_one('#macont03')
    if m3: f.write(m3.prettify())

    f.write('\n\n--- macont04 ---\n')
    m4 = soup.select_one('#macont04')
    if m4: f.write(m4.prettify())
