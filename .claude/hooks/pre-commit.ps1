# Pre-commit validator. Fires on PreToolUse(Bash); only validates when git commit.
# Spec: .claude/hooks/pre-commit.md
$ErrorActionPreference = 'Stop'

$payload = [Console]::In.ReadToEnd() | ConvertFrom-Json
$cmd = $payload.tool_input.command
if (-not $cmd -or $cmd -notmatch '\bgit\s+commit\b') { exit 0 }

$initPy = Join-Path (Get-Location) 'addon_name\__init__.py'
if (-not (Test-Path $initPy)) { exit 0 }

$src = Get-Content $initPy -Raw
$required = @('name', 'author', 'version', 'blender', 'description', 'category')
$missing = @()
foreach ($f in $required) {
    if ($src -notmatch "(?ms)bl_info\s*=\s*\{[^}]*['""]$f['""]\s*:") { $missing += $f }
}

if ($missing.Count -gt 0) {
    [Console]::Error.WriteLine("Pre-commit: bl_info missing fields: $($missing -join ', ')")
    exit 2
}

# Block obvious dev artifacts in staged Python
$staged = (& git diff --cached --name-only --diff-filter=AM 2>$null) | Where-Object { $_ -like 'addon_name/*.py' }
$blockers = @()
foreach ($f in $staged) {
    if (-not (Test-Path $f)) { continue }
    $content = Get-Content $f -Raw
    if ($content -match '\bbreakpoint\s*\(') { $blockers += "$f : breakpoint()" }
    if ($content -match '\bpdb\.set_trace\s*\(') { $blockers += "$f : pdb.set_trace()" }
}
if ($blockers.Count -gt 0) {
    [Console]::Error.WriteLine("Pre-commit: debugger calls in staged files:`n$($blockers -join "`n")")
    exit 2
}

exit 0
