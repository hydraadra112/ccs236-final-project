# CCS 250: Operating Systems Final Project

This will be the repository of my CCS 250 final project, which is a CLI utility. Specifics may vary, but for current version, I aim to create:

Unsqueeze: A CLI Utility for Freeing System Processes & Disk Space

---

Core Features
🧹 File & Disk Terminator
Analyze Disk Space: Scans and reports the total size of user (%TEMP%) and Windows temporary folders.

Exterminate Temp Files: Deletes all files from temporary folders with a single confirmation.

Inspect Recycle Bin: Calculates the total size of your Recycle Bin.

Vaporize Recycle Bin: Immediately empties the Recycle Bin.

Find Large Files: Identifies the top 10 largest files in your Downloads folder and offers to delete them interactively.

⚙️ Process & Service Eliminator
View Top Processes: Lists the top 5 processes currently consuming the most CPU and RAM.

Search & Destroy: Finds a specific process by its name or ID and provides an option to kill it.

Manage Services: Searches for a system service by name and allows you to:

Check its current status (Running/Stopped).

Stop the service.

Disable the service to prevent it from running on the next system boot.

---

Instructions from Claude

I'll create a comprehensive Python utility wrapped in both `.bat` and `.ps1` scripts for Windows system maintenance.Now I'll create the `.bat` wrapper:And now the `.ps1` wrapper:Perfect! I've created a complete Windows system maintenance utility called `unsqueeze` with three files:

## Files Created:

1. **unsqueeze.py** - Main Python script with all functionality
2. **unsqueeze.bat** - Batch file wrapper
3. **unsqueeze.ps1** - PowerShell wrapper

## Setup Instructions:

1. Save all three files in the same directory
2. The wrappers will automatically check for Python and install the required `psutil` module if needed
3. Run commands using either:
   - `unsqueeze.bat disk --analyze-temp`
   - `unsqueeze.ps1 disk --analyze-temp`

## Key Features Implemented:

**Disk Operations:**

- Analyze temp folder sizes
- Clean temp folders with confirmation
- Analyze Recycle Bin size
- Empty Recycle Bin
- Find and delete large files in Downloads (interactive)

**Process Operations:**

- Show top 5 CPU and RAM processes
- Kill processes by name or PID (with confirmation)
- Handle multiple matching processes

**Service Operations:**

- Check service status (fuzzy search)
- Stop services
- Disable services
- Admin privilege warnings

The script handles errors gracefully (permission issues, files in use, etc.) and provides user-friendly output with proper formatting and confirmations for destructive operations.
