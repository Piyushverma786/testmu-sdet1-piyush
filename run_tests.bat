@echo off
REM TestMu AI SDET - Run tests (Windows CMD)
cd /d "%~dp0"

echo === TestMu AI SDET - Setup and Run ===

if not exist reports mkdir reports

echo.
echo [1/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 goto err

echo.
echo [2/3] Installing Playwright Chromium...
playwright install chromium
if errorlevel 1 goto err

echo.
echo [3/3] Running pytest...
pytest
set PYEXIT=%errorlevel%

echo.
echo === Done ===
if %PYEXIT% equ 0 (
    echo All tests passed. Report: reports\test_report.html
) else (
    echo Some tests failed. Check output above and reports\test_report.html
)
exit /b %PYEXIT%

:err
echo Setup failed.
exit /b 1
