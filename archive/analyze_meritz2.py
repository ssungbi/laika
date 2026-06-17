import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://nsso.meritzfire.com/LoginServer/loginFormPageMulti.jsp?InitechEamNoCacheNonce=test',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode('utf-8', errors='replace')

# Find getUserPhoneId function
idx = html.find('getUserPhoneId')
if idx != -1:
    print('getUserPhoneId context:')
    print(html[idx:idx+2000])

# Find the actual submit / form action change
idx2 = html.find('document.login.action')
if idx2 != -1:
    print('\nForm action change:')
    print(html[max(0, idx2-200):idx2+500])

# Find doSubmit or login.submit
for keyword in ['login.submit', '.submit()', 'doLogin', 'doSubmit', 'fn_loginSubmit', 'loginSubmit']:
    idx3 = html.find(keyword)
    if idx3 != -1:
        print(f'\n{keyword} context:')
        print(html[max(0, idx3-200):idx3+500])

# Find AuthNum input
idx4 = html.find('id="AuthNum"')
if idx4 == -1:
    idx4 = html.find("id='AuthNum'")
if idx4 != -1:
    print('\nAuthNum input element:')
    print(html[max(0, idx4-100):idx4+200])
else:
    print('\nAuthNum input element not found directly')

# Search for the birthday field label
for keyword in ['8', 'birth', 'AuthNum']:
    positions = [m.start() for m in re.finditer(keyword, html)]
    if positions:
        print(f'\n--- All occurrences of "{keyword}": {len(positions)} ---')
        for p in positions[:5]:
            print(f'  Position {p}: ...{html[max(0,p-30):p+80]}...')
