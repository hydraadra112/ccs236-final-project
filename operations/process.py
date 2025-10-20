import subprocess

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
