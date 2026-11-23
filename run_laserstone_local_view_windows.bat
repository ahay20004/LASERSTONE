@echo off
setlocal
cd /d "%~dp0"
echo LASERSTONE local scientific view acceptance
echo ==========================================
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  set "PYTHON_CMD=py -3.12"
) else (
  where python >nul 2>&1
  if %ERRORLEVEL% NEQ 0 (
    echo FAIL: Python not found.
    pause
    exit /b 2
  )
  set "PYTHON_CMD=python"
)
%PYTHON_CMD% -m unittest discover -s tests -p "test_local_scientific_*.py" -v
if errorlevel 1 (
  echo FAIL: Scientific view tests did not pass. Browser not opened.
  pause
  exit /b 1
)
%PYTHON_CMD% local_scientific_view.py
if errorlevel 1 (
  echo FAIL: Local scientific view could not be generated.
  pause
  exit /b 1
)
echo.
echo CHECK: The browser should show the dark LOCAL scientific view.
echo CHECK: Score 100, classification Highly Consistent.
echo CHECK: Synthetic demonstration only. No private data used.
echo This is not operational or experimental acceptance.
pause
exit /b 0
