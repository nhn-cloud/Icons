"""NHN Cloud Icons -> draw.io shape libraries (.xml, mxlibrary).

SVG 원본을 base64로 임베드하므로 네트워크 없이 동작하고, 내보내기(PNG/PDF)에서도
아이콘이 그대로 렌더링된다.
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

# ---------------------------------------------------------------- md catalog

CATALOGS = [
    ROOT / "service_icons" / "service_icons.md",
    ROOT / "service_icons" / "resource_icons.md",
    ROOT / "general_icons" / "general_icons.md",
    ROOT / "box_type" / "box_type.md",
]

TR = re.compile(r"<tr\b.*?</tr>", re.S | re.I)
CELL = re.compile(r"<t[hd]\b[^>]*>(.*?)</t[hd]>", re.S | re.I)
IMG = re.compile(r'<img[^>]+src="([^"]+)"', re.I)
TAG = re.compile(r"<[^>]+>")


def stem_key(src: str) -> str:
    """파일 경로에서 확장자/variant를 뺀 식별자."""
    return Path(urllib.parse.unquote(src)).stem


def load_names() -> dict:
    """stem -> ['Compute', 'Instance'] 형태의 표시 이름 조각."""
    names = {}
    for md in CATALOGS:
        if not md.exists():
            continue
        text = md.read_text(encoding="utf-8")
        for row in TR.findall(text):
            cells = CELL.findall(row)
            parts, srcs = [], []
            for c in cells:
                found = IMG.findall(c)
                if found:
                    srcs.extend(found)
                else:
                    t = html.unescape(TAG.sub("", c)).strip()
                    if t:
                        parts.append(" ".join(t.split()))
            if not srcs or not parts:
                continue
            for s in srcs:
                names.setdefault(stem_key(s), parts)
    return names


NAMES = load_names()

PREFIXES = {"ic", "iaas", "paas", "saas", "general", "resources", "groups", "icon"}
NOISE = {"box", "dk", "content"}
ACRONYMS = {
    "ai", "api", "cdn", "dns", "rds", "nks", "nce", "vpc", "iam", "waf", "sms",
    "cli", "sdk", "gpu", "cpu", "nat", "ip", "db", "obs", "nhn", "ssl", "tls",
    "lb", "vm", "os", "id", "url", "http", "https", "mte", "crm", "erp", "mysql",
    "mssql", "mariadb", "pg", "iot", "ocr", "stt", "tts", "nlp", "bgp", "efs",
    "nas", "san", "gslb", "dr", "ha", "ad", "ldap", "sso", "mfa", "kms", "hsm",
}


def titlecase(text: str) -> str:
    out = []
    for w in text.split():
        if w.isupper() and len(w) > 1:
            out.append(w)
        elif w.lower() in ACRONYMS:
            out.append(w.upper())
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def fallback_name(stem: str) -> list:
    parts = [p for p in stem.split("-") if p]
    if len(parts) > 1:
        parts = [p for p in parts if p.lower() not in PREFIXES] or parts[1:]
    out = []
    for p in parts:
        words = [w for w in p.replace("_", " ").split()
                 if w.lower() not in NOISE and not w.isdigit()]
        if words:
            out.append(titlecase(" ".join(words)))
    return out


def display(stem: str) -> list:
    return NAMES.get(stem) or fallback_name(stem) or [stem]


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

GROUPS = [
    ("Services", ROOT / "files" / "services", 64, False),
    ("Resources", ROOT / "files" / "resources", 56, False),
    ("General", ROOT / "files" / "general_icons", 64, False),
    ("BoxType", ROOT / "files" / "box_type", 64, True),
]


def variant_of(p: Path) -> str:
    parts = [x.lower() for x in p.parts]
    if "black" in parts:
        return "black"
    if "color" in parts:
        return "color"
    return "color"


def main():
    index = []
    for name, base, size, is_group in GROUPS:
        if not base.exists():
            continue
        buckets = {"color": [], "black": []}
        for svg in sorted(base.rglob("*.svg"), key=lambda p: str(p).lower()):
            stem = svg.stem
            parts = display(stem)
            label = parts[-1]
            title = " / ".join(parts)
            uri, w, h = svg_data_uri(svg)
            entry = (group_entry(label, title, uri, w, h) if is_group
                     else icon_entry(label, title, uri, w, h, size))
            buckets[variant_of(svg)].append((title.lower(), entry))

        for variant, items in buckets.items():
            if not items:
                continue
            items.sort(key=lambda t: t[0])
            sub = "" if variant == "color" else "black/"
            out = OUT / f"{sub}NHNCloud-{name}-{variant}.xml"
            n, size_b = write_library(out, [e for _, e in items])
            index.append((out.relative_to(OUT).as_posix(), n, size_b))

    for rel, n, size_b in index:
        print(f"{rel:46s} {n:4d} icons  {size_b/1024:8.1f} KB")
    print(f"\ntotal {sum(n for _, n, _ in index)} entries in {len(index)} libraries")


main()
