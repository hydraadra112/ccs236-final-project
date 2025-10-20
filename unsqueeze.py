#!/usr/bin/env python3
"""
unsqueeze - Windows System Maintenance Utility
"""

import os
import sys
import shutil
import psutil
import argparse
from pathlib import Path
import subprocess
import ctypes
import winreg

def is_admin():
    """Check if script is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def format_size(bytes_size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"

def get_folder_size(path):
    """Calculate total size of a folder"""
    total = 0
    try:
        for entry in os.scandir(path):
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
    
    print("Analyzing temp folders...")
    user_size = get_folder_size(user_temp) if user_temp else 0
    win_size = get_folder_size(win_temp)
    total = user_size + win_size
    
    print(f"User Temp: {format_size(user_size)} | Windows Temp: {format_size(win_size)} | Total: {format_size(total)}")

def clean_temp():
    """Clean temp folders"""
    user_temp = os.environ.get('TEMP', '')
    win_temp = os.path.join(os.environ.get('windir', 'C:\\Windows'), 'Temp')
    
    response = input("Delete all files from user and Windows temp folders? (y/n): ").lower()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    deleted_size = 0
    
    for temp_path in [user_temp, win_temp]:
        if not temp_path or not os.path.exists(temp_path):
            continue
            
        for entry in os.scandir(temp_path):
            try:
                size = 0
                if entry.is_file(follow_symlinks=False):
                    size = entry.stat().st_size
                    os.remove(entry.path)
                elif entry.is_dir(follow_symlinks=False):
                    size = get_folder_size(entry.path)
                    shutil.rmtree(entry.path, ignore_errors=True)
                deleted_size += size
            except (PermissionError, FileNotFoundError, OSError):
                continue
    
    print(f"{format_size(deleted_size)} of temp files deleted.")

def analyze_bin():
    """Analyze Recycle Bin size"""
    try:
        # Use PowerShell to get Recycle Bin size
        ps_cmd = "(New-Object -ComObject Shell.Application).NameSpace(0xA).Items() | Measure-Object -Property Size -Sum | Select-Object -ExpandProperty Sum"
        result = subprocess.run(['powershell', '-Command', ps_cmd], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout.strip():
            size = int(result.stdout.strip() or 0)
            print(f"Recycle Bin size: {format_size(size)}")
        else:
            print("Recycle Bin size: 0 B")
    except Exception as e:
        print("Recycle Bin size: Unable to determine")

def empty_bin():
    """Empty Recycle Bin"""
    try:
        subprocess.run(['powershell', '-Command', 
                       'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'],
                      timeout=30)
        print("Recycle Bin emptied.")
    except Exception as e:
        print(f"Error emptying Recycle Bin: {e}")

def find_large():
    """Find and delete large files in Downloads"""
    downloads = Path(os.environ.get('USERPROFILE', '')) / 'Downloads'
    
    if not downloads.exists():
        print("Downloads folder not found.")
        return
    
    print("Scanning Downloads folder...")
    files = []
    
    try:
        for file in downloads.rglob('*'):
            if file.is_file():
                try:
                    size = file.stat().st_size
                    files.append((size, file))
                except (PermissionError, FileNotFoundError, OSError):
                    continue
    except Exception as e:
        print(f"Error scanning: {e}")
        return
    
    files.sort(reverse=True, key=lambda x: x[0])
    top_10 = files[:10]
    
    if not top_10:
        print("No files found in Downloads.")
        return
    
    print("\nTop 10 largest files in Downloads:")
    for i, (size, file) in enumerate(top_10, 1):
        print(f"[{i}] {format_size(size)} - {file.name}")
    
    choice = input("\nEnter file number to delete, 'a' to delete all 10, or 'q' to quit: ").lower()
    
    if choice == 'q':
        return
    elif choice == 'a':
        for _, file in top_10:
            try:
                file.unlink()
            except Exception:
                pass
        print("All 10 files deleted.")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(top_10):
                file = top_10[idx][1]
                file.unlink()
                print(f"{file.name} deleted.")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error deleting file: {e}")

def process_top():
    """Show top processes by CPU and RAM"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Get CPU usage over 0.1 second interval
    psutil.cpu_percent(interval=0.1)
    for proc in processes:
        try:
            p = psutil.Process(proc['pid'])
            proc['cpu_percent'] = p.cpu_percent(interval=0.1)
        except:
            proc['cpu_percent'] = 0
    
    cpu_sorted = sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:5]
    ram_sorted = sorted(processes, key=lambda x: x.get('memory_info', {}).get('rss', 0) if x.get('memory_info') else 0, reverse=True)[:5]
    
    print("\nTop 5 CPU:")
    for proc in cpu_sorted:
        print(f"PID: {proc['pid']} | Name: {proc['name']} | CPU: {proc.get('cpu_percent', 0):.1f}%")
    
    print("\nTop 5 RAM:")
    for proc in ram_sorted:
        mem = proc.get('memory_info', {}).get('rss', 0) if proc.get('memory_info') else 0
        print(f"PID: {proc['pid']} | Name: {proc['name']} | RAM: {format_size(mem)}")

def process_kill(name_or_pid):
    """Kill a process by name or PID"""
    matches = []
    
    # Try as PID first
    try:
        pid = int(name_or_pid)
        try:
            proc = psutil.Process(pid)
            matches.append(proc)
        except psutil.NoSuchProcess:
            pass
    except ValueError:
        # Search by name
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == name_or_pid.lower():
                    matches.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    if not matches:
        print("Process not found.")
        return
    
    if len(matches) == 1:
        proc = matches[0]
        response = input(f"Kill process {proc.pid} {proc.name()}? (y/n): ").lower()
        if response == 'y':
            try:
                proc.kill()
                print(f"Process {proc.pid} killed.")
            except Exception as e:
                print(f"Error killing process: {e}")
    else:
        print(f"Multiple processes found matching {name_or_pid}.")
        for proc in matches:
            print(f"PID: {proc.pid} | Name: {proc.name()}")
        response = input(f"Kill all {len(matches)} matching processes? (y/n): ").lower()
        if response == 'y':
            for proc in matches:
                try:
                    proc.kill()
                except Exception:
                    pass
            print(f"All {len(matches)} processes killed.")

def service_status(service_name):
    """Check service status"""
    try:
        result = subprocess.run(['sc', 'query', 'state=', 'all'], 
                              capture_output=True, text=True, timeout=30)
        
        lines = result.stdout.split('\n')
        matches = []
        current = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('SERVICE_NAME:'):
                if current:
                    matches.append(current)
                name = line.split(':', 1)[1].strip()
                if service_name.lower() in name.lower():
                    current = {'name': name}
                else:
                    current = {}
            elif current and line.startswith('STATE'):
                parts = line.split(':', 1)[1].strip().split()
                if parts:
                    current['status'] = parts[1] if len(parts) > 1 else parts[0]
            elif current and line.startswith('START_TYPE'):
                current['startup'] = line.split(':', 1)[1].strip()
        
        if current:
            matches.append(current)
        
        if not matches:
            print("Service not found.")
            return
        
        for svc in matches:
            print(f"Name: {svc['name']} | Status: {svc.get('status', 'Unknown')} | Startup: {svc.get('startup', 'Unknown')}")
    
    except Exception as e:
        print(f"Error querying service: {e}")

def service_stop(service_name):
    """Stop a service"""
    try:
        result = subprocess.run(['sc', 'stop', service_name], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"Service {service_name} stopped.")
        else:
            print("Error: Could not stop service.")
    except Exception:
        print("Error: Could not stop service.")

def service_disable(service_name):
    """Disable a service"""
    try:
        result = subprocess.run(['sc', 'config', service_name, 'start=', 'disabled'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"Service {service_name} startup type set to Disabled.")
        else:
            print("Error: Could not disable service.")
    except Exception:
        print("Error: Could not disable service.")

def main():
    parser = argparse.ArgumentParser(description='unsqueeze - Windows System Maintenance Utility')
    subparsers = parser.add_subparsers(dest='command', help='Command category')
    
    # Disk commands
    disk_parser = subparsers.add_parser('disk', help='File and disk operations')
    disk_parser.add_argument('--analyze-temp', action='store_true', help='Analyze temp folder sizes')
    disk_parser.add_argument('--clean-temp', action='store_true', help='Clean temp folders')
    disk_parser.add_argument('--analyze-bin', action='store_true', help='Analyze Recycle Bin size')
    disk_parser.add_argument('--empty-bin', action='store_true', help='Empty Recycle Bin')
    disk_parser.add_argument('--find-large', action='store_true', help='Find large files in Downloads')
    
    # Process commands
    process_parser = subparsers.add_parser('process', help='Process operations')
    process_parser.add_argument('--top', action='store_true', help='Show top processes')
    process_parser.add_argument('--kill', metavar='NAME_OR_PID', help='Kill process by name or PID')
    
    # Service commands
    service_parser = subparsers.add_parser('service', help='Service operations')
    service_parser.add_argument('--status', metavar='SERVICE_NAME', help='Check service status')
    service_parser.add_argument('--stop', metavar='SERVICE_NAME', help='Stop service')
    service_parser.add_argument('--disable', metavar='SERVICE_NAME', help='Disable service')
    
    args = parser.parse_args()
    
    if args.command == 'disk':
        if args.analyze_temp:
            analyze_temp()
        elif args.clean_temp:
            clean_temp()
        elif args.analyze_bin:
            analyze_bin()
        elif args.empty_bin:
            empty_bin()
        elif args.find_large:
            find_large()
        else:
            disk_parser.print_help()
    
    elif args.command == 'process':
        if args.top:
            process_top()
        elif args.kill:
            process_kill(args.kill)
        else:
            process_parser.print_help()
    
    elif args.command == 'service':
        if not is_admin():
            print("Warning: Service operations require administrator privileges.")
        
        if args.status:
            service_status(args.status)
        elif args.stop:
            service_stop(args.stop)
        elif args.disable:
            service_disable(args.disable)
        else:
            service_parser.print_help()
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()