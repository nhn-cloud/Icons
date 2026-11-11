# -*- coding: utf-8 -*-
"""dist/ 의 라이브러리로 draw.io clibs 배포 링크 1개를 만든다.

    python tools/make_links.py                 # 기본 브랜치(main) 기준
    python tools/make_links.py --branch alpha  # 다른 브랜치
    python tools/make_links.py --markdown      # README 에 붙일 한 줄

링크는 GitHub raw URL 을 draw.io 가 직접 읽는 방식이라
해당 브랜치가 origin 에 푸시되어 있어야 동작한다.
저장소는 컬러 SVG 만 제공하므로 링크도 하나다.
"""
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = 'nhn-cloud/Icons'
RAW = 'https://raw.githubusercontent.com/' + REPO + '/%s/dist/%s'
EDITOR = 'https://app.diagrams.net/?clibs=%s'

argv = sys.argv
BRANCH = argv[argv.index('--branch') + 1] if '--branch' in argv else 'main'
MARKDOWN = '--markdown' in argv

stems = sorted(p.name for p in (ROOT / 'dist').glob('*.xml'))
if not stems:
    raise SystemExit('dist/ 에 라이브러리가 없습니다. make_drawio_libs.py 를 먼저 실행하세요.')

parts = ['U' + urllib.parse.quote(RAW % (BRANCH, s), safe='') for s in stems]
link = EDITOR % ';'.join(parts)

if MARKDOWN:
    print('[NHN Cloud 아이콘 라이브러리 열기](%s)' % link)
else:
    print('팔레트 %d개, URL %d자, 브랜치 %s' % (len(stems), len(link), BRANCH))
    if len(link) > 2000:
        print('!! URL 이 2000자를 넘습니다. 일부 브라우저·프록시에서 잘릴 수 있습니다.')
    print()
    print(link)
