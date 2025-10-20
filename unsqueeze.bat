@echo off
REM unsqueeze.bat - Batch wrapper for unsqueeze.py

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7+ from python.org
    exit /b 1
)

REM Check if psutil is installed
python -c "import psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo psutil module not found. Installing...
    python -m pip install psutil
    if %errorlevel% neq 0 (
        echo Error: Failed to install psutil.
        echo Please run: pip install psutil
        exit /b 1
    )
)

REM Run the Python script with all arguments
python "%SCRIPT_DIR%unsqueeze.py" %*

exit /b %errorlevel%