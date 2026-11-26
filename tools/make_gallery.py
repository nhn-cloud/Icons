# -*- coding: utf-8 -*-
"""dist/ 의 라이브러리로 아이콘 카탈로그 페이지(gallery.html)를 만든다.

    python tools/make_gallery.py                 # gallery.html 생성
    python tools/make_gallery.py --out x.html

왜 따로 두는가
--------------
draw.io 의 도형 검색은 이름을 이미 알 때만 쓸모가 있다. 어떤 아이콘이 있는지
훑어보려면 Figma 의 `flat icon` 페이지처럼 한눈에 펼쳐 놓은 화면이 필요하다.

클릭하면 열리는 원리
------------------
draw.io 는 URL 조각 `#R<데이터>` 에 담긴 mxGraphModel 을 그대로 읽는다
(`drawio_open.py` 와 같은 방식). 조각은 서버로 가지 않으므로 사내 프록시를 타지 않고,
도형 SVG 가 base64 로 박혀 있어 라이브러리를 설치하지 않은 브라우저에서도 그려진다.

타일마다 셋을 준다.
  열기    draw.io 새 탭에서 그 도형 하나를 올린 새 그림으로 연다. 거기서 저장한다.
  복사    mxGraphModel XML 을 클립보드에 넣는다. 편집 중인 그림에 Ctrl+V 로 붙인다.
  SVG     원본 SVG 를 내려받는다 (PPT·문서에 넣을 때).

`복사` 가 실제로는 가장 많이 쓰인다. 이미 그리던 구성도에 아이콘 하나를 더할 때
새 탭을 여는 것보다 붙여넣는 쪽이 빠르다.
"""
import base64
import html
import json
import re
import sys
import urllib.parse
import zlib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
EDITOR = 'https://app.diagrams.net/'

argv = sys.argv
OUT = Path(argv[argv.index('--out') + 1]) if '--out' in argv else ROOT / 'gallery.html'

IMAGE = re.compile(r'image=data:image/svg\+xml,([A-Za-z0-9+/=]+)')
STROKE = re.compile(r'strokeColor=(#[0-9A-Fa-f]{6}|none)')


def decode(s):
    return urllib.parse.unquote(zlib.decompress(base64.b64decode(s), -15).decode('utf-8'))


def encode(xml):
    """draw.io Graph.compress — drawio_open.py 와 같은 형식."""
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    quoted = urllib.parse.quote(xml).encode('ascii')
    return base64.b64encode(co.compress(quoted) + co.flush()).decode('ascii')


def source_map():
    """(팔레트 제목, 표시명) -> icons/ 원본 SVG 경로. SVG 내려받기 링크에 쓴다."""
    tax = yaml.safe_load((ROOT / 'taxonomy.yaml').read_text(encoding='utf-8'))
    out = {}
    for pal in tax['palettes']:
        pid = pal['id']
        buckets = [(None, pal.get('icons')), ('services', pal.get('services')),
                   ('resources', pal.get('resources')), ('containers', pal.get('containers')),
                   ('service-boxes', pal.get('service_boxes'))]
        ci = pal.get('category_icon')
        if ci:
            item = dict(ci) if isinstance(ci, dict) else {'slug': ci}
            item.setdefault('name', pal['title'].split(' / ')[-1])
            buckets.append(('category', [item]))
        for sub, items in buckets:
            for it in items or []:
                p = ROOT / 'icons' / pid / (sub or '') / (it['slug'] + '.svg')
                if p.exists():
                    out[(pal['title'], it.get('name') or it['slug'])] = \
                        p.relative_to(ROOT).as_posix()
    return out


def thumb(model, composition=False):
    """타일 미리보기. 이미지가 없는 항목(연결선·테두리만 있는 그룹 박스)은 직접 그린다."""
    if composition:
        # 구성도는 도형이 수십 개라 첫 아이콘을 썸네일로 쓰면 무엇인지 오해를 부른다.
        return ('<svg viewBox="0 0 60 60"><rect x="3" y="8" width="54" height="44" fill="none" '
                'stroke="#999" stroke-width="2"/><rect x="9" y="16" width="16" height="12" '
                'fill="#125DE6"/><rect x="35" y="16" width="16" height="12" fill="#125DE6"/>'
                '<rect x="9" y="34" width="16" height="12" fill="#B0C4E8"/>'
                '<rect x="35" y="34" width="16" height="12" fill="#B0C4E8"/>'
                '<path d="M25 22H35M25 40H35M17 28V34M43 28V34" stroke="#999"/></svg>')
    m = IMAGE.search(model)
    if m:
        return '<img loading="lazy" src="data:image/svg+xml;base64,%s" alt="">' % m.group(1)
    sc = STROKE.search(model)
    color = sc.group(1) if sc and sc.group(1) != 'none' else '#999999'
    dash = ' stroke-dasharray="6 3"' if 'dashed=1' in model else ''
    if 'edge="1"' in model:
        return ('<svg viewBox="0 0 60 60"><path d="M4 30H50" stroke="%s" stroke-width="2"%s/>'
                '<path d="M50 26L57 30L50 34Z" fill="%s"/></svg>' % (color, dash, color))
    return ('<svg viewBox="0 0 60 60"><rect x="4" y="10" width="52" height="40" fill="none" '
            'stroke="%s" stroke-width="2"%s/></svg>' % (color, dash))


def build():
    srcs = source_map()
    palettes = []
    total = 0
    for p in sorted(DIST.glob('*.xml')):
        text = p.read_text(encoding='utf-8')
        m = re.search(r'<mxlibrary[^>]*\stitle="([^"]*)"[^>]*>(.*)</mxlibrary>', text, re.S)
        if not m:
            continue
        title = html.unescape(m.group(1))
        short = title.replace('NHN Cloud / ', '')
        composition = p.stem == '06'
        tiles = []
        for e in json.loads(m.group(2)):
            model = decode(e['xml'])
            name = e.get('title') or ''
            tiles.append({
                'name': name,
                'thumb': thumb(model, composition),
                'url': EDITOR + '?title=' + urllib.parse.quote(name) + '#R'
                       + urllib.parse.quote(encode(model)),
                'xml': model,
                'w': e.get('w') or 64,
                'h': e.get('h') or 64,
                'aspect': e.get('aspect') or '',
                'svg': srcs.get((title, name)),
            })
            total += 1
        palettes.append({'no': p.stem, 'title': short, 'tiles': tiles})

    body = []
    for pal in palettes:
        body.append('<section><h2>%s <small>%d</small></h2><div class="grid">'
                    % (html.escape(pal['title']), len(pal['tiles'])))
        for t in pal['tiles']:
            svg_link = ('<a href="%s" download>SVG</a>' % html.escape(t['svg'])) if t['svg'] else ''
            # XML 은 속성에 담는다. <script> 안에 넣으면 그 안의 텍스트는 원시 텍스트라
            # 파서가 실체 참조를 되돌리지 않아 복사한 값이 &lt;mxGraphModel&gt; 로 깨진다.
            body.append(
                '<figure data-name="%s" data-palette="%s" data-title="%s"'
                ' data-w="%s" data-h="%s" data-aspect="%s" data-xml="%s"'
                ' role="checkbox" aria-checked="false" tabindex="0">'
                '<span class="pic">%s</span>'
                '<figcaption>%s</figcaption>'
                '<div class="act">'
                '<a href="%s" target="_blank" rel="noopener">열기</a>'
                '<button type="button" data-copy="1">복사</button>%s</div>'
                '</figure>'
                % (html.escape(t['name'].lower()), html.escape(pal['title'].lower()),
                   html.escape(t['name'], quote=True),
                   t['w'], t['h'], html.escape(t['aspect'], quote=True),
                   html.escape(t['xml'], quote=True),
                   t['thumb'], html.escape(t['name']),
                   html.escape(t['url'], quote=True), svg_link))
        body.append('</div></section>')

    chips = ''.join('<button type="button" data-filter="%s">%s</button>'
                    % (html.escape(p['title'].lower()), html.escape(p['title']))
                    for p in palettes)

    page = (PAGE.replace('__TOTAL__', str(total))
                .replace('__PALETTES__', str(len(palettes)))
                .replace('__CHIPS__', chips)
                .replace('__BODY__', '\n'.join(body)))
    OUT.write_text(page, encoding='utf-8', newline='\n')
    print('%s 생성. 팔레트 %d개 · 도형 %d개 · %.1f KB'
          % (OUT.name, len(palettes), total, len(page) / 1024))


PAGE = """<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<title>NHN Cloud 아이콘 카탈로그</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<style>
 :root{--line:#e5e5e5;--muted:#666;--accent:#125DE6}
 *{box-sizing:border-box}
 body{font:14px/1.6 -apple-system,"Segoe UI",system-ui,sans-serif;color:#222;margin:0;background:#fff}
 header{position:sticky;top:0;background:#fff;border-bottom:1px solid var(--line);
        padding:14px 20px 10px;z-index:5}
 h1{font-size:17px;margin:0 0 2px}
 p.sub{margin:0 0 10px;color:var(--muted);font-size:12px}
 p.sub a{color:var(--accent)}
 .tools{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
 input[type=search]{flex:0 0 260px;padding:7px 10px;border:1px solid var(--line);
                    border-radius:6px;font:inherit}
 .chips{display:flex;gap:4px;flex-wrap:wrap}
 .chips button{font:11px/1 inherit;padding:6px 9px;border:1px solid var(--line);
               background:#fafafa;border-radius:999px;cursor:pointer;color:#444}
 .chips button[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff}
 main{padding:16px 20px 60px}
 section{margin:0 0 26px}
 h2{font-size:13px;color:#444;margin:0 0 8px;font-weight:600;
    border-bottom:1px solid var(--line);padding-bottom:6px}
 h2 small{color:#aaa;font-weight:400;margin-left:4px}
 .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:6px}
 figure{margin:0;border:1px solid var(--line);border-radius:8px;padding:8px 6px 6px;
        text-align:center;background:#fff;cursor:pointer;position:relative;outline:none}
 figure:hover{border-color:#bbb}
 figure:focus-visible{box-shadow:0 0 0 2px #cfe0ff}
 figure[aria-checked=true]{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
 figure[aria-checked=true]::after{content:"✓";position:absolute;top:4px;right:6px;
        font-size:11px;line-height:1;color:#fff;background:var(--accent);
        border-radius:50%;width:15px;height:15px;display:grid;place-items:center}
 .pic{display:flex;align-items:center;justify-content:center;height:56px}
 .pic img,.pic svg{max-width:48px;max-height:48px;display:block}
 a.open{display:block;text-decoration:none}
 figcaption{font-size:11px;color:#333;margin-top:4px;line-height:1.35;
            word-break:break-word;min-height:30px}
 .act{display:flex;gap:4px;justify-content:center;margin-top:4px}
 .act button,.act a{font:10px/1 inherit;padding:4px 6px;border:1px solid var(--line);
        background:#fafafa;border-radius:4px;cursor:pointer;color:#555;text-decoration:none}
 .act button:hover,.act a:hover{background:#f0f0f0}
 .act button.done{background:var(--accent);border-color:var(--accent);color:#fff}
 section[hidden],figure[hidden]{display:none}
 #empty{color:var(--muted);padding:40px 0;text-align:center}
 #bar{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid var(--line);
      box-shadow:0 -2px 10px rgba(0,0,0,.08);z-index:6}
 #bar[hidden]{display:none}
 #bar .row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:10px 20px 0}
 #bar b{font-size:13px}
 #bar .grow{flex:1}
 #bar button{font:12px/1 inherit;padding:8px 12px;border:1px solid var(--line);
             background:#fafafa;border-radius:6px;cursor:pointer;color:#333}
 #bar button.primary{background:var(--accent);border-color:var(--accent);color:#fff}
 #bar small{color:var(--muted);font-size:11px}
 /* 고른 것을 쌓아 두는 자리. 무엇을 담았는지 눈으로 확인하고 하나씩 뺀다. */
 #tray{display:flex;gap:6px;overflow-x:auto;padding:10px 20px 12px;align-items:flex-end;
       background:#fbfbfc;border-top:1px solid #f0f0f0;margin-top:10px;min-height:92px}
 #tray .chip{position:relative;flex:0 0 auto;width:78px;border:1px solid var(--line);
       border-radius:8px;background:#fff;padding:6px 4px 4px;text-align:center;cursor:pointer}
 #tray .chip:hover{border-color:#f5a3a3}
 #tray .chip .pic{height:40px}
 #tray .chip .pic img,#tray .chip .pic svg{max-width:34px;max-height:34px}
 #tray .chip .nm{font-size:10px;line-height:1.3;color:#444;margin-top:3px;
       overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
 #tray .chip .x{position:absolute;top:-6px;right:-6px;width:17px;height:17px;border-radius:50%;
       background:#fff;border:1px solid var(--line);color:#999;font-size:11px;line-height:1;
       display:grid;place-items:center}
 #tray .chip:hover .x{background:#e5484d;border-color:#e5484d;color:#fff}
 #tray .ph{color:var(--muted);font-size:12px;align-self:center}
</style>
<header>
 <h1>NHN Cloud 아이콘 카탈로그</h1>
 <p class="sub">팔레트 __PALETTES__개 · 도형 __TOTAL__개 &nbsp;|&nbsp;
   <b>타일을 누르면 아래 담는 자리에 쌓입니다.</b> 다 고르고 나서 한꺼번에 열거나 라이브러리로 받습니다.
   하나만 쓸 때는 타일의 <b>열기</b>·<b>복사</b>를 쓰세요.
   &nbsp;·&nbsp; <a href="./?setup">팔레트를 draw.io 에 설치</a></p>
 <div class="tools">
  <input type="search" id="q" placeholder="이름으로 찾기 (예: load, shield, rds)" autocomplete="off">
  <div class="chips" id="chips"><button type="button" data-filter="" aria-pressed="true">전체</button>__CHIPS__</div>
 </div>
</header>
<main>
__BODY__
<p id="empty" hidden>찾는 이름이 없습니다.</p>
</main>
<div id="bar" hidden>
  <div class="row">
    <b>담은 아이콘 <span id="count">0</span>개</b>
    <button type="button" id="open" class="primary">draw.io 에서 열기</button>
    <button type="button" id="lib">라이브러리(.xml) 받기</button>
    <button type="button" id="copyAll">모두 복사</button>
    <button type="button" id="clear">비우기</button>
    <span class="grow"></span>
    <small id="hint">담은 것을 누르면 빠집니다. 라이브러리는 draw.io 의
      <b>파일 &gt; 라이브러리 열기 &gt; 디바이스</b> 로 엽니다.</small>
  </div>
  <div id="tray"></div>
</div>
<script>
(function () {
  var q = document.getElementById('q');
  var chips = document.getElementById('chips');
  var figs = [].slice.call(document.querySelectorAll('figure'));
  var secs = [].slice.call(document.querySelectorAll('section'));
  var pal = '';

  function apply() {
    var t = q.value.trim().toLowerCase();
    figs.forEach(function (f) {
      f.hidden = !((!t || f.dataset.name.indexOf(t) >= 0)
                && (!pal || f.dataset.palette === pal));
    });
    var any = false;
    secs.forEach(function (s) {
      var shown = s.querySelector('figure:not([hidden])');
      s.hidden = !shown;
      if (shown) any = true;
    });
    document.getElementById('empty').hidden = any;
  }

  q.addEventListener('input', apply);
  chips.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    pal = b.dataset.filter;
    [].forEach.call(chips.children, function (c) {
      c.setAttribute('aria-pressed', c === b ? 'true' : 'false');
    });
    apply();
  });

  // ---- 클립보드 -------------------------------------------------------
  function copy(text, btn, label) {
    function done() {
      if (!btn) return;
      var old = btn.textContent;
      btn.classList.add('done');
      btn.textContent = label || '복사됨';
      setTimeout(function () { btn.classList.remove('done'); btn.textContent = old; }, 1200);
    }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (err) {}
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-copy]');
    if (!b) return;
    copy(b.closest('figure').dataset.xml, b);
  });

  // ---- 선택 -----------------------------------------------------------
  var sel = [];
  var bar = document.getElementById('bar');
  var count = document.getElementById('count');
  var tray = document.getElementById('tray');

  function paint() {
    count.textContent = sel.length;
    bar.hidden = sel.length === 0;
    tray.textContent = '';
    sel.forEach(function (fig, i) {
      var chip = document.createElement('div');
      chip.className = 'chip';
      chip.title = fig.dataset.title + ' — 눌러서 빼기';
      chip.dataset.i = i;
      chip.innerHTML = '<span class="x">\\u00d7</span>'
        + '<span class="pic">' + fig.querySelector('.pic').innerHTML + '</span>'
        + '<span class="nm">' + fig.querySelector('figcaption').textContent + '</span>';
      tray.appendChild(chip);
    });
    // 마지막으로 담은 것이 보이게 끝으로 민다.
    tray.scrollLeft = tray.scrollWidth;
    // 막대가 마지막 줄을 가리지 않도록 그만큼 아래를 비운다.
    document.body.style.paddingBottom = sel.length ? bar.offsetHeight + 'px' : '';
  }

  tray.addEventListener('click', function (e) {
    var chip = e.target.closest('.chip');
    if (chip) { toggle(sel[+chip.dataset.i]); }
  });

  function toggle(fig) {
    var i = sel.indexOf(fig);
    if (i >= 0) { sel.splice(i, 1); fig.setAttribute('aria-checked', 'false'); }
    else { sel.push(fig); fig.setAttribute('aria-checked', 'true'); }
    paint();
  }

  document.addEventListener('click', function (e) {
    if (e.target.closest('a, button')) return;
    var fig = e.target.closest('figure');
    if (fig) toggle(fig);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var fig = e.target.closest && e.target.closest('figure');
    if (fig) { e.preventDefault(); toggle(fig); }
  });
  document.getElementById('clear').addEventListener('click', function () {
    sel.forEach(function (f) { f.setAttribute('aria-checked', 'false'); });
    sel = []; paint();
  });

  // ---- 선택한 도형들을 한 그림으로 ------------------------------------
  // 각 도형은 자기만의 mxGraphModel 을 들고 있다. 합칠 때 id 가 겹치므로 도형마다
  // 접두사를 붙여 다시 매기고, parent 가 그 안의 id 를 가리키면 같이 바꾼다.
  // parent="1"(최상위)인 셀만 자리를 옮긴다. 자식은 부모 좌표를 따라간다.
  function merge(figs) {
    var out = [], ser = new XMLSerializer(), x = 0, y = 0, rowH = 0;
    figs.forEach(function (fig, idx) {
      var w = +fig.dataset.w || 64, h = +fig.dataset.h || 64;
      if (x > 0 && x + w > 1200) { x = 0; y += rowH + 60; rowH = 0; }
      var doc = new DOMParser().parseFromString(fig.dataset.xml, 'text/xml');
      var root = doc.getElementsByTagName('root')[0];
      if (!root) return;
      var kids = [].slice.call(root.children).filter(function (c) {
        var id = c.getAttribute('id');
        return id !== '0' && id !== '1';
      });
      var map = {};
      kids.forEach(function (c) { map[c.getAttribute('id')] = 's' + idx + '_' + c.getAttribute('id'); });
      kids.forEach(function (c) {
        c.setAttribute('id', map[c.getAttribute('id')]);
        var p = c.getAttribute('parent');
        if (p && map[p]) { c.setAttribute('parent', map[p]); }
        else if (p === '1') {
          var g = c.getElementsByTagName('mxGeometry')[0];
          if (g) {
            if (c.getAttribute('edge') === '1') {
              // 연결선은 x/y 가 아니라 source·target 점으로 자리가 정해진다.
              // 여기를 안 옮기면 선만 제자리에 남아 다른 도형과 겹친다.
              [].forEach.call(g.getElementsByTagName('mxPoint'), function (pt) {
                pt.setAttribute('x', (parseFloat(pt.getAttribute('x') || 0) + x));
                pt.setAttribute('y', (parseFloat(pt.getAttribute('y') || 0) + y));
              });
            } else {
              g.setAttribute('x', (parseFloat(g.getAttribute('x') || 0) + x));
              g.setAttribute('y', (parseFloat(g.getAttribute('y') || 0) + y));
            }
          }
        }
        out.push(ser.serializeToString(c));
      });
      x += w + 60; rowH = Math.max(rowH, h);
    });
    return '<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
           + out.join('') + '</root></mxGraphModel>';
  }

  // draw.io Graph.compress — base64(deflateRaw(encodeURIComponent(xml))).
  // 라이브러리 항목은 반드시 이 형식이어야 한다. Graph.decompress 가 평문을 거부한다.
  // (그림 쪽 #R 은 평문도 받아 주지만 URL 이 길어져 압축이 유리하다.)
  function deflate(text) {
    if (typeof CompressionStream === 'undefined') return Promise.resolve(null);
    var cs = new CompressionStream('deflate-raw');
    var w = cs.writable.getWriter();
    w.write(new TextEncoder().encode(encodeURIComponent(text)));
    w.close();
    return new Response(cs.readable).arrayBuffer().then(function (ab) {
      var buf = new Uint8Array(ab), bin = '';
      for (var i = 0; i < buf.length; i++) { bin += String.fromCharCode(buf[i]); }
      return btoa(bin);
    });
  }

  document.getElementById('open').addEventListener('click', function () {
    if (!sel.length) return;
    var xml = merge(sel);
    var title = encodeURIComponent('NHN Cloud 아이콘 ' + sel.length + '개');
    deflate(xml).then(function (b64) {
      var frag = b64 ? encodeURIComponent(b64) : encodeURIComponent(xml);
      window.open('https://app.diagrams.net/?title=' + title + '#R' + frag, '_blank', 'noopener');
    });
  });

  document.getElementById('copyAll').addEventListener('click', function () {
    if (!sel.length) return;
    copy(merge(sel), this, '복사됨');
  });

  document.getElementById('lib').addEventListener('click', function () {
    if (!sel.length) return;
    var btn = this;
    if (typeof CompressionStream === 'undefined') {
      document.getElementById('hint').textContent =
        '이 브라우저는 라이브러리 생성을 지원하지 않습니다. 최신 Edge·Chrome 에서 열어 주세요.';
      return;
    }
    Promise.all(sel.map(function (fig) {
      return deflate(fig.dataset.xml).then(function (b64) {
        var e = { xml: b64, w: +fig.dataset.w || 64, h: +fig.dataset.h || 64 };
        if (fig.dataset.aspect) { e.aspect = fig.dataset.aspect; }
        e.title = fig.dataset.title;
        return e;
      });
    })).then(function (entries) {
      var xml = '<mxlibrary title="NHN Cloud 선택">' + JSON.stringify(entries) + '</mxlibrary>';
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([xml], { type: 'application/xml' }));
      a.download = 'nhn-cloud-선택-' + entries.length + '개.xml';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 5000);
      var old = btn.textContent;
      btn.textContent = '내려받음';
      setTimeout(function () { btn.textContent = old; }, 1500);
    });
  });
})();
</script>
</html>
"""

build()
