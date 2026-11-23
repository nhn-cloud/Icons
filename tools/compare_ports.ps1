<#
파이썬판과 PowerShell 판이 같은 .drawio 를 내는지 확인한다.

둘 중 하나를 고쳤으면 이걸 돌려 바이트까지 같은지 본다. 파이썬이 없는 PC 에서는
파이썬 쪽을 건너뛰고 PowerShell 판이 오류 없이 도는지만 본다.

  .\tools\compare_ports.ps1              # 저장소의 명세 전부
  .\tools\compare_ports.ps1 spec.yaml    # 지정한 명세만
#>
param([string[]]$Specs)

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
$tmp = Join-Path $env:TEMP ('nhn_cmp_' + [Guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory -Path $tmp | Out-Null

$fail = 0
foreach ($spec in $Specs) {
    $name = [IO.Path]::GetFileNameWithoutExtension($spec)
    $psOut = Join-Path $tmp "$name.ps.drawio"
    $pyOut = Join-Path $tmp "$name.py.drawio"

    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'nhn_diagram.ps1') $spec $psOut | Out-Null
    if ($LASTEXITCODE -ne 0) { "FAIL  $name  : PowerShell 판이 실패했습니다"; $fail++; continue }

    if (-not $hasPython) { "SKIP  $name  : 파이썬이 없어 PowerShell 판만 확인했습니다"; continue }

    & python (Join-Path $PSScriptRoot 'nhn_diagram.py') $spec $pyOut | Out-Null
    if ($LASTEXITCODE -ne 0) { "FAIL  $name  : 파이썬판이 실패했습니다"; $fail++; continue }

    $a = [IO.File]::ReadAllText($pyOut)
    $b = [IO.File]::ReadAllText($psOut)
    if ($a -ceq $b) {
        "OK    $name  ($($b.Length) 바이트)"
    } else {
        "DIFF  $name  : 파이썬 $($a.Length) 바이트 / PowerShell $($b.Length) 바이트"
        $fail++
    }
}

Remove-Item -Recurse -Force $tmp
if ($fail -gt 0) { "`n다른 결과 $fail 건"; exit 1 }
"`n모두 같습니다."
