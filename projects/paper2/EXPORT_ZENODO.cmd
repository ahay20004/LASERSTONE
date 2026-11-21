@echo off
setlocal
cd /d "%~dp0"
set "ROOT=%~dp0"
set "MANIFEST=%ROOT%private\zenodo_manifest.json"
set "OUT=%ROOT%output\zenodo_export"
if not exist "%MANIFEST%" (
  echo BLOCKED: Missing private\zenodo_manifest.json
  echo No ZIP will be published or created without source verification.
  exit /b 2
)
py -3.12 "%ROOT%export_zenodo.py" --manifest "%MANIFEST%" --out "%OUT%"
if errorlevel 1 (
  echo BLOCKED: inspect output\zenodo_export\zenodo_export_status.json
  exit /b 1
)
echo PASS: verified ZIP is in output\zenodo_export
exit /b 0
