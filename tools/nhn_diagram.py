#!/usr/bin/env python3
"""NHN Cloud 아키텍처 구성도(.drawio) 생성기.

NHN Cloud draw.io 아이콘 라이브러리(dist/01.xml ~ 28.xml)의 도형을 그대로 꺼내
YAML/JSON 명세로 구성도를 만듭니다. 아이콘·그룹·화살표 스타일은 라이브러리 값을
그대로 쓰므로 draw.io 팔레트에서 끌어다 놓은 것과 같은 결과가 나옵니다.

사용법
  python nhn_diagram.py spec.yaml out.drawio [--lib DIR_OR_URL]
  python nhn_diagram.py --list [검색어]         # 아이콘 이름 찾기

--lib 기본값: ./dist → 환경변수 NHN_ICONS_DIST →
  https://raw.githubusercontent.com/nhn-cloud/Icons/draft/dist

명세 형식 (YAML)
  title: 3-Tier Web Service        # 선택. 왼쪽 위 제목
  dir: row                         # 최상위 배치 방향 row | col (기본 row)
  items:                           # 노드 또는 그룹의 목록 (재귀)
    - {id: user, icon: Users, label: 사용자}
    - group: Region                # Groups 팔레트 이름 (NHN Cloud, Region, VPC, Subnet ...)
      label: KR1 (판교)             # 생략 시 그룹 이름
      dir: col                     # 자식 배치 방향
      items: [...]
  edges:
    - [user, lb]                                    # 기본 Primary Path
    - [lb, web1, Secondary Path · 점선]
    - {from: web1, to: db, style: Primary Path, label: "3306"}
    - {from: asg, to: obs, exit: bottom, entry: top}   # 연결 방향 고정

  edge 옵션: from, to (노드·그룹 id), style(Arrows 팔레트 이름, 기본 Primary Path),
            label, exit/entry(left|right|top|bottom), extra(draw.io 스타일 문자열 추가)

  노드 옵션: id, icon(필수), label, w/h(크기 덮어쓰기)
  그룹 옵션: id, group(필수), label, dir, gap, pad, align(center|start), min_w, min_h
  특수 항목: {spacer: 60}  — 빈 칸
            {stack: col, items: [...]}  — 테두리 없는 배치 전용 묶음 (row | col)
  icon/group 이름은 대소문자·공백·하이픈을 무시하고 맞춥니다.
  이름이 여러 팔레트에 있으면 "Palette/Title" 로 지정합니다 (예: "Container/Image").
"""
import argparse, base64, json, re, sys, urllib.parse, urllib.request, zlib, os
from xml.sax.saxutils import escape, quoteattr

DEFAULT_URL = "https://raw.githubusercontent.com/nhn-cloud/Icons/draft/dist"

# ---------- 라이브러리 로드 ----------

def _decode(s):
    return urllib.parse.unquote(zlib.decompress(base64.b64decode(s), -15).decode("utf-8"))

def _norm(s):
    return re.sub(r"[\s_\-·,()&]+", "", s.lower())

def _read(src, name):
    if re.match(r"https?://", src):
        with urllib.request.urlopen(f"{src.rstrip('/')}/{name}", timeout=30) as r:
            return r.read().decode("utf-8")
    p = os.path.join(src, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()

def load_library(src):
    shapes = []
    for i in range(1, 100):
        try:
            text = _read(src, f"{i:02d}.xml")
        except Exception:
            text = None
        if text is None:
            if i > 30:
                break
            continue
        m = re.search(r'<mxlibrary[^>]*title="([^"]*)"[^>]*>(.*)</mxlibrary>', text, re.S)
        palette = m.group(1).replace("&amp;", "&").replace("NHN Cloud / ", "")
        for e in json.loads(m.group(2)):
            shapes.append({"palette": palette, "no": i, "title": e["title"],
                           "w": e.get("w"), "h": e.get("h"), "xml": _decode(e["xml"])})
    if not shapes:
        sys.exit(f"라이브러리를 찾지 못했습니다: {src}")
    return shapes

class Library:
    def __init__(self, shapes):
        self.shapes = shapes
        self.by = {}
        for s in shapes:
            for k in (_norm(s["title"]), _norm(s["palette"] + "/" + s["title"])):
                self.by.setdefault(k, []).append(s)

    def find(self, name, kind=None):
        cands = self.by.get(_norm(name), [])
        if kind == "group":
            cands = [c for c in cands if c["palette"] == "Groups"]
        elif kind == "arrow":
            cands = [c for c in cands if c["palette"] == "Arrows"]
        elif kind == "icon":
            cands = [c for c in cands if c["palette"] not in ("Groups", "Arrows")]
            # Retired 는 다른 후보가 있으면 뒤로
            live = [c for c in cands if c["palette"] != "Retired"]
            cands = live or cands
        if not cands:
            near = [s["palette"] + "/" + s["title"] for s in self.shapes
                    if _norm(name)[:4] in _norm(s["title"])][:8]
            raise SystemExit(f"'{name}' ({kind}) 를 라이브러리에서 찾지 못했습니다. 비슷한 이름: {near}")
        if len(cands) > 1:
            # 서비스(64) 우선
            cands.sort(key=lambda c: -(c["w"] or 0))
            print(f"[알림] '{name}' 후보 {len(cands)}개 → {cands[0]['palette']}/{cands[0]['title']} 사용. "
                  f"다른 것: {[c['palette']+'/'+c['title'] for c in cands[1:]]}", file=sys.stderr)
        return cands[0]

# ---------- 레이아웃 ----------

ICON_SLOT_W = 110      # 아이콘 1칸 너비 (레이블 공간 포함)
LABEL_H = 34           # 아이콘 아래 레이블 높이
GROUP_HEAD = 44        # 그룹 머리 (모서리 아이콘 32 + 여백)
ASG_HEAD = 64          # Auto Scaling Group: 아이콘+레이블이 위 가운데
GROUP_PAD = 24
GAP = 36

class Node:
    def __init__(self, spec, lib, ids):
        self.spec = spec
        self.children = []
        self.x = self.y = 0
        if "spacer" in spec:
            self.kind = "spacer"
            v = spec["spacer"]
            self.w = self.h = int(v) if v else 40
            return
        if "stack" in spec:
            self.kind = "stack"
            self.dir = spec.get("stack") or "row"
            self.gap = spec.get("gap", GAP)
            self.pad = spec.get("pad", 0)
            self.align = spec.get("align", "center")
            self.children = [Node(c, lib, ids) for c in spec.get("items", [])]
        elif "group" in spec:
            self.kind = "group"
            self.shape = lib.find(spec["group"], "group")
            self.dir = spec.get("dir", "row")
            self.gap = spec.get("gap", GAP)
            self.pad = spec.get("pad", GROUP_PAD)
            self.align = spec.get("align", "center")
            self.children = [Node(c, lib, ids) for c in spec.get("items", [])]
        else:
            self.kind = "icon"
            if "icon" not in spec:
                raise SystemExit(f"항목에 icon/group/spacer 가 없습니다: {spec}")
            self.shape = lib.find(spec["icon"], "icon")
            self.iw = spec.get("w", self.shape["w"] or 64)
            self.ih = spec.get("h", self.shape["h"] or 64)
        self.id = str(spec.get("id") or f"n{len(ids)+1}")
        if self.id in ids:
            raise SystemExit(f"id 중복: {self.id}")
        ids[self.id] = self

    @property
    def head(self):
        if self.kind == "stack":
            return 0
        return ASG_HEAD if _norm(self.shape["title"]) == "autoscalinggroup" else GROUP_HEAD

    def measure(self):
        if self.kind == "spacer":
            return
        if self.kind == "icon":
            self.w = max(self.iw, ICON_SLOT_W)
            self.h = self.ih + LABEL_H
            return
        for c in self.children:
            c.measure()
        row = self.dir == "row"
        main = sum((c.w if row else c.h) for c in self.children) + self.gap * max(0, len(self.children) - 1)
        cross = max([(c.h if row else c.w) for c in self.children] or [0])
        cw, ch = (main, cross) if row else (cross, main)
        min_w, min_h = (0, 0) if self.kind == "stack" else (220, 140)
        self.w = max(cw + 2 * self.pad, self.spec.get("min_w", min_w))
        self.h = max(ch + self.head + self.pad, self.spec.get("min_h", min_h))

    def place(self):
        """자식 좌표를 이 그룹 기준 상대좌표로 정한다."""
        if self.kind not in ("group", "stack"):
            return
        row = self.dir == "row"
        inner_w = self.w - 2 * self.pad
        inner_h = self.h - self.head - self.pad
        main_total = sum((c.w if row else c.h) for c in self.children) + self.gap * max(0, len(self.children) - 1)
        off = ((inner_w if row else inner_h) - main_total) / 2
        for c in self.children:
            if row:
                c.x = self.pad + off
                c.y = self.head + ((inner_h - c.h) / 2 if self.align == "center" else 0)
                off += c.w + self.gap
            else:
                c.y = self.head + off
                c.x = self.pad + ((inner_w - c.w) / 2 if self.align == "center" else 0)
                off += c.h + self.gap
            c.place()

# ---------- XML 출력 ----------

def _cells(xml):
    cells = re.findall(r"<mxCell\b(?:[^>]*/>|.*?</mxCell>)", xml, re.S)
    return [c for c in cells if 'vertex="1"' in c or 'edge="1"' in c]

def _attr(cell, name):
    m = re.search(rf'\b{name}="([^"]*)"', cell)
    return m.group(1) if m else None

def _set_attr(cell, name, value):
    if re.search(rf'\b{name}="[^"]*"', cell):
        return re.sub(rf'\b{name}="[^"]*"', f"{name}={quoteattr(value)}", cell, count=1)
    return cell.replace("<mxCell", f"<mxCell {name}={quoteattr(value)}", 1)

def _set_geom(cell, x, y, w, h):
    return re.sub(r"<mxGeometry\b[^>]*?(/?)>",
                  lambda m: f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"{m.group(1)}>',
                  cell, count=1)

def emit(node, parent, out):
    if node.kind == "spacer":
        return
    if node.kind == "stack":
        for ch in node.children:
            ch.x += node.x
            ch.y += node.y
            emit(ch, parent, out)
        return
    cells = _cells(node.shape["xml"])
    main = cells[0] if node.kind == "icon" else next(c for c in cells if _attr(c, "parent") == "1")
    label = node.spec.get("label", node.shape["title"])
    if node.kind == "icon":
        x = node.x + (node.w - node.iw) / 2
        c = _set_attr(main, "id", node.id)
        c = _set_attr(c, "parent", parent)
        c = _set_attr(c, "value", label)
        style = _attr(c, "style")
        if "fontSize=" in style:
            style = re.sub(r"fontSize=\d+", "fontSize=12", style)
        c = _set_attr(c, "style", style + ("" if style.endswith(";") else ";") + f"whiteSpace=wrap;labelWidth={max(node.w - 6, node.iw)};")
        out.append(_set_geom(c, x, node.y, node.iw, node.ih))
        return
    c = _set_attr(main, "id", node.id)
    c = _set_attr(c, "parent", parent)
    c = _set_attr(c, "value", label)
    out.append(_set_geom(c, node.x, node.y, node.w, node.h))
    old_id = _attr(main, "id")
    for k, sub in enumerate(cc for cc in cells if _attr(cc, "parent") == old_id):
        s = _set_attr(sub, "id", f"{node.id}__corner{k}")
        s = _set_attr(s, "parent", node.id)
        gm = re.search(r'width="(\d+)" height="(\d+)"', s)
        sw, sh = (int(gm.group(1)), int(gm.group(2))) if gm else (32, 32)
        sx = (node.w - sw) / 2 if node.head == ASG_HEAD else 0
        out.append(_set_geom(s, sx, 0, sw, sh))
    for ch in node.children:
        emit(ch, node.id, out)

def edge_cell(i, e, lib, ids):
    if isinstance(e, (list, tuple)):
        e = {"from": e[0], "to": e[1], "style": e[2] if len(e) > 2 else None,
             "label": e[3] if len(e) > 3 else None}
    for k in ("from", "to"):
        if str(e[k]) not in ids:
            raise SystemExit(f"edge 의 {k}='{e[k]}' 인 id 가 없습니다.")
    shape = lib.find(e.get("style") or "Primary Path", "arrow")
    style = _attr(_cells(shape["xml"])[0], "style")
    side = {"left": (0, 0.5), "right": (1, 0.5), "top": (0.5, 0), "bottom": (0.5, 1)}
    extra = ""
    for key, pre in (("exit", "exit"), ("entry", "entry")):
        if e.get(key):
            x, y = side[e[key]]
            extra += f"{pre}X={x};{pre}Y={y};{pre}Dx=0;{pre}Dy=0;"
    extra += e.get("extra", "")
    return (f'<mxCell id="e{i}" value={quoteattr(str(e.get("label") or ""))} style={quoteattr(style + extra)} '
            f'edge="1" parent="1" source="{e["from"]}" target="{e["to"]}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>')

def build(spec, lib):
    ids = {}
    root = Node({"group": "Generic Group (실선)", "items": spec.get("items", []),
                 "dir": spec.get("dir", "row"), "gap": spec.get("gap", 60), "pad": 0,
                 "min_w": 0, "min_h": 0, "id": "__root"}, lib, ids)
    del ids["__root"]
    root.measure()
    # 최상위는 머리 없이 배치
    root.shape = dict(root.shape, title="__root")
    top = 70 if spec.get("title") else 20
    root.h -= GROUP_HEAD
    root.place()
    out = []
    if spec.get("title"):
        out.append(f'<mxCell id="__title" value={quoteattr(spec["title"])} '
                   f'style="text;html=1;align=left;verticalAlign=middle;fontSize=20;fontStyle=1;fontColor=#222222;" '
                   f'vertex="1" parent="1"><mxGeometry x="20" y="16" width="800" height="36" as="geometry"/></mxCell>')
    for c in root.children:
        c.x += 20
        c.y += top - GROUP_HEAD
        emit(c, "1", out)
    for i, e in enumerate(spec.get("edges", []), 1):
        out.append(edge_cell(i, e, lib, ids))
    body = "".join(out)
    name = escape(spec.get("title") or "NHN Cloud Architecture")
    return ('<mxfile host="nhn_diagram.py"><diagram name=' + quoteattr(name) + ' id="nhn">'
            '<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
            'arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0" background="#FFFFFF">'
            '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + body + '</root></mxGraphModel></diagram></mxfile>')

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--lib", default=None)
    ap.add_argument("--list", nargs="?", const="", default=None, metavar="QUERY")
    a = ap.parse_args()
    src = a.lib or (os.path.isdir("dist") and "dist") or os.environ.get("NHN_ICONS_DIST") or DEFAULT_URL
    lib = Library(load_library(src))
    if a.list is not None:
        q = _norm(a.list)
        for s in lib.shapes:
            if q in _norm(s["palette"] + s["title"]):
                print(f'{s["no"]:02d} {s["palette"]:<22} {s["title"]}  ({s["w"]}x{s["h"]})')
        return
    if not (a.spec and a.out):
        ap.error("spec 와 out 이 필요합니다")
    with open(a.spec, encoding="utf-8") as f:
        text = f.read()
    if a.spec.endswith(".json"):
        spec = json.loads(text)
    else:
        import yaml
        spec = yaml.safe_load(text)
    xml = build(spec, lib)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"저장: {a.out}")

if __name__ == "__main__":
    main()
