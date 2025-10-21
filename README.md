# **CCS 250: Operating Systems Final Project**

## **Project Title:**

**Unsqueeze – A CLI Utility for Freeing System Processes & Disk Space**

---

### **1. Overview**

**Unsqueeze** is a Windows-based command-line interface (CLI) utility designed to optimize system performance by freeing disk space, managing processes, and controlling system services. It combines multiple maintenance and administrative operations into a single unified tool.

This utility demonstrates understanding and application of **process management**, **file system operations**, and **service control**, core concepts of Operating Systems.

---

### **2. System Requirements**

- **Target OS:** Windows 10 or later
- **Language:** Python 3.6+
- **Execution Method:** Command Prompt or PowerShell
- **Dependencies:** Uses only Python Standard Library and built-in PowerShell commands

---

### **3. Project Structure**

| File              | Description                                                                            |
| ----------------- | -------------------------------------------------------------------------------------- |
| **unsqueeze.py**  | Main Python application containing all logic for disk, process, and service operations |
| **unsqueeze.bat** | Windows batch launcher for invoking `unsqueeze.py` from any command line interface     |

---

### **4. Installation & Setup**

1. Download or clone the repository containing `unsqueeze.py` and `unsqueeze.bat`.
2. Place both files in the same directory.
3. (Pending Feature) Add the directory to your **Windows PATH** environment variable for global access.
4. (Pending Feature) Open **Command Prompt** or **PowerShell**, and verify installation using:

   ```bash
   unsqueeze --help
   ```

5. Execute commands in the form:

   ```bash
   unsqueeze <category> <subcommand> [options]
   ```

---

### **5. Command Categories and Operations**

#### **A. Disk Operations**

Manage disk cleanup, file analysis, and storage optimization.

| Command                         | Description                                                                                        |
| ------------------------------- | -------------------------------------------------------------------------------------------------- |
| `unsqueeze disk --analyze-temp` | Calculates and displays the total size of the user and Windows temporary folders.                  |
| `unsqueeze disk --clean-temp`   | Prompts user to delete all files in `%TEMP%` and `%windir%\Temp`, skipping files in use.           |
| `unsqueeze disk --analyze-bin`  | Calculates the total size of the Recycle Bin.                                                      |
| `unsqueeze disk --empty-bin`    | Empties the Recycle Bin immediately, without confirmation.                                         |
| `unsqueeze disk --find-large`   | Scans the Downloads folder for the top 10 largest files and offers deletion options interactively. |

**Example:**

```bash
unsqueeze disk --analyze-temp
# Output:
# User Temp: 1.2 GB | Windows Temp: 300 MB | Total: 1.5 GB
```

**Interactive Example (`--find-large`):**

```
Top 10 largest files in Downloads:
[1] 1024 MB - large_file.iso
[2] 512 MB  - video.mp4
...
Enter file number to delete, 'a' to delete all 10, or 'q' to quit:
```

---

#### **B. Process Operations**

Monitor and control active processes to optimize CPU and memory usage.

| Command                                  | Description                                                       |
| ---------------------------------------- | ----------------------------------------------------------------- |
| `unsqueeze process --top`                | Displays the top 5 processes by CPU usage and top 5 by RAM usage. |
| `unsqueeze process --kill <name_or_pid>` | Terminates processes by PID or name, with confirmation prompts.   |

**Example Output:**

```
Top 5 CPU:
PID: 123 | Name: chrome.exe | CPU: 25.4%

Top 5 RAM:
PID: 456 | Name: sqlserver.exe | RAM: 1536 MB
```

**Kill Example:**

```
unsqueeze process --kill chrome.exe
Multiple processes found matching chrome.exe.
Kill all 4 matching processes? (y/n)
```

---

#### **C. Service Operations**

View, stop, and disable Windows services to manage startup performance.

| Command                                    | Description                                                                                     |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `unsqueeze service --status <name>`        | Performs a fuzzy search for a service by name and displays its status, startup type, and state. |
| `unsqueeze service --stop <exact_name>`    | Stops a specified service.                                                                      |
| `unsqueeze service --disable <exact_name>` | Disables a specified service by changing its startup type.                                      |

**Example Output:**

```
unsqueeze service --status sql
Name: MSSQLSERVER | Status: Running | Startup: Automatic
```

---

### **6. Example Workflow**

Below is a typical system maintenance sequence using **Unsqueeze**:

```bash
unsqueeze disk --analyze-temp
unsqueeze disk --clean-temp
unsqueeze disk --analyze-bin
unsqueeze disk --empty-bin
unsqueeze process --top
unsqueeze process --kill chrome.exe
unsqueeze service --status sql
unsqueeze service --stop MSSQLSERVER
```

---

### **7. Design Notes**

- **Graceful Error Handling:**
  Handles permission errors, missing files, or inaccessible services gracefully without interrupting execution.

- **Interactive Safety:**
  Destructive actions (e.g., deletions, process kills) prompt user confirmation before proceeding.

- **Windows Integration:**
  Leverages built-in PowerShell commands for service and Recycle Bin management, ensuring compatibility without external dependencies.

---

### **8. Example Output Summary**

```
User Temp: 1.2 GB | Windows Temp: 300 MB | Total: 1.5 GB
[✓] Deleted 1.5 GB of temporary files.
Recycle Bin size: 512 MB
Recycle Bin emptied.
Top 5 CPU:
PID: 123 | Name: chrome.exe | CPU: 25.4%
...
Service MSSQLSERVER stopped.
```

---

### **9. Future Improvements**

- Add support for **custom cleanup directories** via configuration file
- Introduce **log file generation** for operation history
- Add **automated scheduling** for maintenance tasks

---

### **10. Conclusion**

The **Unsqueeze** CLI utility demonstrates the integration of multiple core operating system functionalities—**file management, process control, and service administration**—into a unified, user-friendly tool. It is designed for practical system maintenance while highlighting proficiency in process management, filesystem operations, and Windows API interactions through Python.
