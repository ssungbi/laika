import urllib.request, ssl, re, json
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}

def parse_top_levels(html):
    soup = BeautifulSoup(html, 'html.parser')
    depth1_ul = soup.find('ul', class_='depth')
    cats = []
    if depth1_ul:
        for li in depth1_ul.find_all('li', recursive=False):
            a_tag = li.find('a', onclick=re.compile(r"hashchange\('([^']+)'\)"))
            if a_tag:
                text = a_tag.find('span', class_='txt').get_text(strip=True)
                cats.append(text)
    return cats

with open('c:/Users/SB/Desktop/연습용/trees.txt', 'w', encoding='utf-8') as f:
    for i in range(1, 6):
        html = urllib.request.urlopen(urllib.request.Request(f'https://accident.knia.or.kr/myaccident{i}', headers=headers), context=ctx).read().decode('utf-8')
        cats = parse_top_levels(html)
        f.write(f'myaccident{i}: {cats}\n')
