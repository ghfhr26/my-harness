#!/usr/bin/env python3
"""판정 스크립트. 규칙은 rules.json만 읽는다.

사용: python scripts/judge.py <work/주제 경로> <gate>
gate: g1 | g2 | g3 | approval | g4 | review(=g5)
종료 코드: 0 통과, 1 실패. 결과는 JSON으로 stdout에 출력한다.
review만 05-review.json을 쓴다.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = json.loads((ROOT / "rules.json").read_text(encoding="utf-8"))


def read(work, name):
    p = Path(work) / name
    return p.read_text(encoding="utf-8") if p.exists() else None


def result(ok, problems):
    return {"pass": ok, "problems": problems}


def g1(work):
    text = read(work, "01-references.md")
    if text is None:
        return result(False, ["01-references.md 없음"])
    ok_lines = [l for l in text.splitlines() if re.match(r"^- .+ \| https?://\S+\s*$", l)]
    bad = [l for l in text.splitlines() if l.startswith("- ") and l not in ok_lines]
    problems = [f"형식 오류(앱 이름 | ui_url): {l}" for l in bad]
    unique_urls = {l.rsplit("|", 1)[1].strip() for l in ok_lines}
    if len(unique_urls) < RULES["min_references"]:
        problems.append(f"서로 다른 링크 {len(unique_urls)}개 (최소 {RULES['min_references']})")
    return result(not problems, problems)


def g2(work):
    text = read(work, "02-analysis.md")
    if text is None:
        return result(False, ["02-analysis.md 없음"])
    m = re.search(r"^## 반영할 부분\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return result(False, ["'## 반영할 부분' 섹션 없음"])
    items = [l for l in m.group(1).splitlines() if l.startswith("- ")]
    problems = [] if items else ["반영할 부분 항목 0개"]
    problems += [f"PRD § 번호 없음: {l}" for l in items if not re.search(r"§\d", l)]
    return result(not problems, problems)


def parse_table(text):
    rows = []
    for l in text.splitlines():
        l = l.strip()
        if l.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", l):
            rows.append([c.strip() for c in l.strip("|").split("|")])
    return rows[1:] if rows else []  # 헤더 제외


def g3(work):
    problems = []
    text = read(work, "03-keyscreens.md")
    if text is None:
        return result(False, ["03-keyscreens.md 없음"])
    rows = parse_table(text)  # | 화면 | 유형 | node_id | 너비 | 높이 | UI 요소 |
    f = RULES["frame"]
    if len(rows) != f["count"]:
        problems.append(f"프레임 {len(rows)}개 (정확히 {f['count']}개)")
    for r in rows:
        if len(r) < 6:
            problems.append(f"열 부족(화면|유형|node_id|너비|높이|UI 요소): {r}")
            continue
        name, kind, _, w, h, elems = r[:6]
        if (w, h) != (str(f["width"]), str(f["height"])):
            problems.append(f"{name}: {w}×{h} (필요 {f['width']}×{f['height']})")
        for rule in RULES["service_rules"].values():
            if kind == rule["screen_type"]:
                for need in rule["requires"]:
                    if need.replace(" ", "") not in elems.replace(" ", ""):
                        problems.append(f"{name}: 서비스 규칙 위반, '{need}' 없음")
    if RULES.get("require_service_screens"):
        kinds = {r[1] for r in rows if len(r) >= 2}
        for rule in RULES["service_rules"].values():
            if rule["screen_type"] not in kinds:
                problems.append(f"필수 화면 유형 '{rule['screen_type']}' 없음")
    pngs = list((Path(work) / "03-screens").glob("*.png")) if (Path(work) / "03-screens").is_dir() else []
    if len(pngs) != f["count"]:
        problems.append(f"03-screens/*.png {len(pngs)}개 (정확히 {f['count']}개)")
    return result(not problems, problems)


def approval(work):
    text = read(work, "approval.md")
    if text is None:
        return result(False, ["approval.md 없음"])
    problems = []
    if not re.search(r"^결정:\s*승인\s*$", text, re.M):
        problems.append("결정이 '승인'이 아님")
    if not re.search(r"^승인자:\s*\S+", text, re.M):
        problems.append("승인자 없음")
    if not re.search(r"^날짜:\s*\d{4}-\d{2}-\d{2}\s*$", text, re.M):
        problems.append("날짜(YYYY-MM-DD) 없음")
    return result(not problems, problems)


def check_token(t):
    """토큰·컴포넌트 속성 하나를 규칙과 대조해 위반 목록을 돌려준다."""
    v = []
    name = t.get("name", "?")
    kind, val = t.get("type"), t.get("value")
    if kind == "radius":
        s = str(val)
        if s.endswith("%"):
            ok = int(s[:-1]) in RULES["radius"]["allowed_percent"] and t.get("usage") in RULES["radius"]["percent_only_for"]
        else:
            ok = int(s.replace("px", "")) in RULES["radius"]["allowed_px"]
        if not ok:
            v.append(f"{name}: 모서리 {val} 허용 밖")
    elif kind == "color":
        h = str(val).lower()
        if h not in RULES["colors"]["allowed_hex"]:
            v.append(f"{name}: 색상 {val} 허용 밖")
        if h == RULES["colors"]["accent_hex"] and t.get("usage") not in RULES["colors"]["accent_allowed_usage"]:
            v.append(f"{name}: #0066ff를 '{t.get('usage')}'에 사용 (가격 배지·절약 문구만 허용)")
    elif kind == "spacing":
        if int(str(val).replace("px", "")) not in RULES["spacing"]["allowed_px"]:
            v.append(f"{name}: 간격 {val} 허용 밖")
    elif kind == "font":
        fam, size, weight = val.get("family"), val.get("size"), val.get("weight")
        if fam != RULES["font"]["family"]:
            v.append(f"{name}: 폰트 {fam} (Pretendard만)")
        if [size, weight] not in RULES["font"]["allowed_size_weight"]:
            v.append(f"{name}: 크기·굵기 {size}/{weight} 허용 밖")
    elif kind == "shadow":
        v.append(f"{name}: 그림자 사용 (허용 0개)")
    else:
        v.append(f"{name}: 알 수 없는 type {kind}")
    return v


def check_tokens(tokens):
    """토큰 목록 전체를 검사한다. 형식이 틀리면 크래시하지 않고 위반으로 돌려준다."""
    if not isinstance(tokens, list) or not tokens:
        return ["tokens가 비어 있거나 리스트가 아님 (토큰 1개 이상 필요)"]
    problems = []
    for i, t in enumerate(tokens):
        if not isinstance(t, dict):
            problems.append(f"tokens[{i}]: 객체가 아님")
            continue
        try:
            problems += check_token(t)
        except (ValueError, TypeError, AttributeError, KeyError):
            problems.append(f"{t.get('name', '?')}: 값 형식 오류 {t.get('value')}")
    return problems


def load_tokens(work):
    text = read(work, "04-tokens.json")
    if text is None:
        return None, ["04-tokens.json 없음"]
    try:
        data = json.loads(text)
    except ValueError:
        return None, ["04-tokens.json이 올바른 JSON이 아님"]
    if not isinstance(data, dict):
        return None, ['04-tokens.json 형식 오류 ({"tokens": [...]} 필요)']
    return data.get("tokens"), []


def g4(work):
    tokens, err = load_tokens(work)
    if err:
        return result(False, err)
    problems = check_tokens(tokens)
    return result(not problems, problems)


def review(work):
    """S5: 토큰 + 컴포넌트 위반을 모아 05-review.json에 쓴다."""
    problems = list(g4(work)["problems"])
    comp = read(work, "04-components.md")
    if comp is None:
        problems.append("04-components.md 없음")
    else:
        rows = parse_table(comp)
        if not rows:
            problems.append("04-components.md에 컴포넌트 행이 없음 (1개 이상 필요)")
        for r in rows:  # | 컴포넌트 | 모서리 | 그림자 | 색상 | 용도 |
            if len(r) < 5:
                problems.append(f"열 부족(컴포넌트|모서리|그림자|색상|용도): {r}")
                continue
            name, radius, shadow, color, usage = r[:5]
            entries = [
                {"name": name, "type": "radius", "value": radius, "usage": usage},
                {"name": name, "type": "color", "value": color, "usage": usage},
            ]
            if shadow not in ("없음", "none", "-"):
                entries.append({"name": name, "type": "shadow", "value": shadow})
            for e in entries:
                try:
                    problems += check_token(e)
                except (ValueError, TypeError):
                    problems.append(f"{name}: 값 형식 오류 {e['value']}")
    out = {"count": len(problems), "violations": problems}
    (Path(work) / "05-review.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return result(not problems, problems)


GATES = {"g1": g1, "g2": g2, "g3": g3, "approval": approval, "g4": g4, "review": review, "g5": review}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in GATES:
        sys.exit(f"사용: judge.py <work/주제> <{'|'.join(GATES)}>")
    res = GATES[sys.argv[2]](sys.argv[1])
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if res["pass"] else 1)
