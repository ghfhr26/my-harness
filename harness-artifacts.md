# 하네스 산출물 (R4)

## 폴더 규칙
- 모든 산출물은 work/<주제>/ 아래에 둔다 (실행마다 주제별 폴더)

## 단계별 파일
| 단계 | 파일 | 형식 |
|---|---|---|
| S1 | 01-references.md | 앱 이름 + ui_url 목록 |
| S2 | 02-analysis.md | 분석 결과 + 반영할 부분 |
| S3 | 03-keyscreens.md | Figma 링크 + 프레임 3개의 node id와 크기 |
| S3 | 03-screens/*.png | 키스크린 3개 내보내기 (승인자가 보는 자료) |
| 승인 | approval.md | 승인자, 날짜, 결정(승인/거절) |
| S4 | 04-tokens.json, 04-components.md | 사용한 토큰·컴포넌트 목록 |
| S5 | 05-review.json | 위반 항목 목록과 건수 |
| 상태 | state.json | 현재 단계, 구간별 복귀 횟수 |

## 규칙 SSOT
- 파일: rules.json (프로젝트 루트, 1개)
- 판정 스크립트는 이 파일만 읽는다
- 원본은 design.md. rules.json은 스크립트용 사본이며 항목마다 design.md 줄 번호를 남긴다
- 둘이 어긋나면 design.md가 우선한다

## 재개
- 가능. state.json의 현재 단계부터 이어서 실행한다
- 앞 단계 산출물이 있으면 다시 만들지 않는다

## Figma 기록
- S3·S4 결과는 Figma에 그리고, 링크·node id·크기를 위 파일에 기록한다
- 판정은 이 기록을 기준으로 한다
- 기록이 Figma 실제 상태와 일치하는지는 읽기 전용 판정자가 Figma에서 확인한다

## approval.md 권한
- 사람만 쓴다. 에이전트는 쓸 수 없다
- 파일이 없거나 결정이 "승인"이 아니면 S4를 시작하지 못한다
