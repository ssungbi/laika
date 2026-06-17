import urllib.request, ssl
import re
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = 'https://accident.knia.or.kr/myaccident-content?chartNo=%EC%B0%A81-1&chartType=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as res:
    content_bytes = res.read()
    try:
        html = content_bytes.decode('utf-8')
    except:
        html = content_bytes.decode('euc-kr', errors='replace')
        
soup = BeautifulSoup(html, 'html.parser')

# Look for image or flash or video
print("Images with chart/accident:")
for img in soup.find_all('img'):
    src = img.get('src', '')
    if 'chart' in src.lower() or 'accident' in src.lower():
        print(src)
        
# Look for flash/swf
flash_pattern = re.compile(r'swf')
print("SWF?", flash_pattern.search(html))
print("MP4?", 'mp4' in html)

# Look for factors
labels = soup.find_all('label')
for l in labels:
    print('Label:', l.get_text(strip=True))
    
# Look for car names
print("Car Names")
for span in soup.select('span.car_name'):
    print(span.get_text(strip=True))

for div in soup.select('.car_name_a, .car_name_b'):
    print(div.get_text(strip=True))
    
# Let's print out the text of any <td> or <li> that has data-a or data-b
factors = soup.find_all(attrs={"data-a": True})
for f in factors:
    print('Factor text:', f.get_text(strip=True), 'A:', f.get('data-a'), 'B:', f.get('data-b'))
