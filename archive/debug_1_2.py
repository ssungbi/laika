import urllib.request, ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = 'https://accident.knia.or.kr/myaccident-content?chartNo=%EC%B0%A81-2&chartType=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as res:
    html = res.read().decode('euc-kr', errors='replace')
soup = BeautifulSoup(html, 'html.parser')

with open('debug_1_2.txt', 'w', encoding='utf-8') as f:
    f.write('--- default_accident ---\n')
    for el in soup.select('#default_accident td'):
        f.write(el.get_text(strip=True) + '\n')
    
    f.write('\n--- tabs/cases ---\n')
    for el in soup.select('.macont_cont_title'):
        f.write(el.get('id', 'No ID') + ' : ' + el.get_text(strip=True) + '\n')
        
    f.write('\n--- graphs ---\n')
    for el in soup.select('.graph'):
        f.write(el.get('id', 'No ID') + ' : ' + el.get_text(strip=True) + '\n')
        
    f.write('\n--- factors ---\n')
    for el in soup.select('.scr_con'):
        f.write(el.get('id', 'No ID') + ' : ' + str(len(el.select('input[type=checkbox]'))) + ' factors\n')
        
    f.write('\n--- media ---\n')
    for el in soup.select('img, source'):
        f.write(str(el) + '\n')
