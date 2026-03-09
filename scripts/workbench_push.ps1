# workbench_push.ps1
# End-of-session sync script — copies project state into workbench and pushes to GitHub
# Usage: .\scripts\workbench_push.ps1 -ProjectName "3dpie" -ProjectPath "C:\Users\Steven\Chart generator\repo\git"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,

    [Parameter(Mandatory=$true)]
    [string]$ProjectPath
)

$ErrorActionPreference = "Stop"
$WorkbenchPath = "C:\Users\Steven\workbench"
$TargetPath = Join-Path $WorkbenchPath "projects\$ProjectName"

Write-Host "Workbench sync starting for: $ProjectName" -ForegroundColor Cyan

# Verify source project exists
if (-not (Test-Path $ProjectPath)) {
    Write-Error "Project path not found: $ProjectPath"
    exit 1
}

# Verify workbench exists
if (-not (Test-Path $WorkbenchPath)) {
    Write-Error "Workbench not found at: $WorkbenchPath"
    exit 1
}

# Create target project folder if needed
New-Item -ItemType Directory -Force -Path $TargetPath | Out-Null

# Copy state files from docs\ and handoff\ if they exist
$FilesToCopy = @(
    @{ From = Join-Path $ProjectPath "docs\HANDOFF.md";         To = Join-Path $TargetPath "HANDOFF.md" },
    @{ From = Join-Path $ProjectPath "handoff\STATE_VECTOR.json"; To = Join-Path $TargetPath "STATE_VECTOR.json" },
    @{ From = Join-Path $ProjectPath "docs\NEXT_TASK.md";        To = Join-Path $TargetPath "NEXT_TASK.md" }
)

foreach ($File in $FilesToCopy) {
    if (Test-Path $File.From) {
        Copy-Item -Path $File.From -Destination $File.To -Force
        Write-Host "Copied: $($File.From)" -ForegroundColor Green
    } else {
        Write-Host "Skipped (not found): $($File.From)" -ForegroundColor Yellow
    }
}

# Push to GitHub
Set-Location $WorkbenchPath

git add .

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
$CommitMessage = "chore(workbench): sync $ProjectName state -- $Timestamp"

$GitStatus = git status --porcelain
if (-not $GitStatus) {
    Write-Host "No changes to commit for $ProjectName" -ForegroundColor Yellow
    exit 0
}

git commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Error "Git commit failed"
    exit 1
}

git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Error "Git push failed"
    exit 1
}

Write-Host "Workbench sync complete for $ProjectName" -ForegroundColor Green
Write-Host "Committed: $CommitMessage" -ForegroundColor Cyan
