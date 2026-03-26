@echo off
set SCRIPT_DIR=%~dp0
echo Spoustim generator logu (Python)...
python -u "%SCRIPT_DIR%log_generator.py"
if %ERRORLEVEL% neq 0 (
    echo.
    echo CHYBA: Skript skoncil s chybou %ERRORLEVEL%.
    pause
)
