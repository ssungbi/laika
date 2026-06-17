import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()

form_html = '''
    <!-- 메리츠 자동 로그인 폼 -->
    <form id="meritzLoginForm" action="http://sales.meritzfire.com/" method="POST" target="_blank" style="display: none;">
        <input type="hidden" name="userid" value="721010848">
        <input type="hidden" name="password" value="fkdlzk2@">
        <input type="hidden" name="AuthNum" value="19920219">
    </form>
'''

if 'meritzLoginForm' not in text:
    text = text.replace('</body>', form_html + '\n</body>')

if 'onclick="document.getElementById(\'meritzLoginForm\').submit();"' not in text:
    text = text.replace('<div class="quick-start-card card-meritz">', '<div class="quick-start-card card-meritz" onclick="document.getElementById(\'meritzLoginForm\').submit();" style="cursor:pointer;">')

codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Added Meritz auto-login form and onclick handler")
