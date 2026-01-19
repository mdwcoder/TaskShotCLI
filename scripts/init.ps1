# TaskShotCLI Init Script for Windows PowerShell

$ScriptDir = Split-Path $MyInvocation.MyCommand.Path
$RepoDir = Split-Path $ScriptDir -Parent
$SrcDir = "$RepoDir\src"

Write-Host "Repo Dir: $RepoDir"

$ProfilePath = $PROFILE

# Ensure profile exists
if (-not (Test-Path $ProfilePath)) {
    Write-Host "Creating PowerShell profile..."
    New-Item -ItemType File -Path $ProfilePath -Force | Out-Null
}

$FunctionCode = @"
function tsk {
    `$env:PYTHONPATH = "$SrcDir"
    python -m tskcli.cli `$args
}
"@

Write-Host "Adding function to $ProfilePath..."

Add-Content -Path $ProfilePath -Value "`n# TaskShotCLI Function"
Add-Content -Path $ProfilePath -Value $FunctionCode

Write-Host "Success! Added 'tsk' function."
Write-Host "Please restart your PowerShell session or run: . `$PROFILE"
