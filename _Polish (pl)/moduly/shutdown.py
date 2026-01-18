import os
import sys
import platform
import re
from datetime import datetime, timedelta
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__github__ = "https://github.com/seb07uk"
__category__ = "system"
__group__ = "core"
__desc__ = "System Shutdown Utility - schedule or abort system shutdown"

def print_help():
    help_text = """
    TERMINAL CLI - System Shutdown Utility
    ======================================
    Użycie: python shutdown.py [opcja]

    Dostępne formaty:
    1. Brak argumentu     - Wyłącza komputer w ciągu 1 sekundy.
    2. t[sekundy]         - Shutdown za określoną liczbę sekund (np. t30).
    3. t[HH-MM-SS]        - Shutdown o konkretnej godzinie (np. t12-10-00).
    4. help / --h         - Wyświetla tę pomoc.
    5. abort              - Anuluje zaplanowany shutdown.

    Przykłady:
    python shutdown.py t60       # Wyłączenie za minutę
    python shutdown.py t23-59-00 # Wyłączenie tuż przed północą

    ------------------------------------
    Sebastian Januchowski
    polsoft.its@fastservice.com
    https://github.com/seb07uk
    2026© polsoft.ITS London
    """
    print(help_text)

def abort_shutdown():
    if platform.system() == "Windows":
        os.system("shutdown /a")
        print("Zaplanowany shutdown został anulowany.")
    else:
        os.system("sudo shutdown -c")
        print("Shutdown cancelled.")

def get_seconds_until(time_str):
    try:
        now = datetime.now()
        target_time = datetime.strptime(time_str, "%H-%M-%S")
        target_datetime = now.replace(hour=target_time.hour, minute=target_time.minute, second=target_time.second)
        if target_datetime < now:
            target_datetime += timedelta(days=1)
        return int((target_datetime - now).total_seconds())
    except ValueError:
        print("Błąd: Nieprawidłowy format czasu HH-MM-SS.")
        sys.exit(1)

def shutdown_system(delay):
    if platform.system() == "Windows":
        os.system(f"shutdown /s /t {delay} /f")
    else:
        # Konwersja na minuty dla systemów Unix
        delay_min = max(1, delay // 60)
        os.system(f"sudo shutdown -h +{delay_min}")

@command(name="shutdown", aliases=["poweroff", "sd"])
def run(*args):
    """
    Schedule system shutdown or abort scheduled shutdown.
    Usage: shutdown [t<seconds|HH-MM-SS>] | shutdown abort | shutdown help
    """
    # Help handler
    if args and args[0] in ["help", "--h", "/?", "-h"]:
        print_help()
        return
    
    # Abort handler
    if args and args[0].lower() == "abort":
        abort_shutdown()
        return
    
    # No arguments - shutdown immediately
    if not args:
        shutdown_system(1)
        return
    
    # Process time argument
    arg = args[0].lower()
    
    if arg.startswith("t"):
        val = arg[1:]
        if "-" in val:
            sec = get_seconds_until(val)
            print(f"{Color.YELLOW}Shutdown zaplanowany na {val.replace('-', ':')} (za {sec}s).{Color.RESET}")
            shutdown_system(sec)
        elif val.isdigit():
            sec = int(val)
            print(f"{Color.YELLOW}Shutdown za {sec} sekund.{Color.RESET}")
            shutdown_system(sec)
        else:
            print(f"{Color.RED}[!] Błąd: Nieprawidłowy format argumentu '{arg}'{Color.RESET}")
    else:
        print(f"{Color.RED}[!] Nieznany argument. Wpisz 'shutdown help' dla pomocy.{Color.RESET}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        shutdown_system(1)
    else:
        arg = sys.argv[1].lower()
        
        if arg in ["help", "--h", "/?"]:
            print_help()
        elif arg == "abort":
            abort_shutdown()
        elif arg.startswith("t"):
            val = arg[1:]
            if "-" in val:
                sec = get_seconds_until(val)
                print(f"Shutdown zaplanowany na {val.replace('-', ':')} (za {sec}s).")
                shutdown_system(sec)
            elif val.isdigit():
                sec = int(val)
                print(f"Shutdown za {sec} sekund.")
                shutdown_system(sec)
        else:
            print("Nieznany argument. Wpisz 'python shutdown.py help'.")
