import sys

def patch_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Add sidebar link
    kcd_nav_link = '''<a href="#" class="nav-item" onclick="navigateTo('view-kcd'); return false;">
              <span class="material-icons-round">local_hospital</span> KCD-9 질병분류표
            </a>'''
    neo_nav_link = '''<a href="#" class="nav-item" onclick="navigateTo('view-kcd'); return false;">
              <span class="material-icons-round">local_hospital</span> KCD-9 질병분류표
            </a>
            <a href="#" class="nav-item" onclick="navigateTo('view-neo'); return false;">
              <span class="material-icons-round">biotech</span> 신생물 형태분류
            </a>'''
    if "신생물 형태분류" not in html and kcd_nav_link in html:
        html = html.replace(kcd_nav_link, neo_nav_link)

    # 2. Add dashboard link
    kcd_dash_link = '''<a href="#" class="tool-card-new tc-blue" onclick="navigateTo('view-kcd'); return false;">
              <div class="tc-icon-wrap"><span class="material-icons-round">local_hospital</span></div>
              <div class="tc-content">
                <h3>KCD-9 질병분류표</h3>
                <p>제9차 한국표준질병·사인분류</p>
              </div>
            </a>'''
    neo_dash_link = '''<a href="#" class="tool-card-new tc-blue" onclick="navigateTo('view-kcd'); return false;">
              <div class="tc-icon-wrap"><span class="material-icons-round">local_hospital</span></div>
              <div class="tc-content">
                <h3>KCD-9 질병분류표</h3>
                <p>제9차 한국표준질병·사인분류</p>
              </div>
            </a>
            <a href="#" class="tool-card-new tc-purple" onclick="navigateTo('view-neo'); return false;">
              <div class="tc-icon-wrap" style="background:rgba(156,39,176,0.1); color:#9c27b0;"><span class="material-icons-round">biotech</span></div>
              <div class="tc-content">
                <h3 style="color:#9c27b0;">신생물 형태분류</h3>
                <p>KCD 제8차 신생물 분류코드 조회</p>
              </div>
            </a>'''
    if "KCD 제8차 신생물 분류코드 조회" not in html and kcd_dash_link in html:
        html = html.replace(kcd_dash_link, neo_dash_link)
        
    # 3. Add view-neo
    if 'id="view-neo"' not in html:
        neo_view = '''
        <!-- 6. 신생물 형태분류표 View -->
        <div id="view-neo" class="page-view hidden">
          <div class="content-wrapper">
            <div class="sub-header">
              <button class="back-btn" onclick="navigateTo('view-main')">
                <span class="material-icons-round">arrow_back</span>
              </button>
              <h2 class="sub-header-title">신생물 형태분류표</h2>
            </div>
            
            <div class="disability-container" style="max-width:1100px; margin:0 auto; padding-top:20px;">
              <div class="insurance-search-container" style="margin-bottom: 20px;">
                <span class="material-icons-round search-icon">search</span>
                <input type="text" id="neo-search-input" placeholder="질병코드 또는 질병명을 입력하세요 (예: M8010/0, 선종)" onkeyup="filterNeo()">
              </div>
              
              <div id="neo-search-results" style="display: none; margin-bottom: 20px;"></div>
              
              <!-- Selected Chapter Tree View -->
              <div id="neo-tree-container" class="disability-list">
                <!-- JS will populate -->
              </div>
            </div>
          </div>
        </div>
        '''
        
        # Insert before </main>
        html = html.replace('</main>', neo_view + '\n        </main>')
        
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched index.html for Neoplasm")

if __name__ == '__main__':
    patch_index()
