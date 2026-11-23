@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  py -3.12 laserstone_windows_acceptance.py
) else (
  where python >nul 2>&1
  if %ERRORLEVEL% NEQ 0 (
    echo Python not found. Acceptance was not performed.
    pause
    exit /b 2
  )
  python laserstone_windows_acceptance.py
)
set "RESULT=%ERRORLEVEL%"
echo.
echo Report: laserstone_windows_acceptance.json
echo This checks software only. GUI and scientific acceptance remain separate.
pause
exit /b %RESULT%
