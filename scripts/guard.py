#!/usr/bin/env python3
"""PreToolUse 훅. 에이전트별 쓰기 범위를 강제한다. 차단은 종료 코드 2.

stdin의 agent_type이 있으면 서브에이전트(researcher/designer/judge), 없으면 오케스트레이터(메인).
프로젝트 루트는 이 파일 위치 기준이다(훅 입력의 cwd는 에이전트가 cd하면 바뀌므로 쓰지 않는다).
한계: 메인의 Bash는 명령 문자열 휴리스틱으로만 검사한다. 완전한 차단은 아니다.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 서브에이전트가 쓸 수 없는 파일 (메인은 하네스를 유지보수해야 하므로 제외). 소문자로 대조한다.
PROTECTED = [r"^rules\.json$", r"^design\.md$", r"^prd\.md$", r"^claude\.md$", r"^scripts/", r"^tests/", r"^\.claude/", r"(^|/)state\.json$"]
# 에이전트별 편집 허용 (work/<주제>/ 아래)
ALLOW = {
    "researcher": r"^work/[^/]+/0[12]-[^/]+$",
    "designer": r"^work/[^/]+/(03-[^/]+(/[^/]+)?|04-[^/]+)$",
    "judge": None,  # 쓰기 없음
}
# 메인(오케스트레이터)은 산출물(01~05)과 state.json을 직접 쓰지 못한다. state.json은 state.py가 쓴다.
MAIN_BLOCKED = r"^work/[^/]+/(0[1-5]-|approval\.md|03-screens/|state\.json)"
# 메인 Bash가 이 파일을 건드리는 명령은 허용 목록(상태 스크립트, 읽기 전용 명령)만 통과한다.
MAIN_BASH_GUARDED = re.compile(r"approval\.md|state\.json", re.I)
MAIN_BASH_OK = re.compile(r"^(python3? scripts/(state|judge)\.py |cat |type |ls |head |tail |git (status|diff|log|show))")
JUDGE_BASH = re.compile(r"python3? scripts/judge\.py work/[\w가-힣.-]+ (g1|g2|g3|approval|g4|g5|review)", re.I)


def deny(msg):
    print(f"차단: {msg}", file=sys.stderr)
    sys.exit(2)


def rel(path):
    p = Path(path)
    p = p if p.is_absolute() else ROOT / p
    try:
        return p.resolve().relative_to(ROOT).as_posix().lower()
    except ValueError:
        return None  # 프로젝트 밖


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {})
    agent = data.get("agent_type")  # None이면 메인

    if tool in ("Write", "Edit", "NotebookEdit"):
        r = rel(inp.get("file_path") or inp.get("notebook_path") or "")
        if r is None:
            if agent in ALLOW:
                deny(f"{agent}는 프로젝트 밖에 쓸 수 없다")
            return
        if r.endswith("approval.md"):
            deny("approval.md는 사람만 쓴다")
        if agent is None:
            if re.search(MAIN_BLOCKED, r):
                deny(f"오케스트레이터는 {r}를 직접 쓰지 않는다. 산출물은 역할 에이전트에, state.json은 scripts/state.py에 맡긴다")
            return
        if any(re.search(p, r) for p in PROTECTED):
            deny(f"{agent}는 {r}를 수정할 수 없다 (읽기 전용)")
        pattern = ALLOW.get(agent)
        if pattern is None or not re.search(pattern, r):
            deny(f"{agent}의 편집 범위 밖: {r}")

    elif tool == "Bash":
        cmd = inp.get("command", "").strip()
        if agent == "judge":
            if ".." in cmd or not JUDGE_BASH.fullmatch(cmd):
                deny("judge는 'python scripts/judge.py work/<주제> <게이트>'만 실행할 수 있다")
        elif agent in ALLOW:  # researcher, designer는 Bash가 필요 없다
            deny(f"{agent}는 Bash를 쓸 수 없다")
        elif agent is None and MAIN_BASH_GUARDED.search(cmd) and not (MAIN_BASH_OK.match(cmd) and not re.search(r"[>|;&`$]", cmd)):
            deny("approval.md·state.json은 Bash로 고칠 수 없다 (scripts/state.py를 쓴다)")


try:
    main()
except Exception as e:  # 입력이 깨지거나 예상 밖 오류면 통과시키지 않는다 (종료 코드 1은 차단이 아님)
    deny(f"가드 내부 오류, 안전을 위해 차단: {type(e).__name__}: {e}")
sys.exit(0)
