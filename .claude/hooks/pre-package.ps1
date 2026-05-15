# Pre-package validator. Fires on PreToolUse(Bash); only checks build.py package.
# Spec: .claude/hooks/pre-package.md
$ErrorActionPreference = 'Stop'

$payload = [Console]::In.ReadToEnd() | ConvertFrom-Json
$cmd = $payload.tool_input.command
if (-not $cmd) { exit 0 }
if ($cmd -notmatch 'build\.py.*\bpackage\b') { exit 0 }

$initPy = Join-Path (Get-Location) 'addon_name\__init__.py'
if (-not (Test-Path $initPy)) {
    [Console]::Error.WriteLine("Pre-package: addon_name/__init__.py missing")
    exit 2
}

$src = Get-Content $initPy -Raw
if ($src -notmatch 'def\s+register\s*\(' -or $src -notmatch 'def\s+unregister\s*\(') {
    [Console]::Error.WriteLine("Pre-package: register()/unregister() missing in __init__.py")
    exit 2
}

# Optional: warn on dev artifacts in addon dir
$artifacts = Get-ChildItem 'addon_name' -Recurse -Include '__pycache__', '*.pyc', '*.blend1' -ErrorAction SilentlyContinue
if ($artifacts) {
    [Console]::Error.WriteLine("Pre-package warning: dev artifacts in addon_name/ - $($artifacts.Count) item(s). Run build.py clean.")
}

exit 0
