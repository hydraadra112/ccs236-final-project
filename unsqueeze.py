#!/usr/bin/env python3
import sys

# Import logic
from operations.disk import (
    analyze_bin,
    clean_temp,
    analyze_temp,
    empty_bin,
    find_large,
    clean_custom_dir) # Imported the new function here

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

def wait_for_user():
    """Helper to pause execution so user can read output"""
    input("\nPress Enter to continue...")

def menu_disk():
    while True:
        print("\n--- Disk Operations ---")
        print("1. Analyze Temp Files")
        print("2. Clean Temp Files")
        print("3. Analyze Recycle Bin")
        print("4. Empty Recycle Bin")
        print("5. Find Large Files (Downloads)")
        print("6. Clean Custom Directory") # New Menu Item
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            analyze_temp()
            wait_for_user()
        elif choice == '2':
            clean_temp()
            wait_for_user()
        elif choice == '3':
            analyze_bin()
            wait_for_user()
        elif choice == '4':
            empty_bin()
            wait_for_user()
        elif choice == '5':
            find_large()
            wait_for_user()
        elif choice == '6':
            path = input("Enter full path to directory: ").strip()
            if path:
                clean_custom_dir(path)
            else:
                print("No path entered.")
            wait_for_user()
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again.")

def menu_process():
    while True:
        print("\n--- Process Operations ---")
        print("1. View Top Processes (CPU/RAM)")
        print("2. Kill Process")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            process_top()
            wait_for_user()
        elif choice == '2':
            target = input("Enter Process Name or PID to kill: ").strip()
            if target:
                process_kill(target)
            else:
                print("Operation cancelled.")
            wait_for_user()
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again.")

def menu_service():
    while True:
        print("\n--- Service Operations ---")
        print("1. List Services")
        print("2. Check Service Status")
        print("3. Stop Service")
        print("4. Disable Service")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            filter_opt = input("Filter (running/stopped/all) [default: all]: ").strip().lower()
            if filter_opt not in ['running', 'stopped']:
                filter_opt = None
            service_list(filter_opt)
            wait_for_user()
        elif choice == '2':
            name = input("Enter Service Name (fuzzy search): ").strip()
            if name:
                service_status(name)
            wait_for_user()
        elif choice == '3':
            name = input("Enter EXACT Service Name to stop: ").strip()
            if name:
                service_stop(name)
            wait_for_user()
        elif choice == '4':
            name = input("Enter EXACT Service Name to disable: ").strip()
            if name:
                service_disable(name)
            wait_for_user()
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again.")

def main():
    while True:
        print("\n========================================")
        print("   Unsqueeze: System Optimizer Tool")
        print("========================================")
        print("1. Disk Operations")
        print("2. Process Operations")
        print("3. Service Operations")
        print("0. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            menu_disk()
        elif choice == '2':
            menu_process()
        elif choice == '3':
            menu_service()
        elif choice == '0':
            print("Exiting Unsqueeze...")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 0-3.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        sys.exit(0)