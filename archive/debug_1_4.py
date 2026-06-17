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

with open('debug_1_4.txt', 'w', encoding='utf-8') as f:
    f.write('--- CAR A & B ---\n')
    for el in soup.find_all(class_=lambda x: x and 'car' in x):
        f.write(f"Class: {el.get('class')} Text: {el.get_text(strip=True)}\n")
        
    f.write('\n--- ALL IDS ---\n')
    for el in soup.find_all(id=True):
        if el.get('id') in ['caracdsittn', 'applcscore', 'cont_state', 'case1', 'macont03']:
            f.write(f"ID: {el.get('id')} Text: {el.get_text(strip=True)[:100]}\n")
            
    f.write('\n--- MACONT03 DIVS ---\n')
    macont03 = soup.select_one('#macont03')
    if macont03:
        for div in macont03.find_all('div', recursive=False):
            f.write(f"DIV id={div.get('id')} class={div.get('class')}\n")
            f.write(div.get_text(strip=True)[:100] + '\n')
