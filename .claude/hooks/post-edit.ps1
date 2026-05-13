# Post-edit lint. Fires on PostToolUse(Edit|Write); only scans addon_name/*.py.
# Spec: .claude/hooks/post-edit.md
$ErrorActionPreference = 'Stop'

$payload = [Console]::In.ReadToEnd() | ConvertFrom-Json
$path = $payload.tool_input.file_path
if (-not $path) { exit 0 }
if ($path -notmatch '\\addon_name\\.*\.py$' -and $path -notmatch '/addon_name/.*\.py$') { exit 0 }
if (-not (Test-Path $path)) { exit 0 }

$src = Get-Content $path -Raw
$warnings = @()

# Operator classes missing bl_description
$opMatches = [regex]::Matches($src, '(?ms)class\s+(\w+_OT_\w+)\(bpy\.types\.Operator\):(.*?)(?=\nclass\s|\Z)')
foreach ($m in $opMatches) {
    $body = $m.Groups[2].Value
    if ($body -notmatch 'bl_description\s*=') {
        $warnings += "$($m.Groups[1].Value): missing bl_description"
    }
}

# Hardcoded user paths
if ($src -match 'C:\\\\Users\\\\' -or $src -match '/home/[a-z]') {
    $warnings += "hardcoded user path detected — use bpy.path utilities"
}

# print() in operator/utility code (not __init__ banner)
if ($path -notmatch '__init__\.py$') {
    $printCount = ([regex]::Matches($src, '(?m)^\s*print\s*\(')).Count
    if ($printCount -gt 0) {
        $warnings += "$printCount print() call(s) — prefer self.report() or logging"
    }
}

if ($warnings.Count -gt 0) {
    $rel = [System.IO.Path]::GetFileName($path)
    [Console]::Error.WriteLine("Post-edit warnings ($rel):`n  - $($warnings -join "`n  - ")")
}
exit 0
