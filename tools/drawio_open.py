#!/usr/bin/env python3
"""생성한 .drawio 를 브라우저 draw.io 로 바로 연다.

draw.io 웹 편집기는 URL 조각(`#R<데이터>`)에 담긴 도형을 그대로 읽는다.
조각(#)은 서버로 전송되지 않으므로 사내 프록시를 타지 않는다.
다만 Windows `start` 는 명령줄 길이 제한(8191자)이 있어 URL 을 직접 넘기지 못한다.
그래서 같은 폴더에 한 줄짜리 리다이렉트 HTML 을 만들고 그것을 연다.

사용법
  python drawio_open.py out.drawio              # 편집기로 열기
  python drawio_open.py out.drawio --viewer     # 보기 전용(viewer.diagrams.net)
  python drawio_open.py out.drawio --html-only  # 브라우저를 띄우지 않고 HTML 만 생성

편집 결과 저장
  - draw.io 웹에서 Ctrl+S 는 '다운로드'다. 제자리 저장이 필요하면
    draw.io 에서 '파일 > 열기 > 디바이스' 로 .drawio 를 직접 열어 편집한다.
"""
import argparse, base64, html, os, sys, urllib.parse, webbrowser, zlib

EDITOR = "https://app.diagrams.net/"
VIEWER = "https://viewer.diagrams.net/"


def payload(xml):
    """draw.io 의 Graph.decompress 가 읽는 형식: base64(deflateRaw(urlencode(xml)))."""
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    quoted = urllib.parse.quote(xml).encode("ascii")
    return base64.b64encode(co.compress(quoted) + co.flush()).decode("ascii")


def build_url(xml, title, viewer=False):
    base = VIEWER if viewer else EDITOR
    q = f"?title={urllib.parse.quote(title)}" if title else ""
    return f"{base}{q}#R{urllib.parse.quote(payload(xml))}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--viewer", action="store_true")
    ap.add_argument("--html-only", action="store_true")
    a = ap.parse_args()

    with open(a.file, encoding="utf-8") as f:
        xml = f.read()
    title = os.path.basename(a.file)
    url = build_url(xml, title, a.viewer)

    out = os.path.splitext(a.file)[0] + ".open.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write('<!doctype html><meta charset="utf-8">'
                f'<title>{html.escape(title)} 여는 중</title>'
                f'<p>draw.io 로 이동하는 중입니다. 열리지 않으면 '
                f'<a id="go" href="{html.escape(url, quote=True)}">여기를 누르세요</a>.</p>'
                '<script>location.replace(document.getElementById("go").href)</script>')

    print(f"URL 길이: {len(url):,}자")
    print(f"리다이렉트 파일: {out}")
    if a.html_only:
        return
    webbrowser.open("file:///" + os.path.abspath(out).replace("\\", "/"))
    print("브라우저를 열었습니다.")


if __name__ == "__main__":
    main()
