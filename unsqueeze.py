#!/usr/bin/env python3
import sys

# Import logic
from operations.disk import (
    analyze_bin,
    clean_temp,
    analyze_temp,
    empty_bin,
    find_large)

from operations.process import (
    process_kill,
    process_top
)

from operations.service import (
    service_disable,
    service_list,
    service_status,
    service_stop
)

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
