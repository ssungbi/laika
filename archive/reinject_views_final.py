import sys
import re

html_path = r'c:\Users\SB\Desktop\연습용\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject Views
kcd_html = '''
        <!-- 5. KCD 질병분류표 View -->
        <div id="view-kcd" class="page-view hidden">
            <div class="content-wrapper">
                <div class="sub-header">
                    <button class="back-btn" onclick="navigateTo('view-main')">
                        <span class="material-icons-round">arrow_back</span>
                    </button>
                    <h2 class="sub-header-title">KCD-9 질병분류표</h2>
                </div>
                
                <div class="disability-container" style="max-width: 1200px;">
                    <div class="insurance-search-container" style="max-width: 800px; margin: 0 auto 24px auto;">
                        <span class="material-icons-round search-icon" style="position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #9ca3af; font-size: 20px;">search</span>
                        <input type="text" id="kcd-search-input" placeholder="질병코드 또는 질병명을 입력하세요" onkeyup="filterKcd()" style="width: 100%; padding: 14px 16px 14px 44px; font-size: 15px; border: 1px solid #d1d5db; border-radius: 12px; background: #fff; color: #111827; box-sizing: border-box;">
                    </div>
                    
                    <div id="kcd-search-results" style="display: none; max-width: 1200px; margin: 0 auto;"></div>
                    
                    <div id="kcd-chapters-container" class="period-grid" style="max-width: 1200px; margin: 0 auto;"></div>
                    
                    <div id="kcd-tree-container" class="accordion-group" style="display: none; max-width: 1200px; margin: 0 auto;"></div>
                </div>
            </div>
        </div>
'''

neo_html = '''
        <!-- 6. 신생물 형태분류표 View -->
        <div id="view-neo" class="page-view hidden">
            <div class="content-wrapper">
                <div class="sub-header">
                    <button class="back-btn" onclick="navigateTo('view-main')">
                        <span class="material-icons-round">arrow_back</span>
                    </button>
                    <h2 class="sub-header-title">신생물 형태분류표</h2>
                </div>
                
                <div class="disability-container" style="max-width: 1200px;">
                    <div class="insurance-search-container" style="max-width: 800px; margin: 0 auto 24px auto; position: relative;">
                        <span class="material-icons-round search-icon" style="position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #9ca3af; font-size: 20px;">search</span>
                        <input type="text" id="neo-search-input" placeholder="질병코드 또는 질병명을 입력하세요" onkeyup="filterNeo()" style="width: 100%; padding: 14px 16px 14px 44px; font-size: 15px; border: 1px solid #d1d5db; border-radius: 12px; background: #fff; color: #111827; box-sizing: border-box;">
                    </div>
                    
                    <div id="neo-search-results" style="display: none; max-width: 1200px; margin: 0 auto;"></div>
                    
                    <div id="neo-tree-container" class="accordion-group" style="max-width: 1200px; margin: 0 auto;"></div>
                </div>
            </div>
        </div>
'''

if 'id="view-kcd"' not in html:
    html = html.replace('</main>', kcd_html + '\n        </main>')

if 'id="view-neo"' not in html:
    html = html.replace('</main>', neo_html + '\n        </main>')

# 2. Update Navigations in Sidebar
# find the a tag with 'KCD 질병분류표'
html = re.sub(
    r'<a href="#" class="nav-item">(\s*<span class="nav-icon-box">질병</span>\s*<span class="text">KCD 질병분류표</span>\s*)</a>',
    r'<a href="#" class="nav-item" onclick="navigateTo(\'view-kcd\'); return false;">\1</a>',
    html
)
html = re.sub(
    r'<a href="#" class="nav-item">(\s*<span class="nav-icon-box">종양</span>\s*<span class="text">신생물형태분류표</span>\s*)</a>',
    r'<a href="#" class="nav-item" onclick="navigateTo(\'view-neo\'); return false;">\1</a>',
    html
)

# 3. Update Navigations in Main Dashboard
html = re.sub(
    r'<a href="#" class="tool-card-new tc-blue">(\s*<div class="tc-icon material-icons-round">local_hospital</div>\s*<span class="tc-name">KCD<br>질병분류표</span>\s*)</a>',
    r'<a href="#" class="tool-card-new tc-blue" onclick="navigateTo(\'view-kcd\'); return false;">\1</a>',
    html
)
html = re.sub(
    r'<a href="#" class="tool-card-new tc-pink">(\s*<div class="tc-icon material-icons-round">biotech</div>\s*<span class="tc-name">신생물형태<br>분류표</span>\s*)</a>',
    r'<a href="#" class="tool-card-new tc-pink" onclick="navigateTo(\'view-neo\'); return false;">\1</a>',
    html
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML injection complete!")
