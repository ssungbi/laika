import os

with open('index.html', 'r', encoding='cp949', errors='ignore') as f:
    lines = f.readlines()

for i in range(len(lines)):
    line = lines[i]
    if 'stylesheet' in line:
        continue
    
    # Title & Logo
    line = line.replace('<title>보험금계 - 차보 보험 무료 계산</title>', '<title>라이카손해사정 - 보상 업무 통합 페이지</title>')
    line = line.replace('alt="카손"', 'alt="라이카손해사정"')
    line = line.replace('alt="카손"', 'alt="라이카손해사정"')
    line = line.replace('<p>카손</p>', '<p>라이카손해사정</p>')
    line = line.replace('<p>카손</p>', '<p>라이카손해사정</p>')
    
    # Nav Titles
    line = line.replace('<h3 class="nav-title">보험 계산</h3>', '<h3 class="nav-title">보험금 계산기</h3>')
    line = line.replace('<h3 class="nav-title">분류 / </h3>', '<h3 class="nav-title">분류표 / 기준</h3>')
    line = line.replace('<h3 class="nav-title"> / 조정</h3>', '<h3 class="nav-title">판례 / 조정사례</h3>')
    line = line.replace('<h3 class="nav-title">료자 / 감정</h3>', '<h3 class="nav-title">의료자문 / 신체감정</h3>')

    # Nav Items
    line = line.replace('<span class="nav-icon-box">차</span>', '<span class="nav-icon-box">자</span>')
    line = line.replace('<span class="text">차보</span>', '<span class="text">자동차보험</span>')
    line = line.replace('<span class="text">보험</span>', '<span class="text">산재보험</span>')
    line = line.replace('<span class="nav-icon-box">배상</span>', '<span class="nav-icon-box">배상</span>')
    line = line.replace('<span class="text">배상책임보험</span>', '<span class="text">배상책임보험</span>')
    line = line.replace('<span class="nav-icon-box"></span>', '<span class="nav-icon-box">산</span>')
    line = line.replace('<span class="text">/근재보험</span>', '<span class="text">산재/근재보험</span>')
    line = line.replace('<span class="text">개인 비보</span>', '<span class="text">개인 장기보험</span>')
    
    line = line.replace('<span class="nav-icon-box"></span>', '<span class="nav-icon-box">장</span>')
    line = line.replace('<span class="text">분류(개인보험)</span>', '<span class="text">장해분류표(개인보험)</span>')
    line = line.replace('<span class="nav-icon-box">맥브</span>', '<span class="nav-icon-box">맥브</span>')
    line = line.replace('<span class="text">맥브 </span>', '<span class="text">맥브라이드 표</span>')
    line = line.replace('<span class="text">급별 (기)</span>', '<span class="text">장해급별 기준(기본)</span>')
    line = line.replace('<span class="nav-icon-box">붃</span>', '<span class="nav-icon-box">부상</span>')
    line = line.replace('<span class="text">붃급수</span>', '<span class="text">부상급수표</span>')
    line = line.replace('<span class="nav-icon-box">질병</span>', '<span class="nav-icon-box">질병</span>')
    line = line.replace('<span class="text">KCD 질병분류</span>', '<span class="text">KCD-9 질병분류표</span>')
    line = line.replace('<span class="nav-icon-box">종양</span>', '<span class="nav-icon-box">종양</span>')
    line = line.replace('<span class="text">물형분류</span>', '<span class="text">신생물 형태분류표</span>')
    line = line.replace('<span class="nav-icon-box">과실</span>', '<span class="nav-icon-box">과실</span>')
    line = line.replace('<span class="text">차사 과실비율</span>', '<span class="text">자동차사고 과실비율</span>')
    line = line.replace('<span class="text"> 분류</span>', '<span class="text">직업 직무분류표</span>')
    
    line = line.replace('<span class="nav-icon-box">법원</span>', '<span class="nav-icon-box">법원</span>')
    line = line.replace('<span class="text">법원 </span>', '<span class="text">법원 판례</span>')
    line = line.replace('<span class="nav-icon-box">금감</span>', '<span class="nav-icon-box">금감</span>')
    line = line.replace('<span class="text">금융감독 조정</span>', '<span class="text">금융감독원 조정사례</span>')
    
    line = line.replace('<span class="text">료자</span>', '<span class="text">의료자문</span>')
    line = line.replace('<span class="text">감정</span>', '<span class="text">신체감정</span>')

    # Header / Hero
    line = line.replace('2026 최신 기 ', '2026년 최신 기준 적용')
    line = line.replace('<h1> 무페</h1>', '<h1>보상 업무 통합 페이지</h1>')
    line = line.replace('<p class="header-subtitle">   보조 </p>', '<p class="header-subtitle">보상 실무 및 보조 프로그램</p>')
    line = line.replace('<span>로그 </span>', '<span>로그아웃</span>')
    line = line.replace('<strong>보험 </strong>', '<strong>보험금 청구</strong>')
    line = line.replace('<span> 보험 구정 </span>', '<span>각 보험사 청구정보 확인</span>')
    line = line.replace('<strong>메리 보장분석</strong>', '<strong>메리츠 보장분석</strong>')
    line = line.replace('<span>메리  바로</span>', '<span>메리츠 포털 바로가기</span>')

    # Dashboard Sections
    line = line.replace('<h2 class="section-title sec-title-calc"> 보험 계산</h2>', '<h2 class="section-title sec-title-calc">보험금 계산기</h2>')
    line = line.replace('<strong>개인 비보</strong>', '<strong>개인 장기보험</strong>')
    line = line.replace('<span>료비 ·</span>', '<span>의료비, 진단비 등</span>')
    line = line.replace('<strong>차보</strong>', '<strong>자동차보험</strong>')
    line = line.replace('<span>·무보·</span>', '<span>합의금, 무보험상해 등</span>')
    line = line.replace('<strong>배상책임보험</strong>', '<strong>배상책임보험</strong>')
    line = line.replace('<span>배책·배상</span>', '<span>영업배책, 일배책 등</span>')
    line = line.replace('<strong>/근재보험</strong>', '<strong>산재/근재보험</strong>')
    line = line.replace('<span>·근재보상</span>', '<span>산재, 근재보상 등</span>')

    line = line.replace('<h2 class="section-title sec-title-tools"> 분류 / </h2>', '<h2 class="section-title sec-title-tools">분류표 / 기준</h2>')
    line = line.replace('<span class="tc-name">분류<br>(개인보험)</span>', '<span class="tc-name">장해분류표<br>(개인보험)</span>')
    line = line.replace('<span class="tc-name">맥브<br></span>', '<span class="tc-name">맥브라이드<br>표</span>')
    line = line.replace('<span class="tc-name">급별 <br>(기)</span>', '<span class="tc-name">장해급별 기준<br>(기본)</span>')
    line = line.replace('<span class="tc-name">붃급수</span>', '<span class="tc-name">부상급수표</span>')
    line = line.replace('<span class="tc-name">KCD<br>질병분류</span>', '<span class="tc-name">KCD-9<br>질병분류표</span>')
    line = line.replace('<span class="tc-name">물형<br>분류</span>', '<span class="tc-name">신생물 형태<br>분류표</span>')
    line = line.replace('<span class="tc-name">차사<br>과실비율</span>', '<span class="tc-name">자동차사고<br>과실비율</span>')
    line = line.replace('<span class="tc-name"> <br>분류</span>', '<span class="tc-name">직업 직무<br>분류표</span>')

    line = line.replace('<h2 class="section-title sec-title-cases">  / 조정</h2>', '<h2 class="section-title sec-title-cases">판례 / 조정사례</h2>')
    line = line.replace('<strong>법원 </strong>', '<strong>법원 판례</strong>')
    line = line.replace('<span>보험·배상 괠 </span>', '<span>보험 및 배상책임 관련 판례</span>')
    line = line.replace('<strong>금융감독 조정</strong>', '<strong>금융감독원 조정사례</strong>')
    line = line.replace('<span>금감 분쟁조정 </span>', '<span>금감원 분쟁조정 사례</span>')

    line = line.replace('<h2 class="section-title sec-title-medical"> 료자 / 감정</h2>', '<h2 class="section-title sec-title-medical">의료자문 / 신체감정</h2>')
    line = line.replace('<strong>료자</strong>', '<strong>의료자문</strong>')
    line = line.replace('<span>문의  뢰·</span>', '<span>전문의 소견 의뢰 및 결과</span>')
    line = line.replace('<strong>감정</strong>', '<strong>신체감정</strong>')
    line = line.replace('<span> 감정  진행</span>', '<span>법원 신체감정 진행 현황</span>')

    # Views headers
    line = line.replace('<h2 class="sub-header-title">분류 - 갞  </h2>', '<h2 class="sub-header-title">장해분류표 - 계약일자별 기준</h2>')
    line = line.replace('<p class="disability-desc">보험 갞 (계약)   분류 괝 릅니.  기간  주세.</p>', '<p class="disability-desc">보험 계약일자에 따라 장해분류표가 다르게 적용됩니다. 해당 기간을 선택해 주세요.</p>')
    line = line.replace('최신 (18.04 )', '최신 (18.04 이후)')
    line = line.replace('명보 99.02 ~ 05.04', '생명보험 99.02 ~ 05.04')
    line = line.replace('명보 (1995.02.01 ~ 1999.01.31)', '생명보험 95.02 ~ 99.01')
    line = line.replace('명보 95.02 ~ 99.01', '생명보험 95.02 ~ 99.01')
    line = line.replace('명보 83.10 ~ 95.01', '생명보험 83.10 ~ 95.01')
    line = line.replace('보험 98.07 ~ 05.03', '손해보험 98.07 ~ 05.03')
    line = line.replace('보험 98.07 ', '손해보험 98.07 이전')
    
    line = line.replace('<h2 class="sub-header-title" id="dt-title">분류(개인보험)</h2>', '<h2 class="sub-header-title" id="dt-title">장해분류표(개인보험)</h2>')
    line = line.replace('<p class="disability-desc" id="dt-desc">  붜    급률(%)    .</p>', '<p class="disability-desc" id="dt-desc">각 부위별 상세 장해 판정 기준 및 지급률(%)을 확인하세요.</p>')
    line = line.replace(' 급표', '장해 급수표')
    line = line.replace('붜 급표', '부위별 장해표')
    line = line.replace('   기', '세부 판정 기준')

    line = line.replace('<h2 class="sub-header-title">맥브 </h2>', '<h2 class="sub-header-title">맥브라이드 장해평가표</h2>')
    line = line.replace('placeholder="맥브  찾기 (: , 골절 )"', 'placeholder="맥브라이드 장해 찾기 (예: 경추, 골절 등)"')
    line = line.replace('  보기', '전체 목록 보기')
    line = line.replace('증상 찾기', '증상별 찾기')
    line = line.replace('1)  붜 ', '1) 손상 부위 선택')
    line = line.replace('2)  붜 ', '2) 세부 부위 선택')
    line = line.replace('3)  증상 ', '3) 세부 증상 선택')
    line = line.replace('붜 ', '손상 부위')
    
    line = line.replace('<h2 class="sub-header-title">보험 </h2>', '<h2 class="sub-header-title">보험사 정보 조회</h2>')
    line = line.replace('<p class="disability-desc"> 보험   , 기우 주소,   구양 .</p>', '<p class="disability-desc">각 보험회사의 청구 팩스, 등기우편 주소, 약관 및 청구양식을 확인하세요.</p>')
    line = line.replace('placeholder="보험 것 (초성 것 갊,  : )"', 'placeholder="보험사를 검색하세요 (초성 검색 가능, 예: ㅅㅅㅎㅈ)"')

    line = line.replace('<h2 class="sub-header-title">KCD 질병분류 (9)</h2>', '<h2 class="sub-header-title">KCD-9 질병분류표</h2>')
    line = line.replace('placeholder="질병코드  질병명을 "', 'placeholder="질병코드 또는 질병명을 입력하세요"')
    
    line = line.replace('<h2 class="sub-header-title"> 분류</h2>', '<h2 class="sub-header-title">신생물 형태분류표</h2>')
    line = line.replace('placeholder="질병코드  질병명을  (: M8010/0, )"', 'placeholder="질병코드 또는 질병명을 입력하세요 (예: M8010/0, 선종)"')
    
    line = line.replace('title=" "', 'title="맨 위로"')
    
    # Catch any remaining weird characters and replace with generic placeholders if needed
    import re
    line = re.sub(r'[^\x00-\x7F가-힣<>/="\'\-\.,\(\)\s:;!_]', '', line)

    lines[i] = line

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Recovered index.html to UTF-8 with Korean text!")
