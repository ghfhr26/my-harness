#!/usr/bin/env python3
"""state.json 관리. 오케스트레이터만 실행한다.

사용: python scripts/state.py <work/주제> <명령> [인자]
  init                 state.json 생성
  pass <G1|G2|G3|APPROVAL|G4|G5>   판정을 다시 실행해 통과일 때만 시각과 함께 기록
  start S4             G3·승인 통과 기록이 있을 때만 S4 시작 허용
  retry <S1|S2|S3|S4>  복귀 횟수 +1. 상한 초과 시 HALT(종료 코드 2)
  verify               통과 시각이 단계 순서대로인지 사후 검증
종료 코드: 0 성공, 1 거부/실패, 2 HALT(사람에게 넘김)
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = json.loads((ROOT / "rules.json").read_text(encoding="utf-8"))
ORDER = ["G1", "G2", "G3", "APPROVAL", "G4", "G5"]
JUDGE = {"G1": "g1", "G2": "g2", "G3": "g3", "APPROVAL": "approval", "G4": "g4", "G5": "review"}
STAGE_AFTER = {"G1": "S2", "G2": "S3", "G3": "APPROVAL", "APPROVAL": "S4", "G4": "S5", "G5": "DONE"}


def load(work):
    p = Path(work) / "state.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def save(work, st):
    (Path(work) / "state.json").write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def now():
    return datetime.now().isoformat(timespec="seconds")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    work, cmd = sys.argv[1], sys.argv[2]
    arg = sys.argv[3].upper() if len(sys.argv) > 3 else None
    st = load(work)

    if cmd == "init":
        if st:
            sys.exit("state.json이 이미 있다. 이어서 하려면 init 하지 않는다.")
        Path(work).mkdir(parents=True, exist_ok=True)
        save(work, {"stage": "S1", "passed": {}, "returns": {"S1": 0, "S2": 0, "S3": 0, "S4": 0}})
        return 0
    if st is None:
        sys.exit("state.json 없음. 먼저 init 한다.")

    if cmd == "pass":
        if arg not in ORDER:
            sys.exit(f"게이트는 {ORDER} 중 하나")
        prev = ORDER[ORDER.index(arg) - 1] if ORDER.index(arg) else None
        if prev and prev not in st["passed"]:
            print(f"거부: 앞 게이트 {prev} 통과 기록 없음")
            return 1
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "judge.py"), work, JUDGE[arg]], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"거부: {arg} 판정 실패\n{r.stdout}")
            return 1
        st["passed"][arg] = now()
        st["stage"] = STAGE_AFTER[arg]
        save(work, st)
        return 0

    if cmd == "start" and arg == "S4":
        for need in ("G3", "APPROVAL"):
            if need not in st["passed"]:
                print(f"차단: {need} 통과 기록 없음. S4를 시작할 수 없다.")
                return 1
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "judge.py"), work, "approval"], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"차단: approval.md가 승인 상태가 아니다.\n{r.stdout}")
            return 1
        return 0

    if cmd == "retry":
        if arg not in st["returns"]:
            sys.exit("구간은 S1~S4 중 하나")
        limit = RULES["max_returns_per_segment"]
        if st["returns"][arg] >= limit:
            print(f"HALT: {arg} 복귀 {limit}회 초과. 중단하고 사람에게 넘긴다.")
            return 2
        st["returns"][arg] += 1
        st["stage"] = arg
        # 돌아간 구간 이후의 통과 기록은 무효로 한다
        cut = {"S1": "G1", "S2": "G2", "S3": "G3", "S4": "G4"}[arg]
        for g in ORDER[ORDER.index(cut):]:
            st["passed"].pop(g, None)
        save(work, st)
        return 0

    if cmd == "verify":
        stamps = [(g, st["passed"][g]) for g in ORDER if g in st["passed"]]
        problems = []
        for g in ORDER[: len(stamps)]:
            if g not in st["passed"]:
                problems.append(f"{g} 통과 기록 없이 뒤 게이트가 기록됨")
        times = [t for _, t in stamps]
        if times != sorted(times):
            problems.append("통과 시각이 단계 순서와 어긋남")
        print(json.dumps({"pass": not problems, "problems": problems}, ensure_ascii=False, indent=2))
        return 0 if not problems else 1

    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
