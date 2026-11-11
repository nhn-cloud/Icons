# -*- coding: utf-8 -*-
"""dist/ 의 라이브러리로 draw.io clibs 배포 링크 1개를 만든다.

    python tools/make_links.py                      # GitHub Pages 기준 (권장)
    python tools/make_links.py --host raw           # raw.githubusercontent.com
    python tools/make_links.py --branch draft       # 브랜치 지정
    python tools/make_links.py --markdown           # README 에 붙일 한 줄
    python tools/make_links.py --write-index        # index.html 리다이렉트 페이지 생성

clibs 링크는 라이브러리 1개마다 URL 이 하나씩 들어가므로, 팔레트가 25개면
링크가 길어진다. 그래서 파일명을 팔레트 번호 2자리로 줄였고
(패널 이름은 XML 의 title 속성이 결정한다), 더 짧은 GitHub Pages 도메인을 기본으로 쓴다.

| 호스트 | 링크 길이 | 비고 |
| raw    | 약 2,060자 | 별도 설정 없이 바로 동작 |
| pages  | 약 1,440자 | 저장소에 GitHub Pages 를 켜야 함 |

두 호스트 모두 draw.io 가 요구하는 Access-Control-Allow-Origin: * 을 보낸다.

배포용 짧은 주소가 필요하면 --write-index 로 리다이렉트 페이지를 만든다.
NHN Cloud ShortURL 은 원본 URL 을 255자까지만 받으므로 clibs 링크를 그대로 넣을 수 없다
(팔레트 25개면 CDN 을 써도 1,206자). 리다이렉트 페이지 주소는 30자 안팎이라
그대로 배포하거나 ShortURL 에 넣을 수 있다.
"""
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = 'nhn-cloud/Icons'
OWNER, NAME = REPO.split('/')
# libs=none 으로 draw.io 내장 팔레트(일반/기타/고급/기본/화살표/순서도/ER/UML)를 끈다.
# libs 를 생략하면 기본 세트가 켜지고, 빈 값(libs=)은 생략과 같게 취급된다.
# 스크래치 패드는 사용자 기능이라 URL 로 끌 수 없다(비어 있어 방해되지 않음).
EDITOR = 'https://app.diagrams.net/?libs=none&clibs=%s'

argv = sys.argv
BRANCH = argv[argv.index('--branch') + 1] if '--branch' in argv else 'main'
HOST = argv[argv.index('--host') + 1] if '--host' in argv else 'pages'
MARKDOWN = '--markdown' in argv
WRITE_INDEX = '--write-index' in argv

if HOST == 'raw':
    PREFIX = 'https://raw.githubusercontent.com/%s/%s/dist/' % (REPO, BRANCH)
elif HOST == 'pages':
    PREFIX = 'https://%s.github.io/%s/dist/' % (OWNER, NAME)
else:
    raise SystemExit("--host 는 raw 또는 pages")

files = sorted(p.name for p in (ROOT / 'dist').glob('*.xml'))
if not files:
    raise SystemExit('dist/ 에 라이브러리가 없습니다. make_drawio_libs.py 를 먼저 실행하세요.')

# 패널 표시 순서에 대한 실측 결과:
#   최초 방문(저장된 설정 없음) -> clibs 의 역순으로 쌓인다
#   재방문                      -> clibs 순서 그대로 쌓인다
# 둘을 동시에 만족시킬 수 없다. 재방문이 일반적이므로 자연 순서를 쓴다.
# 그 결과 아주 처음 한 번만 Retired 가 위에 오고, 이후에는 계속 정상 순서다.
link = EDITOR % ';'.join('U' + urllib.parse.quote(PREFIX + f, safe='') for f in files)

# draw.io 탭 제목은 열린 파일 이름을 따른다(title 파라미터는 무시된다).
# 이름만 있는 빈 시작 파일을 #U 로 열어 "제목 없는 다이어그램" 대신 이름이 나오게 한다.
# 파일명에 한글을 쓰면 제목에 퍼센트 인코딩된 채 나오므로 ASCII 로 둔다(공백은 그대로 보인다).
STARTER = 'https://%s.github.io/%s/NHN Cloud Icons.drawio' % (OWNER, NAME)
link += '#U' + urllib.parse.quote(STARTER, safe='')

INDEX = """<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<title>NHN Cloud 아이콘 라이브러리</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<style>
  body{font:15px/1.7 -apple-system,"Segoe UI",system-ui,sans-serif;color:#222;
       max-width:34rem;margin:18vh auto;padding:0 1.5rem}
  a{color:#125DE6}
  p.sub{color:#666;font-size:13px}
</style>
<h1>NHN Cloud 아이콘 라이브러리</h1>
<p>draw.io 로 이동하는 중입니다. 자동으로 열리지 않으면 아래를 누르세요.</p>
<p><a id="go" href="__LINK__">draw.io 에서 라이브러리 열기</a></p>
<p class="sub">팔레트 __N__개가 왼쪽 도형 패널에 추가됩니다.
원본 저장소: <a href="https://github.com/__REPO__">github.com/__REPO__</a></p>
<!-- 리다이렉트는 한 가지만 쓴다. meta refresh 와 함께 쓰면 두 번 이동해
     draw.io 가 라이브러리를 중복 등록할 수 있다. -->
<script>location.replace(document.getElementById("go").href);</script>
</html>
"""

if WRITE_INDEX:
    html = (INDEX.replace('__LINK__', link.replace('&', '&amp;'))
                 .replace('__N__', str(len(files)))
                 .replace('__REPO__', REPO))
    out = ROOT / 'index.html'
    out.write_text(html, encoding='utf-8', newline='\n')
    print('index.html 생성 (%d바이트). host=%s, 팔레트 %d개' % (len(html), HOST, len(files)))
    print('배포 주소 예:')
    print('  https://%s.github.io/%s/            (GitHub Pages, %d자)'
          % (OWNER, NAME, len('https://%s.github.io/%s/' % (OWNER, NAME))))
    print('  CDN 에 올리면 더 짧게 가능')
elif MARKDOWN:
    print('[NHN Cloud 아이콘 라이브러리 열기](%s)' % link)
else:
    print('팔레트 %d개 · %d자 · host=%s%s'
          % (len(files), len(link), HOST, '' if HOST == 'pages' else ' branch=' + BRANCH))
    if len(link) > 2000:
        print('!! 2000자를 넘습니다. --host pages 를 쓰면 짧아집니다.')
    print()
    print(link)
