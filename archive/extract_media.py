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

with open('debug_media.txt', 'w', encoding='utf-8') as f:
    video_div = soup.select_one('.macont_cont_video')
    if video_div:
        f.write(video_div.prettify())
    else:
        f.write("No .macont_cont_video found\n")
        
    f.write("\n\nAll scripts:\n")
    for s in soup.find_all('script'):
        if s.string:
            if 'mp4' in s.string or 'png' in s.string or 'gif' in s.string:
                f.write(s.string)
