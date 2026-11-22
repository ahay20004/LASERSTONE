@echo off
setlocal
cd /d "%~dp0..\.."
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3.12 -m unittest discover -s projects\paper2\tests -p test_*.py -v
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Python 3.12 is required. No Python launcher found.
        exit /b 2
    )
    python -m unittest discover -s projects\paper2\tests -p test_*.py -v
)
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: LASERSTONE synthetic integration tests failed.
    exit /b 1
)
echo LASERSTONE synthetic integration tests PASSED. Scientific validity remains NOT ESTABLISHED.
exit /b 0
