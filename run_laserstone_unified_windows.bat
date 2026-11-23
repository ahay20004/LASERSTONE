@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
 set "PY=py -3.12"
) else (
 where python >nul 2>&1
 if %ERRORLEVEL% NEQ 0 (
  echo Python missing
  pause
  exit /b 2
 )
 set "PY=python"
)
%PY% -m unittest discover -s tests -p "test_local_unified_view.py" -v
if errorlevel 1 (
 echo Unified view tests failed.
 pause
 exit /b 1
)
%PY% local_unified_view.py
if errorlevel 1 (
 echo Unified view failed to open.
 pause
 exit /b 1
)
echo Original dark design + local synthetic engine panel opened.
echo Browser inspection is still required before Windows acceptance.
pause
