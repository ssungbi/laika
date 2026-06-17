import urllib.request

req = urllib.request.Request('https://www.koicd.kr/kcd/kcd9.do', headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    with open('kcd9.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved to kcd9.html")
except Exception as e:
    print(e)
