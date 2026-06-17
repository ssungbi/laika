import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://nsso.meritzfire.com/LoginServer/loginFormPageMulti.jsp?InitechEamNoCacheNonce=test',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode('utf-8', errors='replace')

# Find all form tags
forms = re.findall(r'<form[^>]*>', html, re.IGNORECASE)
print('Forms:', forms)

# Find all input names
inputs = re.findall(r'<input[^>]*name=["\']([^"\']*)["\'][^>]*>', html, re.IGNORECASE)
print('Input names:', inputs)

# Find form action
actions = re.findall(r'<form[^>]*action=["\']([^"\']*)["\'][^>]*>', html, re.IGNORECASE)
print('Form actions:', actions)

# Find NextSubmit function
idx = html.find('NextSubmit')
if idx != -1:
    print('\nNextSubmit context:')
    print(html[idx:idx+1500])

# Find AuthNum
idx2 = html.find('AuthNum')
if idx2 != -1:
    print('\nAuthNum context:')
    print(html[max(0, idx2-200):idx2+200])
else:
    print('\nAuthNum not found in HTML')

# Find birthday/생년
idx3 = html.find('birth')
if idx3 != -1:
    print('\nBirth context:')
    print(html[max(0, idx3-200):idx3+200])
