#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path


def format_size(bytes_size):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def get_folder_size(folder_path):
    """Calculate total size of a folder"""
    total = 0
    try:
        for entry in os.scandir(folder_path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_folder_size(entry.path)
            except (PermissionError, FileNotFoundError, OSError):
                continue
    except (PermissionError, FileNotFoundError, OSError):
        pass
    return total


def analyze_temp():
    """Analyze temp folder sizes"""
    user_temp = os.environ.get('TEMP', '')
    win_temp = os.path.join(os.environ.get('windir', 'C:\\Windows'), 'Temp')
    
    user_size = get_folder_size(user_temp) if user_temp and os.path.exists(user_temp) else 0
    win_size = get_folder_size(win_temp) if os.path.exists(win_temp) else 0
    total_size = user_size + win_size
    
    print(f"User Temp: {format_size(user_size)} | Windows Temp: {format_size(win_size)} | Total: {format_size(total_size)}")


def delete_folder_contents(folder_path):
    """Delete all contents of a folder, skipping locked files"""
    deleted_size = 0
    if not os.path.exists(folder_path):
        return deleted_size
    
    for entry in os.listdir(folder_path):
        entry_path = os.path.join(folder_path, entry)
        try:
            if os.path.isfile(entry_path) or os.path.islink(entry_path):
                size = os.path.getsize(entry_path)
                os.unlink(entry_path)
                deleted_size += size
            elif os.path.isdir(entry_path):
                size = get_folder_size(entry_path)
                shutil.rmtree(entry_path, ignore_errors=True)
                deleted_size += size
        except (PermissionError, FileNotFoundError, OSError):
            continue
    return deleted_size


def clean_temp():
    """Clean temp folders with confirmation"""
    response = input("Delete all files from user and Windows temp folders? (y/n): ").lower().strip()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    user_temp = os.environ.get('TEMP', '')
    win_temp = os.path.join(os.environ.get('windir', 'C:\\Windows'), 'Temp')
    
    total_deleted = 0
    if user_temp and os.path.exists(user_temp):
        total_deleted += delete_folder_contents(user_temp)
    if os.path.exists(win_temp):
        total_deleted += delete_folder_contents(win_temp)
    
    print(f"{format_size(total_deleted)} of temp files deleted.")


def analyze_bin():
    """Analyze Recycle Bin size"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             "(New-Object -ComObject Shell.Application).NameSpace(0xA).Items() | Measure-Object -Property Size -Sum | Select-Object -ExpandProperty Sum"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            size = int(result.stdout.strip())
            print(f"Recycle Bin size: {format_size(size)}")
        else:
            print("Recycle Bin size: 0 B")
    except Exception:
        print("Error: Could not analyze Recycle Bin.")


def empty_bin():
    """Empty Recycle Bin"""
    try:
        subprocess.run(
            ['powershell', '-Command', 
             "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
            capture_output=True, timeout=30
        )
        print("Recycle Bin emptied.")
    except Exception:
        print("Error: Could not empty Recycle Bin.")


def find_large():
    """Find and optionally delete large files in Downloads"""
    downloads = os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')
    if not os.path.exists(downloads):
        print("Error: Downloads folder not found.")
        return
    
    files = []
    try:
        for entry in os.scandir(downloads):
            if entry.is_file():
                try:
                    files.append((entry.path, entry.stat().st_size, entry.name))
                except (PermissionError, FileNotFoundError, OSError):
                    continue
    except (PermissionError, OSError):
        print("Error: Cannot access Downloads folder.")
        return
    
    files.sort(key=lambda x: x[1], reverse=True)
    top_10 = files[:10]
    
    if not top_10:
        print("No files found in Downloads.")
        return
    
    print("\nTop 10 largest files in Downloads:")
    for i, (path, size, name) in enumerate(top_10, 1):
        print(f"[{i}] {format_size(size)} - {name}")
    
    print()
    choice = input("Enter file number to delete, 'a' to delete all 10, or 'q' to quit: ").lower().strip()
    
    if choice == 'q':
        return
    elif choice == 'a':
        for path, _, name in top_10:
            try:
                os.remove(path)
            except (PermissionError, FileNotFoundError, OSError):
                pass
        print(f"All {len(top_10)} files deleted.")
    elif choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(top_10):
            path, _, name = top_10[idx]
            try:
                os.remove(path)
                print(f"{name} deleted.")
            except (PermissionError, FileNotFoundError, OSError):
                print(f"Error: Could not delete {name}")
        else:
            print("Invalid file number.")
    else:
        print("Invalid choice.")


def process_top():
    """Show top processes by CPU and RAM"""
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Id,Name,@{Name='CPU';Expression={$_.CPU.ToString('F1')}} | Format-Table -HideTableHeaders"],
            capture_output=True, text=True, timeout=10
        )
        print("\nTop 5 CPU:")
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        print(f"PID: {parts[0]} | Name: {parts[1]} | CPU: {parts[2]}%")
        
        result = subprocess.run(
            ['powershell', '-Command',
             "Get-Process | Sort-Object WS -Descending | Select-Object -First 5 Id,Name,@{Name='RAM';Expression={[math]::Round($_.WS/1MB,2)}} | Format-Table -HideTableHeaders"],
            capture_output=True, text=True, timeout=10
        )
        print("\nTop 5 RAM:")
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        print(f"PID: {parts[0]} | Name: {parts[1]} | RAM: {parts[2]} MB")
    except Exception:
        print("Error: Could not retrieve process information.")


def process_kill(target):
    """Kill process by PID or name"""
    try:
        if target.isdigit():
            pid = int(target)
            result = subprocess.run(
                ['powershell', '-Command',
                 f"Get-Process -Id {pid} -ErrorAction SilentlyContinue | Select-Object Id,Name | ConvertTo-Json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                import json
                proc = json.loads(result.stdout.strip())
                response = input(f"Kill process {proc['Id']} {proc['Name']}? (y/n): ").lower().strip()
                if response == 'y':
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True, timeout=10)
                    print(f"Process {pid} killed.")
                else:
                    print("Operation cancelled.")
            else:
                print("Process not found.")
        else:
            result = subprocess.run(
                ['powershell', '-Command',
                 f"Get-Process -Name '{target}' -ErrorAction SilentlyContinue | Select-Object Id,Name | ConvertTo-Json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                import json
                output = result.stdout.strip()
                procs = json.loads(output)
                if not isinstance(procs, list):
                    procs = [procs]
                
                if len(procs) == 1:
                    proc = procs[0]
                    response = input(f"Kill process {proc['Id']} {proc['Name']}? (y/n): ").lower().strip()
                    if response == 'y':
                        subprocess.run(['taskkill', '/F', '/PID', str(proc['Id'])], capture_output=True, timeout=10)
                        print(f"Process {proc['Id']} killed.")
                    else:
                        print("Operation cancelled.")
                else:
                    print(f"Multiple processes found matching {target}.")
                    for proc in procs:
                        print(f"PID: {proc['Id']} | Name: {proc['Name']}")
                    response = input(f"Kill all {len(procs)} matching processes? (y/n): ").lower().strip()
                    if response == 'y':
                        for proc in procs:
                            subprocess.run(['taskkill', '/F', '/PID', str(proc['Id'])], capture_output=True, timeout=10)
                        print(f"All {len(procs)} processes killed.")
                    else:
                        print("Operation cancelled.")
            else:
                print("Process not found.")
    except Exception as e:
        print(f"Error: Could not kill process. {str(e)}")


def service_list(status_filter=None):
    """List services, optionally filtering by status (running or stopped)"""
    
    ps_command = "Get-Service"
    header = ""
    
    if status_filter:
        status_filter = status_filter.lower().strip()
        if status_filter not in ['running', 'stopped']:
            print("Error: Invalid status. Please use 'running' or 'stopped'.")
            return
        ps_status = status_filter.capitalize()
        ps_command += f" | Where-Object {{$_.Status -eq '{ps_status}'}}"
        header = f"--- {ps_status} Services ---"
    else:
        header = "--- All Services ---"

    # Select properties and convert to JSON
    ps_command += " | Select-Object Name,Status,StartType | ConvertTo-Json"

    try:
        result = subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            import json
            output = result.stdout.strip()
            services = json.loads(output)
            if not isinstance(services, list):
                services = [services]
            
            if services:
                print(header)
                for svc in services:
                    print(f"Name: {svc['Name']} | Status: {svc['Status']} | Startup: {svc['StartType']}")
            else:
                print(f"No services found.")
        else:
            print(f"No services found.")
    except Exception:
        print("Error: Could not retrieve service information.")

def service_status(service_name):
    """Get service status"""
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             f"Get-Service | Where-Object {{$_.Name -like '*{service_name}*' -or $_.DisplayName -like '*{service_name}*'}} | Select-Object Name,Status,StartType | ConvertTo-Json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            import json
            output = result.stdout.strip()
            services = json.loads(output)
            if not isinstance(services, list):
                services = [services]
            
            if services:
                for svc in services:
                    print(f"Name: {svc['Name']} | Status: {svc['Status']} | Startup: {svc['StartType']}")
            else:
                print("Service not found.")
        else:
            print("Service not found.")
    except Exception:
        print("Error: Could not retrieve service information.")


def service_stop(service_name):
    """Stop a service"""
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             f"Stop-Service -Name '{service_name}' -Force -ErrorAction Stop"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"Service {service_name} stopped.")
        else:
            print("Error: Could not stop service.")
    except Exception:
        print("Error: Could not stop service.")


def service_disable(service_name):
    """Disable a service"""
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             f"Set-Service -Name '{service_name}' -StartupType Disabled -ErrorAction Stop"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"Service {service_name} startup type set to Disabled.")
        else:
            print("Error: Could not disable service.")
    except Exception:
        print("Error: Could not disable service.")


def main():
    if len(sys.argv) < 2:
        print("Usage: unsqueeze <command> [options]")
        print("\nCommands:")
        print("  disk      - File & Disk operations")
        print("  process   - Process operations")
        print("  service   - Service operations")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'disk':
        if len(sys.argv) < 3:
            print("Usage: unsqueeze disk <option>")
            print("Options: --analyze-temp, --clean-temp, --analyze-bin, --empty-bin, --find-large")
            return
        
        option = sys.argv[2].lower()
        if option == '--analyze-temp':
            analyze_temp()
            print("\nTo clean temp files, run: unsqueeze disk --clean-temp")
        elif option == '--clean-temp':
            clean_temp()
            print("\nTo check your recycle bin, run: unsqueeze disk --analyze-bin")
        elif option == '--analyze-bin':
            analyze_bin()
            print("\nTo empty the recycle bin, run: unsqueeze disk --empty-bin")
        elif option == '--empty-bin':
            empty_bin()
            print("\nTo find large files in your Downloads, run: unsqueeze disk --find-large")
        elif option == '--find-large':
            find_large()
        else:
            print(f"Unknown option: {option}")
    
    elif command == 'process':
        if len(sys.argv) < 3:
            print("Usage: unsqueeze process <option>")
            print("Options: --top, --kill <name_or_pid>")
            return
        
        option = sys.argv[2].lower()
        if option == '--top':
            process_top()
            print("\nTo kill a process, run: unsqueeze process --kill <name_or_pid>")
        elif option == '--kill':
            if len(sys.argv) < 4:
                print("Usage: unsqueeze process --kill <name_or_pid>")
                return
            process_kill(sys.argv[3])
            print("\nTo see the top processes again, run: unsqueeze process --top")
        else:
            print(f"Unknown option: {option}")
    
    elif command == 'service':
        if len(sys.argv) < 3:
            print("Usage: unsqueeze service <option>")
            print("Options: --list [running|stopped], --status <service_name>, --stop <exact_service_name>, --disable <exact_service_name>")
            return
        
        option = sys.argv[2].lower()

        if option == '--list':
            # Check if a filter (like 'running') was provided
            status_arg = sys.argv[3] if len(sys.argv) >= 4 else None
            service_list(status_arg)
            print(f"\nTo check a specific service, run: unsqueeze service --status <service_name>")
        elif option == '--status':
            if len(sys.argv) < 4:
                print("Usage: unsqueeze service --status <service_name>")
                return
            service_status(sys.argv[3])
            print("\nTo stop a service, run: unsqueeze service --stop <exact_name>")
            print("To disable a service, run: unsqueeze service --disable <exact_name>")
        elif option == '--stop':
            if len(sys.argv) < 4:
                print("Usage: unsqueeze service --stop <exact_service_name>")
                return
            service_name = sys.argv[3]
            service_stop(service_name)
            print(f"\nTo also disable this service, run: unsqueeze service --disable {service_name}")
        elif option == '--disable':
            if len(sys.argv) < 4:
                print("Usage: unsqueeze service --disable <exact_service_name>")
                return
            service_name = sys.argv[3]
            service_disable(service_name)
            print(f"\nTo check the status, run: unsqueeze service --status {service_name}")
        else:
            print(f"Unknown option: {option}")
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: disk, process, service")

if __name__ == '__main__':
    main()
