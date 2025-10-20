# unsqueeze.ps1 - PowerShell wrapper for unsqueeze.py

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if Python is installed
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "Error: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.7+ from python.org"
    exit 1
}

# Check if psutil is installed
$psutilCheck = python -c "import psutil" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "psutil module not found. Installing..." -ForegroundColor Yellow
    python -m pip install psutil
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install psutil." -ForegroundColor Red
        Write-Host "Please run: pip install psutil"
        exit 1
    }
}

# Run the Python script with all arguments
$pythonScript = Join-Path $ScriptDir "unsqueeze.py"
& python $pythonScript $args

exit $LASTEXITCODE