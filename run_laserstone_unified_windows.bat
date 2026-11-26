@echo off
setlocal
cd /d "%~dp0"
title LASERSTONE - Local Launcher
py -3.12 -c "import sys" >nul 2>&1
if not errorlevel 1 (
 set "PY=py -3.12"
) else (
 python -c "import sys; assert sys.version_info >= (3, 12)" >nul 2>&1
 if errorlevel 1 (
  echo Python 3.12 or newer is required.
  pause
  exit /b 2
 )
 set "PY=python"
)
if /i "%~1"=="--selected-release" (
 if "%~2"=="" exit /b 4
 %PY% release_launch.py "%~2"
 exit /b
)
echo Checking local scientific resource readiness...
%PY% resource_preflight.py
if errorlevel 1 echo Resource diagnostics failed. Optional resource readiness is unknown.
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
if /i "%~1"=="--install-shortcut" (
 powershell.exe -NoProfile -Command "$ErrorActionPreference='Stop'; $w=New-Object -ComObject WScript.Shell; $p=Join-Path ([Environment]::GetFolderPath('DesktopDirectory')) 'LASERSTONE.lnk'; $s=$w.CreateShortcut($p); $s.TargetPath=(Join-Path (Get-Location).Path 'run_laserstone_unified_windows.bat'); $s.WorkingDirectory=(Get-Location).Path; $s.Description='LASERSTONE local launcher'; $s.Save()"
 if errorlevel 1 (
  echo Shortcut installation failed.
  pause
  exit /b 3
 )
 echo Desktop shortcut created.
)
echo Local preview opened. No network update was performed.
echo Browser inspection is still required before Windows acceptance.
exit /b 0
