<#
파이썬판과 PowerShell 판이 같은 결과를 내는지 확인한다.

둘 중 하나를 고쳤으면 이걸 돌린다. 파이썬이 없는 PC 에서는 파이썬 쪽을 건너뛰고
PowerShell 판이 오류 없이 도는지만 본다.

  .\tools\compare_ports.ps1                 # 전부
  .\tools\compare_ports.ps1 -Only edit      # 한 경로만 (gen | list | edit)
  .\tools\compare_ports.ps1 spec.yaml       # 지정한 명세만

검사 경로
  gen   명세 -> .drawio 생성물을 바이트까지 비교
  list  --list 질의 결과를 비교
  edit  add/edge/relabel/remove 를 한 단계씩 적용하고 그때마다 list 출력을 비교

edit 가 파일 바이트가 아니라 list 출력을 보는 이유: 파이썬판은 줄마다 개행을 넣어
저장하고 PowerShell 판은 한 줄로 저장해 서식이 다르다. 서식은 draw.io 가 읽는 데
영향이 없고, 봐야 할 것은 도형의 좌표·부모·연결이다.
#>
param(
    [string[]]$Specs,
    [ValidateSet('all', 'gen', 'list', 'edit')][string]$Only = 'all'
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

if (-not $Specs) {
    $Specs = @(Get-ChildItem -Path (Join-Path $root 'icons\06-architecture\compositions') -Filter *.yaml |
               ForEach-Object { $_.FullName })
    $sample = Join-Path $root 'docs\sample-3tier-spec.yaml'
    if (Test-Path -LiteralPath $sample) { $Specs += $sample }
}

$hasPython = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
if (-not $hasPython) { '알림: 파이썬이 없어 PowerShell 판이 도는지만 확인합니다.'; '' }

$tmp = Join-Path $env:TEMP ('nhn_cmp_' + [Guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory -Path $tmp | Out-Null

$script:ok = 0; $script:fail = 0; $script:skip = 0

function Run-Ps([string]$tool, [string[]]$toolArgs) {
    $text = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot $tool) @toolArgs 2>&1 | Out-String
    return @{ out = $text; rc = $LASTEXITCODE }
}

function Run-Py([string]$tool, [string[]]$toolArgs) {
    $text = & python (Join-Path $PSScriptRoot $tool) @toolArgs 2>&1 | Out-String
    return @{ out = $text; rc = $LASTEXITCODE }
}

function Show-Diff([string]$expected, [string]$actual) {
    # 처음 다른 줄 3개까지만 보여 준다
    $e = $expected -split "`r?`n"
    $a = $actual -split "`r?`n"
    $buf = @(); $shown = 0
    for ($i = 0; $i -lt [Math]::Max($e.Count, $a.Count) -and $shown -lt 3; $i++) {
        $x = $(if ($i -lt $e.Count) { $e[$i] } else { '' })
        $y = $(if ($i -lt $a.Count) { $a[$i] } else { '' })
        if ($x -cne $y) {
            $buf += "        파이썬    : $x"
            $buf += "        PowerShell: $y"
            $shown++
        }
    }
    return ($buf -join [Environment]::NewLine)
}

function Report([string]$label, [bool]$same, [string]$detail) {
    if ($same) { "OK    $label"; $script:ok++ }
    else { "DIFF  $label"; if ($detail) { $detail }; $script:fail++ }
}

function Get-FirstShapeId([string]$file) {
    # list 출력에서 기준으로 쓸 첫 도형 id 를 뽑는다 (제목 칸은 뺀다)
    $r = Run-Ps 'drawio_edit.ps1' @($file, 'list')
    foreach ($line in ($r.out -split "`r?`n")) {
        $t = ($line -replace '\s+', ' ').Trim()
        if (-not $t) { continue }
        $f = $t -split ' '
        if ($f.Count -ge 2 -and $f[1] -eq '도형' -and $f[0] -ne '__title') { return $f[0] }
    }
    return $null
}

# ---------- gen: 명세 -> .drawio ----------

if ($Only -eq 'all' -or $Only -eq 'gen') {
    '[생성] 명세 -> .drawio 를 바이트까지 비교'
    foreach ($spec in $Specs) {
        $name = [IO.Path]::GetFileNameWithoutExtension($spec)
        $psOut = Join-Path $tmp "$name.ps.drawio"
        $pyOut = Join-Path $tmp "$name.py.drawio"

        $r = Run-Ps 'nhn_diagram.ps1' @($spec, $psOut)
        if ($r.rc -ne 0) { "FAIL  $name : PowerShell 판이 실패했습니다"; $r.out; $fail++; continue }
        if (-not $hasPython) { "SKIP  $name"; $skip++; continue }

        $r2 = Run-Py 'nhn_diagram.py' @($spec, $pyOut)
        if ($r2.rc -ne 0) { "FAIL  $name : 파이썬판이 실패했습니다"; $r2.out; $fail++; continue }

        $a = [IO.File]::ReadAllText($pyOut)
        $b = [IO.File]::ReadAllText($psOut)
        Report "$name ($($b.Length) 바이트)" ($a -ceq $b) "        파이썬 $($a.Length)B / PowerShell $($b.Length)B"
    }
    ''
}

# ---------- list: --list 질의 ----------

if ($Only -eq 'all' -or $Only -eq 'list') {
    '[조회] --list 질의 결과를 비교'
    # 전체 / 팔레트 / 영문 부분일치 / 한글(엣지 스타일) / 없는 이름
    foreach ($q in @('', 'groups', 'arrows', 'architecture', 'load', 'storage', '점선', 'zzzz없는이름')) {
        $qa = @('--list')
        if ($q -ne '') { $qa += $q }
        $label = $(if ($q -eq '') { '--list (전체)' } else { "--list $q" })

        $r = Run-Ps 'nhn_diagram.ps1' $qa
        if ($r.rc -ne 0) { "FAIL  $label : PowerShell 판이 실패했습니다"; $r.out; $fail++; continue }
        if (-not $hasPython) { "SKIP  $label"; $skip++; continue }

        $r2 = Run-Py 'nhn_diagram.py' $qa
        $n = @($r.out -split "`r?`n" | Where-Object { $_ -ne '' }).Count
        Report "$label ($n 건)" ($r.out -ceq $r2.out) (Show-Diff $r2.out $r.out)
    }
    ''
}

# ---------- edit: 제자리 수정 ----------

if ($Only -eq 'all' -or $Only -eq 'edit') {
    '[편집] 한 단계씩 적용하고 그때마다 list 를 비교'
    foreach ($spec in $Specs) {
        $name = [IO.Path]::GetFileNameWithoutExtension($spec)
        $psF = Join-Path $tmp "$name.edit.ps.drawio"
        $pyF = Join-Path $tmp "$name.edit.py.drawio"

        $r = Run-Ps 'nhn_diagram.ps1' @($spec, $psF)
        if ($r.rc -ne 0) { "FAIL  $name : 생성이 실패했습니다"; $fail++; continue }

        $anchor = Get-FirstShapeId $psF
        if (-not $anchor) { "SKIP  $name : 기준으로 쓸 도형이 없습니다"; $skip++; continue }

        if ($hasPython) {
            $r2 = Run-Py 'nhn_diagram.py' @($spec, $pyF)
            if ($r2.rc -ne 0) { "FAIL  $name : 파이썬 생성이 실패했습니다"; $fail++; continue }
        }

        # 배치 기준 3종(-Below/-RightOf/최상위)과 나머지 명령을 차례로 건다
        $steps = @(
            @{ label = 'add -Below';   ps = @('add', '-Icon', 'Object Storage', '-Id', 'zz1', '-Below', $anchor)
                                       py = @('add', '--icon', 'Object Storage', '--id', 'zz1', '--below', $anchor) },
            @{ label = 'add -RightOf'; ps = @('add', '-Icon', 'Object Storage', '-Id', 'zz2', '-RightOf', $anchor)
                                       py = @('add', '--icon', 'Object Storage', '--id', 'zz2', '--right-of', $anchor) },
            @{ label = 'add (최상위)'; ps = @('add', '-Icon', 'Object Storage', '-Id', 'zz3')
                                       py = @('add', '--icon', 'Object Storage', '--id', 'zz3') },
            @{ label = 'edge';         ps = @('edge', '-From', $anchor, '-To', 'zz1', '-Style', 'Primary Path · 점선', '-Label', '검증')
                                       py = @('edge', '--from', $anchor, '--to', 'zz1', '--style', 'Primary Path · 점선', '--label', '검증') },
            @{ label = 'relabel';      ps = @('relabel', 'zz1', '바뀐 이름')
                                       py = @('relabel', 'zz1', '바뀐 이름') },
            @{ label = 'remove';       ps = @('remove', 'zz2')
                                       py = @('remove', 'zz2') }
        )

        foreach ($s in $steps) {
            $a = Run-Ps 'drawio_edit.ps1' (@($psF) + $s.ps)
            if ($a.rc -ne 0) { "FAIL  $name / $($s.label) : PowerShell 판이 실패했습니다"; $a.out; $fail++; break }
            if (-not $hasPython) { "SKIP  $name / $($s.label)"; $skip++; continue }

            $b = Run-Py 'drawio_edit.py' (@($pyF) + $s.py)
            if ($b.rc -ne 0) { "FAIL  $name / $($s.label) : 파이썬판이 실패했습니다"; $b.out; $fail++; break }

            $la = (Run-Ps 'drawio_edit.ps1' @($psF, 'list')).out
            $lb = (Run-Py 'drawio_edit.py' @($pyF, 'list')).out
            Report "$name / $($s.label)" ($la -ceq $lb) (Show-Diff $lb $la)
        }
    }
    ''
}

Remove-Item -Recurse -Force $tmp

"같음 $ok 건 / 다름 $fail 건 / 건너뜀 $skip 건"
if ($fail -gt 0) { '다른 결과가 있습니다.'; exit 1 }
'모두 같습니다.'
