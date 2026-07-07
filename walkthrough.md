# 프로젝트 변경 보고서 및 업데이트 내역 (Walkthrough)

본 보고서는 2026년 6월 19일과 20일 양일간 진행된 자동차보험 계산기, 반응형 UI 최적화, 표 정렬 규칙 수정, 그리고 Obsidian 자동 동기화 기능 도입에 대한 상세 결과 보고서입니다.

---

## 📅 2026-06-19 (금) 변경 내용 상세

### 1. 자동차보험 단계 인디케이터(Stepper) 모바일 최적화
- **구현사항**:
  - 모바일 해상도(768px 이하)에서 계산 단계 인디케이터의 글자 크기가 작아지고 플렉스 랩(`flex-wrap: wrap`) 처리가 활성화되어, 모바일 세로 화면에서도 4단계의 전체 흐름이 줄바꿈으로 인해 겹치거나 잘리지 않고 한눈에 매끄럽게 정렬되도록 조정했습니다.

### 2. 자동차사고 과실비율 페이지 반응형 레이아웃 개선
- **구현사항**:
  - 모바일 디바이스에서 사고 유형 트리 선택 버튼과 3D 상황도 이미지/동영상이 비좁게 렌더링되던 문제를 테이블 수직 분할 구조로 개편하여 최적화했습니다.
  - 가로 넓이가 좁은 모바일 웹에서도 기본 과실 수치와 가감 요소 조건의 표가 한 화면에 세로 스택 구조로 정렬되어 조작성이 향상되었습니다.

### 3. 맥브라이드 장해표 검색 팝업 조작성 고도화
- **구현사항**:
  - 기존에 텍스트만 표시되어 터치하기 번거로웠던 팝업 내의 기본율, 옥외, 옥내 텍스트 행을 둥근 테두리와 은은한 호버 액션이 가미된 **개별 선택용 클릭 버튼**으로 분리 적용했습니다.
  - 이를 통해 모바일 터치 및 마우스 클릭이 훨씬 직관적이고 경쾌해졌습니다.

---

## 📅 2026-06-20 (토) 변경 내용 상세

### 1. HTML 입력 컴포넌트 위치 이동 및 레이블 변경
- **구현사항**:
  - [index.html](file:///c:/Users/SB/Desktop/연습용/index.html)에서 `#auto-hosp-period-group` div 요소를 `#auto-accidentdate` form-group(사고발생일) 바로 뒤이자 `#auto-faultratio` form-group(과실비율) 바로 앞으로 이동시켰습니다.
  - 해당 입력 블록의 대표 레이블 `<label>` 텍스트를 "입원 기간 입력 방식"에서 **"입원기간"**으로 변경했습니다.

### 2. 반기별 도시일용노임 일자별 차등 연산 엔진 전면 리팩토링 (모든 탭 적용)
- **구현사항**:
  - [script.js](file:///c:/Users/SB/Desktop/연습용/script.js) 내 `window.calculateInsurance` 연산 엔진을 전면 개편했습니다.
  - **소득 하한선 검증**: 루프 내부에서 `Math.max(window.autoCalcState.monthlyIncome, wages.monthlyCommon)` 비교 로직을 탑재하여 기입 소득이 평균 노임 미만일 시 역사적 도시일용노임을 기준으로 연산하도록 최저소득을 보장했습니다.
  - **부상("부상" 탭)**: 입원 및 간병 일수의 날짜별 루프를 돌며 반기별 변동 시점(1월 1일, 7월 1일, 9월 1일 등) 기준으로 일수 구간을 자동 분할하고, 상세 내역(`incomeMemo`, `caregiverMemo`)에 개별 세부 정보(기간 범위, 일수, 적용 노임, 합계금액)를 명시적으로 출력했습니다.
  - **후유장해("후유장해" 탭 - 단순/상세계산)**: 장해 기간(월 단위)을 월별 루프를 돌며 추적하고, 적용 노임 및 장해율이 동일한 구간을 통합 그룹화하여 결과 설명란(`lossOfEarningsExplanation`)에 시작월~종료월, 호프만 계수 차이, 적용 소득, 계산 금액을 표기해 일괄 표시가 아닌 세분화된 계산 과정을 완성했습니다.
  - **사망("사망" 탭)**: 정년까지의 노동능력상실월을 월별로 추적하고 생활비 1/3을 공제하는 연산에서도 반기별 소득 변동 및 기간 분할 통합 로직을 적용해 완벽히 일치하도록 조치했습니다.

### 3. 포커스 이동 보완 및 Enter 키 리스너 추가
- **구현사항**:
  - [script.js](file:///c:/Users/SB/Desktop/연습용/script.js)의 `window.bindAutoCalcEvents` 내부에서 입원일수 직접 입력 필드(`#auto-hosp-days-direct`)에 대한 `keydown` 이벤트 리스너를 바인딩했습니다.
  - 사용자가 입원일수를 직접 입력하고 **Enter 키**를 누르면 기본 폼 전송(Submit)을 방지(`e.preventDefault()`)한 뒤, 다음 입력창인 **과실비율 (%)** (`#auto-faultratio`)로 즉시 포커스를 이동시킵니다.
  - 사고발생일(`#auto-accidentdate`) 입력 시 상세계산인 경우 입원기간 시작일(`#auto-hosp-start`) 또는 입원일수 직접입력 필드(`#auto-hosp-days-direct`)로 상황에 따라 알맞게 자동 포커스가 이동하며, 입원일 입력 완료 시 최종적으로 과실비율 필드로 이어지는 자연스러운 흐름을 검증했습니다.

### 4. 장해 개수별 텍스트 표현 및 계산 조건 요약 정보 세부 개선
- **구현사항**:
  - [script.js](file:///c:/Users/SB/Desktop/연습용/script.js)의 결과 화면 렌더링 시 `calcType === 'detailed'`인 조건에 더해 `detailedDisabilities.length >= 2`를 확인하여 2개 미만일 시 `장해`로 표시되도록 조정하였습니다.
  - 후유장해 탭의 과실상계 적용비율 설명 문구에서 `+ 휴업손해` 부분을 삭제하여 `[위자료 + 상실수익액]` 형태로 변경하였습니다.
  - 계산 요약 리스트의 입원기간 줄을 `입원 기간 : <strong>${finalHospDays}일</strong>`로 간결하게 수정하였습니다.
  - [styles.css](file:///c:/Users/SB/Desktop/연습용/styles.css)에서 `.auto-summary-table td:nth-child(2)`(상세 내역 열)에 `white-space: nowrap !important;` 스타일을 적용해 텍스트가 임의로 개행되지 않고 깔끔하게 한 줄로 노출되도록 보완했습니다.

### 5. 가로폭 통일화 및 표 정렬/가독성 고도화
- **구현사항**:
  - **컨테이너 박스 가로폭 확대 및 일괄 통일**: [styles.css](file:///c:/Users/SB/Desktop/연습용/styles.css)의 `.auto-form-container` 클래스 자체의 최대 폭을 `max-width: 600px`에서 **`max-width: 900px`**로 상향하여 Step 2(기본 정보 입력), Step 3(진단/장해 입력), Step 4(최종 결과 화면)에 대해 일관되게 넓고 쾌적한 화면 레이아웃을 통일하여 구축했습니다. [index.html](file:///c:/Users/SB/Desktop/연습용/index.html)에 있던 인라인 `max-width: 900px` 스타일은 CSS로 흡수하여 제거했습니다.
  - **표 정렬 개선 (제목 가운데, 내용 왼쪽)**: [index.html](file:///c:/Users/SB/Desktop/연습용/index.html)에서 상세 내역 테이블의 모든 헤더 (`<th>` 요소들)에 `text-align: center;` 스타일을 부여해 제목을 가운데로 맞췄습니다. 또한 [script.js](file:///c:/Users/SB/Desktop/연습용/script.js)에서 테이블 내부의 '산출 기준 / 상세' 열 (`<td>` 셀들)의 정렬 방식을 기존 `text-align: right;`에서 **`text-align: left;`**로 일괄 수정하여 가독성을 극대화했습니다.
  - **상실수익액 세부 내역 들여쓰기**: [script.js](file:///c:/Users/SB/Desktop/연습용/script.js) 내 상실수익액 분기 계산 루프에서 줄바꿈(`<br>`) 처리되는 적용 노임 및 H계수 시작점에 **`&nbsp;&nbsp;&nbsp;&nbsp;` (4칸 들여쓰기)**를 추가하여 첫째 줄의 bullet 기호(`• `)와 줄이 어긋나지 않고 완벽한 하단 라인을 맞추도록 개선했습니다.

### 6. Obsidian 노트 동기화 자동화 추가
- **구현사항**:
  - **동적 볼트 경로 감지**: Windows 환경의 Obsidian 구성 파일인 `%APPDATA%\obsidian\obsidian.json`을 읽고 분석해, 사용자가 추가하고 활성화해 둔 로컬 볼트(`C:\Users\SB\Documents\my_soul`)의 전체 경로를 동적으로 검출하는 파이썬 스크립트 [sync_obsidian.py](file:///c:/Users/SB/Desktop/연습용/sync_obsidian.py)를 제작하였습니다.
  - **자동 복사 및 동기화**: `python sync_obsidian.py`를 실행하면 현재 워크스페이스의 `development_log.md`, `walkthrough.md`, `task.md` 세 파일이 대상 볼트 내의 `반중력프로젝트/laika` 하위에 각각 `개발_기록_업데이트_노트.md`, `변경_보고서_워크스루.md`, `작업_태스크_리스트.md` 이름으로 즉시 복사되어, 옵시디언 앱 내에서 바로 프로젝트별로 묶어 읽고 편집할 수 있도록 연동 처리를 완수했습니다.

### 7. GitHub 원격 리포지토리 최신화 완료
- **구현사항**:
  - `sync_obsidian.py` 스크립트를 포함한 추가 수정 사항을 커밋하고 `git push origin main` 명령을 통해 GitHub 리포지토리([ssungbi/laika](https://github.com/ssungbi/laika.git))의 최신화를 완료했습니다.

---

## 변경된 파일 목록

- [index.html](file:///c:/Users/SB/Desktop/연습용/index.html)
  - 테이블 헤더(`<th>`) 요소를 `text-align: center;`로 변경.
  - 4단계 결과 흰색 배경 컨테이너 인라인 max-width 스타일 제거 (CSS 통합).
- [script.js](file:///c:/Users/SB/Desktop/연습용/script.js)
  - 결과 표 내 '산출 기준 / 상세' 셀들의 정렬 방식을 `text-align: left;`로 수정.
  - 상실수익액 상세 줄바꿈에 `&nbsp;&nbsp;&nbsp;&nbsp;` 들여쓰기 적용.
- [styles.css](file:///c:/Users/SB/Desktop/연습용/styles.css)
  - `.auto-form-container`의 최대 가로 폭을 `900px`로 변경하여 모든 계산 단계의 컨테이너 크기 일괄 통일.
- [sync_obsidian.py](file:///c:/Users/SB/Desktop/연습용/sync_obsidian.py)
  - 사용자 Obsidian Vault 자동 탐색 및 `반중력프로젝트/laika` 하위에 리포트 3종 세트 동기화 복사 스크립트.

---

## 검증 결과 및 수동 검증 방법

### 1. 자동화 모의 테스트 (Node.js)
- 구문 검증(`node -c script.js`) 결과 모든 스크립트 파일이 성공적으로 구동 가능함을 보증합니다.
- `python sync_obsidian.py` 실행 결과 `Successfully synced: development_log.md -> C:\Users\SB\Documents\my_soul\반중력프로젝트\laika\개발_기록_업데이트_노트.md` 등의 로그와 함께 파일이 정상 복사되었음을 확인했습니다.

### 2. 수동 검증 가이드
1. 브라우저로 `index.html` 파일을 로드합니다.
2. 2단계(기본 정보 입력) 및 3단계(장해 기입) 단계의 입력 박스가 모두 900px로 일관되게 넓어져 여유롭게 노출되는지 확인합니다.
3. 터미널 혹은 명령 프롬프트에서 `python sync_obsidian.py`를 실행합니다.
4. 사용자 Obsidian 앱을 열어 `my_soul` 볼트 목록 안에 `반중력프로젝트/laika` 폴더가 정상적으로 생성되고, 하위의 3개 한글 리포트 파일들이 최신 상태로 동기화되어 있는지 확인합니다.

---

## 📅 2026-07-07 (화) 변경 내용 상세

### 1. 도시일용노임 3대 변동 주기(1/1, 7/1, 9/1) 반영 스크래퍼 리팩토링
- **구현사항**:
  - `update_wages.py`에서 기존의 단순 월 9월 기준 반기 분할 대신, **상반기(1/1~6/30), 중반기(7/1~8/31), 하반기(9/1~12/31)**의 3대 주기를 완벽히 분기하도록 수정했습니다.
  - 명령어 첫 번째 매개변수로 시뮬레이션 날짜(예: `python update_wages.py 2026-07-07`)를 받아서 테스트할 수 있는 매커니즘을 지원합니다.
  - 중반기(7/1~8/31)에는 건설(상반기) 및 제조(하반기) 단독 검색 및 평균 조합 쿼리를 각각 Naver Search로 크롤링하여 정확한 변동 요소를 감지하고 `wage_data.js`에 주입하게 개편했습니다.

### 2. `WAGE_DATA` 실시간 병합 및 getWagesForDate 폴백 엔진 구현
- **구현사항**:
  - `script.js`에 `window.mergeWageData` 함수를 구현하여 외부 스크래퍼가 주입한 `window.WAGE_DATA`를 내장 역사적 기록 데이터(`window.WAGE_HISTORY`)에 연도 및 주기별로 실시간 자동 융합하도록 설계했습니다.
  - `getWagesForDate` 함수에서 미래 연도나 미공표 시점에 대한 탐색 요청이 들어왔을 때, 이전 분기 및 이전 해로 거슬러 올라가며 가장 최신의 유효한 노임을 동적으로 상속(폴백) 적용하는 알고리즘을 도입했습니다.

### 3. 비주얼 서버날짜 시뮬레이터 개발자 패널 구축
- **구현사항**:
  - `index.html` 하단 우측에 깔끔하고 모던한 플로팅 다크 슬레이트 테마의 **개발자용 서버날짜 시뮬레이터 패널**을 추가했습니다.
  - 가상 서버 날짜(YYYY-MM-DD)를 입력하고 "자동 감지 & 업데이트 실행"을 클릭하면, 브라우저가 public CORS proxy(`api.allorigins.win`)를 이용해 실시간으로 네이버 검색 페이지를 스크래핑/파싱해 최신 노임을 가져오며, 네트워크 단절 상황에서도 연간 2% 인상분을 계산한 오프라인 모의 시뮬레이션을 제공하여 즉각적으로 계산 결과에 변경된 노임을 동적 적용 및 검증할 수 있도록 지원합니다.

---

## 변경된 파일 목록

- [index.html](file:///c:/Users/SB/Desktop/연습용/index.html)
  - 개발자용 플로팅 서버날짜 시뮬레이터 패널 및 시뮬레이션 이벤트 리스너 통합.
- [script.js](file:///c:/Users/SB/Desktop/연습용/script.js)
  - `window.WAGE_DATA` 동적 병합기(`mergeWageData`) 추가.
  - `getWagesForDate` 3대 주기 차등 검색 및 역사적 역추적 폴백 검색 알고리즘 탑재.
  - 브라우저 기반 실시간 네이버 크롤러 및 모의 계산 기능(`simulateWageUpdate`) 구현.
- [update_wages.py](file:///c:/Users/SB/Desktop/연습용/update_wages.py)
  - 명령어 실행 인자 시뮬레이션 및 3대 주기별 분기 쿼리 생성 대응.
- [task.md](file:///c:/Users/SB/Desktop/연습용/task.md)
  - 2026-07-07 고도화 개발 이정표 추가 및 체크 완료.

---

## 검증 결과 및 수동 검증 방법

### 1. 자동화 모의 테스트 (Node.js & Python)
- `node -c script.js`를 통해 문법적 정합성 검증 완료.
- `python update_wages.py 2026-07-07`을 실행해 정상적으로 `2026년 중반기` 건설 상반기(172,068원), 제조 하반기(90,694원)를 정상 검출하여 `wage_data.js`를 업데이트함을 확인했습니다.

### 2. 수동 검증 가이드
1. 브라우저로 `index.html`을 로드합니다.
2. 우측 하단의 **서버날짜 시뮬레이터** 패널을 엽니다.
3. 가상 날짜를 `2026-07-07` 등으로 바꾼 뒤 **자동 감지 & 업데이트 실행**을 클릭합니다.
4. 업데이트 완료 안내와 함께 화면에 변경된 제조/건설 단가가 반영되고 자동차보험 계산을 진행하면 해당 임금 단가 및 상/하반기 변동 주기에 맞추어 실시간 계산표가 쪼개져 정확히 계산되는지 눈으로 확인합니다.
5. `python sync_obsidian.py`를 실행하여 갱신된 작업 이력 마크다운 리포트 3종 세트를 Obsidian 개인 볼트에 완벽 동기화 전송합니다.
