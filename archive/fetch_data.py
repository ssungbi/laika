import urllib.request
import re

url = 'https://bohumschool-archive.pages.dev/assets/index-C-P5BW8L.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
js_data = urllib.request.urlopen(req).read().decode('utf-8')

keys = re.findall(r'(eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+)', js_data)
if keys:
    for k in set(keys):
        print("Key:", k)
else:
    print("No eyJ keys found in index JS")

url2 = 'https://bohumschool-archive.pages.dev/assets/api-Bdw2P012.js'
req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
js_data2 = urllib.request.urlopen(req2).read().decode('utf-8')

keys2 = re.findall(r'(eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+)', js_data2)
if keys2:
    for k in set(keys2):
        print("Key from api JS:", k)
else:
    print("No eyJ keys found in api JS")
