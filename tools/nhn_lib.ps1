# NHN Cloud 구성도 도구 공용 코어 (PowerShell 5.1 이상, 외부 모듈 없음).
#
# nhn_diagram.ps1 · drawio_edit.ps1 · drawio_open.ps1 이 점(.) 으로 불러 쓴다.
# 파이썬판 tools/nhn_diagram.py 와 같은 결과를 내도록 이식했다. 둘 중 하나를 고치면
# 다른 쪽도 맞춰야 한다. 일치 여부는 tools/compare_ports.ps1 로 확인한다.

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch {}
Add-Type -AssemblyName System.IO.Compression -ErrorAction SilentlyContinue

$script:DEFAULT_URL = 'https://raw.githubusercontent.com/nhn-cloud/Icons/draft/dist'

# 레이아웃 상수 — 파이썬판과 같은 값
$script:ICON_SLOT_W = 110   # 아이콘 1칸 너비 (레이블 공간 포함)
$script:LABEL_H     = 34    # 아이콘 아래 레이블 높이
$script:GROUP_HEAD  = 44    # 그룹 머리 (모서리 아이콘 32 + 여백)
$script:ASG_HEAD    = 64    # Auto Scaling Group: 아이콘+레이블이 위 가운데
$script:GROUP_PAD   = 24
$script:GAP         = 36
$script:OVER_INSET  = @(44, 24, 24, 24)   # over 겹침 깊이 (위, 오른쪽, 아래, 왼쪽)
$script:MARGIN      = 20
$script:TITLE_H     = 70

function Nd-Die([string]$msg) { [Console]::Error.WriteLine($msg); exit 1 }

function Nd-Norm([string]$s) {
    if ($null -eq $s) { return '' }
    return [regex]::Replace($s.ToLower(), '[\s_\-·,()&]+', '')
}

function Nd-Fmt0($v) {
    # 파이썬 f"{x:.0f}" 와 같은 반올림(짝수로)
    return [Math]::Round([double]$v, 0, [MidpointRounding]::ToEven).ToString('0', [Globalization.CultureInfo]::InvariantCulture)
}

function Nd-QuoteAttr([string]$v) {
    # xml.sax.saxutils.quoteattr 이식
    if ($null -eq $v) { $v = '' }
    $d = $v.Replace('&', '&amp;').Replace('<', '&lt;').Replace('>', '&gt;')
    $d = $d.Replace("`n", '&#10;').Replace("`r", '&#13;').Replace("`t", '&#9;')
    if ($d.Contains('"')) {
        if ($d.Contains("'")) { return '"' + $d.Replace('"', '&quot;') + '"' }
        return "'" + $d + "'"
    }
    return '"' + $d + '"'
}

function Nd-Escape([string]$v) {
    if ($null -eq $v) { $v = '' }
    return $v.Replace('&', '&amp;').Replace('<', '&lt;').Replace('>', '&gt;')
}

# ---------- 라이브러리 로드 ----------

function Nd-DecodeEntry([string]$s) {
    $raw = [Convert]::FromBase64String($s)
    $ms = New-Object IO.MemoryStream(,$raw)
    $ds = New-Object IO.Compression.DeflateStream($ms, [IO.Compression.CompressionMode]::Decompress)
    $out = New-Object IO.MemoryStream
    $ds.CopyTo($out)
    $ds.Dispose(); $ms.Dispose()
    $text = [Text.Encoding]::UTF8.GetString($out.ToArray())
    $out.Dispose()
    return [Uri]::UnescapeDataString($text)
}

function Nd-FullPath([string]$path) {
    # PowerShell 의 현재 위치는 프로세스 CWD 와 따로 논다. Set-Location 으로 폴더를 옮겨도
    # [IO.File] 은 옛 폴더를 본다. 상대경로를 넘기기 전에 항상 절대경로로 바꾼다.
    return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($path)
}

function Nd-ReadSource([string]$src, [string]$name) {
    if ($src -match '^https?://') {
        $url = $src.TrimEnd('/') + '/' + $name
        try {
            $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
        } catch { return $null }
        if ($r.RawContentLength -eq 0 -and -not $r.Content) { return $null }
        if ($r.Content -is [byte[]]) { return [Text.Encoding]::UTF8.GetString($r.Content) }
        return [string]$r.Content
    }
    $p = Nd-FullPath (Join-Path $src $name)
    if (-not (Test-Path -LiteralPath $p)) { return $null }
    return [IO.File]::ReadAllText($p, [Text.Encoding]::UTF8)
}

function Nd-LoadLibrary([string]$src) {
    $shapes = New-Object Collections.ArrayList
    for ($i = 1; $i -lt 100; $i++) {
        $name = '{0:00}.xml' -f $i
        $text = $null
        try { $text = Nd-ReadSource $src $name } catch { $text = $null }
        if ($null -eq $text) {
            if ($i -gt 30) { break }
            continue
        }
        $m = [regex]::Match($text, '<mxlibrary[^>]*title="([^"]*)"[^>]*>(.*)</mxlibrary>', 'Singleline')
        if (-not $m.Success) { continue }
        $palette = $m.Groups[1].Value.Replace('&amp;', '&').Replace('NHN Cloud / ', '')
        $entries = $m.Groups[2].Value | ConvertFrom-Json
        foreach ($e in $entries) {
            $w = $null; $h = $null; $k = $null
            if ($e.PSObject.Properties.Match('w').Count -gt 0) { $w = $e.w }
            if ($e.PSObject.Properties.Match('h').Count -gt 0) { $h = $e.h }
            if ($e.PSObject.Properties.Match('k').Count -gt 0) { $k = $e.k }
            [void]$shapes.Add([pscustomobject]@{
                palette = $palette; no = $i; title = $e.title
                w = $w; h = $h; k = $k; xml = (Nd-DecodeEntry $e.xml)
            })
        }
    }
    if ($shapes.Count -eq 0) { Nd-Die "라이브러리를 찾지 못했습니다: $src" }
    return $shapes
}

function Nd-NewLibrary($shapes) {
    $by = @{}
    foreach ($s in $shapes) {
        foreach ($k in @((Nd-Norm $s.title), (Nd-Norm ($s.palette + '/' + $s.title)))) {
            if (-not $by.ContainsKey($k)) { $by[$k] = New-Object Collections.ArrayList }
            [void]$by[$k].Add($s)
        }
    }
    return [pscustomobject]@{ shapes = $shapes; by = $by }
}

function Nd-Find($lib, [string]$name, [string]$kind) {
    $key = Nd-Norm $name
    $cands = @()
    if ($lib.by.ContainsKey($key)) { $cands = @($lib.by[$key]) }
    if ($kind -eq 'group') {
        $cands = @($cands | Where-Object { $_.palette -eq 'Box Type' -or $_.palette -eq 'Groups' })
        $grp = @($cands | Where-Object { $_.k -eq 'g' })
        if ($grp.Count -gt 0) { $cands = $grp }
    } elseif ($kind -eq 'arrow') {
        $cands = @($cands | Where-Object { $_.palette -eq 'Arrows' })
    } elseif ($kind -eq 'icon') {
        $cands = @($cands | Where-Object { $_.palette -ne 'Box Type' -and $_.palette -ne 'Groups' -and $_.palette -ne 'Arrows' })
        $live = @($cands | Where-Object { $_.palette -ne 'Retired' })
        if ($live.Count -gt 0) { $cands = $live }
    }
    if ($cands.Count -eq 0) {
        $head = $key
        if ($head.Length -gt 4) { $head = $head.Substring(0, 4) }
        $near = @($lib.shapes | Where-Object { (Nd-Norm $_.title).Contains($head) } |
                  Select-Object -First 8 | ForEach-Object { $_.palette + '/' + $_.title })
        Nd-Die "'$name' ($kind) 를 라이브러리에서 찾지 못했습니다. 비슷한 이름: [$($near -join ', ')]"
    }
    if ($cands.Count -gt 1) {
        # 서비스(64) 우선 — 파이썬 sort 처럼 같은 값이면 원래 순서를 지킨다
        $idx = 0
        $cands = @($cands | ForEach-Object {
            [pscustomobject]@{ i = $idx++; s = $_; w = $(if ($null -eq $_.w) { 0 } else { [int]$_.w }) }
        } | Sort-Object @{Expression = { -$_.w }}, @{Expression = { $_.i }} | ForEach-Object { $_.s })
        $others = @($cands | Select-Object -Skip 1 | ForEach-Object { "'" + $_.palette + '/' + $_.title + "'" })
        [Console]::Error.WriteLine("[알림] '$name' 후보 $($cands.Count)개 → $($cands[0].palette)/$($cands[0].title) 사용. 다른 것: [$($others -join ', ')]")
    }
    return $cands[0]
}

# ---------- 레이아웃 ----------

function Nd-Get($spec, [string]$key, $default) {
    if ($spec.ContainsKey($key) -and $null -ne $spec[$key]) { return $spec[$key] }
    return $default
}

function Nd-Packed($node)   { return @($node.children | Where-Object { -not $_.ContainsKey('over') -or $null -eq $_.over }) }
function Nd-Floating($node) { return @($node.children | Where-Object { $_.ContainsKey('over') -and $null -ne $_.over }) }

function Nd-Head($node) {
    if ($node.kind -eq 'stack') { return 0 }
    if ((Nd-Norm $node.shape.title) -eq 'autoscalinggroup') { return $script:ASG_HEAD }
    return $script:GROUP_HEAD
}

function Nd-NewNode($spec, $lib, $ids) {
    $n = @{ spec = $spec; children = @(); x = 0; y = 0 }
    if ($spec.ContainsKey('spacer')) {
        $n.kind = 'spacer'
        $v = $spec['spacer']
        if ($v) { $n.w = [int]$v } else { $n.w = 40 }
        $n.h = $n.w
        return $n
    }
    if ($spec.ContainsKey('stack')) {
        $n.kind  = 'stack'
        $n.dir   = Nd-Get $spec 'stack' 'row'
        $n.gap   = Nd-Get $spec 'gap' $script:GAP
        $n.pad   = Nd-Get $spec 'pad' 0
        $n.align = Nd-Get $spec 'align' 'center'
        foreach ($c in @(Nd-Get $spec 'items' @())) { $n.children += ,(Nd-NewNode $c $lib $ids) }
    } elseif ($spec.ContainsKey('group')) {
        $n.kind  = 'group'
        $n.shape = Nd-Find $lib $spec['group'] 'group'
        $n.dir   = Nd-Get $spec 'dir' 'row'
        $n.gap   = Nd-Get $spec 'gap' $script:GAP
        $n.pad   = Nd-Get $spec 'pad' $script:GROUP_PAD
        $n.align = Nd-Get $spec 'align' 'center'
        $n.over  = Nd-Get $spec 'over' $null
        $n.inset = @(Nd-Get $spec 'inset' $script:OVER_INSET)
        foreach ($c in @(Nd-Get $spec 'items' @())) { $n.children += ,(Nd-NewNode $c $lib $ids) }
    } else {
        $n.kind = 'icon'
        if (-not $spec.ContainsKey('icon')) { Nd-Die "항목에 icon/group/spacer 가 없습니다: $($spec.Keys -join ',')" }
        $n.shape = Nd-Find $lib $spec['icon'] 'icon'
        $sw = $(if ($null -eq $n.shape.w) { 64 } else { [int]$n.shape.w })
        $sh = $(if ($null -eq $n.shape.h) { 64 } else { [int]$n.shape.h })
        $n.iw = Nd-Get $spec 'w' $sw
        $n.ih = Nd-Get $spec 'h' $sh
    }
    $id = Nd-Get $spec 'id' $null
    if ($null -eq $id -or "$id" -eq '') { $id = 'n' + ($ids.Count + 1) }
    $n.id = [string]$id
    if ($ids.ContainsKey($n.id)) { Nd-Die "id 중복: $($n.id)" }
    $ids[$n.id] = $n
    return $n
}

function Nd-Measure($node) {
    if ($node.kind -eq 'spacer') { return }
    if ($node.kind -eq 'icon') {
        $node.w = [Math]::Max([double]$node.iw, [double]$script:ICON_SLOT_W)
        $node.h = [double]$node.ih + $script:LABEL_H
        return
    }
    foreach ($c in $node.children) { Nd-Measure $c }
    $kids = @(Nd-Packed $node)
    $row = $node.dir -eq 'row'
    $main = 0.0; $cross = 0.0
    foreach ($c in $kids) {
        $main += $(if ($row) { [double]$c.w } else { [double]$c.h })
        $cv = $(if ($row) { [double]$c.h } else { [double]$c.w })
        if ($cv -gt $cross) { $cross = $cv }
    }
    if ($kids.Count -gt 1) { $main += [double]$node.gap * ($kids.Count - 1) }
    if ($row) { $cw = $main; $ch = $cross } else { $cw = $cross; $ch = $main }
    $minW = 220.0; $minH = 140.0
    if ($node.kind -eq 'stack') { $minW = 0.0; $minH = 0.0 }
    $node.w = [Math]::Max($cw + 2 * [double]$node.pad, [double](Nd-Get $node.spec 'min_w' $minW))
    $node.h = [Math]::Max($ch + (Nd-Head $node) + [double]$node.pad, [double](Nd-Get $node.spec 'min_h' $minH))
}

function Nd-Place($node) {
    if ($node.kind -ne 'group' -and $node.kind -ne 'stack') { return }
    $row = $node.dir -eq 'row'
    $innerW = [double]$node.w - 2 * [double]$node.pad
    $innerH = [double]$node.h - (Nd-Head $node) - [double]$node.pad
    $kids = @(Nd-Packed $node)
    $mainTotal = 0.0
    foreach ($c in $kids) { $mainTotal += $(if ($row) { [double]$c.w } else { [double]$c.h }) }
    if ($kids.Count -gt 1) { $mainTotal += [double]$node.gap * ($kids.Count - 1) }
    $off = (($(if ($row) { $innerW } else { $innerH })) - $mainTotal) / 2
    foreach ($c in $kids) {
        if ($row) {
            $c.x = [double]$node.pad + $off
            $c.y = (Nd-Head $node) + $(if ($node.align -eq 'center') { ($innerH - [double]$c.h) / 2 } else { 0 })
            $off += [double]$c.w + [double]$node.gap
        } else {
            $c.y = (Nd-Head $node) + $off
            $c.x = [double]$node.pad + $(if ($node.align -eq 'center') { ($innerW - [double]$c.w) / 2 } else { 0 })
            $off += [double]$c.h + [double]$node.gap
        }
        Nd-Place $c
    }
    foreach ($c in @(Nd-Floating $node)) {
        Nd-Cover $c $node
        Nd-Place $c
    }
}

function Nd-Cover($node, $parent) {
    $byId = @{}
    foreach ($c in $parent.children) {
        $cid = Nd-Get $c.spec 'id' $null
        if ($null -ne $cid -and "$cid" -ne '') { $byId["$cid"] = $c }
    }
    $targets = @()
    foreach ($name in @($node.over)) {
        if (-not $byId.ContainsKey("$name")) {
            $sib = @($byId.Keys | Sort-Object) -join ', '
            Nd-Die "over 의 '$name' 는 '$(Nd-Get $node.spec 'group' '')' 와 같은 그룹 안의 형제여야 합니다. 형제 id: [$sib]"
        }
        $targets += ,$byId["$name"]
    }
    $top = [double]$node.inset[0]; $right = [double]$node.inset[1]
    $bottom = [double]$node.inset[2]; $left = [double]$node.inset[3]
    $x0 = ($targets | ForEach-Object { [double]$_.x } | Measure-Object -Minimum).Minimum
    $y0 = ($targets | ForEach-Object { [double]$_.y } | Measure-Object -Minimum).Minimum
    $x1 = ($targets | ForEach-Object { [double]$_.x + [double]$_.w } | Measure-Object -Maximum).Maximum
    $y1 = ($targets | ForEach-Object { [double]$_.y + [double]$_.h } | Measure-Object -Maximum).Maximum
    $node.x = $x0 + $left
    $node.y = $y0 + $top
    $node.w = [Math]::Max($x1 - $x0 - $left - $right, 40)
    $node.h = [Math]::Max($y1 - $y0 - $top - $bottom, 40)
}

# ---------- XML 출력 ----------

function Nd-Cells([string]$xml) {
    $out = @()
    foreach ($m in [regex]::Matches($xml, '<mxCell\b(?:[^>]*/>|.*?</mxCell>)', 'Singleline')) {
        if ($m.Value.Contains('vertex="1"') -or $m.Value.Contains('edge="1"')) { $out += ,$m.Value }
    }
    return $out
}

function Nd-Attr([string]$cell, [string]$name) {
    $m = [regex]::Match($cell, '\b' + $name + '="([^"]*)"')
    if ($m.Success) { return $m.Groups[1].Value }
    return $null
}

function Nd-SetAttr([string]$cell, [string]$name, [string]$value) {
    $quoted = Nd-QuoteAttr $value
    $rx = New-Object regex ('\b' + $name + '="[^"]*"')
    if ($rx.IsMatch($cell)) { return $rx.Replace($cell, [string]($name + '=' + $quoted), 1) }
    $i = $cell.IndexOf('<mxCell')
    return $cell.Substring(0, $i) + '<mxCell ' + $name + '=' + $quoted + $cell.Substring($i + 7)
}

function Nd-SetGeom([string]$cell, $x, $y, $w, $h) {
    $rx = New-Object regex '<mxGeometry\b[^>]*?(/?)>'
    $ev = [Text.RegularExpressions.MatchEvaluator] {
        param($m)
        '<mxGeometry x="' + (Nd-Fmt0 $x) + '" y="' + (Nd-Fmt0 $y) + '" width="' + (Nd-Fmt0 $w) +
        '" height="' + (Nd-Fmt0 $h) + '" as="geometry"' + $m.Groups[1].Value + '>'
    }
    return $rx.Replace($cell, $ev, 1)
}

function Nd-Emit($node, [string]$parent, $out) {
    if ($node.kind -eq 'spacer') { return }
    if ($node.kind -eq 'stack') {
        foreach ($ch in $node.children) {
            $ch.x = [double]$ch.x + [double]$node.x
            $ch.y = [double]$ch.y + [double]$node.y
            Nd-Emit $ch $parent $out
        }
        return
    }
    $cells = @(Nd-Cells $node.shape.xml)
    if ($node.kind -eq 'icon') {
        $main = $cells[0]
    } else {
        $main = @($cells | Where-Object { (Nd-Attr $_ 'parent') -eq '1' })[0]
    }
    $label = Nd-Get $node.spec 'label' $node.shape.title
    if ($node.kind -eq 'icon') {
        $x = [double]$node.x + ([double]$node.w - [double]$node.iw) / 2
        $c = Nd-SetAttr $main 'id' $node.id
        $c = Nd-SetAttr $c 'parent' $parent
        $c = Nd-SetAttr $c 'value' ([string]$label)
        $style = Nd-Attr $c 'style'
        if ($style.Contains('fontSize=')) { $style = [regex]::Replace($style, 'fontSize=\d+', 'fontSize=12') }
        if (-not $style.EndsWith(';')) { $style += ';' }
        $lw = [int][Math]::Max([double]$node.w - 6, [double]$node.iw)
        $c = Nd-SetAttr $c 'style' ($style + "whiteSpace=wrap;labelWidth=$lw;")
        [void]$out.Add((Nd-SetGeom $c $x $node.y $node.iw $node.ih))
        return
    }
    $c = Nd-SetAttr $main 'id' $node.id
    $c = Nd-SetAttr $c 'parent' $parent
    $c = Nd-SetAttr $c 'value' ([string]$label)
    [void]$out.Add((Nd-SetGeom $c $node.x $node.y $node.w $node.h))
    $oldId = Nd-Attr $main 'id'
    $k = 0
    foreach ($sub in @($cells | Where-Object { (Nd-Attr $_ 'parent') -eq $oldId })) {
        $s = Nd-SetAttr $sub 'id' ($node.id + '__corner' + $k)
        $s = Nd-SetAttr $s 'parent' $node.id
        $gm = [regex]::Match($s, 'width="(\d+)" height="(\d+)"')
        if ($gm.Success) { $sw = [int]$gm.Groups[1].Value; $sh = [int]$gm.Groups[2].Value } else { $sw = 32; $sh = 32 }
        $sx = 0
        if ((Nd-Head $node) -eq $script:ASG_HEAD) { $sx = ([double]$node.w - $sw) / 2 }
        [void]$out.Add((Nd-SetGeom $s $sx 0 $sw $sh))
        $k++
    }
    foreach ($ch in (@(Nd-Packed $node) + @(Nd-Floating $node))) { Nd-Emit $ch $node.id $out }
}

function Nd-EdgeCell([int]$i, $e, $lib, $ids) {
    if ($e -is [object[]] -or $e -is [Collections.ArrayList]) {
        $arr = @($e)
        $h = @{ 'from' = $arr[0]; 'to' = $arr[1] }
        if ($arr.Count -gt 2) { $h['style'] = $arr[2] }
        if ($arr.Count -gt 3) { $h['label'] = $arr[3] }
        $e = $h
    }
    foreach ($k in @('from', 'to')) {
        if (-not $ids.ContainsKey([string]$e[$k])) { Nd-Die "edge 의 $k='$($e[$k])' 인 id 가 없습니다." }
    }
    $shape = Nd-Find $lib (Nd-Get $e 'style' 'Primary Path') 'arrow'
    $style = Nd-Attr @(Nd-Cells $shape.xml)[0] 'style'
    $side = @{ left = @(0, 0.5); right = @(1, 0.5); top = @(0.5, 0); bottom = @(0.5, 1) }
    $extra = ''
    foreach ($key in @('exit', 'entry')) {
        $v = Nd-Get $e $key $null
        if ($v) {
            $xy = $side[[string]$v]
            $extra += "${key}X=$($xy[0]);${key}Y=$($xy[1]);${key}Dx=0;${key}Dy=0;"
        }
    }
    $extra += [string](Nd-Get $e 'extra' '')
    $label = [string](Nd-Get $e 'label' '')
    return '<mxCell id="e' + $i + '" value=' + (Nd-QuoteAttr $label) + ' style=' + (Nd-QuoteAttr ($style + $extra)) +
           ' edge="1" parent="1" source="' + $e['from'] + '" target="' + $e['to'] + '">' +
           '<mxGeometry relative="1" as="geometry"/></mxCell>'
}

function Nd-Compose($spec, $lib, $margin = $script:MARGIN) {
    $ids = @{}
    $rootSpec = @{
        'group' = 'Generic Group (실선)'; 'items' = (Nd-Get $spec 'items' @());
        'dir' = (Nd-Get $spec 'dir' 'row'); 'gap' = (Nd-Get $spec 'gap' 60); 'pad' = 0;
        'min_w' = 0; 'min_h' = 0; 'id' = '__root'
    }
    $root = Nd-NewNode $rootSpec $lib $ids
    $ids.Remove('__root')
    Nd-Measure $root
    # 최상위는 머리 없이 배치
    $root.shape = [pscustomobject]@{ palette = $root.shape.palette; no = $root.shape.no; title = '__root';
                                     w = $root.shape.w; h = $root.shape.h; xml = $root.shape.xml }
    $title = Nd-Get $spec 'title' $null
    $top = $(if ($title) { $script:TITLE_H } else { $margin })
    $root.h = [double]$root.h - $script:GROUP_HEAD
    Nd-Place $root
    $out = New-Object Collections.ArrayList
    if ($title) {
        [void]$out.Add('<mxCell id="__title" value=' + (Nd-QuoteAttr ([string]$title)) +
            ' style="text;html=1;align=left;verticalAlign=middle;fontSize=20;fontStyle=1;fontColor=#222222;"' +
            ' vertex="1" parent="1"><mxGeometry x="' + $margin + '" y="16" width="800" height="36" as="geometry"/></mxCell>')
    }
    foreach ($c in $root.children) {
        $c.x = [double]$c.x + $margin
        $c.y = [double]$c.y + $top - $script:GROUP_HEAD
        Nd-Emit $c '1' $out
    }
    $i = 1
    foreach ($e in @(Nd-Get $spec 'edges' @())) {
        [void]$out.Add((Nd-EdgeCell $i $e $lib $ids))
        $i++
    }
    return @{ cells = $out; w = ([double]$root.w + 2 * $margin); h = ($top + [double]$root.h + $margin) }
}

function Nd-Build($spec, $lib) {
    $body = (Nd-Compose $spec $lib).cells -join ''
    $name = Nd-Escape ([string](Nd-Get $spec 'title' 'NHN Cloud Architecture'))
    return '<mxfile host="nhn_diagram.py"><diagram name=' + (Nd-QuoteAttr $name) + ' id="nhn">' +
           '<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" ' +
           'arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0" background="#FFFFFF">' +
           '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + $body + '</root></mxGraphModel></diagram></mxfile>'
}

# ---------- 명세 읽기 (JSON + YAML 부분집합) ----------
#
# PowerShell 에는 YAML 파서가 없다. 명세가 쓰는 범위만 직접 읽는다.
#   - 들여쓰기 블록 매핑·시퀀스, 인라인 플로우 {a: b} / [a, b]
#   - 주석, 따옴표 문자열, 정수·실수·true/false/null
# 앵커(&a *a), 여러 줄 스칼라(| >), 복합 키는 지원하지 않는다. 만나면 그대로 문자열이 되므로
# 생성기에서 걸린다. 필요하면 .json 명세를 쓴다.

function Nd-ToHashtable($o) {
    if ($null -eq $o) { return $null }
    if ($o -is [string] -or $o -is [bool] -or $o -is [int] -or $o -is [long] -or $o -is [double]) { return $o }
    if ($o -is [Collections.IDictionary]) {
        $h = @{}
        foreach ($k in @($o.Keys)) { $h["$k"] = Nd-ToHashtable $o[$k] }
        return $h
    }
    if ($o -is [object[]] -or $o -is [Collections.ArrayList]) {
        $a = New-Object Collections.ArrayList
        foreach ($x in $o) { [void]$a.Add((Nd-ToHashtable $x)) }
        return ,$a
    }
    if ($o -is [PSCustomObject]) {
        $h = @{}
        foreach ($p in $o.PSObject.Properties) { $h[$p.Name] = Nd-ToHashtable $p.Value }
        return $h
    }
    return $o
}

function Nd-StripComment([string]$line) {
    $sb = New-Object Text.StringBuilder
    $q = $null
    for ($i = 0; $i -lt $line.Length; $i++) {
        $ch = $line[$i]
        if ($null -ne $q) {
            [void]$sb.Append($ch)
            if ($ch -eq $q) { $q = $null }
            continue
        }
        if ($ch -eq '"' -or $ch -eq "'") { $q = $ch; [void]$sb.Append($ch); continue }
        if ($ch -eq '#' -and ($i -eq 0 -or $line[$i - 1] -eq ' ' -or $line[$i - 1] -eq "`t")) { break }
        [void]$sb.Append($ch)
    }
    return $sb.ToString().TrimEnd()
}

function Nd-Scalar([string]$s) {
    $t = $s.Trim()
    if ($t.Length -ge 2) {
        $a = $t[0]; $b = $t[$t.Length - 1]
        if (($a -eq '"' -and $b -eq '"') -or ($a -eq "'" -and $b -eq "'")) {
            return $t.Substring(1, $t.Length - 2)
        }
    }
    if ($t -eq '' -or $t -eq '~' -or $t -eq 'null' -or $t -eq 'Null') { return $null }
    if ($t -eq 'true' -or $t -eq 'True') { return $true }
    if ($t -eq 'false' -or $t -eq 'False') { return $false }
    if ($t -match '^-?\d+$') { return [int]$t }
    if ($t -match '^-?\d+\.\d+$') { return [double]$t }
    return $t
}

function Nd-FlowValue([string]$s, [ref]$i) {
    while ($i.Value -lt $s.Length -and $s[$i.Value] -eq ' ') { $i.Value++ }
    if ($i.Value -ge $s.Length) { return $null }
    $ch = $s[$i.Value]
    if ($ch -eq '{') { return Nd-FlowMap $s $i }
    if ($ch -eq '[') { return ,(Nd-FlowSeq $s $i) }
    $start = $i.Value
    $q = $null
    while ($i.Value -lt $s.Length) {
        $c = $s[$i.Value]
        if ($null -ne $q) {
            if ($c -eq $q) { $q = $null }
            $i.Value++
            continue
        }
        if ($c -eq '"' -or $c -eq "'") { $q = $c; $i.Value++; continue }
        if ($c -eq ',' -or $c -eq '}' -or $c -eq ']') { break }
        $i.Value++
    }
    return Nd-Scalar $s.Substring($start, $i.Value - $start)
}

function Nd-FlowMap([string]$s, [ref]$i) {
    $h = @{}
    $i.Value++   # '{'
    while ($i.Value -lt $s.Length) {
        while ($i.Value -lt $s.Length -and ($s[$i.Value] -eq ' ' -or $s[$i.Value] -eq ',')) { $i.Value++ }
        if ($i.Value -ge $s.Length) { break }
        if ($s[$i.Value] -eq '}') { $i.Value++; break }
        $start = $i.Value
        $q = $null
        while ($i.Value -lt $s.Length) {
            $c = $s[$i.Value]
            if ($null -ne $q) {
                if ($c -eq $q) { $q = $null }
                $i.Value++
                continue
            }
            if ($c -eq '"' -or $c -eq "'") { $q = $c; $i.Value++; continue }
            if ($c -eq ':') { break }
            $i.Value++
        }
        $key = $s.Substring($start, $i.Value - $start).Trim().Trim('"').Trim("'")
        if ($i.Value -lt $s.Length) { $i.Value++ }   # ':'
        $h[$key] = Nd-FlowValue $s $i
    }
    return $h
}

function Nd-FlowSeq([string]$s, [ref]$i) {
    $a = New-Object Collections.ArrayList
    $i.Value++   # '['
    while ($i.Value -lt $s.Length) {
        while ($i.Value -lt $s.Length -and ($s[$i.Value] -eq ' ' -or $s[$i.Value] -eq ',')) { $i.Value++ }
        if ($i.Value -ge $s.Length) { break }
        if ($s[$i.Value] -eq ']') { $i.Value++; break }
        [void]$a.Add((Nd-FlowValue $s $i))
    }
    return ,$a
}

function Nd-YPeek() {
    if ($script:YPos -lt $script:YLines.Count) { return $script:YLines[$script:YPos] }
    return $null
}

function Nd-YBlock([int]$indent) {
    $l = Nd-YPeek
    if ($null -eq $l) { return $null }
    if ($l.text -eq '-' -or $l.text.StartsWith('- ')) { return ,(Nd-YSeq $indent) }
    return Nd-YMap $indent
}

function Nd-YSeq([int]$indent) {
    $items = New-Object Collections.ArrayList
    while ($true) {
        $l = Nd-YPeek
        if ($null -eq $l -or $l.indent -ne $indent) { break }
        if (-not ($l.text -eq '-' -or $l.text.StartsWith('- '))) { break }
        $content = $l.text.Substring(1).Trim()
        $script:YPos++
        if ($content -eq '') {
            $nxt = Nd-YPeek
            if ($null -ne $nxt -and $nxt.indent -gt $indent) { [void]$items.Add((Nd-YBlock $nxt.indent)) }
            else { [void]$items.Add($null) }
        } elseif ($content.StartsWith('{') -or $content.StartsWith('[')) {
            $i = 0
            [void]$items.Add((Nd-FlowValue $content ([ref]$i)))
        } elseif ($content -match '^([^:]+):\s*(.*)$') {
            [void]$items.Add((Nd-YMapFrom $matches[1].Trim() $matches[2] ($indent + 2)))
        } else {
            [void]$items.Add((Nd-Scalar $content))
        }
    }
    return ,$items
}

function Nd-YValueFor([string]$rest, [int]$indent) {
    if ($rest.Trim() -eq '') {
        $nxt = Nd-YPeek
        if ($null -ne $nxt -and $nxt.indent -gt $indent) { return Nd-YBlock $nxt.indent }
        return $null
    }
    $t = $rest.Trim()
    if ($t.StartsWith('{') -or $t.StartsWith('[')) {
        $i = 0
        return Nd-FlowValue $t ([ref]$i)
    }
    return Nd-Scalar $t
}

function Nd-YMapFrom([string]$key, [string]$rest, [int]$indent) {
    $h = @{}
    $h[$key] = Nd-YValueFor $rest $indent
    while ($true) {
        $l = Nd-YPeek
        if ($null -eq $l -or $l.indent -ne $indent) { break }
        if ($l.text -eq '-' -or $l.text.StartsWith('- ')) { break }
        if (-not ($l.text -match '^([^:]+):\s*(.*)$')) { break }
        $k = $matches[1].Trim().Trim('"').Trim("'")
        $r = $matches[2]
        $script:YPos++
        $h[$k] = Nd-YValueFor $r $indent
    }
    return $h
}

function Nd-YMap([int]$indent) {
    $l = Nd-YPeek
    if ($null -eq $l) { return @{} }
    if (-not ($l.text -match '^([^:]+):\s*(.*)$')) { Nd-Die "YAML 을 읽지 못했습니다: $($l.text)" }
    $k = $matches[1].Trim().Trim('"').Trim("'")
    $r = $matches[2]
    $script:YPos++
    return Nd-YMapFrom $k $r $indent
}

function Nd-ParseYaml([string]$text) {
    $lines = New-Object Collections.ArrayList
    foreach ($raw in ($text -split "`n")) {
        $line = $raw.TrimEnd("`r")
        $stripped = Nd-StripComment $line
        if ($stripped.Trim() -eq '') { continue }
        if ($stripped.StartsWith('---') -or $stripped.StartsWith('%')) { continue }
        $indent = $stripped.Length - $stripped.TrimStart(' ').Length
        [void]$lines.Add([pscustomobject]@{ indent = $indent; text = $stripped.Trim() })
    }
    $script:YLines = $lines
    $script:YPos = 0
    if ($lines.Count -eq 0) { return @{} }
    return Nd-YBlock $lines[0].indent
}

function Nd-LoadSpec([string]$path) {
    $text = [IO.File]::ReadAllText($path, [Text.Encoding]::UTF8)
    if ($path.ToLower().EndsWith('.json')) { return Nd-ToHashtable ($text | ConvertFrom-Json) }
    return Nd-ParseYaml $text
}

function Nd-LibSource($libArg) {
    if ($libArg) { return $libArg }
    if (Test-Path -LiteralPath 'dist') { return 'dist' }
    if ($env:NHN_ICONS_DIST) { return $env:NHN_ICONS_DIST }
    return $script:DEFAULT_URL
}
