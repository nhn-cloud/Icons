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


def container_entry(title, uri, stroke, dashed, badge_center=False, mark=None):
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
    out = {'xml': compress(model(cells)), 'w': gw, 'h': gh, 'title': title}
    # Box Type 에는 그룹 컨테이너와 서비스 박스가 같은 이름으로 들어간다(VPC, Security
    # Groups 등). 구성도 생성기가 group: 을 서비스 박스로 잘못 집지 않도록 표시해 둔다.
    # draw.io 는 모르는 키를 무시한다.
    if mark:
        out['k'] = mark
    return out


# 엣지 미리보기 크기. 배포 라이브러리와 같은 값(가로 160, 선이라 높이는 0).
EDGE_W, EDGE_H = 160, 0

# 배포 라이브러리 NHNCloud-Arrows.xml 의 스타일 문자열. 한 글자도 바꾸지 않는다.
EDGE_STYLE = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={color};'
              'strokeWidth=1;dashed={dashed};dashPattern=4 3;'
              'startArrow={start};startFill=1;startSize=6;'
              'endArrow={end};endFill=1;endSize=6;'
              # 글자색은 선 색을 따라가지 않고 네 색 모두 #555555 다(배포본 실측).
              'fontSize=11;fontColor=#555555;labelBackgroundColor=#FFFFFFB3;'
              'labelPadding=2;sketch=0;shadow=0;glass=0;comic=0;'
              'fontFamily=Helvetica;fontStyle=0;')


def edge_entry(title, color, dashed, ends, tags=None):
    """Arrows 팔레트 항목: 도형이 아니라 연결선 스타일 1개."""
    start, end = {'forward': ('none', 'block'),
                  'both':    ('block', 'block'),
                  'none':    ('none', 'none')}[ends]
    style = EDGE_STYLE.format(color=color, dashed=dashed, start=start, end=end)
    cell = ('<mxCell id="2" value="" style="%s" edge="1" parent="1">'
            '<mxGeometry width="%d" relative="1" as="geometry">'
            '<mxPoint x="0" y="0" as="sourcePoint"/>'
            '<mxPoint x="%d" y="0" as="targetPoint"/>'
            '</mxGeometry></mxCell>' % (esc(style), EDGE_W, EDGE_W))
    out = {'xml': compress(model(cell)), 'w': EDGE_W, 'h': EDGE_H, 'title': title}
    if tags:
        out['tags'] = tags
    return out


def style_entries(path):
    """icons/01-arrows/styles.yaml -> 엣지 스타일 엔트리."""
    if not path.exists():
        warnings.append('없음: %s' % path.relative_to(ROOT))
        return []
    data = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    out = []
    for it in data.get('arrows') or []:
        out.append(edge_entry(it.get('name') or it['slug'], it['color'],
                              int(it.get('dashed', 0)), it.get('ends', 'forward'),
                              it.get('tags')))
    return out


def raw_entries(pal):
    """저장해 둔 mxGraphModel 을 그대로 엔트리로.

    Annotations 는 아이콘이 아니라 draw.io 도형이라 SVG 에서 만들 수
    없다. 사내 배포 라이브러리에서 풀어 icons/ 에 XML 로 두고 여기서 다시 압축한다.
    """
    out = []
    for it in pal.get('items') or []:
        src = ICONS / it['src']
        if not src.exists():
            warnings.append('없음: %s' % src.relative_to(ROOT))
            continue
        e = {'xml': compress(src.read_text(encoding='utf-8').strip()),
             'w': it['w'], 'h': it['h'], 'title': it.get('name') or it['slug']}
        if it.get('aspect'):
            e['aspect'] = it['aspect']
        if it.get('tags'):
            e['tags'] = it['tags']
        out.append(e)
    return out

# ------------------------------------------------------------- compositions

def composition_entries(pal, built):
    """구성도 명세(YAML) 1개 = 라이브러리 엔트리 1개.

    끌어다 놓으면 그룹 박스·아이콘·연결선이 한꺼번에 들어가는 예시 구성도다.
    도형은 이번 실행에서 이미 만든 다른 팔레트의 엔트리에서 꺼내 쓴다.
    dist/ 의 지난 결과를 읽지 않으므로 taxonomy 를 고친 직후에도 어긋나지 않는다.
    """
    import nhn_diagram as nd
    shapes = []
    for pid, title, entries in built:
        palette = title.replace('NHN Cloud / ', '')
        for e in entries:
            shapes.append({'palette': palette, 'no': int(pid.split('-')[0]),
                           'title': e['title'], 'w': e.get('w'), 'h': e.get('h'),
                           'k': e.get('k'), 'xml': nd._decode(e['xml'])})
    lib = nd.Library(shapes)
    out = []
    for it in pal.get('compositions') or []:
        src = (ICONS / it['src']) if it.get('src') else               (ICONS / pal['id'] / 'compositions' / (it['slug'] + '.yaml'))
        if not src.exists():
            warnings.append('없음: %s' % src.relative_to(ROOT))
            continue
        spec = yaml.safe_load(src.read_text(encoding='utf-8'))
        cells, w, h = nd.compose(spec, lib)
        out.append({'xml': compress(model(''.join(cells))),
                    'w': round(w), 'h': round(h),
                    'title': it.get('name') or it['slug']})
    return out


# ---------------------------------------------------------------- collect

def asset_path(pal_dir, sub, item):
    """자산 경로. `src` 가 있으면 icons/ 기준 경로로 본다.

    팔레트는 아이콘 유형(Services·Resources·General…)으로 묶고, icons/ 는 서비스
    카테고리(compute·network…)로 두기 때문에 둘이 1:1 이 아니다. 같은 파일이 두
    팔레트에 들어가기도 한다(카테고리 아이콘은 General 과 Extra 양쪽).
    """
    if item.get('src'):
        return ICONS / item['src']
    d = (pal_dir / sub) if sub else pal_dir
    return d / (item['slug'] + '.svg')


def add(entries, pal_dir, sub, item, kind, cat=None):
    """taxonomy 항목 1개를 라이브러리 엔트리로."""
    slug = item['slug']
    title = item.get('name') or slug
    # PPT 15쪽의 Security Groups·Availability Zone·Generic Group 2종은 모서리 아이콘이
    # 없는 박스다. SVG 를 찾지 않고 컨테이너만 만든다.
    if kind == 'container' and item.get('icon') is False:
        stroke, dashed = GROUP_STYLE.get(slug, BOX_STYLE)
        entries.append(container_entry(title, None, stroke, dashed,
                                       slug in BADGE_TOP_CENTER, mark='g'))
        return
    p = asset_path(pal_dir, sub, item)
    if not p.exists():
        warnings.append('없음: %s' % p.relative_to(ROOT))
        return
    uri, w, h = data_uri(p)
    if kind == 'container':
        stroke, dashed = GROUP_STYLE.get(slug, BOX_STYLE)
        entries.append(container_entry(title, uri, stroke, dashed,
                                       slug in BADGE_TOP_CENTER, mark='g'))
    elif kind == 'box':
        entries.append(container_entry(title, uri, *BOX_STYLE, mark='b'))
    else:
        size = SIZE_RESOURCE if kind == 'resource' else SIZE_FLAT
        entries.append(icon_entry(title, uri, w, h, size))


def build(pal, built):
    pid = pal['id']
    pal_dir = ICONS / pid
    e = []
    kind = pal.get('kind')
    if kind == 'styles':
        src = pal.get('source', 'styles.yaml')
        return style_entries(ICONS / src if '/' in src else pal_dir / src)
    if kind == 'raw':
        return raw_entries(pal)
    if kind == 'compositions':
        return composition_entries(pal, built)
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
    dropped = []        # taxonomy 에서 빠져 지운 XML
    built = []          # (팔레트 id, title, 엔트리) — compositions 가 도형을 꺼내 쓴다
    made = {}           # 팔레트 id -> 엔트리

    # compositions 는 다른 팔레트의 도형을 꺼내 쓰므로 나중에 만든다.
    # 팔레트 번호(= 패널 순서)와 무관하게 동작해야 해서 생성 순서와 출력 순서를 나눈다.
    todo = [p for p in tax['palettes'] if p.get('kind') != 'compositions']
    todo += [p for p in tax['palettes'] if p.get('kind') == 'compositions']
    for pal in todo:
        entries = build(pal, built)
        made[pal['id']] = entries
        if entries:
            built.append((pal['id'], pal['title'], entries))

    for pal in tax['palettes']:        # 쓰기는 taxonomy 순서대로
        entries = made.get(pal['id'])
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

    # taxonomy 에서 빠진 팔레트의 XML 은 지운다. 남겨 두면 카탈로그가 dist/*.xml 을
    # 훑어 만들기 때문에 없앤 팔레트가 계속 보인다.
    keep = {r.rsplit('/', 1)[-1] for r, _, _ in rows}
    for stale in sorted(OUT.glob('[0-9][0-9].xml')):
        if stale.name not in keep:
            if not DRY:
                stale.unlink()
            dropped.append(stale.relative_to(ROOT).as_posix())

    for rel, n, b in rows:
        print('%-38s %4d개  %8.1f KB' % (rel, n, b / 1024))
    for rel in dropped:
        print('%-38s  지움 (taxonomy 에 없음)' % rel)
    print('\n라이브러리 %d개 · 엔트리 %d개%s'
          % (len(rows), sum(n for _, n, _ in rows), ' (dry-run, 쓰지 않음)' if DRY else ''))

    if warnings:
        print('\n경고 %d건:' % len(warnings))
        for w in warnings[:8]:
            print('    %s' % w)
        if len(warnings) > 8:
            print('    ... 외 %d건' % (len(warnings) - 8))


main()
