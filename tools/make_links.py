# -*- coding: utf-8 -*-
"""dist/ 의 라이브러리로 draw.io clibs 배포 링크 1개를 만든다.

    python tools/make_links.py                      # GitHub Pages 기준 (권장)
    python tools/make_links.py --host raw           # raw.githubusercontent.com
    python tools/make_links.py --branch draft       # 브랜치 지정
    python tools/make_links.py --markdown           # README 에 붙일 한 줄

clibs 링크는 라이브러리 1개마다 URL 이 하나씩 들어가므로, 팔레트가 25개면
링크가 길어진다. 그래서 파일명을 팔레트 번호 2자리로 줄였고
(패널 이름은 XML 의 title 속성이 결정한다), 더 짧은 GitHub Pages 도메인을 기본으로 쓴다.

| 호스트 | 링크 길이 | 비고 |
| raw    | 약 2,060자 | 별도 설정 없이 바로 동작 |
| pages  | 약 1,440자 | 저장소에 GitHub Pages 를 켜야 함 |

두 호스트 모두 draw.io 가 요구하는 Access-Control-Allow-Origin: * 을 보낸다.
"""
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = 'nhn-cloud/Icons'
OWNER, NAME = REPO.split('/')
EDITOR = 'https://app.diagrams.net/?clibs=%s'

argv = sys.argv
BRANCH = argv[argv.index('--branch') + 1] if '--branch' in argv else 'main'
HOST = argv[argv.index('--host') + 1] if '--host' in argv else 'pages'
MARKDOWN = '--markdown' in argv

if HOST == 'raw':
    PREFIX = 'https://raw.githubusercontent.com/%s/%s/dist/' % (REPO, BRANCH)
elif HOST == 'pages':
    PREFIX = 'https://%s.github.io/%s/dist/' % (OWNER, NAME)
else:
    raise SystemExit("--host 는 raw 또는 pages")

files = sorted(p.name for p in (ROOT / 'dist').glob('*.xml'))
if not files:
    raise SystemExit('dist/ 에 라이브러리가 없습니다. make_drawio_libs.py 를 먼저 실행하세요.')

link = EDITOR % ';'.join('U' + urllib.parse.quote(PREFIX + f, safe='') for f in files)

if MARKDOWN:
    print('[NHN Cloud 아이콘 라이브러리 열기](%s)' % link)
else:
    print('팔레트 %d개 · %d자 · host=%s%s'
          % (len(files), len(link), HOST, '' if HOST == 'pages' else ' branch=' + BRANCH))
    if len(link) > 2000:
        print('!! 2000자를 넘습니다. --host pages 를 쓰면 짧아집니다.')
    print()
    print(link)
