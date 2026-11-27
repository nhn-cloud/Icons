# -*- coding: utf-8 -*-
"""Figma `flat icon` 섹션에서 내보낸 SVG 를 Presentation 팔레트 자산으로 정리한다.

figma_clean.py 는 24px 아키텍처 아이콘용이라 노드 export 에 딸려 오는 조상 배경까지는
걷어내지 못한다. MCP download_assets 의 `export` 는 다음을 함께 담는다.

  <rect width="24" height="24" fill="#F5F5F5"/>          <- 노드 칸 배경
  <path d="M-2900 -815 ..." fill="#404040"/>             <- 페이지 전체 프레임
  <path d="..." fill="white" fill-opacity="0.1"/>        <- 그 프레임의 테두리
  <rect width="2120" height="910" transform=".."/>       <- Subpage 배경
  <rect x="-33" y="-45" width="108" height="108" rx="54" <- 조상 장식(원형 배경)

`svgAssets` 쪽은 깨끗하지만 텍스트 레이어를 빼고 준다. 24h · SQL · 방패(IDS/WAF/DDos)
처럼 글자가 그림의 일부인 아이콘은 `export` 를 받아 이 도구로 정리해야 한다.

원본은 크기가 제각각(24x24 ~ 64x64)이라 저장소 규격인 60x60 캔버스에
48px 상자로 맞춰 가운데 정렬한다.

    python tools/figma_flat_import.py <입력디렉터리> <출력디렉터리> [--prefix ic-presentation-]

입력 파일명이 곧 슬러그다. `exp_` 접두사는 export 본을 구분하려고 붙인 것이라 떼어낸다.
"""
import io
import re
import sys
from pathlib import Path

BOX = 48.0          # 60x60 캔버스 안에서 그림이 차지할 상자
CANVAS = 60.0
FAR = 500           # 좌표가 이 값을 넘으면 페이지 프레임으로 본다

SVG_OPEN = re.compile(r'<svg[^>]*>', re.I)
VIEWBOX = re.compile(r'viewBox="([\d.\s+-]+)"', re.I)
TAG = re.compile(r'<(/?)([a-zA-Z][\w-]*)([^>]*?)(/?)>')
ID_ATTR = re.compile(r'\s+id="[^"]*"')
NUM = re.compile(r'-?\d+(?:\.\d+)?')


def _attr(attrs, name):
    m = re.search(r'\b%s="([^"]*)"' % name, attrs)
    return m.group(1) if m else None


def _f(attrs, name, default=0.0):
    v = _attr(attrs, name)
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def is_junk(tag, attrs, vbw, vbh):
    """조상 배경·페이지 프레임이면 True."""
    if tag == 'path':
        d = _attr(attrs, 'd') or ''
        if any(abs(float(n)) >= FAR for n in NUM.findall(d)):
            return True
        return False
    if tag in ('rect', 'circle', 'ellipse'):
        w = _f(attrs, 'width', _f(attrs, 'r') * 2)
        h = _f(attrs, 'height', _f(attrs, 'r') * 2)
        x, y = _f(attrs, 'x'), _f(attrs, 'y')
        fill = (_attr(attrs, 'fill') or '').lower()
        # Subpage 배경처럼 화면만 한 사각형
        if w >= FAR or h >= FAR:
            return True
        # 노드 칸 배경 (#F5F5F5 전면 사각형). flat icon 의 108x108 타일은
        # 흰 원(rx=54)을 깔고 그 위에 그림을 얹어 두므로 white 도 배경으로 본다.
        # 저장소 아이콘은 배경을 두지 않는다 — 장표 바탕색 위에 그대로 올린다.
        if fill in ('#f5f5f5', '#f9f9f9', 'white', '#ffffff') and w >= vbw and h >= vbh:
            return True
        # 조상 장식 — 캔버스 밖에서 시작하면서 캔버스보다 큰 도형
        if (x < 0 or y < 0) and (w > vbw or h > vbh):
            return True
    return False


def clean(svg):
    head = SVG_OPEN.search(svg)
    if not head:
        raise ValueError('svg 루트를 찾지 못했습니다')
    root = head.group(0)
    m = VIEWBOX.search(root)
    if m and len(m.group(1).split()) == 4:
        _, _, vbw, vbh = (float(v) for v in m.group(1).split())
    else:
        vbw, vbh = _f(root, 'width', 24), _f(root, 'height', 24)

    body = svg[head.end():svg.rfind('</svg>')]

    out = []
    skip_depth = 0      # 버리는 요소 안쪽 깊이
    drop_close = []     # 열림을 지운 <g> 자리 표시
    for tok in _tokens(body):
        kind, tag, attrs, selfclose, raw = tok
        if kind == 'text':
            if skip_depth == 0:
                out.append(raw)
            continue
        if kind == 'open':
            if skip_depth or is_junk(tag, attrs, vbw, vbh):
                if not selfclose:
                    skip_depth += 1
                continue
            if tag == 'g' and 'transform=' not in attrs:
                drop_close.append(True)      # 좌표를 바꾸지 않는 래퍼는 벗긴다
                continue
            if tag == 'g':
                drop_close.append(False)
            out.append(ID_ATTR.sub('', raw))
            continue
        # close
        if skip_depth:
            skip_depth -= 1
            continue
        if tag == 'g':
            if drop_close and drop_close.pop():
                continue
        out.append(raw)

    inner = re.sub(r'\n\s*\n+', '\n', ''.join(out)).strip()

    scale = BOX / max(vbw, vbh)
    tx = (CANVAS - vbw * scale) / 2
    ty = (CANVAS - vbh * scale) / 2
    g = '<g transform="translate(%s %s) scale(%s)">' % (_n(tx), _n(ty), _n(scale))
    return ('<svg width="60" height="60" viewBox="0 0 60 60" fill="none" '
            'xmlns="http://www.w3.org/2000/svg">\n%s\n%s\n</g>\n</svg>\n'
            % (g, inner))


def _n(v):
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    return s if s else '0'


def _tokens(body):
    pos = 0
    for m in TAG.finditer(body):
        if m.start() > pos:
            yield ('text', None, None, False, body[pos:m.start()])
        closing, tag, attrs, selfclose = m.groups()
        kind = 'close' if closing else 'open'
        yield (kind, tag, attrs, bool(selfclose), m.group(0))
        pos = m.end()
    if pos < len(body):
        yield ('text', None, None, False, body[pos:])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    prefix = 'ic-presentation-'
    for a in sys.argv[1:]:
        if a.startswith('--prefix'):
            prefix = a.split('=', 1)[1] if '=' in a else ''
    src, dst = Path(args[0]), Path(args[1])
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in sorted(src.glob('*.svg')):
        slug = p.stem
        if slug.startswith('_'):
            continue                      # 쓰지 않기로 한 내려받기
        if slug.startswith('exp_'):
            slug = slug[4:]
        text = clean(io.open(p, encoding='utf-8').read())
        out = dst / (prefix + slug + '.svg')
        io.open(out, 'w', encoding='utf-8', newline='\n').write(text)
        print('%-34s %5d bytes' % (out.name, len(text)))
        n += 1
    print('\n%d개 -> %s' % (n, dst))


if __name__ == '__main__':
    main()
