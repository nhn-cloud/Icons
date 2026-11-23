<#
이미 있는 .drawio 를 제자리에서 고친다 — PowerShell 판. 설치할 것이 없다.

구성도를 처음 그릴 때는 `nhn_diagram.ps1` 로 명세에서 만든다.
한 번이라도 draw.io 에서 손을 댔다면 **그 파일이 원본**이다. 명세에서 다시 그리지 말고
이 도구로 바뀐 부분만 더하거나 뺀다.

사용법
  .\drawio_edit.ps1 FILE list                      # 현재 도형·연결 목록 (id 포함)
  .\drawio_edit.ps1 FILE add -Icon "RDS Instance" -Label Replica2 -Below db2
  .\drawio_edit.ps1 FILE add -Group Subnet -Label "Private Subnet (Cache)" -Into vpc
  .\drawio_edit.ps1 FILE edge -From web1 -To db3 -Style "Primary Path · 점선" -Label 3306
  .\drawio_edit.ps1 FILE relabel db2 "Replica (읽기 전용)"
  .\drawio_edit.ps1 FILE remove db3                # 딸린 연결선도 함께 지움

배치 기준 (-Below / -RightOf / -Into 가운데 하나)
  -Below ID      그 도형 아래. 부모·가로 위치를 그대로 물려받는다
  -RightOf ID    그 도형 오른쪽
  -Into ID       그 그룹 안. 마지막 자식 아래에 놓는다 (기본값: 캔버스 최상위)
  넣은 뒤 부모 그룹이 좁으면 자동으로 넓힌다. 옆 그룹과 겹치면 draw.io 에서 밀어 준다.

이 도구는 다른 도형의 좌표를 건드리지 않는다. 사용자가 draw.io 에서 옮긴 자리는 그대로 남는다.
#>
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$File,
    [Parameter(Mandatory = $true, Position = 1)][ValidateSet('list', 'add', 'edge', 'relabel', 'remove')][string]$Command,
    [Parameter(Position = 2, ValueFromRemainingArguments = $true)][string[]]$Rest,
    [string]$Lib,
    [string]$Icon,
    [string]$Group,
    [string]$Id,
    [string]$Label,
    [string]$Into,
    [string]$Below,
    [string]$RightOf,
    [double]$W,
    [double]$H,
    [string]$From,
    [string]$To,
    [string]$Style,
    [ValidateSet('left', 'right', 'top', 'bottom')][string]$Exit,
    [ValidateSet('left', 'right', 'top', 'bottom')][string]$Entry
)

. (Join-Path $PSScriptRoot 'nhn_lib.ps1')

$GAP_Y = 60
$GAP_X = 36
$PAD   = 24

# ---------- 파일 입출력 ----------

function Ed-Load([string]$path) {
    $text = [IO.File]::ReadAllText($path, [Text.Encoding]::UTF8)
    $doc = New-Object Xml.XmlDocument
    $doc.PreserveWhitespace = $false
    $doc.LoadXml($text)
    $diagram = $doc.SelectSingleNode('/mxfile/diagram')
    if ($null -eq $diagram) { Nd-Die 'diagram 요소가 없습니다. .drawio 파일이 맞습니까?' }
    $model = $diagram.SelectSingleNode('mxGraphModel')
    if ($null -eq $model) {
        # draw.io 가 압축해 저장한 경우
        $inner = New-Object Xml.XmlDocument
        $inner.LoadXml((Nd-DecodeEntry $diagram.InnerText.Trim()))
        $diagram.RemoveAll()
        $model = $doc.ImportNode($inner.DocumentElement, $true)
        [void]$diagram.AppendChild($model)
    }
    return @{ doc = $doc; diagram = $diagram; model = $model }
}

function Ed-Save([string]$path, $doc) {
    [IO.File]::WriteAllText($path, $doc.OuterXml, (New-Object Text.UTF8Encoding($false)))
}

function Ed-Root($model) { return $model.SelectSingleNode('root') }

function Ed-Cells($model) { return @((Ed-Root $model).SelectNodes('mxCell')) }

function Ed-FindCell($model, [string]$cid) {
    foreach ($c in Ed-Cells $model) {
        if ($c.GetAttribute('id') -eq $cid) { return $c }
    }
    Nd-Die "id '$cid' 인 도형이 없습니다. ``list`` 로 id 를 확인하세요."
}

function Ed-Geom($cell) {
    $g = $cell.SelectSingleNode('mxGeometry')
    if ($null -eq $g) { return $null }
    $h = @{}
    foreach ($k in @('x', 'y', 'width', 'height')) {
        $v = $g.GetAttribute($k)
        $h[$k] = $(if ([string]::IsNullOrEmpty($v)) { 0.0 } else { [double]$v })
    }
    return $h
}

function Ed-NewId($model, [string]$base) {
    $used = @{}
    foreach ($c in Ed-Cells $model) { $used[$c.GetAttribute('id')] = $true }
    if (-not $used.ContainsKey($base)) { return $base }
    $i = 2
    while ($used.ContainsKey("$base$i")) { $i++ }
    return "$base$i"
}

function Ed-Kind($cell) {
    if ($cell.GetAttribute('edge') -eq '1') { return '연결선' }
    $style = $cell.GetAttribute('style')
    if ($style -and ($style.Contains('container=1') -or $style.Contains('swimlane'))) { return '그룹' }
    return '도형'
}

function Ed-Append($model, [string]$cellXml) {
    $root = Ed-Root $model
    $frag = $root.OwnerDocument.CreateDocumentFragment()
    $frag.InnerXml = $cellXml
    [void]$root.AppendChild($frag)
}

# ---------- 조회 ----------

function Ed-CmdList($model) {
    $rows = @()
    foreach ($c in Ed-Cells $model) {
        $cid = $c.GetAttribute('id')
        if ($cid -eq '0' -or $cid -eq '1' -or $cid.Contains('__corner')) { continue }
        if ($c.GetAttribute('edge') -eq '1') {
            $src = $c.GetAttribute('source'); if (-not $src) { $src = '?' }
            $dst = $c.GetAttribute('target'); if (-not $dst) { $dst = '?' }
            $pos = "$src → $dst"
        } else {
            $g = Ed-Geom $c
            if ($null -eq $g) { $g = @{ x = 0.0; y = 0.0; width = 0.0; height = 0.0 } }
            $pos = (Nd-Fmt0 $g['x']) + ',' + (Nd-Fmt0 $g['y']) + ' ' + (Nd-Fmt0 $g['width']) + 'x' + (Nd-Fmt0 $g['height'])
        }
        $val = $c.GetAttribute('value')
        if ($null -eq $val) { $val = '' }
        $val = $val.Replace("`n", ' ')
        if ($val.Length -gt 28) { $val = $val.Substring(0, 28) }
        $rows += ,[pscustomobject]@{ id = $cid; kind = (Ed-Kind $c); label = $val; parent = $c.GetAttribute('parent'); pos = $pos }
    }
    $w = 2
    foreach ($r in $rows) { if ($r.id.Length -gt $w) { $w = $r.id.Length } }
    Write-Output (("{0,-$w}  {1,-6} {2,-30} {3,-10} {4}") -f 'id', '종류', '레이블', '부모', '위치')
    foreach ($r in $rows) {
        Write-Output (("{0,-$w}  {1,-6} {2,-30} {3,-10} {4}") -f $r.id, $r.kind, $r.label, $r.parent, $r.pos)
    }
}

# ---------- 추가 ----------

function Ed-Place($model, $w, $h) {
    if ($Below -or $RightOf) {
        $anchorId = $(if ($Below) { $Below } else { $RightOf })
        $anchor = Ed-FindCell $model $anchorId
        $g = Ed-Geom $anchor
        if ($null -eq $g) { Nd-Die '기준 도형에 좌표가 없습니다(연결선은 기준으로 쓸 수 없습니다).' }
        if ($Below) { return @($anchor.GetAttribute('parent'), $g['x'], $g['y'] + $g['height'] + $GAP_Y) }
        return @($anchor.GetAttribute('parent'), $g['x'] + $g['width'] + $GAP_X, $g['y'])
    }
    $parent = $(if ($Into) { $Into } else { '1' })
    if ($parent -ne '1') { [void](Ed-FindCell $model $parent) }
    $kids = @()
    foreach ($c in Ed-Cells $model) {
        if ($c.GetAttribute('parent') -eq $parent -and -not $c.GetAttribute('id').Contains('__corner') -and $null -ne (Ed-Geom $c)) {
            $kids += ,$c
        }
    }
    if ($kids.Count -eq 0) {
        $head = $(if ($parent -ne '1') { 44 } else { 20 })
        return @($parent, [double]$PAD, [double]($head + 10))
    }
    $low = $null; $lowBottom = [double]::NegativeInfinity
    foreach ($c in $kids) {
        $g = Ed-Geom $c
        $b = $g['y'] + $g['height']
        if ($b -gt $lowBottom) { $lowBottom = $b; $low = $c }
    }
    $g = Ed-Geom $low
    return @($parent, $g['x'], $g['y'] + $g['height'] + $GAP_Y)
}

function Ed-GrowParent($model, [string]$parentId, $x, $y, $w, $h) {
    while ($parentId -and $parentId -ne '1') {
        $p = Ed-FindCell $model $parentId
        $g = Ed-Geom $p
        if ($null -eq $g) { return }
        $needW = $x + $w + $PAD
        $needH = $y + $h + $PAD
        $gw = [Math]::Max($g['width'], $needW)
        $gh = [Math]::Max($g['height'], $needH)
        if ($gw -ne $g['width'] -or $gh -ne $g['height']) {
            $pg = $p.SelectSingleNode('mxGeometry')
            $pg.SetAttribute('width', (Nd-Fmt0 $gw))
            $pg.SetAttribute('height', (Nd-Fmt0 $gh))
            Write-Output ("[알림] 그룹 '$parentId' 를 " + (Nd-Fmt0 $gw) + 'x' + (Nd-Fmt0 $gh) +
                          ' 로 넓혔습니다. 옆 그룹과 겹치면 draw.io 에서 밀어 주세요.')
        }
        $x = $g['x']; $y = $g['y']; $w = $gw; $h = $gh
        $parentId = $p.GetAttribute('parent')
    }
}

function Ed-CmdAdd($model, $library) {
    $name = $(if ($Icon) { $Icon } else { $Group })
    $shape = Nd-Find $library $name $(if ($Group) { 'group' } else { 'icon' })
    $src = @(Nd-Cells $shape.xml)
    if ($Icon) { $main = $src[0] } else { $main = @($src | Where-Object { (Nd-Attr $_ 'parent') -eq '1' })[0] }

    if ($PSBoundParameters.ContainsKey('W')) { $w = $W }
    elseif ($Icon) { $w = $(if ($null -eq $shape.w) { 64 } else { [double]$shape.w }) }
    else { $w = 320.0 }
    if ($PSBoundParameters.ContainsKey('H')) { $h = $H }
    elseif ($Icon) { $h = $(if ($null -eq $shape.h) { 64 } else { [double]$shape.h }) }
    else { $h = 200.0 }

    $placed = Ed-Place $model $w $h
    $parent = [string]$placed[0]; $x = [double]$placed[1]; $y = [double]$placed[2]

    if ($Id) {
        foreach ($c in Ed-Cells $model) {
            if ($c.GetAttribute('id') -eq $Id) { Nd-Die "id '$Id' 가 이미 있습니다." }
        }
        $cid = $Id
    } else {
        $cid = Ed-NewId $model ([regex]::Replace($name.ToLower(), '[^a-z0-9]+', '-').Trim('-'))
    }

    $c = Nd-SetAttr $main 'id' $cid
    $c = Nd-SetAttr $c 'parent' $parent
    $c = Nd-SetAttr $c 'value' $(if ($Label) { $Label } else { $shape.title })
    if ($Icon) {
        $style = Nd-Attr $c 'style'
        $style = [regex]::Replace($style, 'fontSize=\d+', 'fontSize=12')
        if (-not $style.EndsWith(';')) { $style += ';' }
        $lw = [int][Math]::Max($w + 46, $w)
        $c = Nd-SetAttr $c 'style' ($style + "whiteSpace=wrap;labelWidth=$lw;")
    }
    Ed-Append $model (Nd-SetGeom $c $x $y $w $h)

    if ($Group) {   # 그룹 머리의 모서리 아이콘까지 복사
        $old = Nd-Attr $main 'id'
        $k = 0
        foreach ($sub in @($src | Where-Object { (Nd-Attr $_ 'parent') -eq $old })) {
            $s = Nd-SetAttr $sub 'id' "${cid}__corner$k"
            $s = Nd-SetAttr $s 'parent' $cid
            $m = [regex]::Match($s, 'width="(\d+)" height="(\d+)"')
            if ($m.Success) { $sw = [int]$m.Groups[1].Value; $sh = [int]$m.Groups[2].Value } else { $sw = 32; $sh = 32 }
            Ed-Append $model (Nd-SetGeom $s 0 0 $sw $sh)
            $k++
        }
    }

    Ed-GrowParent $model $parent $x $y $w $h
    Write-Output ("추가: $cid ($($shape.palette)/$($shape.title)) → 부모 $parent, " + (Nd-Fmt0 $x) + ',' + (Nd-Fmt0 $y))
}

function Ed-CmdEdge($model, $library) {
    foreach ($cid in @($From, $To)) { [void](Ed-FindCell $model $cid) }
    $shape = Nd-Find $library $(if ($Style) { $Style } else { 'Primary Path' }) 'arrow'
    $style = Nd-Attr @(Nd-Cells $shape.xml)[0] 'style'
    $side = @{ left = @(0, 0.5); right = @(1, 0.5); top = @(0.5, 0); bottom = @(0.5, 1) }
    foreach ($pair in @(@('exit', $Exit), @('entry', $Entry))) {
        if ($pair[1]) {
            $xy = $side[[string]$pair[1]]
            $style += "$($pair[0])X=$($xy[0]);$($pair[0])Y=$($xy[1]);$($pair[0])Dx=0;$($pair[0])Dy=0;"
        }
    }
    $used = @{}
    foreach ($c in Ed-Cells $model) { $used[$c.GetAttribute('id')] = $true }
    $i = 1
    while ($used.ContainsKey("e$i")) { $i++ }
    $eid = "e$i"
    $cell = '<mxCell id="' + $eid + '" value=' + (Nd-QuoteAttr $Label) + ' style=' + (Nd-QuoteAttr $style) +
            ' edge="1" parent="1" source=' + (Nd-QuoteAttr $From) + ' target=' + (Nd-QuoteAttr $To) + '>' +
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
    Ed-Append $model $cell
    Write-Output "연결: $eid  $From → $To ($($shape.title))"
}

# ---------- 수정·삭제 ----------

function Ed-CmdRelabel($model) {
    if (-not $Rest -or $Rest.Count -lt 2) { Nd-Die '사용법: drawio_edit.ps1 FILE relabel ID "새 레이블"' }
    $cid = $Rest[0]
    $text = $Rest[1]
    $c = Ed-FindCell $model $cid
    $c.SetAttribute('value', $text)
    Write-Output "레이블: $cid → $text"
}

function Ed-CmdRemove($model) {
    if (-not $Rest -or $Rest.Count -lt 1) { Nd-Die '사용법: drawio_edit.ps1 FILE remove ID [ID ...]' }
    $doomed = @{}
    foreach ($r in $Rest) { $doomed[$r] = $true }
    for ($round = 0; $round -lt 10; $round++) {
        $added = $false
        foreach ($c in Ed-Cells $model) {
            $p = $c.GetAttribute('parent')
            if ($p -and $doomed.ContainsKey($p)) {
                $cid = $c.GetAttribute('id')
                if (-not $doomed.ContainsKey($cid)) { $doomed[$cid] = $true; $added = $true }
            }
        }
        if (-not $added) { break }
    }
    $root = Ed-Root $model
    $gone = 0
    foreach ($c in Ed-Cells $model) {
        $cid = $c.GetAttribute('id')
        $src = $c.GetAttribute('source')
        $dst = $c.GetAttribute('target')
        if ($doomed.ContainsKey($cid) -or ($src -and $doomed.ContainsKey($src)) -or ($dst -and $doomed.ContainsKey($dst))) {
            [void]$root.RemoveChild($c)
            $gone++
        }
    }
    Write-Output "삭제: $($Rest -join ', ') (셀 $gone 개, 딸린 연결선 포함)"
}

# ---------- 실행 ----------

if (-not (Test-Path -LiteralPath $File)) { Nd-Die "파일이 없습니다: $File" }
$full = (Resolve-Path -LiteralPath $File).Path
$loaded = Ed-Load $full
$model = $loaded.model

if ($Command -eq 'list') {
    Ed-CmdList $model
    return
}

if ($Command -eq 'add' -or $Command -eq 'edge') {
    if ($Command -eq 'add') {
        if ($Icon -and $Group) { Nd-Die '-Icon 과 -Group 은 함께 쓸 수 없습니다.' }
        if (-not $Icon -and -not $Group) { Nd-Die '-Icon 또는 -Group 가운데 하나가 필요합니다.' }
    } else {
        if (-not $From -or -not $To) { Nd-Die '-From 과 -To 가 필요합니다.' }
    }
    $library = Nd-NewLibrary (Nd-LoadLibrary (Nd-LibSource $Lib))
    if ($Command -eq 'add') { Ed-CmdAdd $model $library } else { Ed-CmdEdge $model $library }
} elseif ($Command -eq 'relabel') {
    Ed-CmdRelabel $model
} elseif ($Command -eq 'remove') {
    Ed-CmdRemove $model
}

Ed-Save $full $loaded.doc
Write-Output "저장: $File"
