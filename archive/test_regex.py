import urllib.request, ssl, re
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}

html = urllib.request.urlopen(urllib.request.Request('https://accident.knia.or.kr/myaccident1', headers=headers), context=ctx).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
script_content = soup.find_all('script')
js_text = ''
for sc in script_content:
    if sc.string and 'hashchange' in sc.string:
        js_text += sc.string

chart_pattern = re.compile(r'\$\(_([A-Z0-9]+)_li\)\.html\([\'"](.*?)href=[\'"]/myaccident-content\?chartNo=(.*?)&chartType=\d+.*?<span[^>]*>.*?</span>(.*?)</a>', re.IGNORECASE | re.DOTALL)

matches = list(chart_pattern.finditer(js_text))
print(f'Total matches: {len(matches)}')
