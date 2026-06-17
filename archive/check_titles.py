import urllib.request, ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}

with open('c:/Users/SB/Desktop/연습용/titles.txt', 'w', encoding='utf-8') as f:
    for i in range(1, 6):
        html = urllib.request.urlopen(urllib.request.Request(f'https://accident.knia.or.kr/myaccident{i}', headers=headers), context=ctx).read().decode('utf-8')
        title = BeautifulSoup(html, 'html.parser').find('title').text
        f.write(f'myaccident{i}: {title}\n')
