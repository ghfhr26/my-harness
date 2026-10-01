# 01-references: 자산 제출 화면 레퍼런스

수집 도구: uibowl MCP (search_ui_patterns, search_by_ocr_text). 앱 이름과 ui_url은 검색 결과 값 그대로 사용. 각 항목의 구성 설명은 화면 이미지를 직접 보고 적었다. 무료 등급 한도로 검색당 대표 화면 1장씩만 직접 확인했다.

## 업로드·등록 폼
- 수현이랑 | https://uibowl.io/name/%EC%88%98%ED%98%84%EC%9D%B4%EB%9E%91?patterns=%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B0&patternName=%EA%B3%B5%EC%9C%A0%20%EC%95%A8%EB%B2%94%20%EC%97%85%EB%A1%9C%EB%93%9C
  - 공유 앨범 업로드. 상단 "업로드" 타이틀과 닫기(X), 칩 선택(성별·인원수), 제목 입력(13/30 글자수), 설명(선택) 입력(15/200), 하단 고정 풀폭 "완료" 버튼.
- 다글로 | https://uibowl.io/name/%EB%8B%A4%EA%B8%80%EB%A1%9C?patterns=%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B0&patternName=%EC%9C%A0%ED%8A%9C%EB%B8%8C%20%EB%A7%81%ED%81%AC%20%EC%97%85%EB%A1%9C%EB%93%9C
  - 유튜브 링크 업로드. URL 입력창과 이동 버튼, 언어·주제 행(우측 값과 쉐브론), 화자표시 토글, 하단 "받아쓰기" 버튼은 입력 전 비활성(회색).
- 키피럽 | https://uibowl.io/name/%ED%82%A4%ED%94%BC%EB%9F%BD?patterns=%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B0&patternName=%EC%9D%B8%EC%A6%9D%EC%83%B7-%EC%97%85%EB%A1%9C%EB%93%9C
  - 인증샷 업로드. 어두운 배경의 카메라 화면, 안내 문구, 갤러리/촬영/전환 버튼 3개 하단 배치. 업로드 입력 수단 선택 참고용.
- 달다방 | https://uibowl.io/name/%EB%8B%AC%EB%8B%A4%EB%B0%A9?patterns=%EA%B8%80%EC%93%B0%EA%B8%B0
  - 글쓰기. 게시판 선택 드롭다운, 제목, "상품 선택" 버튼과 "선택된 상품이 없어요" 빈 상태, 서식 툴바가 있는 본문, 하단 "임시저장"(아웃라인)과 "저장"(채움) 2버튼.
- 럽맘 | https://uibowl.io/name/%EB%9F%BD%EB%A7%98?patterns=%EA%B8%80%EC%93%B0%EA%B8%B0&patternName=%EA%B3%A0%EB%AF%BC%EA%B8%80%20%EC%9E%91%EC%84%B1%ED%95%98%EA%B8%B0
  - 고민글 작성. 상단 단계 진행바(2/3), 큰 제목과 보조 설명, 필수(*) 표시 선택 필드, 선택 시 하단 바텀시트 목록. 다단계 등록 구조 참고용.
- 닥터다이어리 | https://uibowl.io/name/%EB%8B%A5%ED%84%B0%EB%8B%A4%EC%9D%B4%EC%96%B4%EB%A6%AC?patterns=%EA%B8%80%EC%93%B0%EA%B8%B0&patternName=%EA%B0%90%EC%A0%95%EC%9D%BC%EA%B8%B0
  - 감정일기 작성. 진입 화면은 그라데이션 배경에 큰 타이틀, 캐릭터 이미지, 하단 비활성 버튼. 바텀시트·토글 포함 6화면 플로우.

## 판매 등록·상품 등록
- 차란 | https://uibowl.io/name/%EC%B0%A8%EB%9E%80?patterns=%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B0&patternName=%EC%A7%81%EC%A0%91%ED%8C%90%EB%A7%A4%20%EC%83%81%ED%92%88%EB%93%B1%EB%A1%9D
  - 직접판매 상품등록(10화면). 첫 화면은 "어떻게 상품을 등록할까요?" 질문과 2x2 예시 카드(전체샷·라벨 등), 보라색 풀폭 "사진으로 등록하기" 버튼, "또는" 구분선 뒤 링크 가져오기 입력, 하단 작은 안내 문구, 우상단 "상품관리" 링크.
- 빼기 | https://uibowl.io/name/%EB%B9%BC%EA%B8%B0?patterns=%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B0&patternName=%EC%83%81%ED%92%88%20%EB%93%B1%EB%A1%9D
  - 중고거래 목록 화면에 우하단 플로팅 "+ 상품 등록" 버튼, 하단 5탭 내비게이션. 등록 진입점 위치 참고용.
- 코오롱몰 | https://uibowl.io/name/%EC%BD%94%EC%98%A4%EB%A1%B1%EB%AA%B0?patterns=%EA%B8%B0%ED%9A%8D%EC%A0%84%C2%B7%EC%9D%B4%EB%B2%A4%ED%8A%B8&imgId=cms35mxas0005jp046ycm9ij1
  - 릴레이 마켓 소개 화면. "검수한 뒤 재판매" 설명 문구, 검정 풀폭 "안입는 옷 판매하러가기" CTA. 판매 신청 진입과 검수 안내 문구 참고용.

## 공개 범위 선택
- 네이버블로그 | https://uibowl.io/name/%EB%84%A4%EC%9D%B4%EB%B2%84%EB%B8%94%EB%A1%9C%EA%B7%B8?patterns=%EA%B8%80%EC%93%B0%EA%B8%B0&imgId=cmumdwlmc000ajm04oqk75d8l
  - 발행 옵션 바텀시트. "공개 설정" 행에 전체/이웃/서로이웃/비공개 4분할 세그먼트 컨트롤(전체 선택 상태, 초록 채움), 아래에 "이 설정을 기본값으로 저장" 토글. 공개 범위 컨트롤의 직접 참고용.
- 배달의민족 | https://uibowl.io/name/%EB%B0%B0%EB%8B%AC%EC%9D%98%EB%AF%BC%EC%A1%B1?patterns=%EB%A6%AC%EB%B7%B0%EC%93%B0%EA%B8%B0&imgId=cmni8t8yr0009ih04e99o23ab
  - 리뷰쓰기 2/2. 별점, 사진 첨부 버튼, 텍스트 입력, "사장님에게만 보이기"와 "메뉴 비공개" 체크박스(물음표 툴팁), 하단 검정 "완료" 버튼. 비공개 옵션의 체크박스 방식 참고용.
- 쑥쑥찰칵 | https://uibowl.io/name/%EC%91%A5%EC%91%A5%EC%B0%B0%EC%B9%B5?patterns=%EC%84%A4%EC%A0%95&imgId=cmub7kwx2000njs04uwzytdex
  - 가족 설정. 카드형 리스트에서 "댓글 공개 범위" 행이 현재 값(엄마 가족·아빠 가족)과 쉐브론을 표시.
- 셀레트립 | https://uibowl.io/name/%EC%85%80%EB%A0%88%ED%8A%B8%EB%A6%BD?patterns=%EC%84%A4%EC%A0%95&imgId=cmqp088u8000hl504m30sar67
  - 여행 설정. 라벨(굵게)과 값을 두 줄로 쌓은 행 목록, "공개 범위" 행의 현재 값이 "비공개", 하단 "여행 삭제" 텍스트 링크.
- 투두메이트 | https://uibowl.io/name/%ED%88%AC%EB%91%90%EB%A9%94%EC%9D%B4%ED%8A%B8?patterns=%EC%84%A4%EC%A0%95&imgId=cmpjgotde006wlg04n8w5gy5p
  - 개인정보 보호 설정. 섹션 제목(팔로우·게시물·대화)별로 행 + 우측 현재값("모든 사람") + 설명 문구, 상단 팔로우 토글. 공개 범위 설정의 섹션·설명 구조 참고용.

## 검수·신청 상태
- 조앤헤일리 | https://uibowl.io/name/%EC%A1%B0%EC%95%A4%ED%97%A4%EC%9D%BC%EB%A6%AC?patterns=%EC%8B%A0%EC%B2%AD%ED%95%98%EA%B8%B0&imgId=cmobg7l9d0003jo04anqgaya9
  - 사진 검수 신청(7화면). "가이드를 참고해 사진 1장을 등록해주세요" 제목, "모든 사진은 안심 검수 후 등록되며 진행 상황은 내 정보함에서 확인" 안내, 사진 추가 박스, 하단 비활성 "등록하기" 버튼. 검수 상태 안내 문구 참고용.
- 히로인스 | https://uibowl.io/name/%ED%9E%88%EB%A1%9C%EC%9D%B8%EC%8A%A4?patterns=%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC&imgId=cmqgalklz00ozld048zjpqf63
  - 쇼핑일기 안내. 보라 그라데이션 헤더, 알약형 안내 배지, "검수 통과하기" 조건 설명, 하단 검정 "확인했어요" 버튼.

## 집계
총 항목은 16개이다.
제외한 앱은 iM뱅크(관심상품 등록, 주제 부적합)와 Kia, 아이쿠카, 마미톡(신청 폼이나 자산 제출과 무관)이다.
