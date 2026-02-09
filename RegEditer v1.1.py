import os
import sys
import ctypes
import winreg
from datetime import datetime

# --- KONFIGURACJA I TŁUMACZENIA ---
LOG_DIR = os.path.join(os.environ['USERPROFILE'], '.polsoft', 'psCLI', 'Log')
LOG_FILE = os.path.join(LOG_DIR, f"RegEditer_{datetime.now().strftime('%Y-%m-%d')}.log")

strings = {
    "pl": {
        "title": "CMD Cli RegEditer v1.1 - TRYB ADMINA",
        "menu_title": "STATUS: UPRAWNIENIA ADMINISTRATORA PRZYZNANE",
        "opt1": "DODAJ NOWY WPIS (REG_SZ)",
        "opt2": "USUŃ KLUCZ LUB WARTOŚĆ",
        "opt3": "EKSPORTUJ DO PLIKU .REG",
        "opt4": "PRZEGLĄDAJ KLUCZ (QUERY)",
        "opt5": "OTWÓRZ SYSTEMOWY REGEDIT",
        "opt6": "INFORMACJE",
        "optL": "ZMIEŃ JĘZYK / CHANGE LANGUAGE",
        "optQ": "WYJŚCIE",
        "select": "Wybierz opcję i naciśnij ENTER: ",
        "path": "ŚCIEŻKA (np. HKLM\\Software\\Test): ",
        "val_name": "NAZWA WARTOŚCI: ",
        "content": "TREŚĆ (DATA): ",
        "done": "OPERACJA ZAKOŃCZONA.",
        "error": "WYSTĄPIŁ BŁĄD: ",
        "admin_req": "Wymagane uprawnienia administratora!",
        "confirm_del": "Czy na pewno usunąć? (t/n): "
    },
    "en": {
        "title": "CMD Cli RegEditer v1.1 - ADMIN MODE",
        "menu_title": "STATUS: ADMIN PRIVILEGES GRANTED",
        "opt1": "ADD NEW ENTRY (REG_SZ)",
        "opt2": "DELETE KEY OR VALUE",
        "opt3": "EXPORT TO .REG FILE",
        "opt4": "BROWSE KEY (QUERY)",
        "opt5": "OPEN SYSTEM REGEDIT",
        "opt6": "INFORMATION",
        "optL": "CHANGE LANGUAGE / ZMIEŃ JĘZYK",
        "optQ": "EXIT",
        "select": "Select an option and press ENTER: ",
        "path": "PATH (e.g. HKLM\\Software\\Test): ",
        "val_name": "VALUE NAME: ",
        "content": "CONTENT (DATA): ",
        "done": "OPERATION COMPLETED.",
        "error": "ERROR OCCURRED: ",
        "admin_req": "Administrator privileges are required!",
        "confirm_del": "Are you sure you want to delete? (y/n): "
    }
}

current_lang = "pl"

# --- FUNKCJE POMOCNICZE ---
def log_event(message):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_root_key(path):
    parts = path.split('\\')
    root = parts[0].upper()
    roots = {
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKCU": winreg.HKEY_CURRENT_USER,
        "HKU": winreg.HKEY_USERS,
        "HKCR": winreg.HKEY_CLASSES_ROOT
    }
    return roots.get(root), "\\".join(parts[1:])

# --- LOGIKA PROGRAMU ---
def add_entry():
    s = strings[current_lang]
    path = input(s["path"])
    name = input(s["val_name"])
    data = input(s["content"])
    try:
        root, subkey = get_root_key(path)
        key = winreg.CreateKey(root, subkey)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, data)
        winreg.CloseKey(key)
        print(s["done"])
        log_event(f"ADD: {path} | {name} = {data}")
    except Exception as e:
        print(f"{s['error']} {e}")
    input("\nPress Enter...")

def delete_entry():
    s = strings[current_lang]
    path = input(s["path"])
    name = input(s["val_name"] + " (empty = entire key): ")
    try:
        root, subkey = get_root_key(path)
        if name == "":
            winreg.DeleteKey(root, subkey)
            log_event(f"DELETE KEY: {path}")
        else:
            key = winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            log_event(f"DELETE VALUE: {path}\\{name}")
        print(s["done"])
    except Exception as e:
        print(f"{s['error']} {e}")
    input("\nPress Enter...")

def main_menu():
    global current_lang
    while True:
        s = strings[current_lang]
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\033[92m____________________________________________polsoft.ITS London_")
        print(f"|  {s['title']:<60} |")
        print(f"|  {s['menu_title']:<60} |")
        print(f"|_______________________________________________________________|\033[0m\n")
        print(f" [1] {s['opt1']}")
        print(f" [2] {s['opt2']}")
        print(f" [3] {s['opt3']}")
        print(f" [4] {s['opt4']}")
        print(f" [5] {s['opt5']}")
        print(f" [6] {s['opt6']}")
        print(f" [L] {s['optL']}")
        print(f" [Q] {s['optQ']}\n")
        
        choice = input(s["select"]).lower()

        if choice == '1': add_entry()
        elif choice == '2': delete_entry()
        elif choice == '3': 
            os.system('cls')
            path = input(s["path"])
            file = input("Filename (backup.reg): ")
            os.system(f'reg export "{path}" "{file}"')
            input("\nPress Enter...")
        elif choice == '4':
            os.system('cls')
            path = input(s["path"])
            os.system(f'reg query "{path}"')
            input("\nPress Enter...")
        elif choice == '5':
            os.startfile("regedit.exe")
        elif choice == '6':
            print("\nAuthor: Sebastian Januchowski\nGitHub: https://github.com/seb07uk")
            input("\nPress Enter...")
        elif choice == 'l':
            current_lang = "en" if current_lang == "pl" else "pl"
        elif choice == 'q':
            log_event("Program terminated.")
            sys.exit()

if __name__ == "__main__":
    if is_admin():
        log_event("Program started (Admin Mode).")
        main_menu()
    else:
        # Re-run the program with admin rights
        print("Requesting admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)