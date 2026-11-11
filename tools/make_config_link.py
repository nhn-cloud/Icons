# -*- coding: utf-8 -*-
"""dist/ 의 라이브러리로 draw.io '설정 링크(#_CONFIG_)' 배포 페이지를 만든다.

    python tools/make_config_link.py                               # 링크와 설정 JSON 출력
    python tools/make_config_link.py --write-index                 # index.html 생성 (배포용)
    python tools/make_config_link.py --write-index --branch draft  # 라이브러리 브랜치 지정

clibs 링크(make_links.py)와 다른 점
-----------------------------------
clibs 는 URL 로 팔레트를 '여는' 것뿐이라 펼침 여부를 정할 수 없다. draw.io 는
expandLibraries 설정이 true(기본값)이면 팔레트를 펼친 채로 연다. 이 값은 URL 파라미터로
줄 수 없고 '설정'으로만 바꿀 수 있다.

이 스크립트는 공식 app.diagrams.net 의 설정 링크(#_CONFIG_ + 압축 JSON)를 만든다.
사용자가 한 번 열고 확인 2회를 누르면 설정이 그 브라우저에 저장되고, 이후로는
아무 파라미터 없는 app.diagrams.net 을 열어도 NHN Cloud 팔레트가 접힌 채로 뜬다.
공식 사이트를 그대로 쓰므로 내보내기·클라우드 저장 기능은 모두 유지된다.

설정 내용
---------
  version                 dist/ 내용의 해시. 팔레트가 바뀌면 값이 바뀌어 사용자 브라우저의
                          패널 구성이 새 팔레트 목록으로 다시 만들어진다.
  expandLibraries=false   팔레트를 항상 접힌 채로 시작 (draw.io 22.1.6 이상)
  libraries               '그 외 도형' 창에 'NHN Cloud' 항목을 추가하고 팔레트 25개를 묶는다.
                          AWS 처럼 체크 하나로 켜고 끌 수 있고, 아이콘이 도형 검색에도 잡힌다.
                          preload=true 로 모든 팔레트를 시작 시 읽어 검색 색인에 넣는다.
  defaultLibraries        처음 켜 둘 항목. 'nhncloud' 하나만 켜고 내장 팔레트는 끈다.

{"merge": {...}} 형식이라 사용자가 따로 가진 설정은 지우지 않고 위 키만 덮어쓴다.

라이브러리 호스트
----------------
기본은 raw.githubusercontent.com 이다. draw.io 가 CORS 허용 목록으로 직접 읽는 호스트라
draw.io 프록시를 거치지 않는다(github.io 는 프록시를 거친다). '그 외 도형' 항목으로 등록한
라이브러리는 못 읽어도 지워지지 않고 팔레트에 오류만 표시된다.
설정 링크는 압축되므로 URL 길이는 문제가 되지 않는다(팔레트 25개 기준 약 400자).

배포 페이지(index.html) 동작
---------------------------
draw.io 는 #_CONFIG_ 링크를 열 때마다 확인 창을 2번 띄운다. 매번 띄우지 않도록
배포 페이지가 자기 도메인 localStorage 에 적용한 version 을 기억한다.

  처음 방문 또는 version 이 바뀜  -> 설정 링크로 이동 (확인 2회)
  이미 적용됨                     -> app.diagrams.net 으로 바로 이동
  주소 뒤에 ?setup               -> 무조건 설정 링크로 이동 (팔레트가 안 보일 때)
"""
import base64
import hashlib
import json
import sys
import urllib.parse
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = 'nhn-cloud/Icons'
OWNER, NAME = REPO.split('/')

argv = sys.argv
def opt(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

# 검증용으로 바꿀 수 있게 열어 둔다. 배포에는 기본값을 쓴다.
EDITOR = opt('--editor', 'https://app.diagrams.net/')
BRANCH = opt('--branch', 'main')
HOST = opt('--host', 'raw')
if HOST == 'raw':
    _default_prefix = 'https://raw.githubusercontent.com/%s/%s/dist/' % (REPO, BRANCH)
elif HOST == 'pages':
    _default_prefix = 'https://%s.github.io/%s/dist/' % (OWNER, NAME)
else:
    raise SystemExit('--host 는 raw 또는 pages')
PREFIX = opt('--prefix', _default_prefix)
WRITE_INDEX = '--write-index' in argv
OUT = Path(opt('--out', str(ROOT / 'index.html')))

files = sorted((ROOT / 'dist').glob('*.xml'))
if not files:
    raise SystemExit('dist/ 에 라이브러리가 없습니다. make_drawio_libs.py 를 먼저 실행하세요.')

urls = [PREFIX + p.name for p in files]

h = hashlib.sha256()
for p in files:
    h.update(p.name.encode())
    h.update(p.read_bytes())
h.update(PREFIX.encode())
h.update(b'config-schema-2')  # 설정 구조를 바꾸면 이 값을 올린다
VERSION = 'nhncloud-icons-' + h.hexdigest()[:10]

import html as _html
import re as _re

def lib_title(path):
    m = _re.match(r'<mxlibrary title="([^"]*)"', path.read_text(encoding='utf-8')[:300])
    return _html.unescape(m.group(1)) if m else path.stem

ENTRY_ID = 'nhncloud'
PREVIEW = PREFIX.rsplit('/dist/', 1)[0] + '/icons/05-groups/containers/grp-nhn-cloud.svg'

config = {'merge': {
    'version': VERSION,
    'expandLibraries': False,
    'defaultLibraries': ENTRY_ID,
    'libraries': [{
        'title': {'main': 'NHN Cloud'},
        'entries': [{
            'id': ENTRY_ID,
            'title': {'main': 'NHN Cloud'},
            'desc': {'main': 'NHN Cloud 공식 아키텍처 아이콘 (%d개 팔레트)' % len(files)},
            'preview': PREVIEW,
            'libs': [{'title': {'main': lib_title(p)}, 'url': u, 'preload': True}
                     for p, u in zip(files, urls)],
        }],
    }],
}}


def drawio_compress(text):
    """draw.io Graph.compress(text) 와 같은 결과.
    base64( deflateRaw( encodeURIComponent(text) ) )"""
    encoded = urllib.parse.quote(text, safe="-_.!~*'()")
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    raw = c.compress(encoded.encode('ascii')) + c.flush()
    return base64.b64encode(raw).decode('ascii')


config_json = json.dumps(config, ensure_ascii=False, separators=(',', ':'))
link = EDITOR + '#_CONFIG_' + drawio_compress(config_json)

INDEX = """<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<title>NHN Cloud 아이콘 라이브러리</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<style>
  body{font:15px/1.7 -apple-system,"Segoe UI",system-ui,sans-serif;color:#222;
       max-width:36rem;margin:18vh auto;padding:0 1.5rem}
  a{color:#125DE6}
  p.sub{color:#666;font-size:13px}
</style>
<h1>NHN Cloud 아이콘 라이브러리</h1>
<p id="msg">draw.io 로 이동하는 중입니다.</p>
<p><a id="go" href="__EDITOR__">draw.io 열기</a> ·
   <a id="setup" href="__LINK__">팔레트 다시 설정</a></p>
<p class="sub">처음 열 때 draw.io 가 설정 적용 여부를 두 번 묻습니다. 두 번 모두 <b>확인</b>을 누르세요.
팔레트 __N__개가 접힌 상태로 왼쪽 도형 패널에 추가됩니다.<br>
팔레트가 보이지 않으면 이 주소 뒤에 <code>?setup</code> 을 붙여 다시 여세요.<br>
원본 저장소: <a href="https://github.com/__REPO__">github.com/__REPO__</a></p>
<script>
(function () {
  var VERSION = '__VERSION__';
  var KEY = 'nhncloud-drawio-config';
  var setupUrl = document.getElementById('setup').href;
  var editorUrl = document.getElementById('go').href;
  var applied = null;
  try { applied = localStorage.getItem(KEY); } catch (e) {}
  var force = /(^|[?&])setup\\b/.test(location.search);

  if (force || applied !== VERSION) {
    try { localStorage.setItem(KEY, VERSION); } catch (e) {}
    location.replace(setupUrl);
  } else {
    location.replace(editorUrl);
  }
})();
</script>
</html>
"""

if WRITE_INDEX:
    html = (INDEX.replace('__LINK__', link)
                 .replace('__EDITOR__', EDITOR)
                 .replace('__VERSION__', VERSION)
                 .replace('__N__', str(len(files)))
                 .replace('__REPO__', REPO))
    OUT.write_text(html, encoding='utf-8', newline='\n')
    print('%s 생성. 팔레트 %d개, version=%s, 설정 링크 %d자'
          % (OUT.name, len(files), VERSION, len(link)))
    print('배포 주소: https://%s.github.io/%s/' % (OWNER, NAME))
else:
    print('팔레트 %d개 · version=%s · 링크 %d자' % (len(files), VERSION, len(link)))
    print()
    print(json.dumps(config, ensure_ascii=False, indent=2))
    print()
    print(link)
