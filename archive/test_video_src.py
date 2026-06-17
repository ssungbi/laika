import urllib.request, ssl, urllib.parse
from bs4 import BeautifulSoup
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://accident.knia.or.kr/myaccident-content?chartNo=' + urllib.parse.quote('차1-1') + '&chartType=1'
html = urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
video_source = soup.select_one('source[type="video/mp4"]')
print(video_source['src'] if video_source else 'No video')
