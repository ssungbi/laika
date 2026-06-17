import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()

text = text.replace('action="http://sales.meritzfire.com/"', 'action="https://sales.meritzfire.com/salesportal/Layout/MeritzSales.jsp"')

codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Changed form action to MeritzSales.jsp")
