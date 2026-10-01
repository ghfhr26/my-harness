#!/usr/bin/env python3
"""T1~T7 (harness-verification.md) + 정상 입력 대조(T0). 입력은 임시 폴더에 생성한다.
사용: python tests/run_tests.py   (전부 기대대로면 종료 코드 0)
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def judge(work, gate):
    return subprocess.run([PY, str(ROOT / "scripts" / "judge.py"), str(work), gate], capture_output=True, text=True, encoding="utf-8", errors="replace").returncode


def judge_run(work, gate):
    return subprocess.run([PY, str(ROOT / "scripts" / "judge.py"), str(work), gate], capture_output=True, text=True, encoding="utf-8")


def guard(tool, agent=None, cwd=None, **tool_input):
    """훅 입력을 흉내 내어 guard.py의 종료 코드를 돌려준다. cwd는 일부러 프로젝트 하위로 줄 수 있다."""
    data = {"tool_name": tool, "tool_input": tool_input, "cwd": str(cwd or ROOT)}
    if agent:
        data["agent_type"] = agent
    return subprocess.run([PY, str(ROOT / "scripts" / "guard.py")], input=json.dumps(data), capture_output=True, text=True, encoding="utf-8").returncode


def state(work, *args):
    return subprocess.run([PY, str(ROOT / "scripts" / "state.py"), str(work), *args], capture_output=True, text=True, encoding="utf-8", errors="replace").returncode


def good_work(base):
    """모든 게이트를 통과하는 정상 입력."""
    w = Path(base)
    (w / "03-screens").mkdir(parents=True)
    for i in range(3):
        (w / "03-screens" / f"{i}.png").write_bytes(b"png")
    (w / "01-references.md").write_text("\n".join(f"- 앱{i} | https://uibowl.io/ui/{i}" for i in range(10)), encoding="utf-8")
    (w / "02-analysis.md").write_text("## 분석\n...\n## 반영할 부분\n- 자산 제출 흐름 반영 (§6-5)\n", encoding="utf-8")
    (w / "03-keyscreens.md").write_text(
        "| 화면 | 유형 | node_id | 너비 | 높이 | UI 요소 |\n|---|---|---|---|---|---|\n"
        "| 홈 | other | 1:1 | 390 | 844 | 카드 |\n"
        "| 제출 | asset-submit | 1:2 | 390 | 844 | 공개 범위 선택, 기본값:비공개 |\n"
        "| 판매신청 | sell-request | 1:3 | 390 | 844 | 검수 상태, 금지 항목 안내 |\n", encoding="utf-8")
    (w / "approval.md").write_text("결정: 승인\n승인자: 홍길동\n날짜: 2026-10-01\n", encoding="utf-8")
    (w / "04-tokens.json").write_text(json.dumps({"tokens": [
        {"name": "r-card", "type": "radius", "value": "24px"},
        {"name": "c-ink", "type": "color", "value": "#141414", "usage": "text"},
        {"name": "c-badge", "type": "color", "value": "#0066ff", "usage": "price-badge"},
        {"name": "s-md", "type": "spacing", "value": "16px"},
        {"name": "f-body", "type": "font", "value": {"family": "Noto Sans KR", "size": 15, "weight": 400}},
    ]}), encoding="utf-8")
    (w / "04-components.md").write_text(
        "| 컴포넌트 | 모서리 | 그림자 | 색상 | 용도 |\n|---|---|---|---|---|\n"
        "| button-primary | 9999px | 없음 | #141414 | cta |\n", encoding="utf-8")
    return w


def main():
    fails = []

    def check(name, got, want):
        ok = got == want
        print(f"{'PASS' if ok else 'FAIL'}  {name}  (결과 {got}, 기대 {want})")
        if not ok:
            fails.append(name)

    def fresh():
        d = tempfile.mkdtemp()
        return good_work(Path(d) / "w")

    w = fresh()
    check("T0 정상 입력: G1~G4, review, approval 모두 통과",
          [judge(w, g) for g in ("g1", "g2", "g3", "approval", "g4", "review")], [0] * 6)

    w = fresh()
    (w / "01-references.md").write_text("\n".join(f"- 앱{i} | https://uibowl.io/ui/{i}" for i in range(9)), encoding="utf-8")
    check("T1 링크 9개 -> G1 실패", judge(w, "g1"), 1)

    w = fresh()
    t = (w / "03-keyscreens.md").read_text(encoding="utf-8").replace("| 390 | 844 | 카드", "| 390 | 800 | 카드")
    (w / "03-keyscreens.md").write_text(t, encoding="utf-8")
    check("T2 프레임 390x800 -> G3 실패", judge(w, "g3"), 1)

    w = fresh()
    d = json.loads((w / "04-tokens.json").read_text(encoding="utf-8"))
    d["tokens"].append({"name": "r-bad", "type": "radius", "value": "20px"})
    (w / "04-tokens.json").write_text(json.dumps(d), encoding="utf-8")
    check("T3 모서리 20px -> G4 실패", judge(w, "g4"), 1)

    w = fresh()
    (w / "04-components.md").write_text(
        "| 컴포넌트 | 모서리 | 그림자 | 색상 | 용도 |\n|---|---|---|---|---|\n"
        "| button-primary | 9999px | 없음 | #0066ff | cta |\n", encoding="utf-8")
    judge(w, "review")
    review = json.loads((w / "05-review.json").read_text(encoding="utf-8"))
    check("T4 #0066ff를 일반 버튼에 사용 -> 위반 1건", review["count"], 1)

    w = fresh()
    t = (w / "03-keyscreens.md").read_text(encoding="utf-8").replace("기본값:비공개", "기본값:멤버 공개")
    (w / "03-keyscreens.md").write_text(t, encoding="utf-8")
    check("T5 공개 범위 기본값이 멤버 공개 -> G-S 실패", judge(w, "g3"), 1)

    w = fresh()
    (w / "approval.md").unlink()
    state(w, "init")
    st = json.loads((w / "state.json").read_text(encoding="utf-8"))
    st["passed"]["G3"] = "2026-10-01T00:00:00"  # G3만 통과한 상태를 만든다
    (w / "state.json").write_text(json.dumps(st), encoding="utf-8")
    check("T6 approval.md 없이 S4 시작 -> 차단", state(w, "start", "S4"), 1)

    w = fresh()
    state(w, "init")
    codes = [state(w, "retry", "S3") for _ in range(4)]
    check("T7 같은 구간 복귀 4회 -> 4번째 중단(HALT)", codes, [0, 0, 0, 2])

    # --- /code-review 지적 대응 (T8~T17) ---
    check("T8 cwd가 scripts/여도 designer의 rules.json 쓰기 차단",
          guard("Write", "designer", cwd=ROOT / "scripts", file_path="rules.json"), 2)
    check("T9 대소문자 우회(Work/t/Approval.md) 차단",
          guard("Write", "designer", file_path="Work/t/Approval.md"), 2)
    check("T10 researcher·designer Bash 차단",
          [guard("Bash", "researcher", command="echo x"), guard("Bash", "designer", command="echo x")], [2, 2])
    check("T11 메인의 Bash 리다이렉트로 approval.md 쓰기 차단",
          guard("Bash", None, command="echo 결정: 승인 > work/a/approval.md"), 2)
    check("T11b 메인의 state.py 실행은 허용",
          guard("Bash", None, command="python scripts/state.py work/a verify"), 0)
    check("T12 메인의 state.json 직접 쓰기 차단",
          guard("Write", None, file_path="work/a/state.json"), 2)
    check("T13 judge의 work/.. 경로 차단",
          guard("Bash", "judge", command="python scripts/judge.py work/.. review"), 2)

    w = fresh()
    (w / "04-tokens.json").write_text(json.dumps({"tokens": []}), encoding="utf-8")
    check("T14 빈 토큰 -> G4 실패", judge(w, "g4"), 1)
    w = fresh()
    (w / "04-components.md").write_text("| 컴포넌트 | 모서리 | 그림자 | 색상 | 용도 |\n|---|---|---|---|---|\n", encoding="utf-8")
    check("T14b 빈 컴포넌트 표 -> G5 실패", judge(w, "review"), 1)

    codes = []
    for body in ("[]", '{"tokens": null}', '{"tokens": [1, "x"]}', "not json"):
        w = fresh()
        (w / "04-tokens.json").write_text(body, encoding="utf-8")
        r = judge_run(w, "g4")
        codes.append((r.returncode, "Traceback" in r.stderr))
    check("T15 깨진 토큰 JSON 4종 -> 크래시 없이 실패", codes, [(1, False)] * 4)

    w = fresh()
    (w / "01-references.md").write_text("\n".join("- 앱 | https://uibowl.io/ui/1" for _ in range(10)), encoding="utf-8")
    check("T16 같은 링크 10번 반복 -> G1 실패", judge(w, "g1"), 1)

    w = fresh()
    t = (w / "03-keyscreens.md").read_text(encoding="utf-8").replace("asset-submit", "other").replace("sell-request", "other")
    (w / "03-keyscreens.md").write_text(t, encoding="utf-8")
    flag = json.loads((ROOT / "rules.json").read_text(encoding="utf-8")).get("require_service_screens", False)
    check(f"T17 서비스 화면 0개: require_service_screens={flag}이면 {'실패' if flag else '통과(합의된 해당 없음 규칙)'}",
          judge(w, "g3"), 1 if flag else 0)

    # --- 2차 /code-review 대응 (T18~T19) ---
    broken = subprocess.run([PY, str(ROOT / "scripts" / "guard.py")], input="not json", capture_output=True, text=True, encoding="utf-8", errors="replace")
    check("T18 깨진 훅 입력 -> 통과시키지 않고 차단(종료 코드 2)", broken.returncode, 2)

    def components(rows):
        return "| 컴포넌트 | 모서리 | 그림자 | 색상 | 용도 |\n|---|---|---|---|---|\n" + rows + "\n"

    w = fresh()
    (w / "04-components.md").write_text(components("| Icon button | 30% | 없음 | #141414 | cta |"), encoding="utf-8")
    check("T19 이름에 icon이 있어도 용도가 app-icon이 아니면 30% 위반", [judge(w, "review")], [1])
    w = fresh()
    (w / "04-components.md").write_text(components("| 앱 아이콘 | 30% | 없음 | #141414 | app-icon |"), encoding="utf-8")
    check("T19b 용도가 app-icon이면 30% 허용", [judge(w, "review")], [0])

    print(f"\n{'전부 통과' if not fails else '실패: ' + ', '.join(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
