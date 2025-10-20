# CCS 250: Operating Systems Final Project

This will be the repository of my CCS 250 final project, which is a CLI utility. Specifics may vary, but for current version, I aim to create:

**Unsqueeze**: A CLI Utility for Freeing System Processes & Disk Space

## Documentation (By Gemini)

----

### **Utility Name:** `unsqueeze`

### **Target Platform:** Windows

### **Commands and Behaviors:**

**1. `unsqueeze disk` (File & Disk Operations)**

  * **`unsqueeze disk --analyze-temp`**

      * **Action:** Calculates the total size of the user temp folder (`%TEMP%`) and the Windows temp folder (`%windir%\Temp`).
      * **Output:** Prints the total size of each folder and a combined total (e.g., `User Temp: 1.2 GB | Windows Temp: 300 MB | Total: 1.5 GB`).

  * **`unsqueeze disk --clean-temp`**

      * **Action:** Prompts the user: `Delete all files from user and Windows temp folders? (y/n)`.
      * If 'y', force-deletes all files and subfolders within `%TEMP%` and `%windir%\Temp`. Must skip any files currently in use (handling permission errors gracefully).
      * **Output:** `[X] MB of temp files deleted.`

  * **`unsqueeze disk --analyze-bin`**

      * **Action:** Calculates the total size of the Recycle Bin.
      * **Output:** `Recycle Bin size: [X] MB`.

  * **`unsqueeze disk --empty-bin`**

      * **Action:** Immediately empties the Recycle Bin without confirmation.
      * **Output:** `Recycle Bin emptied.`

  * **`unsqueeze disk --find-large`**

      * **Action:** Scans the user's `Downloads` folder (`%USERPROFILE%\Downloads`).
      * **Output (Initial):** Lists the top 10 largest files, sorted descending by size.
        ```
        Top 10 largest files in Downloads:
        [1] 1024 MB - large_file.iso
        [2] 512 MB - video.mp4
        ...
        [10] 50 MB - document.pdf
        ```
      * **Prompt:** `Enter file number to delete, 'a' to delete all 10, or 'q' to quit:`
      * **Behavior:**
          * If number (e.g., `2`): Deletes `video.mp4`, prints `video.mp4 deleted.`, and exits.
          * If 'a': Deletes all 10 files listed, prints `All 10 files deleted.`, and exits.
          * If 'q': Exits.

**2. `unsqueeze process` (Process Operations)**

  * **`unsqueeze process --top`**

      * **Action:** Fetches the top 5 processes by CPU usage and top 5 by RAM (working set) usage.
      * **Output:**
        ```
        Top 5 CPU:
        PID: 123 | Name: chrome.exe | CPU: 25.4%
        ...

        Top 5 RAM:
        PID: 456 | Name: sqlserver.exe | RAM: 1536 MB
        ...
        ```

  * **`unsqueeze process --kill <name_or_pid>`**

      * **Action:** Searches for processes by exact PID or by name (e.g., `chrome.exe`).
      * **Behavior:**
          * **No match:** Prints `Process not found.`
          * **PID match:** Prompts `Kill process [PID] [Name]? (y/n)`. If 'y', force-kills the process.
          * **Name match (single):** Prompts `Kill process [PID] [Name]? (y/n)`. If 'y', force-kills the process.
          * **Name match (multiple):** Prints `Multiple processes found matching [Name].` and lists them `PID: [PID] | Name: [Name]`. Prompts `Kill all [N] matching processes? (y/n)`. If 'y', force-kills all listed.

**3. `unsqueeze service` (Service Operations)**

  * **`unsqueeze service --status <service_name>`**

      * **Action:** Searches for a Windows service where `<service_name>` is a case-insensitive "contains" match (e.g., `sql` matches `MSSQLSERVER`).
      * **Output:**
          * **No match:** `Service not found.`
          * **Match(es):** Prints `Name: [Full Service Name] | Status: [Running/Stopped] | Startup: [Automatic/Manual/Disabled]` for all matches.

  * **`unsqueeze service --stop <exact_service_name>`**

      * **Action:** Stops the service matching `<exact_service_name>`.
      * **Output:** `Service [exact_service_name] stopped.` or `Error: Could not stop service.`

  * **`unsqueeze service --disable <exact_service_name>`**

      * **Action:** Sets the startup type of the service matching `<exact_service_name>` to "Disabled".
      * **Output:** `Service [exact_service_name] startup type set to Disabled.` or `Error: Could not disable service.`

---
## How to Use (Claude)

### Files Created:

1. **unsqueeze.bat** - The launcher script
2. **unsqueeze.py** - The main Python application

### Setup Instructions:

1. Save both files in the same directory
2. Add that directory to your Windows PATH, or run from that directory
3. Open Command Prompt or PowerShell and run: `unsqueeze <command>`

### Features Implemented:

#### Disk Operations
- `unsqueeze disk --analyze-temp` - Shows temp folder sizes
- `unsqueeze disk --clean-temp` - Cleans temp folders with confirmation
- `unsqueeze disk --analyze-bin` - Shows Recycle Bin size
- `unsqueeze disk --empty-bin` - Empties Recycle Bin
- `unsqueeze disk --find-large` - Interactive large file finder/deleter

#### Process Operations
- `unsqueeze process --top` - Shows top 5 CPU and RAM processes
- `unsqueeze process --kill <name_or_pid>` - Kills processes with confirmation

#### Service Operations
- `unsqueeze service --list [running|stopped]` - Shows either running or stopped services 
- `unsqueeze service --status <name>` - Shows service status (fuzzy search)
- `unsqueeze service --stop <exact_name>` - Stops a service
- `unsqueeze service --disable <exact_name>` - Disables a service

### Dependencies:
- **Python 3.6+** (uses only standard library)
- **PowerShell** (for Recycle Bin and service operations - built into Windows)
