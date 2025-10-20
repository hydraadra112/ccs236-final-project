import os
import shutil
import subprocess
from ..utils import format_size

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

