import urllib.request, ssl, re
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request('https://accident.knia.or.kr/', headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    soup = BeautifulSoup(res.read(), 'html.parser')
    for a in soup.find_all('a', href=re.compile(r'/myaccident\d+')):
        print(a['href'], a.get_text(strip=True))
except Exception as e:
    print('Error:', e)
