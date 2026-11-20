#!/usr/bin/env python3
"""이미 있는 .drawio 를 제자리에서 고친다. 손으로 옮긴 좌표를 지키기 위한 도구다.

구성도를 처음 그릴 때는 `nhn_diagram.py` 로 명세에서 만든다.
한 번이라도 draw.io 에서 손을 댔다면 **그 파일이 원본**이다. 명세에서 다시 그리지 말고
이 도구로 바뀐 부분만 더하거나 뺀다.

사용법
  python drawio_edit.py FILE list                      # 현재 도형·연결 목록 (id 포함)
  python drawio_edit.py FILE add --icon "RDS Instance" --label Replica2 --below db2
  python drawio_edit.py FILE add --group Subnet --label "Private Subnet (Cache)" --into vpc
  python drawio_edit.py FILE edge --from web1 --to db3 --style "Primary Path · 점선" --label 3306
  python drawio_edit.py FILE relabel db2 "Replica (읽기 전용)"
  python drawio_edit.py FILE remove db3                # 딸린 연결선도 함께 지움

배치 기준 (--below / --right-of / --into 가운데 하나)
  --below ID      그 도형 아래. 부모·가로 위치를 그대로 물려받는다
  --right-of ID   그 도형 오른쪽
  --into ID       그 그룹 안. 마지막 자식 아래에 놓는다 (기본값: 캔버스 최상위)
  넣은 뒤 부모 그룹이 좁으면 자동으로 넓힌다. 옆 그룹과 겹치면 draw.io 에서 밀어 준다.
"""
import argparse, base64, os, re, sys, urllib.parse, zlib
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

# Windows 콘솔 기본 코드페이지에서 레이블의 한글이 깨지지 않게 한다.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nhn_diagram as nd

GAP_Y, GAP_X, PAD = 60, 36, 24


# ---------- 파일 입출력 ----------

def load(path):
    """mxfile → (ElementTree 루트, diagram 요소, mxGraphModel 요소)."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    mxfile = ET.fromstring(text)
    diagram = mxfile.find("diagram")
    if diagram is None:
        sys.exit("diagram 요소가 없습니다. .drawio 파일이 맞습니까?")
    model = diagram.find("mxGraphModel")
    if model is None:  # draw.io 가 압축해 저장한 경우
        model = ET.fromstring(nd._decode(diagram.text.strip()))
        diagram.text = None
        diagram.append(model)
    return mxfile, diagram, model


def save(path, mxfile):
    ET.indent(mxfile, space="")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ET.tostring(mxfile, encoding="unicode"))


def root_of(model):
    return model.find("root")


def cells(model):
    return root_of(model).findall("mxCell")


def find_cell(model, cid):
    for c in cells(model):
        if c.get("id") == cid:
            return c
    sys.exit(f"id '{cid}' 인 도형이 없습니다. `list` 로 id 를 확인하세요.")


def geom(cell):
    g = cell.find("mxGeometry")
    if g is None:
        return None
    return {k: float(g.get(k) or 0) for k in ("x", "y", "width", "height")}


def new_id(model, base):
    used = {c.get("id") for c in cells(model)}
    if base not in used:
        return base
    i = 2
    while f"{base}{i}" in used:
        i += 1
    return f"{base}{i}"


# ---------- 조회 ----------

def kind(cell):
    if cell.get("edge") == "1":
        return "연결선"
    style = cell.get("style") or ""
    return "그룹" if "container=1" in style or "swimlane" in style else "도형"


def cmd_list(model, args):
    rows = []
    for c in cells(model):
        cid = c.get("id")
        if cid in ("0", "1") or "__corner" in (cid or ""):
            continue
        g = geom(c) or {}
        pos = (f'{c.get("source","?")} → {c.get("target","?")}' if c.get("edge") == "1"
               else f'{g.get("x",0):.0f},{g.get("y",0):.0f} {g.get("width",0):.0f}x{g.get("height",0):.0f}')
        rows.append((cid, kind(c), (c.get("value") or "").replace("\n", " ")[:28],
                     c.get("parent"), pos))
    w = max([len(r[0]) for r in rows] or [2])
    print(f'{"id":<{w}}  {"종류":<6} {"레이블":<30} {"부모":<10} 위치')
    for r in rows:
        print(f"{r[0]:<{w}}  {r[1]:<6} {r[2]:<30} {r[3]:<10} {r[4]}")


# ---------- 추가 ----------

def place(model, args, w, h):
    """새 도형의 (부모 id, x, y) 를 정한다."""
    if args.below or args.right_of:
        anchor = find_cell(model, args.below or args.right_of)
        g = geom(anchor)
        if not g:
            sys.exit("기준 도형에 좌표가 없습니다(연결선은 기준으로 쓸 수 없습니다).")
        if args.below:
            return anchor.get("parent"), g["x"], g["y"] + g["height"] + GAP_Y
        return anchor.get("parent"), g["x"] + g["width"] + GAP_X, g["y"]

    parent = args.into or "1"
    if parent != "1":
        find_cell(model, parent)
    kids = [c for c in cells(model) if c.get("parent") == parent
            and "__corner" not in (c.get("id") or "") and geom(c)]
    if not kids:
        head = 44 if parent != "1" else 20
        return parent, PAD, head + 10
    low = max(kids, key=lambda c: geom(c)["y"] + geom(c)["height"])
    g = geom(low)
    return parent, g["x"], g["y"] + g["height"] + GAP_Y


def grow_parent(model, parent_id, x, y, w, h):
    """자식이 삐져나오면 부모 그룹을 넓힌다. 조상까지 거슬러 올라간다."""
    while parent_id and parent_id != "1":
        p = find_cell(model, parent_id)
        g = geom(p)
        if not g:
            return
        need_w, need_h = x + w + PAD, y + h + PAD
        gw, gh = max(g["width"], need_w), max(g["height"], need_h)
        if (gw, gh) != (g["width"], g["height"]):
            pg = p.find("mxGeometry")
            pg.set("width", f"{gw:.0f}")
            pg.set("height", f"{gh:.0f}")
            print(f"[알림] 그룹 '{parent_id}' 를 {gw:.0f}x{gh:.0f} 로 넓혔습니다. "
                  f"옆 그룹과 겹치면 draw.io 에서 밀어 주세요.")
        x, y, w, h = g["x"], g["y"], gw, gh
        parent_id = p.get("parent")


def cmd_add(model, lib, args):
    name = args.icon or args.group
    shape = lib.find(name, "group" if args.group else "icon")
    src = nd._cells(shape["xml"])
    main = src[0] if args.icon else next(c for c in src if nd._attr(c, "parent") == "1")

    w = args.w or (shape["w"] or 64 if args.icon else 320)
    h = args.h or (shape["h"] or 64 if args.icon else 200)
    parent, x, y = place(model, args, w, h)
    cid = args.id or new_id(model, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"))
    if args.id and any(c.get("id") == args.id for c in cells(model)):
        sys.exit(f"id '{args.id}' 가 이미 있습니다.")

    c = nd._set_attr(main, "id", cid)
    c = nd._set_attr(c, "parent", parent)
    c = nd._set_attr(c, "value", args.label or shape["title"])
    if args.icon:
        style = nd._attr(c, "style")
        style = re.sub(r"fontSize=\d+", "fontSize=12", style)
        c = nd._set_attr(c, "style", style + ("" if style.endswith(";") else ";")
                         + f"whiteSpace=wrap;labelWidth={max(w + 46, w)};")
    el = ET.fromstring(nd._set_geom(c, x, y, w, h))
    root_of(model).append(el)

    if args.group:  # 그룹 머리의 모서리 아이콘까지 복사
        old = nd._attr(main, "id")
        for k, sub in enumerate(cc for cc in src if nd._attr(cc, "parent") == old):
            s = nd._set_attr(sub, "id", f"{cid}__corner{k}")
            s = nd._set_attr(s, "parent", cid)
            m = re.search(r'width="(\d+)" height="(\d+)"', s)
            sw, sh = (int(m.group(1)), int(m.group(2))) if m else (32, 32)
            root_of(model).append(ET.fromstring(nd._set_geom(s, 0, 0, sw, sh)))

    grow_parent(model, parent, x, y, w, h)
    print(f"추가: {cid} ({shape['palette']}/{shape['title']}) → 부모 {parent}, {x:.0f},{y:.0f}")


def cmd_edge(model, lib, args):
    for cid in (getattr(args, "from"), args.to):
        find_cell(model, cid)
    shape = lib.find(args.style or "Primary Path", "arrow")
    style = nd._attr(nd._cells(shape["xml"])[0], "style")
    side = {"left": (0, 0.5), "right": (1, 0.5), "top": (0.5, 0), "bottom": (0.5, 1)}
    for key, pre in (("exit", "exit"), ("entry", "entry")):
        v = getattr(args, key)
        if v:
            x, y = side[v]
            style += f"{pre}X={x};{pre}Y={y};{pre}Dx=0;{pre}Dy=0;"
    used = {c.get("id") for c in cells(model)}
    eid = next(f"e{i}" for i in range(1, 10000) if f"e{i}" not in used)
    el = ET.fromstring(
        f'<mxCell id="{eid}" value={quoteattr(args.label or "")} style={quoteattr(style)} '
        f'edge="1" parent="1" source={quoteattr(getattr(args, "from"))} target={quoteattr(args.to)}>'
        f'<mxGeometry relative="1" as="geometry"/></mxCell>')
    root_of(model).append(el)
    print(f'연결: {eid}  {getattr(args, "from")} → {args.to} ({shape["title"]})')


# ---------- 수정·삭제 ----------

def cmd_relabel(model, args):
    c = find_cell(model, args.id)
    c.set("value", args.label)
    print(f"레이블: {args.id} → {args.label}")


def cmd_remove(model, args):
    root = root_of(model)
    doomed = set(args.ids)
    for _ in range(10):  # 자손까지
        more = {c.get("id") for c in cells(model) if c.get("parent") in doomed}
        if more <= doomed:
            break
        doomed |= more
    gone = 0
    for c in list(cells(model)):
        if c.get("id") in doomed or c.get("source") in doomed or c.get("target") in doomed:
            root.remove(c)
            gone += 1
    print(f"삭제: {', '.join(args.ids)} (셀 {gone}개, 딸린 연결선 포함)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--lib", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="도형·연결 목록")

    a = sub.add_parser("add", help="도형·그룹 추가")
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--icon")
    g.add_argument("--group")
    a.add_argument("--id"), a.add_argument("--label")
    a.add_argument("--into"), a.add_argument("--below"), a.add_argument("--right-of")
    a.add_argument("--w", type=float), a.add_argument("--h", type=float)

    e = sub.add_parser("edge", help="연결선 추가")
    e.add_argument("--from", required=True), e.add_argument("--to", required=True)
    e.add_argument("--style"), e.add_argument("--label")
    e.add_argument("--exit", choices=["left", "right", "top", "bottom"])
    e.add_argument("--entry", choices=["left", "right", "top", "bottom"])

    r = sub.add_parser("relabel", help="레이블 변경")
    r.add_argument("id"), r.add_argument("label")

    d = sub.add_parser("remove", help="도형 삭제 (딸린 연결선 포함)")
    d.add_argument("ids", nargs="+")

    args = ap.parse_args()
    mxfile, _, model = load(args.file)

    if args.cmd == "list":
        cmd_list(model, args)
        return
    if args.cmd in ("add", "edge"):
        src = args.lib or (os.path.isdir("dist") and "dist") or \
            os.environ.get("NHN_ICONS_DIST") or nd.DEFAULT_URL
        lib = nd.Library(nd.load_library(src))
        (cmd_add if args.cmd == "add" else cmd_edge)(model, lib, args)
    elif args.cmd == "relabel":
        cmd_relabel(model, args)
    elif args.cmd == "remove":
        cmd_remove(model, args)

    save(args.file, mxfile)
    print(f"저장: {args.file}")


if __name__ == "__main__":
    main()
