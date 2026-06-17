import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://accident.knia.or.kr/myaccident1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as res:
    content = res.read().decode('utf-8')

from bs4 import BeautifulSoup
import re
soup = BeautifulSoup(content, 'html.parser')

scripts = soup.find_all('script')
js_text = ''
for s in scripts:
    if s.string and 'hashchange' in s.string:
        js_text += s.string

print('js_text len:', len(js_text))

chart_pattern = re.compile(r'\$\(_([A-Z0-9]+)_li\)\.html\([\'"](.*?)href=[\'"]/myaccident-content\?chartNo=(.*?)&chartType=\d+.*?<span[^>]*>.*?</span>(.*?)</a>', re.IGNORECASE | re.DOTALL)
matches = list(chart_pattern.finditer(js_text))
print('chart matches:', len(matches))

cat_pattern = re.compile(r'_([A-Z0-9]+)_li\.innerHTML\s*=\s*[\'"].*?hashchange\([\'"]([A-Z0-9]+)[\'"]\).*?<span[^>]*>(.*?)</span>', re.IGNORECASE)
cat_matches = list(cat_pattern.finditer(js_text))
print('cat matches:', len(cat_matches))

# Print what the Javascript looks like if matches fail
if len(matches) == 0:
    print(js_text[:1000])

