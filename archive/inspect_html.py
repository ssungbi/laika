import urllib.request, ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = 'https://accident.knia.or.kr/myaccident-content?chartNo=%EC%B0%A81-1&chartType=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as res:
    html = res.read().decode('euc-kr', errors='replace')
soup = BeautifulSoup(html, 'html.parser')

with open('inspect_out.txt', 'w', encoding='utf-8') as f:
    f.write('--- VIDEO ---\n')
    for video in soup.select('.macont_cont_video'):
        f.write(video.prettify()[:1000] + '\n\n')
        
    f.write('\n--- TABS ---\n')
    # The tabs for 사고상황, 적용, 기본과실 해설
    for tabs in soup.select('.caracdsittn'):
        f.write(tabs.prettify()[:2000] + '\n\n')
        
    f.write('\n--- CONTENT OF TABS ---\n')
    # The content of the tabs
    for content in soup.select('.cont_state'):
        f.write(content.prettify()[:2000] + '\n\n')
        
    f.write('\n--- SCRIPT FOR VIDEO ---\n')
    for s in soup.find_all('script'):
        if s.string and 'mp4' in s.string:
            f.write(s.string + '\n')
