# -*- coding: utf-8 -*-
"""embed/index.html 생성 — draw.io 임베드 방식 시험용 페이지.

배포용 index.html(리다이렉트 방식)과 별개다. 임베드 방식은 다음을 해결한다.
  - 팔레트를 항상 접힌 채로 시작 (expandLibraries: false)
  - 팔레트 순서가 재방문해도 유지됨
  - 라이브러리를 URL 이 아니라 설정으로 전달하므로 링크 길이 제약이 없음

대신 draw.io 가 호스트 페이지에 저장을 위임하는 모드라, 저장·열기를
이 페이지가 직접 처리해야 한다. 그 부분이 아래 save/open 핸들러다.

    python tools/make_embed.py
"""
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OWNER, NAME = 'nhn-cloud', 'Icons'
PREFIX = 'https://%s.github.io/%s/dist/' % (OWNER, NAME)

files = sorted(p.name for p in (ROOT / 'dist').glob('*.xml'))
if not files:
    raise SystemExit('dist/ 가 비어 있습니다. make_drawio_libs.py 를 먼저 실행하세요.')

libs = ',\n    '.join('"U%s%s"' % (PREFIX, f) for f in files)

HTML = '''<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<title>NHN Cloud 아이콘 라이브러리 (임베드 시험판)</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<style>
  html,body{margin:0;height:100%;overflow:hidden;
            font:14px/1.6 -apple-system,"Segoe UI",system-ui,sans-serif}
  #bar{height:38px;display:flex;align-items:center;gap:8px;padding:0 12px;
       background:#f5f5f5;border-bottom:1px solid #ddd;box-sizing:border-box}
  #bar b{font-weight:600;margin-right:6px}
  #bar button{font:inherit;padding:3px 10px;border:1px solid #c6c6c6;border-radius:4px;
              background:#fff;cursor:pointer}
  #bar button:hover{background:#eee}
  #bar span{color:#777;font-size:12px;margin-left:auto}
  #f{border:0;width:100%;height:calc(100% - 38px);display:block}
  #boot{padding:16px;color:#666}
</style>

<div id="bar">
  <b>NHN Cloud 아이콘</b>
  <button id="new">새로 만들기</button>
  <button id="open">열기…</button>
  <button id="save">저장(.drawio)</button>
  <button id="png">PNG 내보내기</button>
  <span id="hint">시험판 · 작업 내용은 이 브라우저에 임시 보관됩니다</span>
  <input id="file" type="file" accept=".drawio,.xml" hidden>
</div>
<div id="boot">draw.io 를 불러오는 중…</div>
<iframe id="f" title="draw.io"
  src="https://embed.diagrams.net/?embed=1&proto=json&configure=1&libraries=1&noSaveBtn=1&noExitBtn=1"></iframe>

<script>
var DRAFT = 'nhncloud-icons-draft';

var CONFIG = {
  // draw.io 내장 팔레트를 끈다
  "defaultLibraries": "",
  "enabledLibraries": [],
  // 저장된 펼침 상태와 무관하게 항상 접힌 채로 시작한다
  "expandLibraries": false,
  // 팔레트를 URL 이 아니라 설정으로 전달한다
  "defaultCustomLibraries": [
    __LIBS__
  ]
};

var f = document.getElementById('f');
var boot = document.getElementById('boot');
var hint = document.getElementById('hint');

function send(o) { f.contentWindow.postMessage(JSON.stringify(o), '*'); }

function draft(v) {
  try { return v === undefined ? localStorage.getItem(DRAFT) : localStorage.setItem(DRAFT, v); }
  catch (e) { return null; }
}

function download(name, blob) {
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
}

function stamp() {
  var d = new Date(), p = function (n) { return (n < 10 ? '0' : '') + n; };
  return d.getFullYear() + p(d.getMonth() + 1) + p(d.getDate()) + '-' + p(d.getHours()) + p(d.getMinutes());
}

window.addEventListener('message', function (evt) {
  if (typeof evt.data !== 'string' || !evt.data.length) return;
  var m;
  try { m = JSON.parse(evt.data); } catch (e) { return; }

  if (m.event === 'configure') {
    send({action: 'configure', config: CONFIG});

  } else if (m.event === 'init') {
    boot.style.display = 'none';
    send({action: 'load', xml: draft() || '', autosave: 1});

  } else if (m.event === 'autosave') {
    draft(m.xml);
    hint.textContent = '임시 저장됨 · ' + new Date().toLocaleTimeString();

  } else if (m.event === 'export') {
    // format:'xml' 이면 <mxfile> 문자열이 m.xml 에, 이미지면 data: URI 가 m.data 에 온다.
    // {action:'save'} 는 임베드 모드에서 응답하지 않으므로 export 로 저장한다.
    if (m.format === 'xml') {
      draft(m.xml);
      download('nhncloud-architecture-' + stamp() + '.drawio',
               new Blob([m.xml], {type: 'application/xml'}));
      hint.textContent = '저장함 · ' + new Date().toLocaleTimeString();
    } else {
      fetch(m.data).then(function (r) { return r.blob(); }).then(function (b) {
        download('nhncloud-architecture-' + stamp() + '.png', b);
      });
    }
  }
});

document.getElementById('save').onclick = function () { send({action: 'export', format: 'xml'}); };
document.getElementById('png').onclick = function () {
  send({action: 'export', format: 'xmlpng', background: '#ffffff', scale: 2});
};
document.getElementById('new').onclick = function () {
  if (!confirm('현재 내용을 지우고 새로 시작할까요?')) return;
  draft('');
  send({action: 'load', xml: '', autosave: 1});
};
document.getElementById('open').onclick = function () { document.getElementById('file').click(); };
document.getElementById('file').onchange = function (e) {
  var file = e.target.files[0];
  if (!file) return;
  var r = new FileReader();
  r.onload = function () { send({action: 'load', xml: String(r.result), autosave: 1}); };
  r.readAsText(file);
  e.target.value = '';
};
</script>
</html>
'''

html = HTML.replace('__LIBS__', libs)
out = ROOT / 'embed' / 'index.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding='utf-8', newline='\n')
print('embed/index.html 생성 (%d bytes, 라이브러리 %d개)' % (len(html), len(files)))
print('배포 주소: https://%s.github.io/%s/embed/' % (OWNER, NAME))
