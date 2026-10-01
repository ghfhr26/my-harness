# 04-components: 자산 제출 화면

Figma 프레임 2:2, 2:46, 2:91 (파일 Nj7ftjAjGvuiAR1DOcV1cC)에서 실제로 쓰인 컴포넌트다. Figma 변수·컴포넌트는 새로 만들지 않았고 승인된 03 프레임은 바꾸지 않았다.

| 컴포넌트 | 모서리 | 그림자 | 색상 | 용도 |
|---|---|---|---|---|
| button-primary | 9999px | 없음 | #141414 | 제출(활성), 판매 신청 화면 하단 CTA |
| button-outline | 9999px | 없음 | #e0e0e0 | 임시저장 |
| button-disabled | 9999px | 없음 | #f3f3f3 | 필수 입력 전 제출 비활성 |
| button-pill-soft | 9999px | 없음 | #ffffff | 파일 선택 |
| text-input | 16px | 없음 | #f0f0f0 | 제목, 설명 입력 |
| attach-dropzone | 16px | 없음 | #f0f0f0 | 파일 첨부 전 영역 |
| attached-file-row | 16px | 없음 | #f0f0f0 | 파일 첨부 후 행 (1px 아웃라인) |
| segmented-control | 9999px | 없음 | #f3f3f3 | 공개 범위 선택 (비공개/멤버 공개/판매 신청), 기본값:비공개 |
| segmented-control-active | 9999px | 없음 | #ffffff | 선택된 공개 범위 옵션 |
| status-badge | 9999px | 없음 | #f3f3f3 | 검수 상태 배지(임시저장, 검수 대기, 수정 요청, 승인됨, 반려) |
| status-badge-active | 9999px | 없음 | #141414 | 현재 검수 상태 |
| review-status-card | 24px | 없음 | #f3f3f3 | 검수 상태 영역과 안내 문구 |
| forbidden-notice-card | 24px | 없음 | #f0f0f0 | 금지 항목 안내 (1px 아웃라인) |
| asset-card | 24px | 없음 | #f0f0f0 | 내 자산 목록 카드 (1px 아웃라인) |
| floating-button | 9999px | 없음 | #141414 | + 새 자산 |

## 폰트 편차 (숨기지 않고 기록)
- 사용자 지시로 Pretendard가 아니라 Noto Sans KR을 썼다. Figma 환경에 Pretendard가 없다.
- 사용자 지시로 rules.json의 font.family가 Noto Sans KR로 바뀌어 G4를 통과했다(21:30:15). 04-tokens.json의 font 토큰 family는 처음부터 실제 사용 폰트인 Noto Sans KR로 적었다. rules.json은 내가 수정하지 않았다.
- 600 굵기 자리(17/600, 15/600, 12/600)는 Noto Sans KR에 SemiBold가 없어 Medium(500)으로 렌더링됐다. 토큰에는 design.md 의도인 600을 적고 usage에 대체 사실을 적었다.
