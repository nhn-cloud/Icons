<#
생성한 .drawio 를 브라우저 draw.io 로 바로 연다 — PowerShell 판. 설치할 것이 없다.

draw.io 웹 편집기는 URL 조각(`#R<데이터>`)에 담긴 도형을 그대로 읽는다.
조각(#)은 서버로 전송되지 않으므로 사내 프록시를 타지 않는다.
다만 명령줄 길이 제한이 있어 URL 을 직접 넘기지 못한다. 그래서 같은 폴더에
한 줄짜리 리다이렉트 HTML 을 만들고 그것을 연다.

사용법
  .\drawio_open.ps1 out.drawio              # 편집기로 열기
  .\drawio_open.ps1 out.drawio -Viewer      # 보기 전용(viewer.diagrams.net)
  .\drawio_open.ps1 out.drawio -HtmlOnly    # 브라우저를 띄우지 않고 HTML 만 생성

편집 결과 저장
  - draw.io 웹에서 Ctrl+S 는 '다운로드'다. 제자리 저장이 필요하면
    draw.io 에서 '파일 > 열기 > 디바이스' 로 .drawio 를 직접 열어 편집한다.
#>
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$File,
    [switch]$Viewer,
    [switch]$HtmlOnly
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$EditorUrl = 'https://app.diagrams.net/'
$ViewerUrl = 'https://viewer.diagrams.net/'

function Quote-Url([string]$s) {
    # 파이썬 urllib.parse.quote 와 같은 규칙 (안 바꾸는 문자: 영숫자 _ . - ~ /)
    $sb = New-Object Text.StringBuilder
    foreach ($b in [Text.Encoding]::UTF8.GetBytes($s)) {
        $c = [char]$b
        if (($c -ge 'A' -and $c -le 'Z') -or ($c -ge 'a' -and $c -le 'z') -or ($c -ge '0' -and $c -le '9') -or
            $c -eq '_' -or $c -eq '.' -or $c -eq '-' -or $c -eq '~' -or $c -eq '/') {
            [void]$sb.Append($c)
        } else {
            [void]$sb.AppendFormat('%{0:X2}', $b)
        }
    }
    return $sb.ToString()
}

function Deflate-Base64([string]$text) {
    # draw.io 의 Graph.decompress 가 읽는 형식: base64(deflateRaw(urlencode(xml)))
    $bytes = [Text.Encoding]::ASCII.GetBytes($text)
    $ms = New-Object IO.MemoryStream
    $ds = New-Object IO.Compression.DeflateStream($ms, [IO.Compression.CompressionMode]::Compress, $true)
    $ds.Write($bytes, 0, $bytes.Length)
    $ds.Dispose()
    $out = [Convert]::ToBase64String($ms.ToArray())
    $ms.Dispose()
    return $out
}

function Html-Escape([string]$s) {
    return $s.Replace('&', '&amp;').Replace('<', '&lt;').Replace('>', '&gt;').Replace('"', '&quot;').Replace("'", '&#x27;')
}

if (-not (Test-Path -LiteralPath $File)) { [Console]::Error.WriteLine("파일이 없습니다: $File"); exit 1 }

$xml = [IO.File]::ReadAllText((Resolve-Path -LiteralPath $File).Path, [Text.Encoding]::UTF8)
$title = Split-Path $File -Leaf
$base = $(if ($Viewer) { $ViewerUrl } else { $EditorUrl })
$url = $base + '?title=' + (Quote-Url $title) + '#R' + (Quote-Url (Deflate-Base64 (Quote-Url $xml)))

$full = (Resolve-Path -LiteralPath $File).Path
$out = Join-Path ([IO.Path]::GetDirectoryName($full)) ([IO.Path]::GetFileNameWithoutExtension($full) + '.open.html')
$html = '<!doctype html><meta charset="utf-8">' +
        '<title>' + (Html-Escape $title) + ' 여는 중</title>' +
        '<p>draw.io 로 이동하는 중입니다. 열리지 않으면 ' +
        '<a id="go" href="' + (Html-Escape $url) + '">여기를 누르세요</a>.</p>' +
        '<script>location.replace(document.getElementById("go").href)</script>'
[IO.File]::WriteAllText($out, $html, (New-Object Text.UTF8Encoding($false)))

Write-Output ('URL 길이: {0:N0}자' -f $url.Length)
Write-Output "리다이렉트 파일: $out"
if ($HtmlOnly) { return }
Start-Process $out
Write-Output '브라우저를 열었습니다.'
