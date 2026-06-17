import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://nsso.meritzfire.com/LoginServer/loginFormPageMulti.jsp?InitechEamNoCacheNonce=test',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode('utf-8', errors='replace')

# Find the actual HTML form body with inputs
idx = html.find('<form name="login"')
if idx != -1:
    form_end = html.find('</form>', idx)
    form_html = html[idx:form_end+7]
    
    # Find all input elements
    inputs = re.findall(r'<input[^>]*>', form_html, re.IGNORECASE)
    print('All inputs in form:')
    for inp in inputs:
        print(f'  {inp}')
    
    # Find select elements
    selects = re.findall(r'<select[^>]*>.*?</select>', form_html, re.DOTALL | re.IGNORECASE)
    print(f'\nAll selects in form: {len(selects)}')
    for s in selects:
        print(f'  {s[:200]}')
    
    # Find AuthNum input or any related element
    auth_area = re.findall(r'[Aa]uth[Nn]um.*?>', form_html)
    print(f'\nAuthNum related: {auth_area}')
    
    # Print the full form HTML for analysis
    print('\n--- FULL FORM HTML ---')
    print(form_html)
