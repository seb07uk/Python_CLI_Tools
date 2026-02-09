import os
import subprocess
import sys
import ctypes

def is_admin():
    """Checks if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def backup_drivers(destination_path):
    """Backs up drivers using the DISM tool."""
    
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        print(f"[*] Created folder: {destination_path}")

    print(f"[*] Starting driver export to: {destination_path}")
    print("[!] This may take a few minutes...")

    # DISM command to export drivers
    # /Export-Driver extracts third-party (OEM) drivers from the driver store
    cmd = [
        "dism", 
        "/online", 
        "/export-driver", 
        f"/destination:{destination_path}"
    ]

    try:
        # Run the process
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[+] Success! Drivers have been saved.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error during DISM command execution:")
        print(e.stderr)
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")

if __name__ == "__main__":
    # 1. Check permissions
    if not is_admin():
        print("[-] ERROR: You must run this script as an ADMINISTRATOR.")
        # Optional: attempt to relaunch with admin rights
        # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        input("Press Enter to close...")
        sys.exit()

    # 2. Define path (defaults to 'DriverBackup' folder on Desktop)
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    backup_folder = os.path.join(desktop, 'DriverBackup')

    # 3. Run the function
    backup_drivers(backup_folder)
    
    input("\nProcess complete. Press Enter to exit...")