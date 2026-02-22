# TestMu AI SDET - Run tests script
# Run this in PowerShell from the project root: .\run_tests.ps1

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "=== TestMu AI SDET - Setup & Run ===" -ForegroundColor Cyan

# Create reports directory for pytest-html
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
    Write-Host "Created reports/ directory" -ForegroundColor Green
}

# 1. Install Python dependencies
Write-Host "`n[1/3] Installing dependencies (pip install -r requirements.txt)..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }

# 2. Install Playwright Chromium
Write-Host "`n[2/3] Installing Playwright Chromium..." -ForegroundColor Yellow
playwright install chromium
if ($LASTEXITCODE -ne 0) { throw "playwright install failed" }

# 3. Run pytest
Write-Host "`n[3/3] Running pytest..." -ForegroundColor Yellow
pytest
$pytestExit = $LASTEXITCODE

Write-Host "`n=== Done ===" -ForegroundColor Cyan
if ($pytestExit -eq 0) {
    Write-Host "All tests passed. Report: reports\test_report.html" -ForegroundColor Green
} else {
    Write-Host "Some tests failed. Check output above and reports\test_report.html" -ForegroundColor Red
}
exit $pytestExit
