<#
.SYNOPSIS
  Copies the SDLC package into a target repository.

.DESCRIPTION
  Dry run by default: prints what would happen and changes nothing.
  Use -Apply to copy. Existing files are never overwritten silently.

  Ownership rules:
    - Project-owned (.agents/rules/project.md): never overwritten.
    - Templates (.github/*): copied only when missing, never overwritten.
    - Package-owned (AGENTS.md, .agents/rules/instructions.md, guides,
      references, sdlc-* skills, README, SDLC_VERSION):
        * first install  : a differing file is a CONFLICT and is skipped
                           (with -Force the old file is saved as .bak first);
        * later updates  : overwritten (detected by an existing .agents/SDLC_VERSION).

.EXAMPLE
  .\tools\install-package.ps1 -Target C:\WebApps\my-project
  .\tools\install-package.ps1 -Target C:\WebApps\my-project -Apply
#>
param(
    [Parameter(Mandatory = $true)][string]$Target,
    [switch]$Apply,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

$src = Join-Path (Split-Path -Parent $PSScriptRoot) 'package'
if (-not (Test-Path -LiteralPath $src)) { throw "Package not found: $src. Run: python3 tools/build_package.py" }
if (-not (Test-Path -LiteralPath $Target)) { throw "Target not found: $Target" }
$src = (Resolve-Path -LiteralPath $src).Path
$Target = (Resolve-Path -LiteralPath $Target).Path

$isUpdate = Test-Path -LiteralPath (Join-Path $Target '.agents/SDLC_VERSION')
$owned = @('AGENTS.md', '.agents/rules/instructions.md', '.agents/README.md', '.agents/SDLC_VERSION',
           '.agents/guides/*', '.agents/references/*', '.agents/skills/sdlc-*')

function Test-Owned([string]$rel) {
    foreach ($p in $owned) { if ($rel -like $p) { return $true } }
    return $false
}

$summary = @{}
$conflicts = @()
$versionPending = $false
$mode = if ($Apply) { 'APPLY' } else { 'DRY RUN' }
Write-Host ("SDLC package install [{0}] -> {1} ({2})" -f $mode, $Target, $(if ($isUpdate) { 'update' } else { 'first install' }))

Get-ChildItem -LiteralPath $src -Recurse -File -Force | ForEach-Object {
    $rel = ($_.FullName.Substring($src.Length).TrimStart('\', '/')) -replace '\\', '/'
    $dest = Join-Path $Target $rel
    $write = $false

    if (-not (Test-Path -LiteralPath $dest)) {
        $action = 'NEW'; $write = $true
    }
    elseif ((Get-FileHash -LiteralPath $_.FullName).Hash -eq (Get-FileHash -LiteralPath $dest).Hash) {
        $action = 'SAME'
    }
    elseif ($rel -eq '.agents/rules/project.md' -or -not (Test-Owned $rel)) {
        $action = 'KEEP'
    }
    elseif ($isUpdate) {
        $action = 'UPDATE'; $write = $true
    }
    elseif ($Force) {
        $action = 'REPLACE'; $write = $true
    }
    else {
        $action = 'CONFLICT'; $conflicts += $rel
    }

    $summary[$action] = 1 + [int]$summary[$action]
    if ($action -ne 'SAME') { Write-Host ("  {0,-9} {1}" -f $action, $rel) }

    # The version marker is written last, and only when no conflict was skipped.
    # Otherwise the next run would look like an update and overwrite the skipped
    # file without a backup.
    if ($rel -eq '.agents/SDLC_VERSION') {
        if ($write) { $versionPending = $true }
    }
    elseif ($Apply -and $write) {
        if ($action -eq 'REPLACE') { Copy-Item -LiteralPath $dest -Destination ($dest + '.bak') -Force }
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $dest -Force
    }
}

if ($Apply -and $versionPending -and $conflicts.Count -eq 0) {
    $verSrc = Join-Path $src '.agents/SDLC_VERSION'
    $verDest = Join-Path $Target '.agents/SDLC_VERSION'
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $verDest) | Out-Null
    Copy-Item -LiteralPath $verSrc -Destination $verDest -Force
}

Write-Host ''
Write-Host ('Summary: ' + (($summary.GetEnumerator() | Sort-Object Name | ForEach-Object { '{0}={1}' -f $_.Name, $_.Value }) -join ', '))
if ($conflicts.Count -gt 0) {
    Write-Host ''
    Write-Host 'Conflicts were skipped. Move any project-specific content from the existing file into'
    Write-Host '.agents/rules/project.md, then re-run with -Apply -Force (the old file is saved as .bak).'
}
if (-not $Apply) { Write-Host 'Nothing was changed. Re-run with -Apply to copy.' }
