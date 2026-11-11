# -*- coding: utf-8 -*-
"""Figma 에서 내보낸 아이콘 SVG 를 저장소 형식으로 정리한다.

Figma 의 노드 내보내기는 부모 프레임의 배경 사각형과 섹션 <g> 래퍼를 함께 담는다.
  <rect width="60" height="60" fill="#F2F2F2"/>        <- 아이콘 칸 배경
  <rect width="10592" height="4946" transform=".."/>   <- 페이지 전체 배경
  <g id="[NHNCloud]_architecture_icon_Color"> <g id="Service Icons_1"> ...
저장소 자산은 60x60 캔버스에 path 만 있는 형태라 위를 제거한다.

    python tools/figma_clean.py <입력.svg> <출력.svg>
    python tools/figma_clean.py --dir <입력디렉터리> <출력디렉터리>
"""
import io
import re
import sys
from pathlib import Path

# 배경으로 간주해 제거할 rect: fill 이 흰색/회색이고 테두리가 없는 전면 사각형
BG_RECT = re.compile(
    r'<rect\b(?=[^>]*\bwidth="(?:60|\d{3,})")'
    r'(?=[^>]*\bfill="(?:#F2F2F2|#f2f2f2|white|#FFFFFF|#ffffff)")'
    r'[^>]*/>',
    re.I)
G_OPEN = re.compile(r'<g\s+id="[^"]*"\s*>')
G_CLOSE = re.compile(r'</g>')


def clean(svg):
    head = re.match(r'<svg[^>]*>', svg)
    if not head:
        raise ValueError('svg 루트를 찾지 못했습니다')
    body = svg[head.end():]
    body = body[:body.rfind('</svg>')]

    body = BG_RECT.sub('', body)
    # transform 없는 단순 <g id=".."> 래퍼만 벗긴다. transform 이 있으면 좌표가 바뀌므로 유지.
    if 'transform=' not in body:
        body = G_OPEN.sub('', body)
        body = G_CLOSE.sub('', body)
    body = re.sub(r'\n\s*\n+', '\n', body).strip()

    return ('<svg width="60" height="60" viewBox="0 0 60 60" fill="none" '
            'xmlns="http://www.w3.org/2000/svg">\n%s\n</svg>\n' % body)


def main():
    args = [a for a in sys.argv[1:] if a != '--dir']
    if '--dir' in sys.argv:
        src, dst = Path(args[0]), Path(args[1])
        dst.mkdir(parents=True, exist_ok=True)
        n = 0
        for p in sorted(src.glob('*.svg')):
            out = clean(io.open(p, encoding='utf-8').read())
            io.open(dst / p.name, 'w', encoding='utf-8', newline='\n').write(out)
            n += 1
        print('%d개 정리 -> %s' % (n, dst))
    else:
        out = clean(io.open(args[0], encoding='utf-8').read())
        io.open(args[1], 'w', encoding='utf-8', newline='\n').write(out)
        print('%s (%d bytes)' % (args[1], len(out)))


main()
