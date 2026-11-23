<#
NHN Cloud 아키텍처 구성도(.drawio) 생성기 — PowerShell 판. 설치할 것이 없다.

NHN Cloud draw.io 아이콘 라이브러리(dist/01.xml ~ 29.xml)의 도형을 그대로 꺼내
YAML/JSON 명세로 구성도를 만든다. 파이썬판 tools/nhn_diagram.py 와 같은 결과를 낸다.

사용법
  .\nhn_diagram.ps1 -List              # 도형 이름 전체
  .\nhn_diagram.ps1 -List 로드밸런      # 이름 찾기 (한글/영문 부분 일치)
  .\nhn_diagram.ps1 spec.yaml out.drawio
  .\nhn_diagram.ps1 spec.yaml out.drawio -Lib dist

-Lib 기본값: ./dist → 환경변수 NHN_ICONS_DIST →
  https://raw.githubusercontent.com/nhn-cloud/Icons/draft/dist

명세 형식은 SKILL.md 와 파이썬판 머리말을 보라. 둘은 같은 형식을 읽는다.
#>
param(
    [Parameter(Position = 0)][string]$Spec,
    [Parameter(Position = 1)][string]$Out,
    [string]$Lib,
    [switch]$List
)

. (Join-Path $PSScriptRoot 'nhn_lib.ps1')

$src = Nd-LibSource $Lib
$library = Nd-NewLibrary (Nd-LoadLibrary $src)

if ($List) {
    $q = Nd-Norm $Spec
    foreach ($s in $library.shapes) {
        if ((Nd-Norm ($s.palette + $s.title)).Contains($q)) {
            $w = $(if ($null -eq $s.w) { 'None' } else { $s.w })
            $h = $(if ($null -eq $s.h) { 'None' } else { $s.h })
            Write-Output ('{0:00} {1,-22} {2}  ({3}x{4})' -f $s.no, $s.palette, $s.title, $w, $h)
        }
    }
    return
}

if (-not $Spec -or -not $Out) {
    Nd-Die '사용법: .\nhn_diagram.ps1 spec.yaml out.drawio   (이름 찾기는 -List)'
}
if (-not (Test-Path -LiteralPath $Spec)) { Nd-Die "명세 파일이 없습니다: $Spec" }

$specData = Nd-LoadSpec (Resolve-Path -LiteralPath $Spec).Path
$xml = Nd-Build $specData $library
[IO.File]::WriteAllText($Out, $xml, (New-Object Text.UTF8Encoding($false)))
Write-Output "저장: $Out"
