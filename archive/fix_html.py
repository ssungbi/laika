import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()

# Remove the one from <head>
head_start = text.find('<!-- 메리츠 영업포탈 이동 -->')
if head_start != -1:
    head_end = text.find('</script>\n</head>', head_start)
    if head_end != -1:
        text = text[:head_start] + text[head_end+10:]

# Replace the one at the bottom
bottom_start = text.find('<!-- 메리츠 프록시 로그인 -->')
if bottom_start != -1:
    bottom_end = text.find('</html>', bottom_start)
    new_script = """    <!-- 메리츠 영업포탈 자동 로그인 시도 -->
    <script>
        function openMeritzLogin() {
            // 외부 도메인 자동입력은 보안상 차단되므로, 영업포탈의 URL에 파라미터를 실어서 보냅니다.
            var url = 'https://sales.meritzfire.com/salesportal/Layout/MeritzSales.jsp?userid=721010848&password=fkdlzk2@&AuthNum=19920219';
            window.open(url, '_blank');
        }
    </script>
</body>
"""
    text = text[:bottom_start] + new_script + text[bottom_end:]

codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Fixed HTML scripts")
