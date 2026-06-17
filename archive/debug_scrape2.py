import urllib.request, ssl
import re
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://accident.knia.or.kr/myaccident1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as res:
    content = res.read().decode('utf-8')

soup = BeautifulSoup(content, 'html.parser')
js_text = ''
for s in soup.find_all('script'):
    if s.string and 'hashchange' in s.string:
        js_text += s.string

match = re.search(r'var _([A-Z0-9]+)_li\s*=\s*document\.createElement\([\'"]li[\'"]\).*?innerHTML\s*=\s*[\'"](.*?)[\'"];', js_text, re.DOTALL | re.IGNORECASE)
if match:
    print('Found JS structure:', match.group(0))
    print('Var:', match.group(1))
    print('HTML:', match.group(2))
    
    # Try finding hashchange and txt
    html_str = match.group(2)
    cat_pattern2 = re.search(r'hashchange\(\\\'([A-Z0-9]+)\\\'\).*?<span[^>]*>(.*?)</span>', html_str)
    if cat_pattern2:
        print('Cat Node ID:', cat_pattern2.group(1))
        print('Cat Text:', cat_pattern2.group(2))
    else:
        print('Could not find hashchange/txt inside HTML')
else:
    print('No JS structure found')
