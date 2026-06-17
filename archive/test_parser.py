import urllib.request, ssl, json
from bs4 import BeautifulSoup
import sys
sys.path.append('c:/Users/SB/Desktop/연습용')
from build_accident_data import parse_tree_from_html

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}

html = urllib.request.urlopen(urllib.request.Request('https://accident.knia.or.kr/myaccident1', headers=headers), context=ctx).read().decode('utf-8')
tree = parse_tree_from_html(html, 1)

charts = []
def find_charts(nodes):
    for n in nodes:
        if n['type'] == 'chart':
            charts.append(n)
        elif 'children' in n:
            find_charts(n['children'])
            
find_charts(tree)
print(f'Total charts in tree1: {len(charts)}')
