@echo off
setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher.
    exit /b 1
)

REM Call the Python script with all arguments
python "%SCRIPT_DIR%unsqueeze.py" %*

exit /b %errorlevel%
