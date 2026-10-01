# 하네스 역할 (R6)

## 역할
| 역할 | 하는 일 | 편집 가능 폴더 | 도구 |
|---|---|---|---|
| researcher | S1 수집, S2 분석·반영안 | work/<주제>/01-*, 02-* | uibowl MCP, 읽기 |
| designer | S3 키스크린, S4 토큰·컴포넌트 | work/<주제>/03-*, 04-* | Figma MCP, 쓰기 |
| judge (읽기 전용) | G1~G5 판정, S5 위반 검토 | 쓰기 없음 | Read, 판정 스크립트 실행, Figma 읽기 |
| 사람 | 승인 | approval.md만 | |

- 에이전트별 편집 폴더는 1개씩이고 서로 겹치지 않는다.
- state.json은 오케스트레이터(메인 Claude)만 갱신한다.
- rules.json, design.md, prd.md, scripts/는 모든 에이전트가 읽기 전용이다.

## 읽기 전용 강제
- judge는 Write/Edit 도구 없이 Read와 판정 스크립트 실행만 허용한다.
- 판정 스크립트(scripts/)가 05-review.json을 쓴다.
- scripts/는 에이전트가 수정하지 못한다. 판정자의 독립성을 유지하기 위해서다.

## approval.md 쓰기 차단
- .claude/settings.json의 permissions.deny에 approval.md 쓰기를 넣는다.
- 사람은 직접 파일을 편집해 승인한다.

## 자연어 트리거
| 말 | 동작 |
|---|---|
| "[주제] 시작해" | work/<주제>/ 생성, S1부터 실행 |
| "이어서 해" | state.json의 현재 단계부터 재개 |
| "검토해" | S5만 실행 |
| "상태 알려줘" | state.json과 게이트 통과 현황 출력 |

## 열린 항목 (R7에서 결정)
- 폴더 단위 쓰기 제한(researcher는 01·02만, designer는 03·04만)을 지침과 훅 중 무엇으로 보장할지
