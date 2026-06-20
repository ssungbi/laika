# 개발 태스크 리스트

- [x] 1. index.html 내 입원기간 필드(#auto-hosp-period-group) 위치 이동 및 레이블 변경 ("입원기간")
- [x] 2. script.js 내 window.calculateInsurance 리팩토링 (부상, 후유장해, 사망에 대한 반기별 노임 차등 세분화 루프 설계 및 소득 하한선 적용)
- [x] 3. script.js 내 포커스 이동 보완 및 직접 입력 필드(#auto-hosp-days-direct) Enter 키 핸들러 추가
- [x] 4. 구문 검증 및 수동 동작 확인

## 추가 피드백 보완 사항
- [x] 상세계산에서 장해를 2개 이상 추가하지 않았을 때 '중복장해'가 아니라 '장해'로 조건부 텍스트 출력 분기
- [x] 후유장해 과실상계 비율 설명 텍스트에서 '휴업손해' 단어 제거 (`[위자료 + 상실수익액]`)
- [x] 입원 기간 표시 형식을 '입원 기간 : 30일' 포맷으로 간결화
- [x] 위자료 상세 기준 텍스트가 줄바꿈되지 않도록 `styles.css` 내 상세 내역 열(`td:nth-child(2)`) `white-space: nowrap` 적용
- [x] 계산 금액 열의 금액이 줄바꿈되어 밀리지 않도록 `styles.css` 내 `th:last-child, td:last-child`에 `white-space: nowrap !important` 적용 및 `index.html` 내 헤더 `min-width: 140px` 조정
- [x] 결과 화면 흰색 배경 폭(`max-width`)을 기존 700px에서 **900px**로 확대하여 가로 공간과 내부 표 레이아웃에 여유 제공
- [x] 모든 계산 단계(Step 2, Step 3, Step 4)의 흰색 컨테이너 배경 최대 가로폭(`max-width`)을 **900px**로 일괄 통일하여 여유 공간 제공
- [x] 상세 내역 표의 제목(헤더)을 **가운데 정렬(`text-align: center;`)**로, 행 내용들은 **왼쪽 정렬(`text-align: left;`)**로 통일하여 가독성 강화
- [x] 상실수익액 산출 내역에서 줄바꿈된 두 번째 줄(월 적용노임 및 H계수 시작 지점)에 **들여쓰기(`&nbsp;&nbsp;&nbsp;&nbsp;`)** 적용
- [x] 프로젝트 개발 통합 기록 문서(`development_log.md`)를 작성하여 워크스페이스에 통합
- [x] 사용자의 PC 환경 내 Obsidian 설정(`obsidian.json`)을 자동으로 찾아 활성 볼트(`my_soul`) 내 **`반중력프로젝트`** 폴더 하위로 개발 로그, 워크스루, 태스크 등 3대 산출물 파일을 동적 복사 및 동기화해 주는 **자동 싱크 스크립트(`sync_obsidian.py`)** 구현 및 즉시 동기화 구동
- [x] GitHub 원격 리포지토리 최신화 완료 (`git push origin main`)
