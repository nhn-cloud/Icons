"""NHN Cloud Icons -> draw.io shape libraries (.xml, mxlibrary).

SVG 원본을 base64로 임베드하므로 네트워크 없이 동작하고, 내보내기(PNG/PDF)에서도
아이콘이 그대로 렌더링된다.

이름과 검색어는 icons.json(단일 명부)에서만 가져온다. 카탈로그 md 를 여기서 다시
파싱하지 않는다 — 출처가 둘로 갈리면 조용히 어긋나기 때문.

  python drawio/make_drawio_libs.py . drawio
"""
import base64
import html
import json
import os
import re
import sys
import urllib.parse
import zlib
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()

MANIFEST = ROOT / "icons.json"
if not MANIFEST.exists():
    sys.exit("icons.json 이 없습니다. 먼저 python scripts/build_manifest.py 를 실행하세요.")
ICONS = json.loads(MANIFEST.read_text(encoding="utf-8"))["icons"]

# ---------------------------------------------------------------- svg -> style

VIEWBOX = re.compile(r'viewBox="([\d.\s+-]+)"', re.I)


def svg_size(text: str, default=(60, 60)):
    m = VIEWBOX.search(text)
    if m:
        v = m.group(1).split()
        if len(v) == 4:
            try:
                return float(v[2]), float(v[3])
            except ValueError:
                pass
    return default


def svg_data_uri(path: Path) -> tuple:
    text = path.read_text(encoding="utf-8")
    w, h = svg_size(text)
    b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
    # draw.io 스타일 문자열에서는 ';base64' 를 쓸 수 없어 콤마 뒤에 바로 base64를 둔다.
    return f"data:image/svg+xml,{b64}", w, h


# ---------------------------------------------------------------- mxlibrary

def compress(xml: str) -> str:
    """Graph.compress = base64(deflateRaw(encodeURIComponent(xml)))"""
    quoted = urllib.parse.quote(xml, safe="!~*'()")
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    raw = co.compress(quoted.encode("utf-8")) + co.flush()
    return base64.b64encode(raw).decode("ascii")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def model(cells_xml: str) -> str:
    return (
        '<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
        + cells_xml
        + "</root></mxGraphModel>"
    )


def icon_entry(label, title, uri, w, h, size):
    scale = size / max(w, h)
    cw, ch = round(w * scale), round(h * scale)
    style = (
        "shape=image;html=1;labelBackgroundColor=none;imageAspect=0;aspect=fixed;"
        "verticalLabelPosition=bottom;verticalAlign=top;fontSize=11;"
        f"image={uri};"
    )
    cell = (
        f'<mxCell id="2" value="{esc(label)}" style="{esc(style)}" vertex="1" parent="1">'
        f'<mxGeometry x="0" y="0" width="{cw}" height="{ch}" as="geometry"/></mxCell>'
    )
    return {"xml": compress(model(cell)), "w": cw, "h": ch,
            "aspect": "fixed", "title": title}


def group_entry(label, title, uri, w, h):
    """박스 형태 아이콘: 컨테이너 사각형 + 좌상단 배지 아이콘."""
    gw, gh = 320, 200
    box = (
        "rounded=0;html=1;whiteSpace=wrap;container=1;collapsible=0;"
        "recursiveResize=0;pointerEvents=0;expand=0;"
        "fillColor=none;strokeColor=#999999;dashed=1;dashPattern=8 4;"
        "verticalAlign=top;align=left;spacingLeft=38;spacingTop=4;"
        "fontSize=12;fontColor=#666666;"
    )
    badge = (
        "shape=image;html=1;imageAspect=0;aspect=fixed;movable=0;resizable=0;"
        f"rotatable=0;deletable=0;editable=0;connectable=0;image={uri};"
    )
    cells = (
        f'<mxCell id="2" value="{esc(label)}" style="{esc(box)}" vertex="1" parent="1">'
        f'<mxGeometry x="0" y="0" width="{gw}" height="{gh}" as="geometry"/></mxCell>'
        f'<mxCell id="3" value="" style="{esc(badge)}" vertex="1" parent="2">'
        f'<mxGeometry x="6" y="6" width="26" height="26" as="geometry"/></mxCell>'
    )
    return {"xml": compress(model(cells)), "w": gw, "h": gh, "title": title}


def write_library(path: Path, entries: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    path.write_text(f"<mxlibrary>{payload}</mxlibrary>", encoding="utf-8")
    return len(entries), path.stat().st_size


# ---------------------------------------------------------------- collect

# icons.json 의 kind -> (라이브러리 이름, 아이콘 변 길이, 그룹 컨테이너 여부)
KINDS = {
    "service":  ("Services", 64, False),
    "resource": ("Resources", 56, False),
    "general":  ("General", 64, False),
    "box":      ("BoxType", 64, True),
}


def tags_for(ic):
    """사이드바 검색어. 공백 구분이므로 각 토큰에 공백이 없어야 한다."""
    t = list(ic.get("tags") or [])
    t.append(ic["stem"].replace("ic-", ""))          # 파일명 통째로도 검색되게
    if ic.get("category"):
        t.append(ic["category"])
    seen, out = set(), []
    for x in t:
        for piece in str(x).split():
            k = piece.lower()
            if k and k not in seen:
                seen.add(k)
                out.append(piece)
    return " ".join(out)


def main():
    index = []
    skipped = []
    for kind, (libname, size, is_group) in KINDS.items():
        buckets = {"color": [], "black": []}
        for ic in ICONS:
            if ic["kind"] != kind:
                continue
            tags = tags_for(ic)
            for variant, fmts in ic["files"].items():
                svg_rel = fmts.get("svg")
                if not svg_rel:
                    skipped.append((ic["id"], variant))
                    continue
                svg = ROOT / svg_rel
                if not svg.exists():
                    skipped.append((ic["id"], variant))
                    continue
                label = ic["name"]
                uri, w, h = svg_data_uri(svg)
                entry = (group_entry(label, label, uri, w, h) if is_group
                         else icon_entry(label, label, uri, w, h, size))
                entry["tags"] = tags
                buckets.setdefault(variant, []).append((label.lower(), entry))

        for variant, items in buckets.items():
            if not items:
                continue
            items.sort(key=lambda t: t[0])
            sub = "" if variant == "color" else "black/"
            out = OUT / f"{sub}NHNCloud-{libname}-{variant}.xml"
            n, size_b = write_library(out, [e for _, e in items])
            index.append((out.relative_to(OUT).as_posix(), n, size_b))

    index.sort()
    for rel, n, size_b in index:
        print(f"{rel:46s} {n:4d} icons  {size_b/1024:8.1f} KB")
    print()
    print(f"total {sum(n for _, n, _ in index)} entries in {len(index)} libraries")
    if skipped:
        print(f"SVG 가 없어 제외: {len(skipped)}건")


main()
