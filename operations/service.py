import subprocess

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
