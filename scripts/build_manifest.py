# -*- coding: utf-8 -*-
"""
files/ 트리와 카탈로그 md 를 읽어 icons.json 단일 명부를 만든다.

표시 이름은 카탈로그 md 를 1차 출처로 쓰고, 카탈로그에 없는 아이콘만 파일명에서
유추한 뒤 needs_review 로 표시한다. (유추한 이름을 확정처럼 쓰지 않기 위함)

표 모양이 파일마다 다르다: 이름을 <th> 로 쓰는 표(service/box/general)와
<td> 두 칸(서비스 + 리소스)을 rowspan 으로 묶어 쓰는 표(resource)가 섞여 있다.
"""
import os, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "icons.json")

CATALOGS = {
    "service":  "service_icons/service_icons.md",
    "resource": "service_icons/resource_icons.md",
    "general":  "general_icons/general_icons.md",
    "box":      "box_type/box_type.md",
}
TOP_KIND = {"services": "service", "resources": "resource",
            "general_icons": "general", "box_type": "box",
            "category_icons": "category"}

NEWLINE = chr(10)
CELL = re.compile(r"<(th|td)([^>]*)>(.*?)</\1>", re.S)
HEADER_WORDS = {"png", "svg", "color", "black", "service", "resource", "icon"}


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def strip_tags(x):
    x = re.sub(r"<br\s*/?>", " / ", x, flags=re.I)     # 여러 서비스를 한 칸에 적은 경우
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip(" /")


def parse_rows(txt):
    """(이름, [경로...]) 를 순서대로 돌려준다. rowspan 값은 다음 행으로 이어받는다."""
    carry = []                                   # [[값, 남은_행수], ...]
    for tr in re.findall(r"<tr>(.*?)</tr>", txt, re.S):
        srcs = re.findall(r'<img\s+src="([^"]+)"', tr)
        texts, spans = [], []
        for tag, attrs, inner in CELL.findall(tr):
            if "<img" in inner:
                continue
            val = strip_tags(inner)
            if not val or val.lower() in HEADER_WORDS:
                continue
            rs = re.search(r'rowspan="(\d+)"', attrs)
            texts.append(val)
            spans.append(int(rs.group(1)) if rs else 1)
        if not srcs:                             # 머리글 행 — rowspan 만 기록
            carry = [[v, n - 1] for v, n in zip(texts, spans) if n > 1]
            continue
        name = " ".join(x for x in ([c[0] for c in carry] + texts) if x)
        yield name, srcs
        nxt = [c for c in ([v, n - 1] for v, n in ((c[0], c[1]) for c in carry)) if c[1] > 0]
        nxt += [[v, n - 1] for v, n in zip(texts, spans) if n > 1]
        carry = nxt


name_of, section_of = {}, {}
for kind, path in CATALOGS.items():
    for block in re.split(r"(?m)^#{2,3}\s+", read(path)):
        if not block.strip():
            continue
        head, _, rest = block.partition(NEWLINE)
        section = head.strip().lstrip("#").strip()
        for nm, srcs in parse_rows(rest):
            for sp in srcs:
                name_of[sp.lstrip("/")] = nm
                section_of[sp.lstrip("/")] = section


# ---------- 아이콘 단위로 묶기 ----------
def parse_path(rel):
    parts = rel.split("/")
    kind = TOP_KIND.get(parts[1], "other")
    variant = "black" if "black" in parts else "color"
    cat = [p for p in parts[2:-1] if p not in ("color", "black")]
    stem, ext = parts[-1].rsplit(".", 1)
    return kind, (cat[0] if cat else None), variant, ext.lower(), stem


icons = collections.OrderedDict()
for dp, dn, fn in os.walk(os.path.join(ROOT, "files")):
    rel_dir = os.path.relpath(dp, ROOT).replace("\\", "/")
    if rel_dir.startswith("files/pptx"):
        continue
    for f in sorted(fn):
        if "." not in f or f.rsplit(".", 1)[-1].lower() not in ("png", "svg"):
            continue
        rel = rel_dir + "/" + f
        kind, category, variant, ext, stem = parse_path(rel)
        ic = icons.setdefault((kind, category or "", stem), {
            "id": None, "kind": kind, "category": category,
            "name": None, "section": None, "files": {}, "tags": [],
            "needs_review": False,
        })
        ic["files"].setdefault(variant, {})[ext] = rel
        if rel in name_of and not ic["name"]:
            ic["name"] = name_of[rel]
            ic["section"] = section_of[rel]


# ---------- 이름 유추 + id + tags ----------
def titleize(stem):
    s = re.sub(r"-box$", "", re.sub(r"^ic-", "", stem))
    return " ".join(w.upper() if len(w) <= 3 and w.isalpha() else w.capitalize()
                    for w in re.split(r"[-_]", s) if w)


def tagify(ic, stem):
    t = set()
    for src in (ic.get("name") or "", titleize(stem), ic.get("category") or "",
                ic.get("section") or "", ic["kind"]):
        for w in re.split(r"[^0-9A-Za-z]+", src):
            if len(w) >= 2:
                t.add(w.lower())
    for w in re.split(r"[-_]", re.sub(r"^ic-", "", stem)):     # 약어 검색용: dsr, nks, ncr
        if len(w) >= 2:
            t.add(w.lower())
    if ic["kind"] != "box":
        t.discard("box")
    return sorted(t)


out = []
for (kind, category, stem), ic in icons.items():
    ic["id"] = f"{kind}/{category}/{stem}" if category else f"{kind}/{stem}"
    if not ic["name"]:
        ic["name"] = titleize(stem)
        ic["name_source"] = "derived"
        ic["needs_review"] = True
    else:
        ic["name_source"] = "catalog"
        # 카탈로그 이름과 파일명이 토큰을 하나도 공유하지 않으면 오기재 의심
        st = re.sub(r"[^a-z0-9]", "", stem.lower())
        toks = [t for t in re.split(r"[^a-z0-9]+", ic["name"].lower()) if len(t) > 2]
        if toks and not any(t in st for t in toks):
            ic["needs_review"] = True
            ic["review_note"] = "카탈로그 이름이 파일명과 일치하지 않음"
    ic["tags"] = tagify(ic, stem)
    ic["stem"] = stem
    out.append(ic)

out.sort(key=lambda x: (x["kind"], x["category"] or "", x["stem"]))

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"$comment": "files/ 트리에서 생성된 단일 명부. scripts/build_manifest.py 로 재생성한다.",
               "generated_from": "files/", "count": len(out), "icons": out},
              f, ensure_ascii=False, indent=1)

print(f"아이콘 {len(out)}건 -> icons.json")
print("  종류별:", dict(collections.Counter(i["kind"] for i in out)))
nr = [i for i in out if i["needs_review"]]
print(f"  카탈로그에 이름 있음: {len(out)-len(nr)}건 / 이름 유추(needs_review): {len(nr)}건")
print(f"  SVG 없음: {sum(1 for i in out if not any('svg' in v for v in i['files'].values()))}건")
print(f"  black 변형 없음: {sum(1 for i in out if 'black' not in i['files'])}건")
