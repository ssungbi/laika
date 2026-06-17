import codecs

html = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
html = html.replace("if (log) log.innerHTML +=", "alert('JS Error: ' + message); if (log) log.innerHTML +=")
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(html)
print("Added alert to window.onerror")
