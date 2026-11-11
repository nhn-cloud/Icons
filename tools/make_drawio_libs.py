# -*- coding: utf-8 -*-
"""taxonomy.yaml + icons/ -> draw.io shape libraries (dist/).

저장소는 컬러 SVG 만 관리한다. 블랙 팔레트와 PNG 는 제공하지 않는다.

팔레트 1개 = 라이브러리 XML 1개. 디렉터리 번호가 곧 팔레트 번호이자 패널 순서다.
SVG 원본을 base64로 임베드하므로 네트워크 없이 동작하고, 내보내기(PNG/PDF)에서도
아이콘이 그대로 렌더링된다.

    python tools/make_drawio_libs.py            # dist/ 에 생성
    python tools/make_drawio_libs.py --dry-run  # 쓰지 않고 점검만
"""
import base64
import html
import json
import sys
import urllib.parse
import zlib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / 'icons'
OUT = ROOT / 'dist'
DRY = '--dry-run' in sys.argv

SIZE_SERVICE = 64
SIZE_RESOURCE = 48
SIZE_FLAT = 64

# scheme.md '그룹 정의' 표의 선 색·선 종류. 키는 컨테이너 슬러그.
GROUP_STYLE = {
    'grp-nhn-cloud':           ('#111111', False),
    'grp-on-premise':          ('#555555', False),
    'grp-organization':        ('#555555', False),
    'grp-project':             ('#555555', False),
    'grp-region':              ('#999999', True),
    'grp-vpc':                 ('#999999', False),
    'grp-subnet':              ('#BBBBBB', False),
    'grp-auto-scaling-group':  ('#125CE7', True),
    'grp-instance-contents':   ('#125CE7', False),
    'grp-server-contents':     ('#BBBBBB', False),
    'grp-nhn-cloud-account':   ('#BBBBBB', False),
}
# 서비스 박스 기본 스타일 (그룹 컨테이너와 구분되도록 점선 회색)
BOX_STYLE = ('#999999', True)

warnings = []


# ---------------------------------------------------------------- svg -> uri

def svg_size(text, default=(60, 60)):
    import re
    m = re.search(r'viewBox="([\d.\s+-]+)"', text, re.I)
    if m:
        v = m.group(1).split()
        if len(v) == 4:
            try:
                return float(v[2]), float(v[3])
            except ValueError:
                pass
    return default


def png_size(blob, default=(60, 60)):
    """PNG IHDR 청크에서 가로·세로를 읽는다 (바이트 16~24)."""
    if blob[:8] == b'\x89PNG\r\n\x1a\n' and blob[12:16] == b'IHDR':
        return (int.from_bytes(blob[16:20], 'big'),
                int.from_bytes(blob[20:24], 'big'))
    return default


def data_uri(path):
    """SVG 또는 PNG 원본을 draw.io style 에 넣을 data URI 로.

    draw.io 스타일 문자열에서는 ';base64' 를 쓸 수 없어 콤마 뒤에 바로 base64를 둔다.
    """
    if path.suffix.lower() == '.png':
        blob = path.read_bytes()
        w, h = png_size(blob)
        return 'data:image/png,%s' % base64.b64encode(blob).decode('ascii'), w, h
    text = path.read_text(encoding='utf-8')
    w, h = svg_size(text)
    b64 = base64.b64encode(text.encode('utf-8')).decode('ascii')
    return 'data:image/svg+xml,%s' % b64, w, h


# ---------------------------------------------------------------- mxlibrary

def compress(xml):
    """Graph.compress = base64(deflateRaw(encodeURIComponent(xml)))"""
    quoted = urllib.parse.quote(xml, safe="!~*'()")
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    raw = co.compress(quoted.encode('utf-8')) + co.flush()
    return base64.b64encode(raw).decode('ascii')


def esc(s):
    return html.escape(s, quote=True)


def model(cells_xml):
    return ('<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
            + cells_xml + '</root></mxGraphModel>')


def icon_entry(title, uri, w, h, size):
    scale = size / max(w, h)
    cw, ch = round(w * scale), round(h * scale)
    style = ('shape=image;html=1;labelBackgroundColor=none;imageAspect=0;aspect=fixed;'
             'verticalLabelPosition=bottom;verticalAlign=top;fontSize=11;'
             'image=%s;' % uri)
    cell = ('<mxCell id="2" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="%d" height="%d" as="geometry"/></mxCell>'
            % (esc(title), esc(style), cw, ch))
    return {'xml': compress(model(cell)), 'w': cw, 'h': ch,
            'aspect': 'fixed', 'title': title}


def container_entry(title, uri, stroke, dashed):
    """그룹 컨테이너·서비스 박스: 크기 조절되는 컨테이너 + 좌상단 모서리 아이콘."""
    gw, gh = 320, 200
    box = ('rounded=0;html=1;whiteSpace=wrap;container=1;collapsible=0;'
           'recursiveResize=0;pointerEvents=0;expand=0;'
           'fillColor=none;strokeColor=%s;%s'
           'verticalAlign=top;align=left;spacingLeft=38;spacingTop=4;'
           'fontSize=12;fontColor=#666666;'
           % (stroke, 'dashed=1;dashPattern=8 4;' if dashed else 'dashed=0;'))
    cells = ('<mxCell id="2" value="%s" style="%s" vertex="1" parent="1">'
             '<mxGeometry x="0" y="0" width="%d" height="%d" as="geometry"/></mxCell>'
             % (esc(title), esc(box), gw, gh))
    if uri:
        badge = ('shape=image;html=1;imageAspect=0;aspect=fixed;movable=0;resizable=0;'
                 'rotatable=0;deletable=0;editable=0;connectable=0;image=%s;' % uri)
        cells += ('<mxCell id="3" value="" style="%s" vertex="1" parent="2">'
                  '<mxGeometry x="6" y="6" width="24" height="24" as="geometry"/></mxCell>'
                  % esc(badge))
    return {'xml': compress(model(cells)), 'w': gw, 'h': gh, 'title': title}


# ---------------------------------------------------------------- collect

def asset_path(pal_dir, sub, slug):
    d = (pal_dir / sub) if sub else pal_dir
    return d / (slug + '.svg')


def add(entries, pal_dir, sub, item, kind, cat=None):
    """taxonomy 항목 1개를 라이브러리 엔트리로."""
    slug = item['slug']
    p = asset_path(pal_dir, sub, slug)
    if not p.exists():
        warnings.append('없음: %s' % p.relative_to(ROOT))
        return
    uri, w, h = data_uri(p)
    title = item.get('name') or slug
    if kind == 'container':
        stroke, dashed = GROUP_STYLE.get(slug, BOX_STYLE)
        entries.append(container_entry(title, uri, stroke, dashed))
    elif kind == 'box':
        entries.append(container_entry(title, uri, *BOX_STYLE))
    else:
        size = SIZE_RESOURCE if kind == 'resource' else SIZE_FLAT
        entries.append(icon_entry(title, uri, w, h, size))


def build(pal):
    pid = pal['id']
    pal_dir = ICONS / pid
    e = []
    kind = pal.get('kind')
    if kind == 'styles':
        return e
    if kind == 'groups':
        for it in pal.get('containers') or []:
            add(e, pal_dir, 'containers', it, 'container')
        for it in pal.get('service_boxes') or []:
            add(e, pal_dir, 'service-boxes', it, 'box')
        return e
    if kind == 'flat':
        for it in pal.get('icons') or []:
            add(e, pal_dir, None, it, 'flat')
        return e
    # category
    ci = pal.get('category_icon')
    if ci:
        item = dict(ci) if isinstance(ci, dict) else {'slug': ci}
        item.setdefault('name', pal['title'].split(' / ')[-1])
        add(e, pal_dir, 'category', item, 'flat')
    for it in pal.get('services') or []:
        add(e, pal_dir, 'services', it, 'service')
    for it in pal.get('resources') or []:
        add(e, pal_dir, 'resources', it, 'resource')
    return e


def main():
    tax = yaml.safe_load((ROOT / 'taxonomy.yaml').read_text(encoding='utf-8'))
    rows = []
    for pal in tax['palettes']:
        entries = build(pal)
        if not entries:
            continue
        out = OUT / ('NHNCloud-%s.xml' % pal['id'])
        payload = json.dumps(entries, ensure_ascii=False, separators=(',', ':'))
        blob = '<mxlibrary>%s</mxlibrary>' % payload
        if not DRY:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(blob, encoding='utf-8')
        rows.append((out.relative_to(ROOT).as_posix(), len(entries), len(blob)))

    for rel, n, b in rows:
        print('%-38s %4d개  %8.1f KB' % (rel, n, b / 1024))
    print('\n라이브러리 %d개 · 엔트리 %d개%s'
          % (len(rows), sum(n for _, n, _ in rows), ' (dry-run, 쓰지 않음)' if DRY else ''))

    if warnings:
        print('\n경고 %d건:' % len(warnings))
        for w in warnings[:8]:
            print('    %s' % w)
        if len(warnings) > 8:
            print('    ... 외 %d건' % (len(warnings) - 8))


main()
