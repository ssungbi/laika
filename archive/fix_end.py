import sys

html_path = r'c:\Users\SB\Desktop\연습용\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the start of the scroll to top button
btn_index = html.find('<button id="scrollToTopBtn"')
if btn_index != -1:
    html = html[:btn_index]

proper_ending = '''    <!-- Scroll to Top Button -->
    <button id="scrollToTopBtn" class="scroll-to-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="맨 위로">
        <span class="material-icons-round">arrow_upward</span>
    </button>

    <script src="script.js?v=35"></script>

    <!-- 메리츠 영업포탈 이동 -->
    <script>
        function openMeritzLogin() {
            // 메리츠 영업포탈 로그인 화면으로 이동
            var url = 'https://sales.meritzfire.com/salesportal/Layout/MeritzSales.jsp';
            window.open(url, '_blank');
        }
    </script>
</body>
</html>
'''

html += proper_ending

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
