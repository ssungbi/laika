import codecs

html = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()

html = html.replace("loadDisabilityTable('v0505', '05.05 ~ 18.03')", "loadDisabilityTable('v0505_unified', '05.05 ~ 18.03')")

codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(html)
print("index.html fixed v0505_unified call.")
