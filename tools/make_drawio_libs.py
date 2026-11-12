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

# 그룹 컨테이너 기본 크기와 모서리 아이콘 크기.
# AWS 는 390x280 박스에 25px 아이콘(48px 서비스 아이콘 기준). 우리는 64px 이라 1.33배.
GROUP_W, GROUP_H = 520, 370
BADGE = 32

# scheme.md '그룹 정의' 표의 선 색·선 종류. 키는 컨테이너 슬러그.
# PPT 15쪽(Icons / Groups)의 도형 값과 일치한다. 모서리 아이콘이 없는 4종은
# taxonomy 에서 icon: false 로 표시하고 박스만 만든다.
GROUP_STYLE = {
    'grp-nhn-cloud':           ('#111111', False),
    'grp-on-premise':          ('#555555', False),
    'grp-organization':        ('#555555', False),
    'grp-project':             ('#555555', False),
    'grp-region':              ('#999999', True),
    'grp-vpc':                 ('#999999', False),
    'grp-availability-zone':   ('#B28FD1', True),
    'grp-subnet':              ('#BBBBBB', False),
    'grp-security-groups':     ('#EE97AA', False),
    'grp-auto-scaling-group':  ('#125CE7', True),
    'grp-instance-contents':   ('#125CE7', False),
    'grp-server-contents':     ('#BBBBBB', False),
    'grp-nhn-cloud-account':   ('#BBBBBB', False),
    'grp-generic-group-dashed': ('#DDDDDD', True),
    'grp-generic-group-solid':  ('#DDDDDD', False),
}
# PPT 15쪽과 Figma `03 Architecture icon` 페이지의 Groups 표(4597:219944) 모두에서
# Auto Scaling Group 만 모서리 아이콘이 좌상단이 아니라 상단 가운데이고, 레이블도
# 그 아이콘 아래에 가운데로 붙는다. 나머지 14종은 모두 좌상단이다.
BADGE_TOP_CENTER = {'grp-auto-scaling-group'}

# 서비스 박스 기본 스타일 (그룹 컨테이너와 구분되도록 점선 회색).
# 현재 taxonomy.yaml 의 service_boxes 는 비어 있다 (PPT 15쪽 그룹 박스만 싣는다).
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


def data_uri(path):
    """SVG 원본을 draw.io style 에 넣을 data URI 로.

    draw.io 스타일 문자열에서는 ';base64' 를 쓸 수 없어 콤마 뒤에 바로 base64를 둔다.
    """
    text = path.read_text(encoding='utf-8')
    w, h = svg_size(text)
    b64 = base64.b64encode(text.encode('utf-8')).decode('ascii')
    return 'data:image/svg+xml,%s' % b64, w, h


# ---------------------------------------------------------------- mxlibrary
LIBRARY_TAGS = 'nhn nhncloud'

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


def container_entry(title, uri, stroke, dashed, badge_center=False):
    """그룹 컨테이너·서비스 박스: 크기 조절되는 컨테이너 + 모서리 아이콘.

    AWS 그룹 도형(aws-sample-groups.svg)에서 실측한 비율을 따른다.
    AWS 는 박스 390x280, 모서리 아이콘 25x25 를 (0,0) 에 밀착시키고
    레이블을 x=32 부터 쓴다. 서비스 아이콘은 48px.
    우리 서비스 아이콘이 64px 이라 1.33배를 적용했다.

    badge_center 면 PPT 의 Auto Scaling Group 처럼 아이콘을 상단 가운데에 두고
    레이블을 그 아래 가운데에 둔다.
    """
    gw, gh = GROUP_W, GROUP_H
    if badge_center:
        # Figma 4597:220072 — 아이콘을 가운데 두고 그 아래 4px 띄워 레이블도 가운데.
        label = 'align=center;spacingLeft=0;spacingTop=%d;' % (BADGE + 4)
        bx = (gw - BADGE) // 2
    elif uri:
        # Figma — 아이콘 32 다음 8px 띄우고 레이블(텍스트 x=40).
        label = 'align=left;spacingLeft=%d;spacingTop=6;' % (BADGE + 8)
        bx = 0
    else:
        # 모서리 아이콘이 없는 4종은 레이블을 아이콘 자리만큼 들여쓰지 않는다
        # (Figma 는 박스 왼쪽에서 10px, PPT 는 박스 왼쪽에 붙임).
        label = 'align=left;spacingLeft=10;spacingTop=6;'
        bx = 0
    box = ('rounded=0;html=1;whiteSpace=wrap;container=1;collapsible=0;'
           'recursiveResize=0;pointerEvents=0;expand=0;'
           'fillColor=none;strokeColor=%s;%s'
           'verticalAlign=top;%s'
           'fontSize=13;fontColor=#666666;'
           % (stroke, 'dashed=1;dashPattern=8 4;' if dashed else 'dashed=0;',
              label))
    cells = ('<mxCell id="2" value="%s" style="%s" vertex="1" parent="1">'
             '<mxGeometry x="0" y="0" width="%d" height="%d" as="geometry"/></mxCell>'
             % (esc(title), esc(box), gw, gh))
    if uri:
        badge = ('shape=image;html=1;imageAspect=0;aspect=fixed;movable=0;resizable=0;'
                 'rotatable=0;deletable=0;editable=0;connectable=0;image=%s;' % uri)
        cells += ('<mxCell id="3" value="" style="%s" vertex="1" parent="2">'
                  '<mxGeometry x="%d" y="0" width="%d" height="%d" as="geometry"/></mxCell>'
                  % (esc(badge), bx, BADGE, BADGE))
    return {'xml': compress(model(cells)), 'w': gw, 'h': gh, 'title': title}


# 엣지 미리보기 크기. 가로 100, 선은 세로 가운데에 둔다(높이 0 이면 패널 썸네일이 찌그러진다).
EDGE_W, EDGE_H = 100, 20


def edge_entry(title, color, pattern, ends):
    """Arrows 팔레트 항목: 도형이 아니라 연결선 스타일 1개.

    PPT 16쪽의 선은 모두 1pt 이고 화살촉은 채운 삼각형(triangle)이다.
    draw.io 에서는 block + endFill=1 이 같은 모양이다.
    """
    arrow = {
        'forward': 'startArrow=none;startFill=0;endArrow=block;endFill=1;',
        'both':    'startArrow=block;startFill=1;endArrow=block;endFill=1;',
        'none':    'startArrow=none;startFill=0;endArrow=none;endFill=0;',
    }[ends]
    dash = 'dashed=1;dashPattern=%s;' % pattern if pattern else 'dashed=0;'
    style = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;jettySize=auto;'
             'orthogonalLoop=1;labelBackgroundColor=#FFFFFF;fontSize=11;'
             'strokeColor=%s;strokeWidth=1;%s%s' % (color, dash, arrow))
    cell = ('<mxCell id="2" value="" style="%s" edge="1" parent="1">'
            '<mxGeometry width="%d" height="%d" relative="1" as="geometry">'
            '<mxPoint x="0" y="%d" as="sourcePoint"/>'
            '<mxPoint x="%d" y="%d" as="targetPoint"/>'
            '</mxGeometry></mxCell>'
            % (esc(style), EDGE_W, EDGE_H, EDGE_H // 2, EDGE_W, EDGE_H // 2))
    return {'xml': compress(model(cell)), 'w': EDGE_W, 'h': EDGE_H, 'title': title}


def style_entries(path):
    """icons/01-arrows/styles.yaml -> 엣지 스타일 엔트리."""
    if not path.exists():
        warnings.append('없음: %s' % path.relative_to(ROOT))
        return []
    data = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    patterns = data.get('dash_patterns') or {}
    out = []
    for it in data.get('arrows') or []:
        dash = it.get('dash', 'solid')
        if dash not in patterns:
            warnings.append('%s: 모르는 dash 값 %r' % (it['slug'], dash))
            continue
        out.append(edge_entry(it.get('name') or it['slug'], it['color'],
                              patterns[dash], it.get('ends', 'forward')))
    return out

# ---------------------------------------------------------------- collect

def asset_path(pal_dir, sub, slug):
    d = (pal_dir / sub) if sub else pal_dir
    return d / (slug + '.svg')


def add(entries, pal_dir, sub, item, kind, cat=None):
    """taxonomy 항목 1개를 라이브러리 엔트리로."""
    slug = item['slug']
    title = item.get('name') or slug
    # PPT 15쪽의 Security Groups·Availability Zone·Generic Group 2종은 모서리 아이콘이
    # 없는 박스다. SVG 를 찾지 않고 컨테이너만 만든다.
    if kind == 'container' and item.get('icon') is False:
        stroke, dashed = GROUP_STYLE.get(slug, BOX_STYLE)
        entries.append(container_entry(title, None, stroke, dashed,
                                       slug in BADGE_TOP_CENTER))
        return
    p = asset_path(pal_dir, sub, slug)
    if not p.exists():
        warnings.append('없음: %s' % p.relative_to(ROOT))
        return
    uri, w, h = data_uri(p)
    if kind == 'container':
        stroke, dashed = GROUP_STYLE.get(slug, BOX_STYLE)
        entries.append(container_entry(title, uri, stroke, dashed,
                                       slug in BADGE_TOP_CENTER))
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
        return style_entries(pal_dir / pal.get('source', 'styles.yaml'))
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
        # 파일명은 팔레트 번호 2자리만 쓴다. clibs 링크 1개에 25개 URL 이 들어가므로
        # 파일명 1자가 25자씩 불어난다. 패널에 보이는 이름은 title 속성이 결정한다.
        out = OUT / ('%s.xml' % pal['id'].split('-')[0])
        payload = json.dumps(entries, ensure_ascii=False, separators=(',', ':'))
        # tags 는 draw.io 가 라이브러리의 모든 아이콘 검색어에 덧붙인다.
        # 검색창에 'nhn load balancer' 처럼 nhn 을 함께 치면 NHN Cloud 아이콘만 남는다
        # (draw.io 검색은 단어 AND 이고 내장 도형에는 nhn 태그가 없다).
        # Configuration libraries 로 등록했을 때만 검색 색인에 들어간다.
        blob = '<mxlibrary title="%s" tags="%s">%s</mxlibrary>' % (
            esc(pal['title']), LIBRARY_TAGS, payload)
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
