@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3.12 agent_local_inventory.py
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Python not found. Inventory was not performed.
        exit /b 2
    )
    python agent_local_inventory.py
)
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Agent inventory failed.
    exit /b 1
)
echo Inventory only. No agents were started or validated.
exit /b 0
