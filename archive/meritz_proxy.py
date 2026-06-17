"""
메리츠 로그인 프록시 서버
- 메리츠 로그인 페이지를 가져와서 자동입력 JS를 주입
- 모든 하위 요청(CSS/JS/이미지/폼 제출)을 메리츠로 프록시
"""
import http.server
import urllib.request
import urllib.parse
import ssl
import http.cookiejar
import threading
import sys

PROXY_PORT = 53299
MERITZ_BASE = "https://nsso.meritzfire.com"
LOGIN_PATH = "/LoginServer/loginFormPageMulti.jsp?InitechEamNoCacheNonce=L2n%2BxFlheCY2n1gAtWPxAQ%3D%3D"

# 자동입력 스크립트 (로그인 페이지 끝에 주입)
AUTOFILL_JS = """
<script>
(function() {
    function fillFields() {
        var uid = document.getElementById('userid') || document.getElementsByName('userid')[0];
        var pwd = document.getElementById('password') || document.getElementsByName('password')[0];
        var auth = document.getElementById('AuthNum') || document.getElementsByName('AuthNum')[0];
        
        if (uid) {
            uid.value = '721010848';
            uid.style.borderColor = '#4CAF50';
        }
        if (pwd) {
            pwd.value = 'fkdlzk2@';
            pwd.style.borderColor = '#4CAF50';
        }
        if (auth) {
            auth.value = '19920219';
            auth.style.borderColor = '#4CAF50';
        }
        
        console.log('Auto-fill complete!', uid, pwd, auth);
    }
    
    // 페이지 로드 후 약간의 딜레이를 두고 실행
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        setTimeout(fillFields, 500);
    } else {
        window.addEventListener('DOMContentLoaded', function() {
            setTimeout(fillFields, 500);
        });
    }
    
    // 혹시 늦게 렌더링되는 필드를 위해 한번 더
    window.addEventListener('load', function() {
        setTimeout(fillFields, 1000);
        setTimeout(fillFields, 2000);
    });
})();
</script>
"""

# SSL 컨텍스트 (인증서 검증 비활성화 - 내부망용)
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# 쿠키 저장소
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
    urllib.request.HTTPSHandler(context=ssl_ctx)
)


class MeritzProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[Proxy] {args[0]}")

    def do_GET(self):
        if self.path == '/meritz' or self.path == '/meritz/':
            # 메리츠 로그인 페이지 요청
            self._proxy_request("GET", LOGIN_PATH)
        elif self.path.startswith('/LoginServer/') or self.path.startswith('/css/') or \
             self.path.startswith('/js/') or self.path.startswith('/images/') or \
             self.path.startswith('/wizvera/') or self.path.startswith('/include/') or \
             self.path.startswith('/img/') or self.path.startswith('/nls3/') or \
             self.path.startswith('/lottie/'):
            self._proxy_request("GET", self.path)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        self._proxy_request("POST", self.path, post_data)

    def _proxy_request(self, method, path, data=None):
        url = MERITZ_BASE + path
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'identity',
            }
            
            if method == "POST":
                headers['Content-Type'] = self.headers.get('Content-Type', 'application/x-www-form-urlencoded')
            
            # Referer 설정 (메리츠 서버가 체크할 수 있음)
            if '/idPasswordLogin' in path:
                headers['Referer'] = MERITZ_BASE + LOGIN_PATH
            
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            resp = opener.open(req, timeout=15)
            
            body = resp.read()
            content_type = resp.headers.get('Content-Type', 'text/html')
            
            # HTML 응답이면 URL 리라이트 + 자동입력 JS 주입
            if 'text/html' in content_type:
                charset = 'utf-8'
                if 'charset=' in content_type:
                    charset = content_type.split('charset=')[-1].strip()
                
                html = body.decode(charset, errors='replace')
                
                # 상대 경로를 프록시 경로로 유지 (이미 상대경로이므로 그대로 작동)
                # ../css/ → /css/ 등으로 변환
                html = html.replace('href="../css/', 'href="/css/')
                html = html.replace('href="../js/', 'href="/js/')
                html = html.replace('src="../css/', 'src="/css/')
                html = html.replace('src="../js/', 'src="/js/')
                html = html.replace('src="../wizvera/', 'src="/wizvera/')
                html = html.replace('src="../include/', 'src="/include/')
                html = html.replace('href="../images/', 'href="/images/')
                html = html.replace('src="../images/', 'src="/images/')
                html = html.replace('src="../img/', 'src="/img/')
                html = html.replace('src="../lottie/', 'src="/lottie/')
                
                # 로그인 페이지에만 자동입력 JS 주입
                if 'loginFormPage' in path or path == LOGIN_PATH:
                    html = html.replace('</body>', AUTOFILL_JS + '\n</body>')
                
                body = html.encode(charset, errors='replace')
            
            # 리다이렉트 처리
            status = resp.status
            if status in (301, 302, 303, 307, 308):
                location = resp.headers.get('Location', '')
                if location.startswith(MERITZ_BASE):
                    location = location[len(MERITZ_BASE):]
                self.send_response(status)
                self.send_header('Location', location)
                self.end_headers()
                return
            
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            # CORS 허용
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)
            
        except Exception as e:
            print(f"[Proxy Error] {method} {url}: {e}")
            self.send_response(502)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            error_msg = f"<h2>프록시 오류</h2><p>{str(e)}</p><p>URL: {url}</p>"
            self.wfile.write(error_msg.encode('utf-8'))


def run_proxy():
    server = http.server.HTTPServer(('127.0.0.1', PROXY_PORT), MeritzProxyHandler)
    print(f"[Meritz Proxy] 서버 시작: http://localhost:{PROXY_PORT}/meritz")
    print(f"[Meritz Proxy] 이 주소를 브라우저에서 열면 자동입력된 로그인 페이지가 나타납니다!")
    server.serve_forever()


if __name__ == '__main__':
    run_proxy()
